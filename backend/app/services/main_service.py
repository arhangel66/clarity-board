"""Main service - per-connection orchestrator."""

import logging
import uuid

from app.models import (
    CARD_TYPE_COLORS,
    DEFAULT_QUESTIONS,
    PHASE_ORDER,
    Card,
    CardType,
    InitResult,
    ProcessResult,
    QuestionAction,
    State,
)
from app.services.ai_service import AIService
from app.services.decoder import decode_ai_response
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

    def __init__(
        self,
        state_service: StateService,
        ai_service: AIService,
    ) -> None:
        """Initialize main service.

        Args:
            state_service: State persistence service.
            ai_service: AI service for LLM calls.
        """
        self.state_service = state_service
        self.ai_service = ai_service

        # Per-connection state
        self.session_id: str | None = None
        self.state: State | None = None

    def init(self, session_id: str | None) -> InitResult:
        """Handle init message - load existing session or prepare for new.

        Args:
            session_id: Session ID from client localStorage (or None).

        Returns:
            InitResult with session data or ready flag.
        """
        if session_id:
            self.session_id = session_id
            self.state = self.state_service.get(session_id)

            if self.state:
                # Existing session found
                return InitResult(
                    session_loaded={
                        "id": self.state.session_id,
                        "question": self.state.question,
                    },
                    cards=[self._card_to_dict(card) for card in self.state.cards],
                    question_update={
                        "phase": self.state.phase.value,
                        "question": self.state.current_question,
                        "hint": self.state.current_hint,
                        "phaseIndex": self.state.phase_index,
                    },
                )

        # No session_id or session not found - generate new ID, wait for first message
        self.session_id = generate_id("session")
        self.state = None
        return InitResult(ready=True)

    def new_session(self) -> None:
        """Reset for new session (called on clear_session message)."""
        self.session_id = generate_id("session")
        self.state = None

    async def process_user_message(self, message: str) -> ProcessResult:
        """Process user message - create session if needed, run AI, update state.

        Args:
            message: User's input text.

        Returns:
            ProcessResult with cards and question update.
        """
        # Ensure we have state
        self.state = self.state or self.state_service.get_or_create(
            self.session_id, question=message
        )

        is_new_session = len(self.state.cards) == 0

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
                card = self._create_card(op["card"])
                self.state.cards.append(card)
                new_cards.append(card)

            elif op_type == "update_card":
                result = self._update_card(op["card_id"], op["updates"])
                if result:
                    updated_cards.append(result)

            elif op_type == "delete_card":
                if self._delete_card(op["card_id"]):
                    deleted_card_ids.append(op["card_id"])

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
            },
        )

    def handle_card_move(self, card_id: str, x: float, y: float, pinned: bool) -> dict | None:
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
                self.state_service.save(self.state)
                return {
                    "id": card_id,
                    "x": x,
                    "y": y,
                    "pinned": pinned,
                }

        return None

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
                    # Fallback to DEFAULT_QUESTIONS
                    question, hint = DEFAULT_QUESTIONS[next_phase]
                    self.state.current_question = question
                    self.state.current_hint = hint

        elif ai_response.question_action == QuestionAction.CLARIFY:
            # Use AI's custom question
            if ai_response.next_question:
                self.state.current_question = ai_response.next_question
            if ai_response.next_hint:
                self.state.current_hint = ai_response.next_hint

        # KEEP: don't change the question

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

        # Don't allow updating question card
        if card.type == CardType.QUESTION:
            logger.warning(f"Attempted to update question card: {card_id}")
            return None

        # Apply updates
        result: dict = {"id": card_id}

        if "text" in updates:
            # Regular cards only (question cards blocked above)
            card.text = updates["text"][:50]
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
            "is_root": card.type == CardType.QUESTION,
        }
