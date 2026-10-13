#!/usr/bin/env bash
set -Eeuo pipefail

NAMESPACE="${NAMESPACE:-nexvion}"
OUTPUT_DIR="${OUTPUT_DIR:-logging/collected}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
OUTPUT_FILE="${OUTPUT_DIR}/kubernetes-logs-${TIMESTAMP}.log"

mkdir -p "$OUTPUT_DIR"

{
    echo "NEXVION KUBERNETES LOG COLLECTION"
    echo "Timestamp: $(date --iso-8601=seconds)"
    echo "Namespace: ${NAMESPACE}"
    echo

    for DEPLOYMENT in nexvion-web nexvion-helm-web; do
        echo "===== DEPLOYMENT: ${DEPLOYMENT} ====="
        if ! kubectl logs "deployment/${DEPLOYMENT}" \
            -n "$NAMESPACE" --all-pods=true --prefix=true --tail=200; then
            echo "WARNING: Unable to collect logs from ${DEPLOYMENT}"
        fi
        echo
    done

    echo "===== KUBERNETES EVENTS ====="
    kubectl get events -n "$NAMESPACE" \
        --sort-by=.lastTimestamp 2>&1 || true
    echo
} > "$OUTPUT_FILE"

echo "Log collection completed."
echo "Output file: ${OUTPUT_FILE}"
echo "Collected lines: $(wc -l < "$OUTPUT_FILE")"
