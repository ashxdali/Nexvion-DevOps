#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/backups"

# Default retention period: 7 days
RETENTION_DAYS="${1:-7}"

echo "======================================"
echo " Nexvion DevOps - Backup Cleanup"
echo "======================================"

# Validate retention period
if [[ ! "$RETENTION_DAYS" =~ ^[0-9]+$ ]]; then
    echo "[ERROR] Retention period must be a number."
    echo "Usage: $0 [retention_days]"
    exit 1
fi

if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "[INFO] No backup directory exists. Nothing to clean."
    exit 0
fi

echo "[INFO] Backup directory: $BACKUP_DIR"
echo "[INFO] Retention period: $RETENTION_DAYS days"

# Find only Nexvion backup archives older than the retention period
while IFS= read -r -d '' backup_file; do
    echo "[INFO] Removing old backup: $backup_file"
    rm -- "$backup_file"
done < <(
    find "$BACKUP_DIR" \
        -maxdepth 1 \
        -type f \
        -name 'nexvion_backup_*.tar.gz' \
        -mtime "+$RETENTION_DAYS" \
        -print0
)

echo "[OK] Backup cleanup completed."
