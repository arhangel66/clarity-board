import json

from app.models import Card, CardType, SessionPhase, State
from app.services.main_service import MainService
from app.services.special_questions import SpecialQuestionsService


class DummyStateService:
    def save(self, state: State) -> None:  # pragma: no cover - not used
        pass


class DummyAIService:
    async def generate_response(self, message: str, state: State) -> str:
        return """{
            "operations": [],
            "question_action": "keep",
            "next_question": null,
            "next_hint": null
        }"""


def _make_questions_file(tmp_path) -> str:
    payload = {
        "title": "Test",
        "author": "Test",
        "categories": [
            {
                "id": "test",
                "name": "Test",
                "name_en": "Test",
                "color": "red",
                "questions": [
                    {
                        "id": 1,
                        "question": "Что еще важно учесть?",
                        "hint": "Подумайте о деталях.",
                    }
                ],
            }
        ],
        "total_questions": 1,
    }
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


def _make_state(cards_count: int) -> State:
    cards = [
        Card(
            id=f"card_{i}",
            text=f"Fact {i}",
            type=CardType.FACT,
            x=0.5,
            y=0.5,
        )
        for i in range(cards_count)
    ]
    return State(
        session_id="session_1",
        question="Central problem",
        phase=SessionPhase.FACTS,
        current_question="List concrete facts.",
        current_hint="",
        phase_index=1,
        puzzlement_turns=3,
        cards=cards,
    )


def test_special_question_always_unlocked(tmp_path) -> None:
    data_path = _make_questions_file(tmp_path)
    service = MainService(
        state_service=DummyStateService(),
        ai_service=DummyAIService(),
        special_questions_service=SpecialQuestionsService(data_path),
    )
    # Even with 0 cards, it should be unlocked now
    service.state = _make_state(cards_count=0)

    prompt = service.request_special_question()

    assert prompt is not None
    assert prompt["id"] == "test:1"


def test_special_question_records_pending_and_history(tmp_path) -> None:
    data_path = _make_questions_file(tmp_path)
    service = MainService(
        state_service=DummyStateService(),
        ai_service=DummyAIService(),
        special_questions_service=SpecialQuestionsService(data_path),
    )
    service.state = _make_state(cards_count=10)

    prompt = service.request_special_question()

    assert prompt is not None
    assert service.state.pending_special_question is not None
    assert service.state.pending_special_question.question == "Что еще важно учесть?"
    assert len(service.state.special_questions_history) == 1
    assert service.state.special_questions_history[0].answer is None


def test_special_question_answer_clears_pending(tmp_path) -> None:
    data_path = _make_questions_file(tmp_path)
    service = MainService(
        state_service=DummyStateService(),
        ai_service=DummyAIService(),
        special_questions_service=SpecialQuestionsService(data_path),
    )
    service.state = _make_state(cards_count=10)

    prompt = service.request_special_question()
    assert prompt is not None
    question_id = prompt["id"]

    service._record_special_answer(question_id, "Нужно учесть сроки.")

    assert service.state.pending_special_question is None
    assert service.state.special_questions_history[0].answer == "Нужно учесть сроки."
