from app.models import AIResponse, Card, CardType, QuestionAction, SessionPhase, State
from app.services.main_service import MainService


class DummyStateService:
    def save(self, state: State) -> None:  # pragma: no cover - not used
        pass


class DummyAIService:
    pass


def make_service(state: State) -> MainService:
    service = MainService(state_service=DummyStateService(), ai_service=DummyAIService())
    service.state = state
    return service


def test_question_card_update_allowed_in_phase_question() -> None:
    question_card = Card(
        id="card_q",
        text="Original problem",
        type=CardType.QUESTION,
        x=0.5,
        y=0.5,
    )
    state = State(
        session_id="session_1",
        question="Original problem",
        phase=SessionPhase.QUESTION,
        current_question="State the problem in one sentence.",
        current_hint="",
        phase_index=0,
        puzzlement_turns=1,
        cards=[question_card],
    )

    service = make_service(state)
    result = service._update_card("card_q", {"text": "Refined central problem"})

    assert result is not None
    assert result["text"] == "Refined central problem"
    assert state.cards[0].text == "Refined central problem"


def test_question_card_update_blocked_outside_phase_question() -> None:
    question_card = Card(
        id="card_q",
        text="Original problem",
        type=CardType.QUESTION,
        x=0.5,
        y=0.5,
    )
    state = State(
        session_id="session_2",
        question="Original problem",
        phase=SessionPhase.FACTS,
        current_question="List concrete facts.",
        current_hint="",
        phase_index=1,
        puzzlement_turns=3,
        cards=[question_card],
    )

    service = make_service(state)
    result = service._update_card("card_q", {"text": "Should not update"})

    assert result is None
    assert state.cards[0].text == "Original problem"


def test_phase_transition_delayed_until_min_puzzlement_turns() -> None:
    state = State(
        session_id="session_3",
        question="Initial problem",
        phase=SessionPhase.QUESTION,
        current_question="State the problem in one sentence.",
        current_hint="",
        phase_index=0,
        puzzlement_turns=2,
        cards=[],
    )

    service = make_service(state)
    ai_response = AIResponse(
        question_action=QuestionAction.NEXT,
        next_question="List concrete facts.",
        next_hint="Dates, numbers, actions.",
    )

    service._apply_question_action(ai_response)

    assert state.phase == SessionPhase.QUESTION
    assert state.phase_index == 0
