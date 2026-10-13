import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

import importlib.util

ANALYZER_PATH = (
    PROJECT_ROOT / "ai" / "incident-analysis" / "analyze-incident.py"
)

SPEC = importlib.util.spec_from_file_location(
    "analyze_incident", ANALYZER_PATH
)
ANALYZER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYZER)

analyze_log = ANALYZER.analyze_log



class IncidentAnalyzerTests(unittest.TestCase):

    def analyze_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            logfile = Path(directory) / "test.log"
            logfile.write_text(text, encoding="utf-8")
            return analyze_log(logfile)

    def test_empty_log(self):
        total_lines, findings = self.analyze_text("")
        self.assertEqual(total_lines, 0)
        self.assertEqual(findings, [])

    def test_normal_log_has_no_findings(self):
        total_lines, findings = self.analyze_text(
            "INFO Application started successfully\n"
        )
        self.assertEqual(total_lines, 1)
        self.assertEqual(findings, [])

    def test_connection_failure(self):
        _, findings = self.analyze_text(
            "ERROR Database connection failed\n"
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"]["name"], "Connection failure")
        self.assertEqual(findings[0]["rule"]["severity"], "HIGH")

    def test_oom_is_critical(self):
        _, findings = self.analyze_text(
            "Container OOMKilled\n"
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"]["name"], "Resource pressure")
        self.assertEqual(findings[0]["rule"]["severity"], "CRITICAL")

    def test_one_finding_per_line(self):
        _, findings = self.analyze_text(
            "WARNING Request timeout\n"
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"]["name"], "Timeout")

    def test_repeated_incidents_remain_separate_findings(self):
        _, findings = self.analyze_text(
            "ERROR Database connection failed\n"
            "ERROR Database connection failed\n"
        )
        self.assertEqual(len(findings), 2)
        self.assertEqual(
            [finding["line"] for finding in findings],
            [1, 2],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
