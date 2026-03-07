"""Mock AI service for E2E testing with deterministic responses."""

import json
import logging

from app.models import State
from app.services.decoder import CANVAS_HEIGHT, CANVAS_WIDTH

logger = logging.getLogger(__name__)


class MockAIService:
    """Mock AI service that returns deterministic responses for E2E tests."""

    async def generate_response(self, message: str, state: State) -> str:
        """Return mock response based on message content.

        Args:
            message: User's input message.
            state: Current session state.

        Returns:
            Deterministic JSON string.
        """
        logger.info(f"[MockAI] Processing: {message[:50]}...")

        # Detect language (simple heuristic)
        is_russian = any(char in message.lower() for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

        # Build response based on phase and message content
        operations = []

        # Always create a card from user input
        card_text = message[:50] if len(message) > 50 else message
        card_type = self._detect_card_type(message)

        # Position in pixels — decoder divides by CANVAS_WIDTH/HEIGHT to normalize to [0,1]
        card_count = len(state.cards)
        x = int(CANVAS_WIDTH * (0.3 + (card_count % 3) * 0.2))
        y = int(CANVAS_HEIGHT * (0.3 + (card_count // 3) * 0.15))

        operations.append(
            {
                "type": "create_card",
                "card": {
                    "text": card_text,
                    "type": card_type,
                    "emoji": self._get_emoji(card_type),
                    "importance": 0.7,
                    "confidence": 0.8,
                    "x": x,
                    "y": y,
                },
            }
        )

        # Build response
        response = {
            "operations": operations,
            "current_phase": state.phase.value,
            "question_action": "next",
            "next_question": (
                "Расскажите больше деталей?" if is_russian else "Can you tell me more?"
            ),
            "next_hint": "Факты важны" if is_russian else "Facts matter",
        }

        return json.dumps(response)

    def _detect_card_type(self, message: str) -> str:
        """Detect card type from message content."""
        lower = message.lower()

        if any(word in lower for word in ["?", "почему", "как", "why", "how", "what"]):
            return "question"
        if any(word in lower for word in ["боль", "проблема", "pain", "problem", "issue"]):
            return "pain"
        if any(word in lower for word in ["ресурс", "resource", "have", "есть", "умею"]):
            return "resource"
        if any(word in lower for word in ["гипотеза", "hypothesis", "maybe", "возможно"]):
            return "hypothesis"
        if any(word in lower for word in ["нужно", "надо", "should", "must", "todo", "сделать"]):
            return "todo"

        return "fact"

    def _get_emoji(self, card_type: str) -> str:
        """Get emoji for card type."""
        emojis = {
            "question": "❓",
            "fact": "📌",
            "pain": "😣",
            "resource": "💪",
            "hypothesis": "💡",
            "todo": "✅",
        }
        return emojis.get(card_type, "📌")

    async def translate_question_hint(
        self, question: str, hint: str, locale: str
    ) -> tuple[str, str] | None:
        """Pass through without translation in mock mode."""
        if not question and not hint:
            return None
        return question, hint
