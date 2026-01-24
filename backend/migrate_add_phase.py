"""Migration script to add phase column to sessions table."""

import sqlite3
from pathlib import Path


def migrate() -> None:
    """Add phase column to sessions table if it doesn't exist."""
    db_path = Path(__file__).parent / "fact_cards.db"

    if not db_path.exists():
        print(f"Database not found at {db_path}, skipping migration.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if phase column exists
    cursor.execute("PRAGMA table_info(sessions)")
    columns = [col[1] for col in cursor.fetchall()]

    if "phase" not in columns:
        print("Adding phase column to sessions table...")
        cursor.execute("ALTER TABLE sessions ADD COLUMN phase TEXT DEFAULT 'question'")
        conn.commit()
        print("Migration complete!")
    else:
        print("Phase column already exists, skipping migration.")

    conn.close()


if __name__ == "__main__":
    migrate()
