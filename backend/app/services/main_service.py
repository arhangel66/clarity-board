"""Main service - per-connection orchestrator."""

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

        # 3. Create cards with AI-provided positions
        new_cards = []
        for card_data in ai_response.cards:
            card = self._create_card(card_data)
            self.state.cards.append(card)
            new_cards.append(card)

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
        }
