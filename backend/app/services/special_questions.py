"""Special questions service for curated prompt deck."""

from __future__ import annotations

import json
import random
from pathlib import Path

from app.models import SpecialQuestion


class SpecialQuestionsService:
    """Load and serve random special questions from a JSON deck."""

    def __init__(self, data_path: str | Path | None = None) -> None:
        self.data_path = Path(data_path) if data_path else self._default_path()
        self._questions_by_locale, self._index_by_locale = self._load_questions()

    def _default_path(self) -> Path:
        return Path(__file__).resolve().parents[3] / "data" / "questions.json"

    def _load_questions(
        self,
    ) -> tuple[dict[str, list[SpecialQuestion]], dict[str, dict[str, SpecialQuestion]]]:
        if not self.data_path.exists():
            return {"ru": [], "en": []}, {"ru": {}, "en": {}}

        with self.data_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        questions_by_locale: dict[str, list[SpecialQuestion]] = {"ru": [], "en": []}
        index_by_locale: dict[str, dict[str, SpecialQuestion]] = {"ru": {}, "en": {}}
        for category in data.get("categories", []):
            category_id = str(category.get("id", ""))
            for question in category.get("questions", []):
                q_id = f"{category_id}:{question.get('id')}"
                question_ru = str(question.get("question", "")).strip()
                hint_ru = str(question.get("hint", "")).strip()
                question_en = str(question.get("question_en", "")).strip() or question_ru
                hint_en = str(question.get("hint_en", "")).strip() or hint_ru

                for locale, q_text, h_text in (
                    ("ru", question_ru, hint_ru),
                    ("en", question_en, hint_en),
                ):
                    if not q_text:
                        continue
                    entry = SpecialQuestion(
                        id=q_id,
                        category_id=category_id,
                        question=q_text,
                        hint=h_text,
                    )
                    questions_by_locale[locale].append(entry)
                    index_by_locale[locale][q_id] = entry

        return questions_by_locale, index_by_locale

    def random_question(
        self, exclude_ids: set[str] | None = None, locale: str = "ru"
    ) -> SpecialQuestion | None:
        """Return a random question, avoiding exclude_ids when possible."""
        normalized = self._normalize_locale(locale)
        questions = self._questions_by_locale.get(normalized, [])
        if not questions:
            return None

        exclude_ids = exclude_ids or set()
        available = [q for q in questions if q.id not in exclude_ids]
        if not available:
            available = questions
        return random.choice(available)

    def get_question_by_id(self, question_id: str, locale: str = "ru") -> SpecialQuestion | None:
        normalized = self._normalize_locale(locale)
        return self._index_by_locale.get(normalized, {}).get(question_id)

    @staticmethod
    def _normalize_locale(locale: str | None) -> str:
        value = str(locale or "").strip().lower()
        if value.startswith("en"):
            return "en"
        return "ru"
