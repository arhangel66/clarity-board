"""Validation layer for AI-generated card operations.

Pure functions that filter out invalid operations before they reach the canvas.
All rejections are logged with structured details for analysis.
"""

import logging
from difflib import SequenceMatcher

from app.models import CardType, SessionPhase, State

logger = logging.getLogger(__name__)

# Similarity threshold for duplicate detection (0.0–1.0)
DUPLICATE_THRESHOLD = 0.8

# Coordinate bounds
MIN_COORD = 0.0
MAX_COORD = 1.0

# Text length limits (match Card model max_length=200;
# decoder applies stricter 50/100 summarization limits upstream)
MAX_TEXT_REGULAR = 200
MAX_TEXT_QUESTION = 200


def validate_operations(
    operations: list[dict],
    state: State,
    session_id: str = "",
) -> list[dict]:
    """Validate a list of decoded AI operations against current state.

    Filters out invalid operations and logs each rejection.

    Args:
        operations: Decoded operations from AI response.
        state: Current session state with existing cards.
        session_id: Session ID for logging context.

    Returns:
        List of valid operations only.
    """
    valid: list[dict] = []
    existing_texts = [_normalize_text(c.text) for c in state.cards]
    card_ids = {c.id for c in state.cards}

    for op in operations:
        op_type = op.get("type")

        if op_type == "create_card":
            result = _validate_create_card(op, existing_texts, state, session_id)
            if result:
                # Track the new text so subsequent creates in the same batch
                # are also checked for duplicates against each other
                existing_texts.append(_normalize_text(result["card"]["text"]))
                valid.append(result)

        elif op_type == "update_card":
            result = _validate_update_card(op, card_ids, state, session_id)
            if result:
                valid.append(result)

        elif op_type == "delete_card":
            result = _validate_delete_card(op, card_ids, state, session_id)
            if result:
                valid.append(result)

        else:
            _log_rejection(session_id, "unknown_operation", f"Unknown op type: {op_type}")

    return valid


def _validate_create_card(
    op: dict,
    existing_texts: list[str],
    state: State,
    session_id: str,
) -> dict | None:
    """Validate a create_card operation."""
    card = op.get("card", {})
    text = card.get("text", "")

    if not text:
        _log_rejection(session_id, "empty_text", "create_card with empty text")
        return None

    # Check text length
    card_type = card.get("type", "fact")
    max_len = MAX_TEXT_QUESTION if card_type == CardType.QUESTION.value else MAX_TEXT_REGULAR
    if len(text) > max_len:
        _log_rejection(
            session_id,
            "text_too_long",
            f"Text {len(text)} chars, max {max_len}: '{text[:30]}...'",
        )
        card = {**card, "text": text[:max_len]}

    # Check coordinates
    x = card.get("x", 0.5)
    y = card.get("y", 0.5)
    if not (_is_valid_coord(x) and _is_valid_coord(y)):
        _log_rejection(
            session_id,
            "coords_out_of_bounds",
            f"Coordinates ({x}, {y}) out of [0,1] range, clamping",
        )
        card = {
            **card,
            "x": _clamp(x),
            "y": _clamp(y),
        }

    # Check for duplicates
    normalized = _normalize_text(text)
    for existing in existing_texts:
        similarity = _text_similarity(normalized, existing)
        if similarity >= DUPLICATE_THRESHOLD:
            _log_rejection(
                session_id,
                "duplicate_card",
                f"Text '{text[:30]}' is {similarity:.0%} similar to existing card",
            )
            return None

    return {"type": "create_card", "card": card}


def _validate_update_card(
    op: dict,
    card_ids: set[str],
    state: State,
    session_id: str,
) -> dict | None:
    """Validate an update_card operation."""
    card_id = op.get("card_id")
    updates = op.get("updates", {})

    if not card_id:
        _log_rejection(session_id, "missing_card_id", "update_card without card_id")
        return None

    if card_id not in card_ids:
        _log_rejection(session_id, "card_not_found", f"update_card references unknown {card_id}")
        return None

    # Check root card protection
    target_card = next((c for c in state.cards if c.id == card_id), None)
    if target_card and target_card.type == CardType.QUESTION:
        if state.phase != SessionPhase.QUESTION:
            _log_rejection(
                session_id,
                "root_card_protection",
                f"Attempted to update question card {card_id} outside Phase 1",
            )
            return None

    # Validate text length in updates
    if "text" in updates:
        text = updates["text"]
        if target_card:
            max_len = (
                MAX_TEXT_QUESTION if target_card.type == CardType.QUESTION else MAX_TEXT_REGULAR
            )
            if len(text) > max_len:
                _log_rejection(
                    session_id,
                    "text_too_long",
                    f"Update text {len(text)} chars, max {max_len}",
                )
                updates = {**updates, "text": text[:max_len]}

    return {"type": "update_card", "card_id": card_id, "updates": updates}


def _validate_delete_card(
    op: dict,
    card_ids: set[str],
    state: State,
    session_id: str,
) -> dict | None:
    """Validate a delete_card operation."""
    card_id = op.get("card_id")

    if not card_id:
        _log_rejection(session_id, "missing_card_id", "delete_card without card_id")
        return None

    if card_id not in card_ids:
        _log_rejection(session_id, "card_not_found", f"delete_card references unknown {card_id}")
        return None

    # Protect root card
    target_card = next((c for c in state.cards if c.id == card_id), None)
    if target_card and target_card.type == CardType.QUESTION:
        _log_rejection(
            session_id,
            "root_card_protection",
            f"Attempted to delete question card {card_id}",
        )
        return None

    return {"type": "delete_card", "card_id": card_id}


def _normalize_text(text: str) -> str:
    """Normalize text for comparison: lowercase, strip, collapse whitespace."""
    return " ".join(text.lower().strip().split())


def _text_similarity(a: str, b: str) -> float:
    """Calculate text similarity ratio between two normalized strings."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _is_valid_coord(value: float) -> bool:
    """Check if coordinate is within [0, 1]."""
    try:
        f = float(value)
        return MIN_COORD <= f <= MAX_COORD
    except (TypeError, ValueError):
        return False


def _clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp a value to range."""
    try:
        return max(min_val, min(max_val, float(value)))
    except (TypeError, ValueError):
        return 0.5


def _log_rejection(session_id: str, event_type: str, details: str) -> None:
    """Log a validation rejection with structured context."""
    logger.warning(
        "AI validation rejected: %s | session=%s | %s",
        event_type,
        session_id,
        details,
    )
