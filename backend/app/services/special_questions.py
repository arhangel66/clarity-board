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
        self._questions = self._load_questions()

    def _default_path(self) -> Path:
        return Path(__file__).resolve().parents[3] / "data" / "questions.json"

    def _load_questions(self) -> list[SpecialQuestion]:
        if not self.data_path.exists():
            return []

        with self.data_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        questions: list[SpecialQuestion] = []
        for category in data.get("categories", []):
            category_id = str(category.get("id", ""))
            for question in category.get("questions", []):
                q_id = f"{category_id}:{question.get('id')}"
                questions.append(
                    SpecialQuestion(
                        id=q_id,
                        category_id=category_id,
                        question=str(question.get("question", "")).strip(),
                        hint=str(question.get("hint", "")).strip(),
                    )
                )

        return questions

    def random_question(self, exclude_ids: set[str] | None = None) -> SpecialQuestion | None:
        """Return a random question, avoiding exclude_ids when possible."""
        if not self._questions:
            return None

        exclude_ids = exclude_ids or set()
        available = [q for q in self._questions if q.id not in exclude_ids]
        if not available:
            available = self._questions
        return random.choice(available)
