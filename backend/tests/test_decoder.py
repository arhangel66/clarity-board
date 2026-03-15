"""Tests for decoder module - pure function that parses AI responses."""

import pytest

from app.models import Card, CardType, QuestionAction
from app.services.decoder import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    MIN_DISTANCE,
    _clamp_float,
    _parse_card,
    decode_ai_response,
    deconflict_positions,
)


def test_decode_valid_create_card() -> None:
    """AI creates a card - verify all fields are parsed correctly."""
    raw_json = """{
        "operations": [{
            "type": "create_card",
            "card": {
                "text": "Test fact about situation",
                "type": "fact",
                "emoji": "📝",
                "importance": 0.7,
                "confidence": 0.9,
                "x": 960,
                "y": 540
            }
        }],
        "question_action": "keep",
        "next_question": null,
        "next_hint": null
    }"""

    result = decode_ai_response(raw_json)

    assert len(result.operations) == 1
    assert result.operations[0]["type"] == "create_card"

    card = result.operations[0]["card"]
    assert card["text"] == "Test fact about situation"
    assert card["type"] == "fact"
    assert card["emoji"] == "📝"
    assert card["importance"] == 0.7
    assert card["confidence"] == 0.9
    assert card["x"] == pytest.approx(0.5, abs=0.01)
    assert card["y"] == pytest.approx(0.5, abs=0.01)

    assert result.question_action == QuestionAction.KEEP
    assert result.next_question is None


def test_decode_invalid_json_returns_clarify() -> None:
    """Malformed JSON -> fallback with CLARIFY action."""
    raw_json = "{ this is not valid json }"

    result = decode_ai_response(raw_json)

    assert result.operations == []
    assert result.question_action == QuestionAction.CLARIFY
    assert result.next_question is not None
    assert "understand" in result.next_question.lower()


def test_decode_unknown_card_type_defaults_to_fact() -> None:
    """Invalid card type -> defaults to CardType.FACT."""
    card_data = {
        "text": "Some text",
        "type": "unknown_type",
        "x": 500,
        "y": 300,
    }

    result = _parse_card(card_data)

    assert result is not None
    assert result["type"] == CardType.FACT.value


def test_decode_position_normalization() -> None:
    """Pixel coordinates (1920x1080) -> normalized [0,1] coordinates."""
    card_data = {
        "text": "Test card",
        "type": "fact",
        "x": CANVAS_WIDTH,
        "y": CANVAS_HEIGHT,
    }

    result = _parse_card(card_data)

    assert result is not None
    assert result["x"] == pytest.approx(0.95, abs=0.01)
    assert result["y"] == pytest.approx(0.95, abs=0.01)

    card_data_zero = {
        "text": "Test card",
        "type": "fact",
        "x": 0,
        "y": 0,
    }

    result_zero = _parse_card(card_data_zero)
    assert result_zero["x"] == pytest.approx(0.05, abs=0.01)
    assert result_zero["y"] == pytest.approx(0.05, abs=0.01)


def test_decode_text_truncation() -> None:
    """Question card: 100 chars max, other cards: 50 chars max."""
    long_text = "A" * 200

    question_card = _parse_card({"text": long_text, "type": "question", "x": 500, "y": 300})
    fact_card = _parse_card({"text": long_text, "type": "fact", "x": 500, "y": 300})

    assert question_card is not None
    assert len(question_card["text"]) == 100

    assert fact_card is not None
    assert len(fact_card["text"]) == 50


def test_clamp_float_handles_invalid_input() -> None:
    """Invalid values (None, 'abc', {}) -> default 0.5."""
    assert _clamp_float(None) == 0.5
    assert _clamp_float("abc") == 0.5
    assert _clamp_float({}) == 0.5
    assert _clamp_float([]) == 0.5

    assert _clamp_float(0.3) == 0.3
    assert _clamp_float(1.5) == 1.0
    assert _clamp_float(-0.5) == 0.0


def test_deconflict_positions_shifts_overlapping_cards() -> None:
    """Cards placed too close to existing ones get shifted."""
    existing = [
        Card(id="card_1", text="Existing", type=CardType.FACT, x=0.5, y=0.5),
    ]
    operations = [
        {
            "type": "create_card",
            "card": {"text": "New", "type": "fact", "x": 0.5, "y": 0.5},
        },
    ]

    result = deconflict_positions(operations, existing)

    card = result[0]["card"]
    dx = card["x"] - 0.5
    dy = card["y"] - 0.5
    distance = (dx**2 + dy**2) ** 0.5
    assert distance >= MIN_DISTANCE


def test_deconflict_positions_no_shift_when_far_apart() -> None:
    """Cards far apart are not shifted."""
    existing = [
        Card(id="card_1", text="Existing", type=CardType.FACT, x=0.2, y=0.2),
    ]
    operations = [
        {
            "type": "create_card",
            "card": {"text": "New", "type": "fact", "x": 0.8, "y": 0.8},
        },
    ]

    result = deconflict_positions(operations, existing)

    card = result[0]["card"]
    assert card["x"] == pytest.approx(0.8, abs=0.001)
    assert card["y"] == pytest.approx(0.8, abs=0.001)


def test_deconflict_positions_handles_multiple_new_cards() -> None:
    """Multiple new cards at same position all get unique positions."""
    existing: list[Card] = []
    operations = [
        {"type": "create_card", "card": {"text": f"Card {i}", "type": "fact", "x": 0.5, "y": 0.5}}
        for i in range(3)
    ]

    result = deconflict_positions(operations, existing)

    positions = [(op["card"]["x"], op["card"]["y"]) for op in result]
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dx = positions[i][0] - positions[j][0]
            dy = positions[i][1] - positions[j][1]
            distance = (dx**2 + dy**2) ** 0.5
            assert distance >= MIN_DISTANCE * 0.99


def test_deconflict_positions_ignores_non_create_ops() -> None:
    """update_card and delete_card operations are not affected."""
    existing: list[Card] = []
    operations = [
        {"type": "update_card", "card_id": "card_1", "updates": {"text": "Updated"}},
        {"type": "delete_card", "card_id": "card_2"},
    ]

    result = deconflict_positions(operations, existing)

    assert result == operations
