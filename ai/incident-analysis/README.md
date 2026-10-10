# Nexvion Incident Analysis

## Objective

Analyze application logs, identify potential incidents, suggest severity
levels, and provide investigation steps for DevOps troubleshooting.

## Implementation

The current implementation uses Python 3 and regular-expression rules.
It does not require external Python packages or a locally installed AI model.

## Run the Analysis

Analyze Kubernetes frontend logs:

```bash
python3 ai/incident-analysis/analyze-incident.py \
  logging/reports/frontend.log
```

Test with simulated incidents:

```bash
python3 ai/incident-analysis/analyze-incident.py \
  ai/incident-analysis/sample-incidents.log
```

The default report location is:

`logging/reports/incident-analysis-report.txt`

A different output location can be specified with `--output`.

## Detection Categories

- Application errors and exceptions
- Connection failures
- Request timeouts
- Warnings
- Memory pressure and OOM-related messages

## Output

The report includes:
- Number of lines analyzed
- Potential findings and suggested severity
- Original matching log entries
- Possible causes
- Recommended investigation steps
- Suggested Kubernetes commands

## Safety

The analyzer only reads the supplied log file and writes a report.
It does not execute the suggested commands or modify Kubernetes resources.

Severity and root-cause suggestions are preliminary and must be verified.

## Limitations

This is a rule-based incident triage tool, not a genuine AI model.
It does not understand context beyond its configured patterns, and one log
entry can match more than one rule.

The sample incident file contains simulated entries for testing.
Its findings must not be interpreted as actual production incidents.
