"""Tests for MainService business logic."""

import asyncio

import pytest

from app.access import AccessBlockedError, AccessService
from app.models import Card, CardType, SessionPhase, SpecialQuestion, State
from app.services.main_service import MainService
from app.services.state_service import StateService


class DummyStateService:
    def save(self, state: State) -> None:
        pass


class DummyAIService:
    def __init__(self, response_json: str | None = None) -> None:
        self.response_json = response_json or '{"operations": [], "question_action": "keep"}'
        self.call_count = 0

    async def generate_response(self, message: str, state: State) -> str:
        self.call_count += 1
        return self.response_json


def make_service(state: State) -> MainService:
    service = MainService(state_service=DummyStateService(), ai_service=DummyAIService())
    service.state = state
    return service


def test_delete_question_card_blocked() -> None:
    """Cannot delete a question card."""
    question_card = Card(
        id="card_q",
        text="Central problem",
        type=CardType.QUESTION,
        x=0.5,
        y=0.5,
    )
    fact_card = Card(
        id="card_f",
        text="Some fact",
        type=CardType.FACT,
        x=0.6,
        y=0.6,
    )
    state = State(
        session_id="session_1",
        question="Central problem",
        phase=SessionPhase.FACTS,
        current_question="List concrete facts.",
        current_hint="",
        phase_index=1,
        puzzlement_turns=3,
        cards=[question_card, fact_card],
    )

    service = make_service(state)

    result_question = service._delete_card("card_q")
    assert result_question is False
    assert len(state.cards) == 2

    result_fact = service._delete_card("card_f")
    assert result_fact is True
    assert len(state.cards) == 1
    assert state.cards[0].id == "card_q"


def test_apply_operations_handles_multiple_create_cards() -> None:
    """Multiple create_card operations from single AI response are processed."""
    state = State(
        session_id="session_2",
        question="Problem",
        phase=SessionPhase.FACTS,
        current_question="List facts",
        current_hint="",
        phase_index=1,
        puzzlement_turns=3,
        cards=[],
    )

    service = make_service(state)

    card_data_1 = {
        "text": "First fact",
        "type": CardType.FACT.value,
        "emoji": "1️⃣",
        "importance": 0.5,
        "confidence": 0.8,
        "x": 0.3,
        "y": 0.4,
    }
    card_data_2 = {
        "text": "Second fact",
        "type": CardType.FACT.value,
        "emoji": "2️⃣",
        "importance": 0.6,
        "confidence": 0.7,
        "x": 0.7,
        "y": 0.6,
    }

    card1 = service._create_card(card_data_1)
    card2 = service._create_card(card_data_2)
    state.cards.append(card1)
    state.cards.append(card2)

    assert len(state.cards) == 2
    assert state.cards[0].text == "First fact"
    assert state.cards[1].text == "Second fact"


def test_special_question_clears_pending_after_answer() -> None:
    """After answering, pending_special_question should be cleared."""
    special_q = SpecialQuestion(
        id="sq_1",
        category_id="cat_1",
        question="What is your biggest fear?",
        hint="Be honest",
    )
    state = State(
        session_id="session_3",
        question="Problem",
        phase=SessionPhase.FACTS,
        current_question="List facts",
        current_hint="",
        phase_index=1,
        puzzlement_turns=3,
        cards=[],
        pending_special_question=special_q,
        special_questions_history=[],
    )

    from app.models import SpecialQuestionAnswer

    state.special_questions_history.append(
        SpecialQuestionAnswer(
            id="sq_1",
            category_id="cat_1",
            question="What is your biggest fear?",
            hint="Be honest",
            answer=None,
            asked_at="2024-01-01T00:00:00",
            answered_at=None,
        )
    )

    service = make_service(state)
    service._record_special_answer("sq_1", "Fear of failure")

    assert state.pending_special_question is None

    answered_entry = state.special_questions_history[0]
    assert answered_entry.answer == "Fear of failure"
    assert answered_entry.answered_at is not None


def test_process_user_message_records_new_session_consumption(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    access_service = AccessService(state_service=state_service)
    ai_service = DummyAIService()
    service = MainService(
        state_service=state_service,
        ai_service=ai_service,
        access_service=access_service,
    )
    service.user_id = "user_1"
    service.session_id = "session_new"
    service.state = state_service.get_or_create("session_new", question="", user_id="user_1")
    state_service.save(service.state)

    asyncio.run(service.process_user_message("Help me think this through"))

    snapshot = access_service.get_access_snapshot("user_1")
    assert snapshot.status.free_sessions_used == 1
    assert snapshot.status.free_sessions_remaining == 2
    assert ai_service.call_count == 1


def test_process_user_message_blocks_blank_session_after_limit(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    access_service = AccessService(state_service=state_service)
    ai_service = DummyAIService()
    service = MainService(
        state_service=state_service,
        ai_service=ai_service,
        access_service=access_service,
    )
    service.user_id = "user_1"
    service.session_id = "session_blocked"
    service.state = state_service.get_or_create("session_blocked", question="", user_id="user_1")
    state_service.save(service.state)

    for session_id in ("used_1", "used_2", "used_3"):
        access_service.record_session_consumed("user_1", session_id)

    with pytest.raises(AccessBlockedError):
        asyncio.run(service.process_user_message("Need a fourth session"))

    assert ai_service.call_count == 0


def test_process_user_message_allows_existing_started_session_after_limit(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    access_service = AccessService(state_service=state_service)
    ai_service = DummyAIService()
    state = State(session_id="session_started", user_id="user_1", question="Started already")
    state_service.save(state)

    service = MainService(
        state_service=state_service,
        ai_service=ai_service,
        access_service=access_service,
    )
    service.user_id = "user_1"
    service.session_id = state.session_id
    service.state = state

    for session_id in ("used_1", "used_2", "used_3"):
        access_service.record_session_consumed("user_1", session_id)

    asyncio.run(service.process_user_message("Continue the existing board"))

    assert ai_service.call_count == 1


def test_guard_question_refinements_blocks_after_limit() -> None:
    """Question card updates are blocked after 1 refinement."""
    question_card = Card(
        id="card_q",
        text="Central problem",
        type=CardType.QUESTION,
        x=0.5,
        y=0.5,
    )
    state = State(
        session_id="session_guard",
        question="Central problem",
        phase=SessionPhase.QUESTION,
        current_question="Define your problem",
        current_hint="",
        phase_index=0,
        puzzlement_turns=1,
        question_refinement_count=1,
        cards=[question_card],
    )

    service = make_service(state)

    operations = [
        {"type": "update_card", "card_id": "card_q", "updates": {"text": "New text"}},
        {"type": "create_card", "card": {"text": "A fact", "type": "fact", "x": 0.3, "y": 0.4}},
    ]

    result = service._guard_question_refinements(operations)

    assert len(result) == 1
    assert result[0]["type"] == "create_card"


def test_guard_question_refinements_allows_below_limit() -> None:
    """Question card updates are allowed when below limit."""
    question_card = Card(
        id="card_q",
        text="Central problem",
        type=CardType.QUESTION,
        x=0.5,
        y=0.5,
    )
    state = State(
        session_id="session_guard2",
        question="Central problem",
        phase=SessionPhase.QUESTION,
        current_question="Define your problem",
        current_hint="",
        phase_index=0,
        puzzlement_turns=1,
        question_refinement_count=0,
        cards=[question_card],
    )

    service = make_service(state)

    operations = [
        {"type": "update_card", "card_id": "card_q", "updates": {"text": "Refined"}},
    ]

    result = service._guard_question_refinements(operations)

    assert len(result) == 1
