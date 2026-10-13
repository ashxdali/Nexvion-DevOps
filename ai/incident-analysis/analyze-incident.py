#!/usr/bin/env python3

"""
Nexvion Incident Analysis Tool

Classifies log entries, groups repeated findings, and suggests
investigation steps using configurable keyword-based rules.

This is rule-based analysis, not a real AI model.
"""

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


RULES = [
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
    {
        "name": "Connection failure",
        "pattern": r"\b(connection refused|connection reset|connection failed|failed to connect)\b",
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
        "cause": "The log entry may indicate a condition that needs attention.",
        "investigation": [
            "Review the complete warning message.",
            "Check whether the warning repeats or affects functionality.",
        ],
        "commands": [
            "kubectl get events -n nexvion --sort-by=.lastTimestamp",
        ],
    },
]

SEVERITY_ORDER = ("CRITICAL", "HIGH", "MEDIUM", "LOW")


def analyze_log(logfile):
    """Return total lines and at most one highest-priority finding per line."""
    findings = []
    total_lines = 0

    with logfile.open("r", encoding="utf-8", errors="replace") as stream:
        for line_number, line in enumerate(stream, start=1):
            total_lines += 1
            text = line.rstrip()

            for rule in RULES:
                if re.search(rule["pattern"], text, re.IGNORECASE):
                    findings.append(
                        {
                            "line": line_number,
                            "rule": rule,
                            "text": text,
                        }
                    )
                    # Rules are ordered by priority. Avoid duplicate findings
                    # when multiple patterns match the same log line.
                    break

    return total_lines, findings


def generate_report(logfile, total_lines, findings):
    """Generate a text report with severity totals and grouped findings."""
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    severity_counts = Counter(
        finding["rule"]["severity"] for finding in findings
    )

    grouped = defaultdict(list)
    for finding in findings:
        grouped[finding["rule"]["name"]].append(finding)

    lines = [
        "NEXVION INCIDENT ANALYSIS REPORT",
        "=" * 50,
        f"Generated: {now}",
        f"Input file: {logfile}",
        f"Total lines analyzed: {total_lines}",
        f"Unique finding lines: {len(findings)}",
        f"Unmatched lines: {total_lines - len(findings)}",
        "",
        "SEVERITY SUMMARY",
        "-" * 50,
    ]

    for severity in SEVERITY_ORDER:
        lines.append(f"{severity}: {severity_counts[severity]}")

    lines.extend(["", "GROUPED FINDINGS", "-" * 50])

    if not findings:
        lines.extend(
            [
                "No configured incident patterns were detected.",
                "This does not guarantee that the system is error-free.",
            ]
        )

    for name, group in grouped.items():
        rule = group[0]["rule"]
        line_numbers = ", ".join(str(item["line"]) for item in group)

        lines.extend(
            [
                "",
                f"Incident type: {name}",
                f"Suggested severity: {rule['severity']}",
                f"Matching entries: {len(group)}",
                f"Log line numbers: {line_numbers}",
                f"Possible cause: {rule['cause']}",
                "Example log entry:",
                f"  {group[0]['text']}",
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
            "-" * 50,
            "This tool uses keyword-based rules, not a real AI model.",
            "Each log line is assigned only its first matching rule.",
            "Repeated entries are grouped by incident type in the report.",
            "Severity and possible causes are preliminary suggestions.",
            "Review original logs and verify findings before acting.",
            "Suggested commands are not executed by this tool.",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Classify Nexvion logs and suggest incident investigations."
    )
    parser.add_argument("logfile", type=Path, help="Path to the input log file")
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
