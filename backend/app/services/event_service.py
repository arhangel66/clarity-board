"""Structured event logging service."""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class EventService:
    """Logs structured analytics events to a JSON-lines file."""

    def __init__(self, log_path: str | None = None) -> None:
        if log_path is None:
            data_dir = Path(__file__).resolve().parents[2] / "data"
            data_dir.mkdir(exist_ok=True)
            log_path = str(data_dir / "events.jsonl")
        self.log_path = Path(log_path)

    def _write(self, event: dict) -> None:
        event["timestamp"] = datetime.now(UTC).isoformat()
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except OSError:
            logger.exception("Failed to write event")

    def session_start(self, session_id: str, user_id: str) -> None:
        self._write(
            {
                "event": "session_start",
                "session_id": session_id,
                "user_id": user_id,
            }
        )

    def session_end(self, session_id: str, user_id: str, card_count: int, phase: str) -> None:
        self._write(
            {
                "event": "session_end",
                "session_id": session_id,
                "user_id": user_id,
                "card_count": card_count,
                "phase_reached": phase,
            }
        )

    def card_created(self, session_id: str, user_id: str, card_type: str, created_by: str) -> None:
        self._write(
            {
                "event": "card_created",
                "session_id": session_id,
                "user_id": user_id,
                "card_type": card_type,
                "created_by": created_by,
            }
        )

    def connection_created(self, session_id: str, user_id: str, connection_type: str) -> None:
        self._write(
            {
                "event": "connection_created",
                "session_id": session_id,
                "user_id": user_id,
                "connection_type": connection_type,
            }
        )

    def phase_changed(self, session_id: str, user_id: str, from_phase: str, to_phase: str) -> None:
        self._write(
            {
                "event": "phase_changed",
                "session_id": session_id,
                "user_id": user_id,
                "from_phase": from_phase,
                "to_phase": to_phase,
            }
        )

    def ai_call(self, session_id: str, user_id: str, message_length: int) -> None:
        self._write(
            {
                "event": "ai_call",
                "session_id": session_id,
                "user_id": user_id,
                "message_length": message_length,
            }
        )

    def special_question_used(self, session_id: str, user_id: str, question_id: str) -> None:
        self._write(
            {
                "event": "special_question_used",
                "session_id": session_id,
                "user_id": user_id,
                "question_id": question_id,
            }
        )

    def user_message(self, session_id: str, user_id: str, input_type: str) -> None:
        self._write(
            {
                "event": "user_message",
                "session_id": session_id,
                "user_id": user_id,
                "input_type": input_type,
            }
        )
