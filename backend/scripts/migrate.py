#!/usr/bin/env python3
"""Managed schema migrations for Fact Card SQLite database."""

from __future__ import annotations

import argparse
import sqlite3
from collections.abc import Callable
from pathlib import Path


def _sessions_columns(cursor: sqlite3.Cursor) -> set[str]:
    cursor.execute("PRAGMA table_info(sessions)")
    return {row[1] for row in cursor.fetchall()}


def migration_0001_sessions_base(cursor: sqlite3.Cursor) -> None:
    """Create baseline sessions schema."""
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            state_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS sessions_user_id_idx ON sessions(user_id);
        """
    )


def migration_0002_ensure_user_id(cursor: sqlite3.Cursor) -> None:
    """Ensure sessions.user_id exists for compatibility with older DB files."""
    columns = _sessions_columns(cursor)
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE sessions ADD COLUMN user_id TEXT")


def migration_0003_ensure_title(cursor: sqlite3.Cursor) -> None:
    """Ensure sessions.title exists for compatibility with older DB files."""
    columns = _sessions_columns(cursor)
    if "title" not in columns:
        cursor.execute("ALTER TABLE sessions ADD COLUMN title TEXT")


MIGRATIONS: list[tuple[str, Callable[[sqlite3.Cursor], None]]] = [
    ("0001_sessions_base", migration_0001_sessions_base),
    ("0002_ensure_user_id", migration_0002_ensure_user_id),
    ("0003_ensure_title", migration_0003_ensure_title),
]


def _ensure_meta_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )


def _applied_versions(cursor: sqlite3.Cursor) -> set[str]:
    cursor.execute("SELECT version FROM schema_migrations")
    return {row[0] for row in cursor.fetchall()}


def apply_migrations(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    _ensure_meta_table(cursor)
    conn.commit()
    applied = _applied_versions(cursor)

    for version, migration_fn in MIGRATIONS:
        if version in applied:
            continue
        migration_fn(cursor)
        cursor.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))
        conn.commit()
        print(f"Applied migration: {version}")

    conn.close()
    print(f"Migrations complete for: {db_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run managed SQLite migrations.")
    default_db = Path(__file__).resolve().parents[1] / "data" / "fact_cards.db"
    parser.add_argument("--db-path", type=Path, default=default_db, help="Path to SQLite DB file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    apply_migrations(args.db_path)
