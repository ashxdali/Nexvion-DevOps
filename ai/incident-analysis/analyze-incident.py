#!/usr/bin/env python3

"""
Nexvion Incident Analysis Tool

Analyzes application logs using keyword-based rules.
Produces possible causes and investigation recommendations.

Note: This version uses rule-based analysis, not an AI model.
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


RULES = [
    {
        "name": "Application error",
        "pattern": r"\b(error|exception|fatal)\b",
        "severity": "HIGH",
        "cause": "The application may have encountered an internal error.",
        "investigation": [
            "Inspect the surrounding log entries.",
            "Check application configuration and recent changes.",
            "Review the application pod status and restart count.",
        ],
        "commands": [
            "kubectl get pods -n nexvion",
            "kubectl logs -n nexvion deployment/nexvion-web --tail=100",
        ],
    },
    {
        "name": "Connection failure",
        "pattern": r"\b(connection refused|connection reset|connection failed)\b",
        "severity": "HIGH",
        "cause": "A service may be unavailable or refusing connections.",
        "investigation": [
            "Verify that the destination service is running.",
            "Check service names, ports, endpoints, and network policies.",
            "Review the affected container's logs.",
        ],
        "commands": [
            "kubectl get services,endpoints -n nexvion",
            "kubectl get pods -n nexvion",
        ],
    },
    {
        "name": "Timeout",
        "pattern": r"\b(timeout|timed out|deadline exceeded)\b",
        "severity": "MEDIUM",
        "cause": "A request or operation may be taking longer than expected.",
        "investigation": [
            "Check application response times and resource usage.",
            "Inspect network connectivity and dependency availability.",
            "Look for repeated timeout entries.",
        ],
        "commands": [
            "kubectl top pods -n nexvion",
            "kubectl get pods -n nexvion",
        ],
    },
    {
        "name": "Warning",
        "pattern": r"\b(warning|warn)\b",
        "severity": "LOW",
        "cause": "The application has reported a condition that may need attention.",
        "investigation": [
            "Review the complete warning message.",
            "Check whether the warning repeats or affects functionality.",
        ],
        "commands": [
            "kubectl get events -n nexvion --sort-by=.lastTimestamp",
        ],
    },
    {
        "name": "Resource pressure",
        "pattern": r"\b(out of memory|oomkilled|outofmemory|memory pressure)\b",
        "severity": "CRITICAL",
        "cause": "A process or container may be experiencing memory pressure.",
        "investigation": [
            "Check container restart counts and termination reasons.",
            "Review memory requests, limits, and recent workload changes.",
            "Check node memory pressure before changing resource limits.",
        ],
        "commands": [
            "kubectl get pods -n nexvion",
            "kubectl describe pods -n nexvion",
            "kubectl top pods -n nexvion",
        ],
    },
]


def analyze_log(logfile):
    findings = []
    total_lines = 0

    with logfile.open("r", encoding="utf-8", errors="replace") as stream:
        for line_number, line in enumerate(stream, start=1):
            total_lines += 1

            for rule in RULES:
                if re.search(rule["pattern"], line, re.IGNORECASE):
                    findings.append(
                        {
                            "line": line_number,
                            "rule": rule,
                            "text": line.rstrip(),
                        }
                    )

    return total_lines, findings


def generate_report(logfile, total_lines, findings):
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    lines = [
        "NEXVION INCIDENT ANALYSIS REPORT",
        "=" * 45,
        f"Generated: {now}",
        f"Input file: {logfile}",
        f"Total lines analyzed: {total_lines}",
        f"Potential findings: {len(findings)}",
        "",
        "SEVERITY SUMMARY",
        "-" * 45,
    ]

    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        count = sum(
            1 for finding in findings
            if finding["rule"]["severity"] == severity
        )
        lines.append(f"{severity}: {count}")

    lines.extend(["", "FINDINGS AND RECOMMENDATIONS", "-" * 45])

    if not findings:
        lines.extend(
            [
                "No configured incident patterns were detected.",
                "This does not guarantee that the system is error-free.",
            ]
        )

    for index, finding in enumerate(findings, start=1):
        rule = finding["rule"]

        lines.extend(
            [
                "",
                f"Finding {index}: {rule['name']}",
                f"Log line: {finding['line']}",
                f"Suggested severity: {rule['severity']}",
                f"Log entry: {finding['text']}",
                f"Possible cause: {rule['cause']}",
                "Recommended investigation:",
            ]
        )

        lines.extend(f"  - {step}" for step in rule["investigation"])
        lines.append("Suggested commands:")

        lines.extend(f"  $ {command}" for command in rule["commands"])

    lines.extend(
        [
            "",
            "IMPORTANT LIMITATIONS",
            "-" * 45,
            "This version uses keyword-based rules, not a real AI model.",
            "Severity and root-cause suggestions are preliminary.",
            "Review the original logs and verify findings before acting.",
            "Commands are recommendations and have not been executed.",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Nexvion logs and suggest incident investigations."
    )
    parser.add_argument("logfile", type=Path, help="Path to the log file")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("logging/reports/incident-analysis-report.txt"),
        help="Report output path",
    )
    args = parser.parse_args()

    if not args.logfile.is_file():
        parser.error(f"Log file not found: {args.logfile}")

    total_lines, findings = analyze_log(args.logfile)
    report = generate_report(args.logfile, total_lines, findings)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")

    print(report)
    print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()
