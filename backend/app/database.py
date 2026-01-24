"""SQLite database setup and operations."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models import Card, CardType, Connection, ConnectionType, CreatedBy, Session


class Database:
    """SQLite database handler for Fact Card System."""

    def __init__(self, db_path: str = "fact_cards.db") -> None:
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = Path(db_path)
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cards (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                text TEXT NOT NULL,
                type TEXT NOT NULL,
                emoji TEXT DEFAULT '',
                color TEXT DEFAULT '#3B82F6',
                importance REAL DEFAULT 0.5,
                confidence REAL DEFAULT 0.8,
                x REAL DEFAULT 0.5,
                y REAL DEFAULT 0.5,
                target_x REAL DEFAULT 0.5,
                target_y REAL DEFAULT 0.5,
                pinned INTEGER DEFAULT 0,
                is_root INTEGER DEFAULT 0,
                is_new INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                embedding TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS connections (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                from_id TEXT NOT NULL,
                to_id TEXT NOT NULL,
                type TEXT NOT NULL,
                strength REAL DEFAULT 0.5,
                label TEXT,
                created_by TEXT DEFAULT 'ai',
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (from_id) REFERENCES cards(id) ON DELETE CASCADE,
                FOREIGN KEY (to_id) REFERENCES cards(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_cards_session ON cards(session_id);
            CREATE INDEX IF NOT EXISTS idx_connections_session ON connections(session_id);
        """
        )

        conn.commit()
        conn.close()

    # --- Session Operations ---

    def create_session(self, session: Session) -> Session:
        """Create a new session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sessions (id, question, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                session.id,
                session.question,
                session.created_at.isoformat(),
                session.updated_at.isoformat(),
            ),
        )

        conn.commit()
        conn.close()
        return session

    def get_session(self, session_id: str) -> Session | None:
        """Get a session by ID with all cards and connections."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        cards = self.get_cards_by_session(session_id)
        connections = self.get_connections_by_session(session_id)

        session = Session(
            id=row["id"],
            question=row["question"],
            cards=cards,
            connections=connections,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

        conn.close()
        return session

    def update_session_timestamp(self, session_id: str) -> None:
        """Update session's updated_at timestamp."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE sessions SET updated_at = ? WHERE id = ?",
            (datetime.utcnow().isoformat(), session_id),
        )

        conn.commit()
        conn.close()

    # --- Card Operations ---

    def create_card(self, session_id: str, card: Card) -> Card:
        """Create a new card in a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        embedding_json = json.dumps(card.embedding) if card.embedding else None

        cursor.execute(
            """
            INSERT INTO cards (
                id, session_id, text, type, emoji, color,
                importance, confidence, x, y, target_x, target_y,
                pinned, is_root, is_new, created_at, embedding
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                card.id,
                session_id,
                card.text,
                card.type.value,
                card.emoji,
                card.color,
                card.importance,
                card.confidence,
                card.x,
                card.y,
                card.target_x,
                card.target_y,
                int(card.pinned),
                int(card.is_root),
                int(card.is_new),
                card.created_at.isoformat(),
                embedding_json,
            ),
        )

        conn.commit()
        conn.close()
        return card

    def get_cards_by_session(self, session_id: str) -> list[Card]:
        """Get all cards for a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cards WHERE session_id = ?", (session_id,))
        rows = cursor.fetchall()

        cards = []
        for row in rows:
            embedding = json.loads(row["embedding"]) if row["embedding"] else None
            card = Card(
                id=row["id"],
                text=row["text"],
                type=CardType(row["type"]),
                emoji=row["emoji"],
                color=row["color"],
                importance=row["importance"],
                confidence=row["confidence"],
                x=row["x"],
                y=row["y"],
                target_x=row["target_x"],
                target_y=row["target_y"],
                pinned=bool(row["pinned"]),
                is_root=bool(row["is_root"]),
                is_new=bool(row["is_new"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                embedding=embedding,
            )
            cards.append(card)

        conn.close()
        return cards

    def update_card(self, card_id: str, updates: dict[str, Any]) -> None:
        """Update a card with partial data."""
        if not updates:
            return

        conn = self._get_connection()
        cursor = conn.cursor()

        set_clauses = []
        values = []

        for key, value in updates.items():
            if key == "embedding":
                set_clauses.append(f"{key} = ?")
                values.append(json.dumps(value) if value else None)
            elif isinstance(value, bool):
                set_clauses.append(f"{key} = ?")
                values.append(int(value))
            else:
                set_clauses.append(f"{key} = ?")
                values.append(value)

        values.append(card_id)

        cursor.execute(
            f"UPDATE cards SET {', '.join(set_clauses)} WHERE id = ?",
            values,
        )

        conn.commit()
        conn.close()

    def get_card_by_id(self, card_id: str) -> Card | None:
        """Get a card by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        embedding = json.loads(row["embedding"]) if row["embedding"] else None
        card = Card(
            id=row["id"],
            text=row["text"],
            type=CardType(row["type"]),
            emoji=row["emoji"],
            color=row["color"],
            importance=row["importance"],
            confidence=row["confidence"],
            x=row["x"],
            y=row["y"],
            target_x=row["target_x"],
            target_y=row["target_y"],
            pinned=bool(row["pinned"]),
            is_root=bool(row["is_root"]),
            is_new=bool(row["is_new"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            embedding=embedding,
        )

        conn.close()
        return card

    # --- Connection Operations ---

    def create_connection(self, session_id: str, connection: Connection) -> Connection:
        """Create a new connection in a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO connections (
                id, session_id, from_id, to_id, type, strength, label, created_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                connection.id,
                session_id,
                connection.from_id,
                connection.to_id,
                connection.type.value,
                connection.strength,
                connection.label,
                connection.created_by.value,
            ),
        )

        conn.commit()
        conn.close()
        return connection

    def get_connections_by_session(self, session_id: str) -> list[Connection]:
        """Get all connections for a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM connections WHERE session_id = ?", (session_id,))
        rows = cursor.fetchall()

        connections = []
        for row in rows:
            connection = Connection(
                id=row["id"],
                from_id=row["from_id"],
                to_id=row["to_id"],
                type=ConnectionType(row["type"]),
                strength=row["strength"],
                label=row["label"],
                created_by=CreatedBy(row["created_by"]),
            )
            connections.append(connection)

        conn.close()
        return connections

    def find_card_by_text(self, session_id: str, text: str) -> Card | None:
        """Find a card by text (partial match)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # First try exact match
        cursor.execute(
            "SELECT * FROM cards WHERE session_id = ? AND text = ?",
            (session_id, text),
        )
        row = cursor.fetchone()

        # If not found, try partial match
        if not row:
            cursor.execute(
                "SELECT * FROM cards WHERE session_id = ? AND text LIKE ?",
                (session_id, f"%{text}%"),
            )
            row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        embedding = json.loads(row["embedding"]) if row["embedding"] else None
        card = Card(
            id=row["id"],
            text=row["text"],
            type=CardType(row["type"]),
            emoji=row["emoji"],
            color=row["color"],
            importance=row["importance"],
            confidence=row["confidence"],
            x=row["x"],
            y=row["y"],
            target_x=row["target_x"],
            target_y=row["target_y"],
            pinned=bool(row["pinned"]),
            is_root=bool(row["is_root"]),
            is_new=bool(row["is_new"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            embedding=embedding,
        )

        conn.close()
        return card

    def get_root_card(self, session_id: str) -> Card | None:
        """Get the root card for a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM cards WHERE session_id = ? AND is_root = 1",
            (session_id,),
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        embedding = json.loads(row["embedding"]) if row["embedding"] else None
        card = Card(
            id=row["id"],
            text=row["text"],
            type=CardType(row["type"]),
            emoji=row["emoji"],
            color=row["color"],
            importance=row["importance"],
            confidence=row["confidence"],
            x=row["x"],
            y=row["y"],
            target_x=row["target_x"],
            target_y=row["target_y"],
            pinned=bool(row["pinned"]),
            is_root=bool(row["is_root"]),
            is_new=bool(row["is_new"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            embedding=embedding,
        )

        conn.close()
        return card
