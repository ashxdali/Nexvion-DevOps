#!/usr/bin/env bash

set -Eeuo pipefail

DEFAULT_URL="http://localhost:8082/application/"
URL="${1:-$DEFAULT_URL}"

echo "======================================"
echo " Nexvion DevOps - Website Health Check"
echo "======================================"

echo
echo "[INFO] Checking: $URL"

if ! command -v curl >/dev/null 2>&1; then
    echo "[ERROR] curl is not installed."
    exit 1
fi

if HTTP_CODE=$(curl -sS -o /dev/null -w "%{http_code}" \
    --connect-timeout 5 --max-time 10 "$URL"); then

    echo "[INFO] HTTP status: $HTTP_CODE"

    if [[ "$HTTP_CODE" =~ ^2[0-9][0-9]$ ]]; then
        echo "[OK] Website is responding successfully."
        exit 0
    else
        echo "[ERROR] Website returned HTTP status $HTTP_CODE."
        exit 1
    fi
else
    echo "[ERROR] Website is unreachable."
    echo "[INFO] Check whether the web server is running and the URL is correct."
    exit 1
fi
