import json
from pathlib import Path

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
                        "question_en": "What else is important to consider?",
                        "hint": "Подумайте о деталях.",
                        "hint_en": "Think about the details.",
                    }
                ],
            }
        ],
        "total_questions": 1,
    }
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


def _make_state(cards_count: int, locale: str = "ru") -> State:
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
        locale=locale,
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


def test_special_question_uses_locale_en(tmp_path) -> None:
    data_path = _make_questions_file(tmp_path)
    service = MainService(
        state_service=DummyStateService(),
        ai_service=DummyAIService(),
        special_questions_service=SpecialQuestionsService(data_path),
    )
    service.state = _make_state(cards_count=5, locale="en")

    prompt = service.request_special_question()

    assert prompt is not None
    assert prompt["question"] == "What else is important to consider?"
    assert prompt["category_label"] == "Test"


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


def test_real_special_question_deck_metadata_is_consistent() -> None:
    data_path = Path(__file__).resolve().parents[1] / "data" / "questions.json"
    payload = json.loads(data_path.read_text(encoding="utf-8"))

    assert payload["total_questions"] == sum(
        len(category["questions"]) for category in payload["categories"]
    )
    assert [category["name"] for category in payload["categories"]] == [
        "Ракурс",
        "Структура",
        "Контекст",
    ]
    assert [category["name_en"] for category in payload["categories"]] == [
        "Perspective",
        "Structure",
        "Context",
    ]

    for category in payload["categories"]:
        assert category["questions"]
        for question in category["questions"]:
            assert question["question"].strip()
            assert question["question_en"].strip()


def test_real_special_question_service_localizes_category_labels() -> None:
    service = SpecialQuestionsService()

    prompt_ru = service.get_question_by_id("reflector:1", locale="ru")
    prompt_en = service.get_question_by_id("reflector:1", locale="en")

    assert prompt_ru is not None
    assert prompt_en is not None
    assert prompt_ru.category_label == "Ракурс"
    assert prompt_en.category_label == "Perspective"
