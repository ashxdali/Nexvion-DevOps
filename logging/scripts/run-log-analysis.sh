#!/usr/bin/env bash
set -Eeuo pipefail

NAMESPACE="${NAMESPACE:-nexvion}"
OUTPUT_DIR="${OUTPUT_DIR:-logging/reports}"
LOG_DIR="${LOG_DIR:-logging/collected}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

echo "========================================"
echo " Nexvion Log Analysis Workflow"
echo "========================================"

# Step 1: Collect Kubernetes logs and events.
echo
echo "[1/3] Collecting Kubernetes logs..."

NAMESPACE="$NAMESPACE" \
OUTPUT_DIR="$LOG_DIR" \
    ./logging/scripts/collect-kubernetes-logs.sh

LATEST_LOG="$(find "$LOG_DIR" -maxdepth 1 -type f \
    -name 'kubernetes-logs-*.log' -printf '%T@ %p\n' |
    sort -nr | head -n 1 | cut -d ' ' -f 2-)"

if [[ -z "$LATEST_LOG" || ! -f "$LATEST_LOG" ]]; then
    echo "ERROR: No collected log file was found."
    exit 1
fi

echo "Input log: $LATEST_LOG"

# Step 2: Run keyword-based log analysis.
echo
echo "[2/3] Running log analysis..."

python3 logging/scripts/analyze-logs.py \
    "$LATEST_LOG" \
    --output "$OUTPUT_DIR/log-analysis-${TIMESTAMP}.txt"

# Step 3: Run incident classification.
echo
echo "[3/3] Running incident analysis..."

python3 ai/incident-analysis/analyze-incident.py \
    "$LATEST_LOG" \
    --output "$OUTPUT_DIR/incident-analysis-${TIMESTAMP}.txt"

echo
echo "========================================"
echo " Log analysis workflow completed"
echo "========================================"
echo "Collected log: $LATEST_LOG"
echo "Reports:"
echo "  $OUTPUT_DIR/log-analysis-${TIMESTAMP}.txt"
echo "  $OUTPUT_DIR/incident-analysis-${TIMESTAMP}.txt"
