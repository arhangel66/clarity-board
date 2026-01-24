#!/usr/bin/env python3
"""CLI REPL для тестирования AI Fact Card логики."""

import asyncio

from app.construct import ai_service
from app.models import (
    AIOperationAskQuestion,
    AIOperationCreateCard,
    AIOperationCreateConnection,
    QuestionAction,
    SessionPhase,
)

# Фазы с начальными вопросами и подсказками
PHASE_CONFIG: dict[SessionPhase, tuple[str, str]] = {
    SessionPhase.FACTS: (
        "What are the concrete facts of the situation?",
        "Numbers, dates, events - things that can be verified",
    ),
    SessionPhase.PAINS: (
        "What specific pains or tensions do you feel?",
        "Physical sensations, emotions, conflicts",
    ),
    SessionPhase.RESOURCES: (
        "What resources do you have available?",
        "Money, people, skills, time, energy",
    ),
    SessionPhase.GAPS: (
        "What information is missing?",
        "What don't you know? What assumptions are you making?",
    ),
    SessionPhase.CONNECTIONS: (
        "What connections do you see between cards?",
        "Causes, contradictions, dependencies",
    ),
}

PHASES_ORDER = [
    SessionPhase.FACTS,
    SessionPhase.PAINS,
    SessionPhase.RESOURCES,
    SessionPhase.GAPS,
    SessionPhase.CONNECTIONS,
]


class CLISession:
    """Минимальное состояние сессии для CLI."""

    def __init__(self, question: str) -> None:
        self.session_question = question
        self.phase_index = 0
        self.phase = PHASES_ORDER[0]
        self.current_question, self.current_hint = PHASE_CONFIG[self.phase]
        self.cards: list[dict[str, str]] = []

    async def process_message(self, text: str) -> str:
        """Обработать сообщение и вернуть текстовый результат."""
        existing_texts = [c["text"] for c in self.cards]

        response = await ai_service.process_user_message(
            message=text,
            phase=self.phase,
            current_question=self.current_question,
            session_question=self.session_question,
            existing_cards_texts=existing_texts,
        )

        # Собрать результат
        output = self._format_response(response)

        # Обновить состояние
        self._update_state(response)

        return output

    def _format_response(self, response) -> str:
        """Форматировать ответ AI в читаемый текст."""
        lines: list[str] = []

        # Карточки
        new_cards = [op for op in response.operations if isinstance(op, AIOperationCreateCard)]
        if new_cards:
            lines.append("\n📦 Новые карточки:")
            for op in new_cards:
                card = op.card
                imp = f"imp: {card.importance:.1f}" if card.importance else ""
                lines.append(f"  [{card.type.value}] {card.emoji} {card.text} ({imp})")
                self.cards.append({"text": card.text, "type": card.type.value})

        # Связи
        connections = [
            op for op in response.operations if isinstance(op, AIOperationCreateConnection)
        ]
        if connections:
            lines.append("\n🔗 Связи:")
            for op in connections:
                conn = op.connection
                lines.append(
                    f'  "{conn.from_text}" --{conn.type.value}--> "{conn.to_text}" ({conn.strength:.1f})'
                )

        # Вопросы от AI
        questions = [op for op in response.operations if isinstance(op, AIOperationAskQuestion)]
        if questions:
            lines.append("\n💬 AI спрашивает:")
            for op in questions:
                lines.append(f"  {op.text}")

        return "\n".join(lines) if lines else "(нет операций)"

    def _update_state(self, response) -> None:
        """Обновить фазу/вопрос по ответу AI."""
        # Обновить вопрос/подсказку если AI дал новые
        if response.next_question:
            self.current_question = response.next_question
        if response.next_hint:
            self.current_hint = response.next_hint

        # Перейти к следующей фазе если AI сказал "next"
        if response.question_action == QuestionAction.NEXT:
            if self.phase_index < len(PHASES_ORDER) - 1:
                self.phase_index += 1
                self.phase = PHASES_ORDER[self.phase_index]
                q, h = PHASE_CONFIG[self.phase]
                self.current_question = response.next_question or q
                self.current_hint = response.next_hint or h

    def print_status(self) -> None:
        """Вывести текущий статус."""
        phase_num = self.phase_index + 1
        total = len(PHASES_ORDER)
        print(f"\n📍 Фаза: {self.phase.value} ({phase_num}/{total})")
        print(f"❓ {self.current_question}")
        print(f"💡 {self.current_hint}")


async def main() -> None:
    """Main CLI loop."""
    print("\n🎯 Fact Card CLI")
    print("=" * 40)
    print("Команды: cards - показать карточки, q/quit/exit - выход\n")

    question = input("Введи центральный вопрос (Enter для примера): ").strip()
    if not question:
        question = "Как улучшить баланс работа/жизнь?"

    session = CLISession(question)

    print(f"\n📋 Центральный вопрос: {question}")
    session.print_status()

    while True:
        try:
            print()
            user_input = input("> ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                break

            if user_input.lower() == "cards":
                print("\n📚 Все карточки:")
                if not session.cards:
                    print("  (пусто)")
                for c in session.cards:
                    print(f"  [{c['type']}] {c['text']}")
                continue

            if user_input.lower() == "phase":
                session.print_status()
                continue

            if user_input.lower() == "next":
                # Принудительно следующая фаза
                if session.phase_index < len(PHASES_ORDER) - 1:
                    session.phase_index += 1
                    session.phase = PHASES_ORDER[session.phase_index]
                    q, h = PHASE_CONFIG[session.phase]
                    session.current_question = q
                    session.current_hint = h
                    session.print_status()
                else:
                    print("🏁 Это последняя фаза!")
                continue

            result = await session.process_message(user_input)
            print(result)
            session.print_status()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback

            traceback.print_exc()

    print("\n👋 Пока!")


if __name__ == "__main__":
    asyncio.run(main())
