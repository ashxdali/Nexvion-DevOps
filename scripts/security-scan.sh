#!/usr/bin/env bash
set -Eeuo pipefail

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

# Generate the complete JSON report.
if ! trivy image \
  --scanners vuln \
  --format json \
  --output "$REPORT_FILE" \
  "$IMAGE_NAME"; then
    echo "ERROR: Trivy could not complete the vulnerability scan."
    exit 1
fi

echo "Security report saved: $REPORT_FILE"

# Fail when HIGH or CRITICAL vulnerabilities are detected.
trivy image \
  --scanners vuln \
  --severity HIGH,CRITICAL \
  --exit-code "$TRIVY_EXIT_CODE" \
  --format table \
  "$IMAGE_NAME"

echo "Security scan passed. No HIGH or CRITICAL vulnerabilities found."
