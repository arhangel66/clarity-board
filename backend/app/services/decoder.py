"""Pure function decoder for AI responses."""

import json
import logging
from typing import Any

from app.models import AIResponse, CardType, QuestionAction

logger = logging.getLogger(__name__)

# Canvas dimensions (AI thinks in pixels, we normalize to [0,1])
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080


def decode_ai_response(raw_json: str) -> AIResponse:
    """Decode raw JSON string from AI into AIResponse.

    Pure function - easy to unit test with different JSON inputs.

    Args:
        raw_json: Raw JSON string from AI.

    Returns:
        AIResponse with parsed operations and question action.
    """
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response JSON: {e}")
        return AIResponse(
            operations=[],
            question_action=QuestionAction.CLARIFY,
            next_question="I didn't quite understand. Could you rephrase that?",
        )

    # Parse all operations
    operations = []
    for op in data.get("operations", []):
        parsed = _parse_operation(op)
        if parsed:
            operations.append(parsed)

    # Parse question_action
    action_str = data.get("question_action", "keep")
    try:
        question_action = QuestionAction(action_str)
    except ValueError:
        question_action = QuestionAction.KEEP

    return AIResponse(
        operations=operations,
        question_action=question_action,
        next_question=data.get("next_question"),
        next_hint=data.get("next_hint"),
    )


def _parse_operation(op: dict) -> dict | None:
    """Parse a single operation from AI response.

    Args:
        op: Raw operation dictionary from AI.

    Returns:
        Parsed operation dictionary or None if invalid.
    """
    op_type = op.get("type")

    if op_type == "create_card":
        card_data = op.get("card", {})
        card = _parse_card(card_data)
        if card:
            return {"type": "create_card", "card": card}

    elif op_type == "update_card":
        card_id = op.get("card_id")
        updates = op.get("updates", {})
        if card_id and updates:
            parsed_updates = _parse_card_updates(updates)
            if parsed_updates:
                return {"type": "update_card", "card_id": card_id, "updates": parsed_updates}

    elif op_type == "delete_card":
        card_id = op.get("card_id")
        if card_id:
            return {"type": "delete_card", "card_id": card_id}

    return None


def _parse_card_updates(updates: dict) -> dict | None:
    """Parse card update fields.

    Args:
        updates: Raw updates dictionary from AI.

    Returns:
        Validated updates dictionary or None if empty.
    """
    parsed = {}

    if "text" in updates and updates["text"]:
        # 50 chars limit for regular cards (question cards can't be updated)
        parsed["text"] = str(updates["text"])[:50]

    if "importance" in updates:
        parsed["importance"] = _clamp_float(updates["importance"])

    if "confidence" in updates:
        parsed["confidence"] = _clamp_float(updates["confidence"])

    if "emoji" in updates:
        parsed["emoji"] = str(updates["emoji"])[:4]

    return parsed if parsed else None


def _parse_card(card_data: dict) -> dict | None:
    """Parse card data from AI response.

    Args:
        card_data: Raw card dictionary from AI.

    Returns:
        Normalized card dictionary or None if invalid.
    """
    text = card_data.get("text", "")
    if not text:
        return None

    # Validate and normalize card type
    type_str = card_data.get("type", "fact")
    try:
        card_type = CardType(type_str)
    except ValueError:
        card_type = CardType.FACT

    # Parse and normalize position from pixels to [0,1]
    raw_x = card_data.get("x", CANVAS_WIDTH // 2)
    raw_y = card_data.get("y", CANVAS_HEIGHT // 2)

    # Normalize to [0,1] and clamp to safe boundaries
    x = _clamp_float(raw_x / CANVAS_WIDTH, min_val=0.05, max_val=0.95)
    y = _clamp_float(raw_y / CANVAS_HEIGHT, min_val=0.05, max_val=0.95)

    # Question cards get 100 chars, regular cards get 50 chars
    max_len = 100 if card_type == CardType.QUESTION else 50

    return {
        "text": text[:max_len],
        "type": card_type.value,
        "emoji": card_data.get("emoji", ""),
        "importance": _clamp_float(card_data.get("importance", 0.5)),
        "confidence": _clamp_float(card_data.get("confidence", 0.8)),
        "x": x,
        "y": y,
    }


def _clamp_float(value: Any, min_val: float = 0.0, max_val: float = 1.0) -> float:
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
