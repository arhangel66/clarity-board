"""Special questions service for curated prompt deck."""

from __future__ import annotations

import json
import logging
import random
from pathlib import Path

from app.models import SpecialQuestion

logger = logging.getLogger(__name__)


class SpecialQuestionsService:
    """Load and serve random special questions from a JSON deck."""

    def __init__(self, data_path: str | Path | None = None) -> None:
        self.data_path = Path(data_path) if data_path else self._default_path()
        self._questions_by_locale, self._index_by_locale = self._load_questions()

    def _default_path(self) -> Path:
        # In container: /app/app/services/special_questions.py -> parents[2] = /app
        return Path(__file__).resolve().parents[2] / "data" / "questions.json"

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
            category_label_ru = str(category.get("name", "")).strip() or category_id
            category_label_en = str(category.get("name_en", "")).strip() or category_label_ru
            for question in category.get("questions", []):
                q_id = f"{category_id}:{question.get('id')}"
                question_ru = str(question.get("question", "")).strip()
                hint_ru = str(question.get("hint", "")).strip()
                question_en = str(question.get("question_en", "")).strip() or question_ru
                hint_en = str(question.get("hint_en", "")).strip() or hint_ru

                for locale, q_text, h_text, category_label in (
                    ("ru", question_ru, hint_ru, category_label_ru),
                    ("en", question_en, hint_en, category_label_en),
                ):
                    if not q_text:
                        continue
                    entry = SpecialQuestion(
                        id=q_id,
                        category_id=category_id,
                        category_label=category_label,
                        question=q_text,
                        hint=h_text,
                    )
                    questions_by_locale[locale].append(entry)
                    index_by_locale[locale][q_id] = entry

        actual_total = sum(
            len(category.get("questions", [])) for category in data.get("categories", [])
        )
        declared_total = data.get("total_questions")
        if isinstance(declared_total, int) and declared_total != actual_total:
            logger.warning(
                "Special question deck total_questions mismatch: declared=%s actual=%s",
                declared_total,
                actual_total,
            )

        return questions_by_locale, index_by_locale

    def random_question(
        self, exclude_ids: set[str] | None = None, locale: str = "ru"
    ) -> SpecialQuestion | None:
        """Return a random question, avoiding exclude_ids when possible."""
        normalized = self._normalize_locale(locale)
        questions = self._questions_by_locale.get(normalized, [])
        if not questions:
            logger.error(f"No questions found for locale: {normalized}")
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
