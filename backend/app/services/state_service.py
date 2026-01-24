"""State service for session persistence with JSON blob storage."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.models import (
    DEFAULT_QUESTIONS,
    Card,
    CardType,
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
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """
        )

        conn.commit()
        conn.close()

    def get(self, session_id: str) -> State | None:
        """Load state from DB.

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

    def get_or_create(self, session_id: str, question: str = "") -> State:
        """Get existing state OR create new one.

        Args:
            session_id: Session ID.
            question: Central problem (used only when creating new state).

        Returns:
            State object.
        """
        existing = self.get(session_id)
        if existing:
            return existing

        # Create new state with default question
        phase = SessionPhase.QUESTION
        default_q, default_hint = DEFAULT_QUESTIONS[phase]

        return State(
            session_id=session_id,
            question=question,
            phase=phase,
            current_question=default_q,
            current_hint=default_hint,
            phase_index=0,
            puzzlement_turns=0,
            cards=[],
        )

    def save(self, state: State) -> None:
        """Upsert state to DB as JSON blob.

        Args:
            state: State to save.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()
        state_json = self._serialize_state(state)

        cursor.execute(
            """
            INSERT INTO sessions (id, state_json, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
            """,
            (state.session_id, state_json, now, now),
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
            "question": state.question,
            "phase": state.phase.value,
            "current_question": state.current_question,
            "current_hint": state.current_hint,
            "phase_index": state.phase_index,
            "puzzlement_turns": state.puzzlement_turns,
            "cards": [self._card_to_dict(card) for card in state.cards],
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
            question=data["question"],
            phase=SessionPhase(data["phase"]),
            current_question=data.get("current_question", ""),
            current_hint=data.get("current_hint", ""),
            phase_index=data.get("phase_index", 0),
            puzzlement_turns=data.get("puzzlement_turns", 0),
            cards=cards,
            pending_special_question=SpecialQuestion(**pending) if pending else None,
            special_questions_history=[SpecialQuestionAnswer(**entry) for entry in history],
        )

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
