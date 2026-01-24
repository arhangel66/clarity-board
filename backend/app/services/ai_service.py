"""AI service for processing user input and generating card operations."""

import json
import logging
from typing import Any

from openai import OpenAI

from app.models import (
    AIOperationAskQuestion,
    AIOperationCreateCard,
    AIOperationCreateConnection,
    AIResponse,
    CardCreate,
    CardType,
    ConnectionCreate,
    ConnectionType,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a fact-card therapy assistant based on Kurpatov's methodology.

Your role:
1. Convert user input into concrete FACTS, not abstractions
2. If user gives an abstraction ("I'm tired", "I feel bad"), ask for specifics - what exactly happened?
3. For each valid fact, determine: type, emoji, importance, confidence
4. Propose connections between cards when you see relationships
5. Periodically ask about "empty zones" - what's missing?

Card types:
- question (purple): The central problem being explored
- fact (blue): Concrete, verifiable events/data - "I sleep 5 hours", "I have a 500k loan"
- pain (red): Problems, tensions, fears - specific ones, not abstract
- resource (green): Assets, helpers, opportunities - things that can help
- hypothesis (yellow): Unverified assumptions - things to check

Important rules:
- Be concise in card text (max 100 characters)
- Choose appropriate emoji that captures the essence
- importance: 0-1, how central this fact is to the problem
- confidence: 0-1, how certain this is a fact (1.0 for verified facts, lower for assumptions)
- If something sounds like an abstraction, ASK for concrete facts behind it
- When proposing connections, use "root" to connect to the central question

You must respond ONLY with valid JSON in this exact format:
{
  "operations": [
    {
      "type": "create_card",
      "card": {
        "text": "Card text here",
        "type": "fact",
        "emoji": "emoji",
        "importance": 0.7,
        "confidence": 1.0
      }
    },
    {
      "type": "create_connection",
      "connection": {
        "from_text": "partial text of source card",
        "to_text": "root",
        "type": "causes",
        "strength": 0.8
      }
    },
    {
      "type": "ask_question",
      "text": "Clarifying question here?"
    }
  ]
}

Connection types: "causes", "relates", "contradicts", "blocks"

IMPORTANT: Always respond with valid JSON only. No markdown, no explanations outside the JSON."""


class AIService:
    """Service for AI-powered card operations."""

    def __init__(self, openai_client: OpenAI) -> None:
        """Initialize AI service.

        Args:
            openai_client: OpenAI client instance.
        """
        self.client = openai_client
        self.model = "gpt-4o-mini"  # TODO: switch to gpt-5-mini-2025-08-07 when available

    async def process_user_message(
        self,
        message: str,
        session_question: str,
        existing_cards_texts: list[str],
    ) -> AIResponse:
        """Process user message and generate card operations.

        Args:
            message: User's input message.
            session_question: The central question of the session.
            existing_cards_texts: List of existing card texts for context.

        Returns:
            AIResponse with operations to perform.
        """
        # Build context about existing cards
        context = f"Central question: {session_question}\n"
        if existing_cards_texts:
            context += f"Existing cards: {', '.join(existing_cards_texts)}\n"
        context += f"\nUser says: {message}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": context},
                ],
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                return AIResponse(operations=[])

            return self._parse_response(content)

        except Exception as e:
            logger.error(f"Error processing message with AI: {e}")
            # Return a fallback ask_question operation
            return AIResponse(
                operations=[
                    AIOperationAskQuestion(
                        type="ask_question",
                        text="Could you tell me more about that? What specifically happened?",
                    )
                ]
            )

    def _parse_response(self, content: str) -> AIResponse:
        """Parse AI response JSON into AIResponse model.

        Args:
            content: Raw JSON string from AI.

        Returns:
            Parsed AIResponse.
        """
        try:
            data = json.loads(content)
            operations: list[
                AIOperationCreateCard | AIOperationCreateConnection | AIOperationAskQuestion
            ] = []

            for op in data.get("operations", []):
                op_type = op.get("type")

                if op_type == "create_card":
                    card_data = op.get("card", {})
                    try:
                        card_type = CardType(card_data.get("type", "fact"))
                    except ValueError:
                        card_type = CardType.FACT

                    card = CardCreate(
                        text=card_data.get("text", "")[:200],
                        type=card_type,
                        emoji=card_data.get("emoji", ""),
                        importance=self._clamp_float(card_data.get("importance", 0.5)),
                        confidence=self._clamp_float(card_data.get("confidence", 0.8)),
                    )
                    operations.append(AIOperationCreateCard(type="create_card", card=card))

                elif op_type == "create_connection":
                    conn_data = op.get("connection", {})
                    try:
                        conn_type = ConnectionType(conn_data.get("type", "relates"))
                    except ValueError:
                        conn_type = ConnectionType.RELATES

                    connection = ConnectionCreate(
                        from_text=conn_data.get("from_text", ""),
                        to_text=conn_data.get("to_text", "root"),
                        type=conn_type,
                        strength=self._clamp_float(conn_data.get("strength", 0.5)),
                        label=conn_data.get("label"),
                    )
                    operations.append(
                        AIOperationCreateConnection(type="create_connection", connection=connection)
                    )

                elif op_type == "ask_question":
                    text = op.get("text", "Could you tell me more?")
                    operations.append(AIOperationAskQuestion(type="ask_question", text=text))

            return AIResponse(operations=operations)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response JSON: {e}")
            return AIResponse(
                operations=[
                    AIOperationAskQuestion(
                        type="ask_question",
                        text="I didn't quite understand. Could you rephrase that?",
                    )
                ]
            )

    def _clamp_float(self, value: Any, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Clamp a value to float range.

        Args:
            value: Value to clamp.
            min_val: Minimum value.
            max_val: Maximum value.

        Returns:
            Clamped float value.
        """
        try:
            f = float(value)
            return max(min_val, min(max_val, f))
        except (TypeError, ValueError):
            return 0.5
