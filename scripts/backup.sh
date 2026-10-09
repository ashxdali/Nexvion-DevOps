#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APPLICATION_DIR="$PROJECT_ROOT/application"
BACKUP_DIR="$PROJECT_ROOT/backups"

TIMESTAMP="$(date +%Y-%m-%d_%H-%M-%S)"
BACKUP_FILE="$BACKUP_DIR/nexvion_backup_${TIMESTAMP}.tar.gz"

echo "======================================"
echo " Nexvion DevOps - Application Backup"
echo "======================================"

# Check application directory
if [[ ! -d "$APPLICATION_DIR" ]]; then
    echo "[ERROR] Application directory not found."
    exit 1
fi

# Check tar availability
if ! command -v tar >/dev/null 2>&1; then
    echo "[ERROR] tar is not installed."
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "[INFO] Creating application backup..."

# Archive the application files
tar -czf "$BACKUP_FILE" \
    -C "$PROJECT_ROOT" \
    application

# Verify the archive
if tar -tzf "$BACKUP_FILE" >/dev/null 2>&1; then
    echo "[OK] Backup created successfully."
    echo "[INFO] Backup location: $BACKUP_FILE"
    echo "[INFO] Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "[ERROR] Backup verification failed."
    rm -f "$BACKUP_FILE"
    exit 1
fi
