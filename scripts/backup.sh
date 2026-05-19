#!/bin/bash
#
# BridgeWatch AI - Database Backup Script
# Supports: PostgreSQL (production) and SQLite (development)
#
# Usage:
#   ./scripts/backup.sh                  # PostgreSQL backup (default)
#   ./scripts/backup.sh --sqlite ./data/db.sqlite  # SQLite backup
#   ./scripts/backup.sh --docker         # Backup Docker Postgres container
#
# Environment variables (for PostgreSQL):
#   DB_NAME     - Database name (default: bridgewatch)
#   DB_USER     - Database user (default: postgres)
#   DB_PASS     - Database password (default: postgres)
#   DB_HOST     - Database host (default: localhost)
#   DB_PORT     - Database port (default: 5432)
#   BACKUP_DIR  - Backup directory (default: ./backups)
#   RETENTION_DAYS - Days to keep backups (default: 30)

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────
DB_NAME="${DB_NAME:-bridgewatch}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

# ── Backup functions ───────────────────────────────────────────────

backup_postgres() {
    local backup_file="$BACKUP_DIR/bridgewatch_pg_$TIMESTAMP.sql.gz"
    echo "[backup] Starting PostgreSQL backup..."
    echo "[backup]  Host: $DB_HOST:$DB_PORT  DB: $DB_NAME"

    PGPASSWORD="$DB_PASS" pg_dump \
        -h "$DB_HOST" \
        -p "$DB_PORT" \
        -U "$DB_USER" \
        -d "$DB_NAME" \
        --format=custom \
        --verbose \
        --file="$backup_file" 2>&1 | grep -v "^\s*$" | sed 's/^/[pg_dump] /'

    echo "[backup]  Completed: $(ls -lh "$backup_file" | awk '{print $5}')"
    echo "[backup]  File: $backup_file"
}

backup_sqlite() {
    local db_path="${1:-}"
    if [[ -z "$db_path" ]]; then
        echo "[backup] ERROR: SQLite database path required. Use --sqlite <path>"
        exit 1
    fi
    if [[ ! -f "$db_path" ]]; then
        echo "[backup] ERROR: SQLite database not found: $db_path"
        exit 1
    fi

    local backup_file="$BACKUP_DIR/bridgewatch_sqlite_$TIMESTAMP.db"
    echo "[backup] Starting SQLite backup..."
    echo "[backup]  Source: $db_path"

    sqlite3 "$db_path" ".backup '$backup_file'"
    gzip -f "$backup_file"
    local final_file="${backup_file}.gz"

    echo "[backup]  Completed: $(ls -lh "$final_file" | awk '{print $5}')"
    echo "[backup]  File: $final_file"
}

backup_docker() {
    local container_name="${DB_DOCKER_CONTAINER:-bridgewatch-postgres-1}"
    local backup_file="$BACKUP_DIR/bridgewatch_pg_${TIMESTAMP}.sql.gz"
    echo "[backup] Starting Docker PostgreSQL backup..."
    echo "[backup]  Container: $container_name"

    docker exec "$container_name" pg_dump \
        -U "$DB_USER" \
        -d "$DB_NAME" \
        --format=custom \
        --file="/tmp/bridgewatch_backup.dump"

    docker cp "$container_name:/tmp/bridgewatch_backup.dump" "$backup_file"
    docker exec "$container_name" rm -f "/tmp/bridgewatch_backup.dump"
    gzip -f "$backup_file"

    echo "[backup]  Completed: $(ls -lh "${backup_file}.gz" | awk '{print $5}')"
    echo "[backup]  File: ${backup_file}.gz"
}

# ── Cleanup old backups ────────────────────────────────────────────

cleanup_old() {
    local count
    count=$(find "$BACKUP_DIR" -name "bridgewatch_*.gz" -mtime "+$RETENTION_DAYS" | wc -l)
    if [[ "$count" -gt 0 ]]; then
        find "$BACKUP_DIR" -name "bridgewatch_*.gz" -mtime "+$RETENTION_DAYS" -delete
        echo "[backup]  Cleaned up $count old backup(s) (>${RETENTION_DAYS}d)"
    fi
}

# ── Main ───────────────────────────────────────────────────────────

case "${1:-}" in
    --sqlite)
        backup_sqlite "${2:-}"
        ;;
    --docker)
        backup_docker
        ;;
    --help|-h)
        echo "Usage: $0 [--sqlite <path> | --docker | --help]"
        echo ""
        echo "  (no flag)     PostgreSQL backup using env vars"
        echo "  --sqlite      Backup SQLite database file"
        echo "  --docker      Backup PostgreSQL running in Docker"
        echo "  --help        Show this help"
        exit 0
        ;;
    *)
        backup_postgres
        ;;
esac

cleanup_old
echo "[backup] Done."
