#!/bin/bash
#
# BridgeWatch AI - Database Restore Script
#
# Usage:
#   ./scripts/restore.sh ./backups/bridgewatch_pg_20260519_120000.sql.gz
#   ./scripts/restore.sh ./backups/bridgewatch_sqlite_20260519_120000.db.gz
#
# Environment variables (same as backup.sh):
#   DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

set -euo pipefail

DB_NAME="${DB_NAME:-bridgewatch}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <backup-file>"
    echo ""
    echo "  Supports: .sql.gz (PostgreSQL custom format)"
    echo "            .db.gz  (SQLite backup)"
    exit 1
fi

BACKUP_FILE="$1"

if [[ ! -f "$BACKUP_FILE" ]]; then
    echo "[restore] ERROR: File not found: $BACKUP_FILE"
    exit 1
fi

echo "[restore] Starting restore from: $BACKUP_FILE"
echo "[restore]  Size: $(ls -lh "$BACKUP_FILE" | awk '{print $5}')"

case "$BACKUP_FILE" in
    *.sql.gz)
        echo "[restore] Detected PostgreSQL backup"
        echo "[restore]  WARNING: This will OVERWRITE the '$DB_NAME' database!"
        read -rp "  Continue? (y/N) " confirm
        if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
            echo "[restore] Cancelled."
            exit 0
        fi
        PGPASSWORD="$DB_PASS" pg_restore \
            -h "$DB_HOST" \
            -p "$DB_PORT" \
            -U "$DB_USER" \
            -d "$DB_NAME" \
            --clean \
            --if-exists \
            --verbose \
            "$BACKUP_FILE" 2>&1 | grep -v "^\s*$" | sed 's/^/[pg_restore] /'
        echo "[restore] PostgreSQL restore completed."
        ;;
    *.db.gz)
        echo "[restore] Detected SQLite backup"
        local restore_path="${BACKUP_FILE%.gz}"
        gunzip -k -f "$BACKUP_FILE" 2>/dev/null || true
        if [[ -f "$restore_path" ]]; then
            echo "[restore]  Restored to: $restore_path"
            echo "[restore]  Copy to your SQLite database location and restart."
        else
            echo "[restore] ERROR: Could not extract backup"
            exit 1
        fi
        ;;
    *)
        echo "[restore] ERROR: Unknown backup format. Use .sql.gz (PostgreSQL) or .db.gz (SQLite)"
        exit 1
        ;;
esac

echo "[restore] Done."
