#!/usr/bin/env bash
# backup.sh - Backup The Missing Piece data
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

echo "Creating backup..."
tar -czf "$BACKUP_FILE" -C "$SCRIPT_DIR" data .env 2>/dev/null
echo "Backup created: $BACKUP_FILE"
