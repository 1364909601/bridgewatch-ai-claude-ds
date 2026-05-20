"""
Database migration helpers — adds missing columns for SQLite development.

In production, use Alembic for schema migrations.
"""

import logging
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine

logger = logging.getLogger(__name__)

# Known schema changes that need to be applied to existing tables
# Format: {table: [(column_name, column_def_sql), ...]}
_MISSING_COLUMNS: dict[str, list[tuple[str, str]]] = {
    "system_log": [
        ("user_id", "VARCHAR(64)"),
        ("operator_name", "VARCHAR(100)"),
        ("ip_address", "VARCHAR(50)"),
    ],
}


def _get_existing_columns_sync(conn: Any, table: str) -> set[str]:
    """Sync helper to inspect columns (must run via conn.run_sync)."""
    inspector = inspect(conn)
    return {c["name"] for c in inspector.get_columns(table)}


async def migrate_dev_database(engine: AsyncEngine) -> None:
    """Add missing columns to existing SQLite tables (dev mode only).

    Safe to call multiple times — only adds columns that don't exist.
    """
    try:
        async with engine.begin() as conn:
            for table, columns in _MISSING_COLUMNS.items():
                existing = await conn.run_sync(_get_existing_columns_sync, table)
                for col_name, col_type in columns:
                    if col_name not in existing:
                        sql = f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}"
                        await conn.execute(text(sql))
                        logger.info("Migration: added column %s.%s (%s)", table, col_name, col_type)
    except Exception:
        logger.exception("Schema migration failed (non-fatal)")
