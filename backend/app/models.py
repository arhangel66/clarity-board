"""Pydantic models for Fact Card System."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class SessionPhase(str, Enum):
    """Phases of the guided therapy flow."""

    QUESTION = "question"
    FACTS = "facts"
    PAINS = "pains"
    RESOURCES = "resources"
    GAPS = "gaps"
    CONNECTIONS = "connections"


class CardType(str, Enum):
    """Types of cards in the system."""

    QUESTION = "question"
    FACT = "fact"
    PAIN = "pain"
    RESOURCE = "resource"
    HYPOTHESIS = "hypothesis"
    TODO = "todo"


class ConnectionType(str, Enum):
    """Types of connections between cards."""

    CAUSES = "causes"
    RELATES = "relates"
    CONTRADICTS = "contradicts"
    BLOCKS = "blocks"


class CreatedBy(str, Enum):
    """Who created the connection."""

    AI = "ai"
    USER = "user"


class QuestionAction(str, Enum):
    """What to do with the current question after processing user answer."""

    KEEP = "keep"  # Keep the same question, user needs to provide more
    NEXT = "next"  # Move to the next question in the flow
    CLARIFY = "clarify"  # Show a clarifying question


# --- Card Model ---


class Card(BaseModel):
    """A card representing a fact, pain, resource, or hypothesis."""

    id: str
    text: str = Field(max_length=200)
    type: CardType
    emoji: str = ""
    importance: float = Field(default=0.5, ge=0, le=1)
    confidence: float = Field(default=0.8, ge=0, le=1)
    x: float = Field(default=0.5, ge=0, le=1)
    y: float = Field(default=0.5, ge=0, le=1)
    pinned: bool = False


# --- Connection Model ---


class Connection(BaseModel):
    """A connection between two cards."""

    id: str
    from_id: str
    to_id: str
    type: ConnectionType = ConnectionType.RELATES
    strength: float = Field(default=0.5, ge=0, le=1)
    label: str | None = None
    created_by: CreatedBy = CreatedBy.USER


# --- State Model ---


class State(BaseModel):
    """Session state - stored as JSON blob in DB."""

    session_id: str
    user_id: str = ""
    question: str  # Central problem
    phase: SessionPhase = SessionPhase.QUESTION
    current_question: str = ""
    current_hint: str = ""
    phase_index: int = 0
    puzzlement_turns: int = 0
    cards: list[Card] = Field(default_factory=list)
    connections: list[Connection] = Field(default_factory=list)
    pending_special_question: SpecialQuestion | None = None
    special_questions_history: list[SpecialQuestionAnswer] = Field(default_factory=list)


# --- AI Response Model ---


class AIResponse(BaseModel):
    """Parsed AI response containing card operations."""

    operations: list[dict] = Field(default_factory=list)  # Parsed operations from AI
    question_action: QuestionAction = QuestionAction.KEEP
    next_question: str | None = None
    next_hint: str | None = None


# --- Service Result Models ---


class InitResult(BaseModel):
    """Result of MainService.init() call."""

    ready: bool = False
    session_loaded: dict | None = None
    cards: list[dict] | None = None
    connections: list[dict] | None = None
    question_update: dict | None = None


class ProcessResult(BaseModel):
    """Result of MainService.process_user_message() call."""

    session_loaded: dict | None = None
    cards_add: list[dict] | None = None
    cards_update: list[dict] | None = None
    cards_delete: list[str] | None = None
    question_update: dict


# --- Special Question Models ---


class SpecialQuestion(BaseModel):
    """A curated question prompt."""

    id: str
    category_id: str
    question: str
    hint: str = ""


class SpecialQuestionAnswer(BaseModel):
    """Stored question + answer pair."""

    id: str
    category_id: str
    question: str
    hint: str = ""
    answer: str | None = None
    asked_at: str
    answered_at: str | None = None


# --- Color Mapping ---


CARD_TYPE_COLORS: dict[CardType, str] = {
    CardType.QUESTION: "#8B5CF6",  # Purple
    CardType.FACT: "#3B82F6",  # Blue
    CardType.PAIN: "#EF4444",  # Red
    CardType.RESOURCE: "#22C55E",  # Green
    CardType.HYPOTHESIS: "#EAB308",  # Yellow
    CardType.TODO: "#14B8A6",  # Teal
}


# --- Phase Configuration ---


DEFAULT_QUESTIONS: dict[SessionPhase, tuple[str, str]] = {
    SessionPhase.QUESTION: (
        "Что самое важное вы хотите сейчас решить?",
        "Сформулируйте коротко.",
    ),
    SessionPhase.FACTS: (
        "List concrete facts.",
        "Dates, numbers, actions.",
    ),
    SessionPhase.PAINS: (
        "What hurts most, specifically?",
        "Concrete symptoms only.",
    ),
    SessionPhase.RESOURCES: (
        "What resources are available?",
        "People, skills, time, money.",
    ),
    SessionPhase.GAPS: (
        "What's missing here?",
        "Unknowns, blind spots.",
    ),
    SessionPhase.CONNECTIONS: (
        "What connects these items?",
        "Causes, blockers, dependencies.",
    ),
}

PHASE_ORDER: list[SessionPhase] = [
    SessionPhase.QUESTION,
    SessionPhase.FACTS,
    SessionPhase.PAINS,
    SessionPhase.RESOURCES,
    SessionPhase.GAPS,
    SessionPhase.CONNECTIONS,
]
