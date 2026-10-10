# Nexvion Log Analysis

## Objective
Collect Kubernetes application logs and analyze them for common error indicators using a Python script.

## Log Collection
Collect the latest 200 log lines:

```bash
kubectl logs -n nexvion deployment/nexvion-web --tail=200 > logging/reports/frontend.log
```

## Log Analysis
Run the analyzer:

```bash
python3 logging/scripts/analyze-logs.py logging/reports/frontend.log
```

The report is saved to `logging/reports/log-analysis-report.txt`.

## Detection Categories
The analyzer checks for:
- ERROR
- WARNING
- TIMEOUT
- CONNECTION

Keyword matches are indicators for investigation, not confirmed incidents.

## Limitations
This implementation analyzes saved log files. It does not provide real-time log aggregation, indexing, dashboards, or alerting.

