"""Main service - per-connection orchestrator."""

import logging
import uuid
from datetime import datetime

from app.models import (
    CARD_TYPE_COLORS,
    PHASE_ORDER,
    Card,
    CardType,
    Connection,
    ConnectionType,
    CreatedBy,
    InitResult,
    ProcessResult,
    QuestionAction,
    SessionPhase,
    SpecialQuestionAnswer,
    State,
)
from app.services.ai_service import AIService
from app.services.decoder import decode_ai_response
from app.services.special_questions import SpecialQuestionsService
from app.services.state_service import StateService

logger = logging.getLogger(__name__)


def generate_id(prefix: str = "card") -> str:
    """Generate a unique ID.

    Args:
        prefix: ID prefix.

    Returns:
        Unique ID string.
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


class MainService:
    """Per-connection orchestrator for the Fact Card System."""

    MIN_PUZZLEMENT_TURNS = 3
    SPECIAL_QUESTION_MIN_CARDS = 0

    def __init__(
        self,
        state_service: StateService,
        ai_service: AIService,
        special_questions_service: SpecialQuestionsService | None = None,
    ) -> None:
        """Initialize main service.

        Args:
            state_service: State persistence service.
            ai_service: AI service for LLM calls.
        """
        self.state_service = state_service
        self.ai_service = ai_service
        self.special_questions_service = special_questions_service

        # Per-connection state
        self.session_id: str | None = None
        self.state: State | None = None
        self.user_id: str | None = None
        self.locale: str = "ru"

    def init(self, session_id: str | None, user_id: str, locale: str | None = None) -> InitResult:
        """Handle init message - load existing session or prepare for new.

        Args:
            session_id: Session ID from client localStorage (or None).
            user_id: Authenticated user ID.

        Returns:
            InitResult with session data or ready flag.
        """
        self.user_id = user_id
        if locale:
            self.locale = self._normalize_locale(locale)

        if session_id:
            self.session_id = session_id
            self.state = self.state_service.get_for_user(session_id, user_id)

            if self.state:
                if not locale and self.state.locale:
                    self.locale = self.state.locale
                # Existing session found
                question_update = (
                    {
                        "phase": self.state.phase.value,
                        "question": self.state.current_question,
                        "hint": self.state.current_hint,
                        "phaseIndex": self.state.phase_index,
                        "special_questions_unlocked": self._special_questions_unlocked(),
                    }
                    if self.state.current_question or self.state.current_hint
                    else None
                )
                return InitResult(
                    session_loaded={
                        "id": self.state.session_id,
                        "question": self.state.question,
                    },
                    cards=[self._card_to_dict(card) for card in self.state.cards],
                    question_update=question_update,
                    connections=[self._connection_to_dict(conn) for conn in self.state.connections],
                )

        # No session_id or session not found - create a new session immediately
        self.session_id = generate_id("session")
        self.state = self.state_service.get_or_create(
            self.session_id, question="", user_id=user_id, locale=self.locale
        )
        self._ensure_initial_question_card()
        self.state_service.save(self.state)
        question_update = (
            {
                "phase": self.state.phase.value,
                "question": self.state.current_question,
                "hint": self.state.current_hint,
                "phaseIndex": self.state.phase_index,
                "special_questions_unlocked": self._special_questions_unlocked(),
            }
            if self.state.current_question or self.state.current_hint
            else None
        )
        return InitResult(
            session_loaded={
                "id": self.state.session_id,
                "question": self.state.question,
            },
            cards=[self._card_to_dict(card) for card in self.state.cards],
            question_update=question_update,
        )

    def new_session(self) -> None:
        """Reset for new session (called on clear_session message)."""
        self.session_id = generate_id("session")
        self.state = None

    def create_new_session(self, user_id: str) -> State:
        """Create and persist a new session for a user."""
        self.user_id = user_id
        self.session_id = generate_id("session")
        self.state = self.state_service.get_or_create(
            self.session_id, question="", user_id=user_id, locale=self.locale
        )
        self._ensure_initial_question_card()
        self.state_service.save(self.state)
        return self.state

    async def process_user_message(
        self, message: str, special_question_id: str | None = None
    ) -> ProcessResult:
        """Process user message - create session if needed, run AI, update state.

        Args:
            message: User's input text.

        Returns:
            ProcessResult with cards and question update.
        """
        # Ensure we have state
        self.state = self.state or self.state_service.get_or_create(
            self.session_id,
            question=message,
            user_id=self.user_id or "",
            locale=self.locale,
        )

        is_new_session = len(self.state.cards) == 0

        if not self.state.question:
            self.state.question = message
            self._ensure_initial_question_card()

        if special_question_id:
            self._record_special_answer(special_question_id, message)

        # 1. AI generates raw JSON
        raw_json = await self.ai_service.generate_response(message, self.state)

        # 2. Decode (pure function)
        ai_response = decode_ai_response(raw_json)

        # 3. Process all operations
        new_cards: list[Card] = []
        updated_cards: list[dict] = []
        deleted_card_ids: list[str] = []

        for op in ai_response.operations:
            op_type = op.get("type")

            if op_type == "create_card":
                card_data = op["card"]
                if card_data.get("type") == CardType.QUESTION.value:
                    existing_question = next(
                        (card for card in self.state.cards if card.type == CardType.QUESTION),
                        None,
                    )
                    if existing_question:
                        existing_question.text = card_data["text"][:100]
                        updated_cards.append(
                            {"id": existing_question.id, "text": existing_question.text}
                        )
                    else:
                        card = self._create_card(card_data)
                        self.state.cards.append(card)
                        new_cards.append(card)
                else:
                    card = self._create_card(card_data)
                    self.state.cards.append(card)
                    new_cards.append(card)

            elif op_type == "update_card":
                result = self._update_card(op["card_id"], op["updates"])
                if result:
                    updated_cards.append(result)

            elif op_type == "delete_card":
                if self._delete_card(op["card_id"]):
                    deleted_card_ids.append(op["card_id"])

        if self.state.phase == SessionPhase.QUESTION:
            self.state.puzzlement_turns += 1

        # 4. Update phase based on question_action
        self._apply_question_action(ai_response)

        # 5. Save state
        self.state_service.save(self.state)

        # 6. Build result
        return ProcessResult(
            session_loaded=(
                {"id": self.state.session_id, "question": self.state.question}
                if is_new_session
                else None
            ),
            cards_add=[self._card_to_dict(card) for card in new_cards] if new_cards else None,
            cards_update=updated_cards if updated_cards else None,
            cards_delete=deleted_card_ids if deleted_card_ids else None,
            question_update={
                "phase": self.state.phase.value,
                "question": self.state.current_question,
                "hint": self.state.current_hint,
                "phaseIndex": self.state.phase_index,
                "special_questions_unlocked": self._special_questions_unlocked(),
            },
        )

    def request_special_question(self) -> dict | None:
        """Select a random special question and store it as pending."""
        if not self.state or not self.special_questions_service:
            return None

        if not self._special_questions_unlocked():
            return None

        if self.state.pending_special_question:
            return self.state.pending_special_question.model_dump()

        exclude_ids = {entry.id for entry in self.state.special_questions_history}
        question = self.special_questions_service.random_question(
            exclude_ids, locale=self.state.locale
        )
        if not question:
            return None

        now = datetime.utcnow().isoformat()
        self.state.pending_special_question = question
        self.state.special_questions_history.append(
            SpecialQuestionAnswer(
                id=question.id,
                category_id=question.category_id,
                question=question.question,
                hint=question.hint,
                answer=None,
                asked_at=now,
                answered_at=None,
            )
        )
        self.state_service.save(self.state)
        return question.model_dump()

    def handle_card_move(
        self,
        card_id: str,
        x: float,
        y: float,
        pinned: bool,
        width: float | None = None,
        height: float | None = None,
        custom_scale: float | None = None,
    ) -> dict | None:
        """Handle card move event.

        Args:
            card_id: ID of the card to move.
            x: New x position (0-1).
            y: New y position (0-1).
            pinned: Whether card is pinned.

        Returns:
            Update dict for WebSocket response or None.
        """
        if not self.state:
            return None

        # Find and update card
        for card in self.state.cards:
            if card.id == card_id:
                card.x = x
                card.y = y
                card.pinned = pinned
                if height is not None:
                    card.height = height
                if custom_scale is not None:
                    card.custom_scale = custom_scale
                self.state_service.save(self.state)
                return {
                    "x": x,
                    "y": y,
                    "pinned": pinned,
                    "width": getattr(card, "width", None),
                    "height": getattr(card, "height", None),
                    "custom_scale": getattr(card, "custom_scale", 1.0),
                }

        return None

    def update_card(self, card_id: str, updates: dict) -> dict | None:
        """Update a card from user input and persist.

        Args:
            card_id: ID of card to update.
            updates: Dictionary with fields to update.

        Returns:
            Update dict for WebSocket response or None if failed.
        """
        if not self.state:
            return None

        result = self._update_card(card_id, updates)
        if result:
            self.state_service.save(self.state)
        return result

    def create_connection(
        self,
        from_id: str,
        to_id: str,
        conn_type: str = "relates",
        label: str | None = None,
        created_by: str = "user",
    ) -> dict | None:
        """Create a new connection between cards."""
        if not self.state:
            return None

        # Verify cards exist
        card_ids = {c.id for c in self.state.cards}
        if from_id not in card_ids or to_id not in card_ids:
            logger.warning(f"Attempted to connect non-existent cards: {from_id} -> {to_id}")
            return None

        # Avoid duplicates
        existing = next(
            (c for c in self.state.connections if c.from_id == from_id and c.to_id == to_id), None
        )
        if existing:
            return self._connection_to_dict(existing)

        conn = Connection(
            id=generate_id("conn"),
            from_id=from_id,
            to_id=to_id,
            type=ConnectionType(conn_type),
            label=label,
            created_by=CreatedBy(created_by),
        )
        self.state.connections.append(conn)
        self.state_service.save(self.state)
        return self._connection_to_dict(conn)

    def delete_connection(self, connection_id: str) -> bool:
        """Delete a connection by ID."""
        if not self.state:
            return False

        original_len = len(self.state.connections)
        self.state.connections = [c for c in self.state.connections if c.id != connection_id]

        if len(self.state.connections) < original_len:
            self.state_service.save(self.state)
            return True
        return False

    def _ensure_initial_question_card(self) -> None:
        """Ensure a visible question card exists for the session."""
        if not self.state:
            return
        if not self.state.current_question:
            return

        existing_question = next(
            (card for card in self.state.cards if card.type == CardType.QUESTION),
            None,
        )
        if existing_question:
            return

        question_card = Card(
            id=generate_id("card"),
            text=self.state.current_question,
            type=CardType.QUESTION,
            x=0.5,
            y=0.5,
            pinned=True,
        )
        self.state.cards.append(question_card)

    def _create_card(self, card_data: dict) -> Card:
        """Create a Card from decoded AI data.

        Args:
            card_data: Card data from decoder (includes x, y from AI).

        Returns:
            Complete Card instance.
        """
        return Card(
            id=generate_id("card"),
            text=card_data["text"],
            type=CardType(card_data["type"]),
            emoji=card_data.get("emoji", ""),
            importance=card_data.get("importance", 0.5),
            confidence=card_data.get("confidence", 0.8),
            x=card_data.get("x", 0.5),
            y=card_data.get("y", 0.5),
            pinned=False,
        )

    def _apply_question_action(self, ai_response) -> None:
        """Update phase and question based on AI response.

        Args:
            ai_response: Decoded AI response.
        """
        if (
            self.state.phase == SessionPhase.QUESTION
            and ai_response.question_action == QuestionAction.NEXT
            and self.state.puzzlement_turns < self.MIN_PUZZLEMENT_TURNS
        ):
            ai_response.question_action = QuestionAction.CLARIFY

        if ai_response.question_action == QuestionAction.NEXT:
            # Move to next phase
            current_index = PHASE_ORDER.index(self.state.phase)
            if current_index < len(PHASE_ORDER) - 1:
                next_phase = PHASE_ORDER[current_index + 1]
                self.state.phase = next_phase
                self.state.phase_index = current_index + 1

                # Try AI-generated question first, fallback to defaults
                if ai_response.next_question and ai_response.next_hint:
                    self.state.current_question = ai_response.next_question
                    self.state.current_hint = ai_response.next_hint
                else:
                    # Keep previous question/hint if AI didn't provide them
                    pass

        elif ai_response.question_action == QuestionAction.CLARIFY:
            # Use AI's custom question
            if ai_response.next_question:
                self.state.current_question = ai_response.next_question
            if ai_response.next_hint:
                self.state.current_hint = ai_response.next_hint

        # KEEP: don't change the question

    def _special_questions_unlocked(self) -> bool:
        # Always unlocked for now
        return True

    async def set_locale(self, locale: str) -> dict | None:
        normalized = self._normalize_locale(locale)
        self.locale = normalized

        if not self.state:
            return None

        if self.state.locale == normalized:
            return None

        self.state.locale = normalized

        question_update: dict | None = None
        if self.state.current_question or self.state.current_hint:
            translated = await self.ai_service.translate_question_hint(
                self.state.current_question,
                self.state.current_hint,
                normalized,
            )
            if translated:
                self.state.current_question, self.state.current_hint = translated
            question_update = {
                "phase": self.state.phase.value,
                "question": self.state.current_question,
                "hint": self.state.current_hint,
                "phaseIndex": self.state.phase_index,
                "special_questions_unlocked": self._special_questions_unlocked(),
            }

        special_prompt: dict | None = None
        if self.state.pending_special_question and self.special_questions_service:
            localized = self.special_questions_service.get_question_by_id(
                self.state.pending_special_question.id,
                normalized,
            )
            if localized:
                self.state.pending_special_question = localized
                for entry in reversed(self.state.special_questions_history):
                    if entry.id == localized.id and entry.answer is None:
                        entry.question = localized.question
                        entry.hint = localized.hint
                        break
                special_prompt = localized.model_dump()

        self.state_service.save(self.state)

        if not question_update and not special_prompt:
            return None

        return {"question_update": question_update, "special_prompt": special_prompt}

    def _record_special_answer(self, special_question_id: str, answer: str) -> None:
        if not self.state:
            return

        now = datetime.utcnow().isoformat()
        for entry in reversed(self.state.special_questions_history):
            if entry.id == special_question_id and entry.answer is None:
                entry.answer = answer
                entry.answered_at = now
                break

        if (
            self.state.pending_special_question
            and self.state.pending_special_question.id == special_question_id
        ):
            self.state.pending_special_question = None

    @staticmethod
    def _normalize_locale(locale: str) -> str:
        value = str(locale or "").strip().lower()
        if value.startswith("en"):
            return "en"
        return "ru"

    def _update_card(self, card_id: str, updates: dict) -> dict | None:
        """Update a card with new values.

        Args:
            card_id: ID of card to update.
            updates: Dictionary with fields to update.

        Returns:
            Update dict for WebSocket response or None if failed.
        """
        if not self.state:
            return None

        # Find card
        card = next((c for c in self.state.cards if c.id == card_id), None)
        if not card:
            logger.warning(f"Card not found for update: {card_id}")
            return None

        if card.type == CardType.QUESTION and self.state.phase != SessionPhase.QUESTION:
            logger.warning(f"Attempted to update question card outside Phase 1: {card_id}")
            return None

        # Apply updates
        result: dict = {"id": card_id}

        if "text" in updates:
            max_len = 100 if card.type == CardType.QUESTION else 50
            card.text = str(updates["text"])[:max_len]
            result["text"] = card.text

        if "importance" in updates:
            card.importance = max(0.0, min(1.0, float(updates["importance"])))
            result["importance"] = card.importance

        if "confidence" in updates:
            card.confidence = max(0.0, min(1.0, float(updates["confidence"])))
            result["confidence"] = card.confidence

        if "emoji" in updates:
            card.emoji = updates["emoji"][:4]
            result["emoji"] = card.emoji

        return result if len(result) > 1 else None

    def _delete_card(self, card_id: str) -> bool:
        """Delete a card by ID (internal method for AI operations).

        Args:
            card_id: ID of card to delete.

        Returns:
            True if card was deleted, False otherwise.
        """
        if not self.state:
            return False

        # Find card
        card = next((c for c in self.state.cards if c.id == card_id), None)
        if not card:
            logger.warning(f"Card not found for delete: {card_id}")
            return False

        # Don't allow deleting question card
        if card.type == CardType.QUESTION:
            logger.warning(f"Attempted to delete question card: {card_id}")
            return False

        # Remove card
        self.state.cards = [c for c in self.state.cards if c.id != card_id]
        logger.info(f"Deleted card: {card_id}")

        return True

    def delete_card(self, card_id: str) -> bool:
        """Delete a card from current session (public method with save).

        Args:
            card_id: ID of card to delete.

        Returns:
            True if card was deleted, False otherwise.
        """
        if self._delete_card(card_id):
            self.state_service.save(self.state)
            return True
        return False

    def _card_to_dict(self, card: Card) -> dict:
        """Convert Card to dictionary for WebSocket response.

        Args:
            card: Card instance.

        Returns:
            Dictionary representation for frontend.
        """
        return {
            "id": card.id,
            "text": card.text,
            "type": card.type.value,
            "emoji": card.emoji,
            "color": CARD_TYPE_COLORS.get(card.type, "#3B82F6"),
            "importance": card.importance,
            "confidence": card.confidence,
            "x": card.x,
            "y": card.y,
            "pinned": card.pinned,
            "width": card.width,
            "height": card.height,
            "custom_scale": card.custom_scale,
            "is_root": card.type == CardType.QUESTION,
        }

    def _connection_to_dict(self, conn: Connection) -> dict:
        """Convert Connection to dictionary for WebSocket response.

        Args:
            conn: Connection instance.

        Returns:
            Dictionary representation for frontend.
        """
        return {
            "id": conn.id,
            "from_id": conn.from_id,
            "to_id": conn.to_id,
            "type": conn.type.value,
            "strength": conn.strength,
            "label": conn.label,
            "created_by": conn.created_by.value,
        }
