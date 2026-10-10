#!/usr/bin/env python3

import argparse
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ERROR_PATTERNS = {
    "ERROR": re.compile(r"\b(error|exception|fatal|panic)\b", re.I),
    "WARNING": re.compile(r"\b(warn|warning)\b", re.I),
    "TIMEOUT": re.compile(r"\b(timeout|timed out|deadline exceeded)\b", re.I),
    "CONNECTION": re.compile(
        r"\b(connection refused|connection reset|connection failed)\b", re.I
    ),
}

def analyze_logs(log_text):
    counts = Counter()
    findings = []

    for line_number, line in enumerate(log_text.splitlines(), start=1):
        matched_categories = [
            category
            for category, pattern in ERROR_PATTERNS.items()
            if pattern.search(line)
        ]

        if matched_categories:
            counts.update(matched_categories)
            findings.append((line_number, matched_categories, line))

    return counts, findings


def main():
    parser = argparse.ArgumentParser(
        description="Analyze application logs for common issues."
    )
    parser.add_argument("logfile", help="Path to a saved log file")
    parser.add_argument(
        "--output",
        default="logging/reports/log-analysis-report.txt",
        help="Path for the analysis report",
    )
    args = parser.parse_args()

    log_path = Path(args.logfile)

    if not log_path.is_file():
        parser.error(f"Log file not found: {log_path}")

    try:
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        parser.error(f"Cannot read log file: {exc}")

    counts, findings = analyze_logs(log_text)

    report_path = Path(args.output)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "NEXVION LOG ANALYSIS REPORT",
        "=" * 40,
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Input file: {log_path}",
        f"Total lines: {len(log_text.splitlines())}",
        "",
        "FINDINGS SUMMARY",
        "-" * 40,
    ]

    for category in ERROR_PATTERNS:
        report.append(f"{category}: {counts[category]}")

    report.extend(["", "MATCHED LOG ENTRIES", "-" * 40])

    if findings:
        for line_number, categories, line in findings:
            report.append(
                f"Line {line_number} [{', '.join(categories)}]: {line}"
            )
    else:
        report.append("No matching errors, warnings, timeouts, or connection issues found.")

    report.extend([
        "",
        "Note: Matches are keyword-based indicators, not confirmed incidents.",
    ])

    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n".join(report[:9]))
    print(f"\nFull report saved to: {report_path}")


if __name__ == "__main__":
    main()
