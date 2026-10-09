#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APPLICATION_DIR="$PROJECT_ROOT/application"

echo "======================================"
echo " Nexvion DevOps - Environment Setup"
echo "======================================"

echo
echo "[INFO] Checking project directories..."

if [[ ! -d "$APPLICATION_DIR" ]]; then
    echo "[ERROR] Application directory not found: $APPLICATION_DIR"
    exit 1
fi

if [[ ! -f "$APPLICATION_DIR/index.html" ]]; then
    echo "[ERROR] Homepage not found."
    exit 1
fi

if [[ ! -d "$PROJECT_ROOT/scripts" ]]; then
    echo "[ERROR] Scripts directory not found."
    exit 1
fi

echo "[OK] Project structure verified."
echo
echo "[INFO] Checking required tools..."

for tool in git docker curl tar; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "[OK] $tool is installed."
    else
        echo "[WARNING] $tool is not installed."
    fi
done

echo
echo "[INFO] Checking Docker service..."

if docker info >/dev/null 2>&1; then
    echo "[OK] Docker is running and accessible."
else
    echo "[WARNING] Docker is unavailable or permission is denied."
fi

echo
echo "[INFO] Environment check completed."
