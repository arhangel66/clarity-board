"""Tests for AI output validation layer."""

from app.models import Card, CardType, SessionPhase, State
from app.services.validator import validate_operations


def _make_state(
    phase: SessionPhase = SessionPhase.FACTS,
    cards: list[Card] | None = None,
) -> State:
    return State(
        session_id="test_session",
        question="Central problem",
        phase=phase,
        current_question="List facts",
        current_hint="",
        phase_index=1,
        puzzlement_turns=3,
        cards=cards or [],
    )


def _question_card(card_id: str = "card_q") -> Card:
    return Card(id=card_id, text="Central problem", type=CardType.QUESTION, x=0.5, y=0.5)


def _fact_card(card_id: str = "card_f", text: str = "Some fact") -> Card:
    return Card(id=card_id, text=text, type=CardType.FACT, x=0.6, y=0.6)


# --- Duplicate detection ---


def test_duplicate_card_is_rejected() -> None:
    """Card with near-identical text to existing card is filtered out."""
    state = _make_state(cards=[_fact_card(text="Boss rejected 3 reports")])
    ops = [
        {
            "type": "create_card",
            "card": {"text": "boss rejected 3 reports", "type": "fact", "x": 0.3, "y": 0.4},
        },
    ]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_similar_card_above_threshold_is_rejected() -> None:
    """Card with >80% similarity to existing is rejected."""
    state = _make_state(cards=[_fact_card(text="Sales dropped by 30%")])
    ops = [
        {
            "type": "create_card",
            "card": {"text": "Sales dropped by 30", "type": "fact", "x": 0.3, "y": 0.4},
        },
    ]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_different_card_is_accepted() -> None:
    """Card with different text passes validation."""
    state = _make_state(cards=[_fact_card(text="Boss rejected 3 reports")])
    ops = [
        {
            "type": "create_card",
            "card": {"text": "Team has 5 members", "type": "fact", "x": 0.3, "y": 0.4},
        },
    ]

    result = validate_operations(ops, state)

    assert len(result) == 1


def test_batch_duplicates_within_same_response() -> None:
    """Two identical cards in the same AI response — second is rejected."""
    state = _make_state(cards=[])
    ops = [
        {
            "type": "create_card",
            "card": {"text": "New fact alpha", "type": "fact", "x": 0.3, "y": 0.4},
        },
        {
            "type": "create_card",
            "card": {"text": "new fact alpha", "type": "fact", "x": 0.5, "y": 0.6},
        },
    ]

    result = validate_operations(ops, state)

    assert len(result) == 1


# --- Coordinate validation ---


def test_out_of_bounds_coords_are_clamped() -> None:
    """Coordinates outside [0,1] are clamped, not rejected."""
    state = _make_state()
    ops = [
        {
            "type": "create_card",
            "card": {"text": "Valid text", "type": "fact", "x": 1.5, "y": -0.3},
        },
    ]

    result = validate_operations(ops, state)

    assert len(result) == 1
    assert result[0]["card"]["x"] == 1.0
    assert result[0]["card"]["y"] == 0.0


def test_valid_coords_pass_through() -> None:
    """Valid coordinates are preserved."""
    state = _make_state()
    ops = [
        {"type": "create_card", "card": {"text": "Valid text", "type": "fact", "x": 0.3, "y": 0.7}},
    ]

    result = validate_operations(ops, state)

    assert result[0]["card"]["x"] == 0.3
    assert result[0]["card"]["y"] == 0.7


# --- Text length validation ---


def test_long_text_is_truncated() -> None:
    """Text exceeding 200 char model limit is truncated, not rejected."""
    state = _make_state()
    long_text = "A" * 250
    ops = [
        {"type": "create_card", "card": {"text": long_text, "type": "fact", "x": 0.5, "y": 0.5}},
    ]

    result = validate_operations(ops, state)

    assert len(result) == 1
    assert len(result[0]["card"]["text"]) == 200


def test_text_within_limit_passes_through() -> None:
    """Text within 200 char limit passes through unchanged."""
    state = _make_state()
    text = "A" * 150
    ops = [
        {"type": "create_card", "card": {"text": text, "type": "fact", "x": 0.5, "y": 0.5}},
    ]

    result = validate_operations(ops, state)

    assert len(result) == 1
    assert len(result[0]["card"]["text"]) == 150


# --- Root card protection ---


def test_delete_question_card_blocked() -> None:
    """AI cannot delete the question card."""
    state = _make_state(cards=[_question_card(), _fact_card()])
    ops = [{"type": "delete_card", "card_id": "card_q"}]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_update_question_card_blocked_outside_phase1() -> None:
    """AI cannot update question card outside Phase 1."""
    state = _make_state(phase=SessionPhase.FACTS, cards=[_question_card()])
    ops = [{"type": "update_card", "card_id": "card_q", "updates": {"text": "New text"}}]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_update_question_card_allowed_in_phase1() -> None:
    """AI can update question card in Phase 1."""
    state = _make_state(phase=SessionPhase.QUESTION, cards=[_question_card()])
    ops = [{"type": "update_card", "card_id": "card_q", "updates": {"text": "Refined problem"}}]

    result = validate_operations(ops, state)

    assert len(result) == 1


# --- Invalid card_id references ---


def test_update_nonexistent_card_rejected() -> None:
    """Update referencing non-existent card ID is rejected."""
    state = _make_state(cards=[_fact_card()])
    ops = [{"type": "update_card", "card_id": "card_nonexistent", "updates": {"text": "New"}}]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_delete_nonexistent_card_rejected() -> None:
    """Delete referencing non-existent card ID is rejected."""
    state = _make_state(cards=[_fact_card()])
    ops = [{"type": "delete_card", "card_id": "card_nonexistent"}]

    result = validate_operations(ops, state)

    assert len(result) == 0


# --- Empty / malformed operations ---


def test_empty_text_create_rejected() -> None:
    """Create card with empty text is rejected."""
    state = _make_state()
    ops = [{"type": "create_card", "card": {"text": "", "type": "fact", "x": 0.5, "y": 0.5}}]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_unknown_operation_type_rejected() -> None:
    """Unknown operation type is filtered out."""
    state = _make_state()
    ops = [{"type": "explode_card", "card_id": "card_f"}]

    result = validate_operations(ops, state)

    assert len(result) == 0


def test_delete_fact_card_allowed() -> None:
    """Deleting a regular fact card is allowed."""
    state = _make_state(cards=[_question_card(), _fact_card()])
    ops = [{"type": "delete_card", "card_id": "card_f"}]

    result = validate_operations(ops, state)

    assert len(result) == 1
    assert result[0]["card_id"] == "card_f"
