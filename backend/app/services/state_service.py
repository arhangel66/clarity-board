"""State service for session persistence with JSON blob storage."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.models import (
    DEFAULT_QUESTIONS,
    Card,
    CardType,
    Connection,
    ConnectionType,
    CreatedBy,
    SessionPhase,
    SpecialQuestion,
    SpecialQuestionAnswer,
    State,
)


class StateService:
    """Service for persisting session state as JSON blob."""

    def __init__(self, db_path: str = "fact_cards.db") -> None:
        """Initialize state service.

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
        """Initialize database schema with single sessions table."""
        conn = self._get_connection()
        cursor = conn.cursor()

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
        self._ensure_column(cursor, "user_id", "TEXT")
        self._ensure_column(cursor, "title", "TEXT")
        conn.commit()
        conn.close()

    def _ensure_column(self, cursor: sqlite3.Cursor, name: str, column_type: str) -> None:
        cursor.execute("PRAGMA table_info(sessions)")
        columns = {row["name"] for row in cursor.fetchall()}
        if name not in columns:
            cursor.execute(f"ALTER TABLE sessions ADD COLUMN {name} {column_type}")

    def get(self, session_id: str) -> State | None:
        """Load state from DB by session ID (no user check).

        Args:
            session_id: Session ID.

        Returns:
            State or None if not found.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT state_json FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return self._deserialize_state(row["state_json"])

    def get_for_user(self, session_id: str, user_id: str) -> State | None:
        """Load state for a user (and claim legacy rows if needed).

        Args:
            session_id: Session ID.
            user_id: Authenticated user ID.

        Returns:
            State or None if not found or not owned by user.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT state_json, user_id FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        stored_user_id = row["user_id"]
        if stored_user_id and stored_user_id != user_id:
            conn.close()
            return None

        if not stored_user_id:
            cursor.execute("UPDATE sessions SET user_id = ? WHERE id = ?", (user_id, session_id))
            conn.commit()

        state = self._deserialize_state(row["state_json"])
        if not state.user_id:
            state.user_id = user_id
        conn.close()
        return state

    def get_or_create(self, session_id: str, question: str = "", user_id: str = "") -> State:
        """Get existing state OR create new one.

        Args:
            session_id: Session ID.
            question: Central problem (used only when creating new state).
            user_id: Authenticated user ID.

        Returns:
            State object.
        """
        existing = self.get_for_user(session_id, user_id) if user_id else self.get(session_id)
        if existing:
            return existing

        # Create new state with default question
        phase = SessionPhase.QUESTION
        default_q, default_hint = DEFAULT_QUESTIONS[phase]

        return State(
            session_id=session_id,
            user_id=user_id,
            question=question,
            phase=phase,
            current_question=default_q,
            current_hint=default_hint,
            phase_index=0,
            puzzlement_turns=0,
            cards=[],
            connections=[],
        )

    def save(self, state: State) -> None:
        """Upsert state to DB as JSON blob.

        Args:
            state: State to save.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()
        title = self._derive_title(state)
        state_json = self._serialize_state(state)

        cursor.execute(
            """
            INSERT INTO sessions (id, user_id, title, state_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                user_id = excluded.user_id,
                title = excluded.title,
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
            """,
            (state.session_id, state.user_id, title, state_json, now, now),
        )

        conn.commit()
        conn.close()

    def _serialize_state(self, state: State) -> str:
        """Serialize State to JSON string.

        Args:
            state: State to serialize.

        Returns:
            JSON string.
        """
        data = {
            "session_id": state.session_id,
            "user_id": state.user_id,
            "question": state.question,
            "phase": state.phase.value,
            "current_question": state.current_question,
            "current_hint": state.current_hint,
            "phase_index": state.phase_index,
            "puzzlement_turns": state.puzzlement_turns,
            "cards": [self._card_to_dict(card) for card in state.cards],
            "connections": [self._connection_to_dict(conn) for conn in state.connections],
            "pending_special_question": (
                state.pending_special_question.model_dump()
                if state.pending_special_question
                else None
            ),
            "special_questions_history": [
                entry.model_dump() for entry in state.special_questions_history
            ],
        }
        return json.dumps(data)

    def _deserialize_state(self, json_str: str) -> State:
        """Deserialize JSON string to State.

        Args:
            json_str: JSON string.

        Returns:
            State object.
        """
        data = json.loads(json_str)

        cards = [self._dict_to_card(c) for c in data.get("cards", [])]
        pending = data.get("pending_special_question")
        history = data.get("special_questions_history", [])

        return State(
            session_id=data["session_id"],
            user_id=data.get("user_id", ""),
            question=data["question"],
            phase=SessionPhase(data["phase"]),
            current_question=data.get("current_question", ""),
            current_hint=data.get("current_hint", ""),
            phase_index=data.get("phase_index", 0),
            puzzlement_turns=data.get("puzzlement_turns", 0),
            cards=cards,
            connections=[self._dict_to_connection(c) for c in data.get("connections", [])],
            pending_special_question=SpecialQuestion(**pending) if pending else None,
            special_questions_history=[SpecialQuestionAnswer(**entry) for entry in history],
        )

    def list_sessions(self, user_id: str) -> list[dict]:
        """List sessions for a user (most recent first)."""
        self._claim_legacy_sessions(user_id)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, state_json, created_at, updated_at FROM sessions WHERE user_id = ? "
            "ORDER BY updated_at DESC",
            (user_id,),
        )
        rows = cursor.fetchall()
        conn.close()

        sessions: list[dict] = []
        for row in rows:
            title = row["title"] or ""
            if not title:
                state = self._deserialize_state(row["state_json"])
                title = self._derive_title(state)
            sessions.append(
                {
                    "id": row["id"],
                    "title": title or "Untitled board",
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
            )
        return sessions

    def _claim_legacy_sessions(self, user_id: str) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET user_id = ? WHERE user_id IS NULL", (user_id,))
        conn.commit()
        conn.close()

    def _derive_title(self, state: State) -> str:
        if state.question:
            return state.question[:80]
        question_card = next((card for card in state.cards if card.type == CardType.QUESTION), None)
        if question_card:
            return question_card.text[:80]
        return "Untitled board"

    def _card_to_dict(self, card: Card) -> dict:
        """Convert Card to dictionary for JSON serialization.

        Args:
            card: Card instance.

        Returns:
            Dictionary representation.
        """
        return {
            "id": card.id,
            "text": card.text,
            "type": card.type.value,
            "emoji": card.emoji,
            "importance": card.importance,
            "confidence": card.confidence,
            "x": card.x,
            "y": card.y,
            "pinned": card.pinned,
        }

    def _dict_to_card(self, data: dict) -> Card:
        """Convert dictionary to Card.

        Args:
            data: Dictionary representation.

        Returns:
            Card instance.
        """
        return Card(
            id=data["id"],
            text=data["text"],
            type=CardType(data["type"]),
            emoji=data.get("emoji", ""),
            importance=data.get("importance", 0.5),
            confidence=data.get("confidence", 0.8),
            x=data.get("x", 0.5),
            y=data.get("y", 0.5),
            pinned=data.get("pinned", False),
        )

    def _connection_to_dict(self, conn: Connection) -> dict:
        """Convert Connection to dictionary for JSON serialization."""
        return {
            "id": conn.id,
            "from_id": conn.from_id,
            "to_id": conn.to_id,
            "type": conn.type.value,
            "strength": conn.strength,
            "label": conn.label,
            "created_by": conn.created_by.value,
        }

    def _dict_to_connection(self, data: dict) -> Connection:
        """Convert dictionary to Connection."""
        return Connection(
            id=data["id"],
            from_id=data["from_id"],
            to_id=data["to_id"],
            type=ConnectionType(data["type"]),
            strength=data.get("strength", 0.5),
            label=data.get("label"),
            created_by=CreatedBy(data.get("created_by", "user")),
        )
