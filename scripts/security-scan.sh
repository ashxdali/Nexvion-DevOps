#!/usr/bin/env bash

set -euo pipefail

IMAGE_NAME="${1:-nexvion-ecommerce:1.0}"
REPORT_DIR="security/reports"
REPORT_FILE="$REPORT_DIR/nexvion-trivy-report.json"
TRIVY_EXIT_CODE="${TRIVY_EXIT_CODE:-1}"

mkdir -p "$REPORT_DIR"

echo "========================================"
echo " Nexvion Docker Security Scan"
echo "========================================"
echo "Image: $IMAGE_NAME"
echo "Policy: Fail on HIGH or CRITICAL vulnerabilities"

# Save the complete JSON report before applying the security gate.
trivy image \
  --scanners vuln \
  --format json \
  --output "$REPORT_FILE" \
  "$IMAGE_NAME"

echo "Security report saved: $REPORT_FILE"

# Fail the pipeline if HIGH or CRITICAL vulnerabilities are found.
trivy image \
  --scanners vuln \
  --severity HIGH,CRITICAL \
  --exit-code "$TRIVY_EXIT_CODE" \
  --format table \
  "$IMAGE_NAME"

echo "Security scan passed. No HIGH or CRITICAL vulnerabilities found."
