"""Pydantic models for Fact Card System."""

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


# --- State Model ---


class State(BaseModel):
    """Session state - stored as JSON blob in DB."""

    session_id: str
    question: str  # Central problem
    phase: SessionPhase = SessionPhase.QUESTION
    current_question: str = ""
    current_hint: str = ""
    phase_index: int = 0
    cards: list[Card] = Field(default_factory=list)


# --- AI Response Model ---


class AIResponse(BaseModel):
    """Parsed AI response containing card operations."""

    cards: list[dict] = Field(default_factory=list)  # Raw card dicts from AI
    question_action: QuestionAction = QuestionAction.KEEP
    next_question: str | None = None
    next_hint: str | None = None


# --- Service Result Models ---


class InitResult(BaseModel):
    """Result of MainService.init() call."""

    ready: bool = False
    session_loaded: dict | None = None
    cards: list[dict] | None = None
    question_update: dict | None = None


class ProcessResult(BaseModel):
    """Result of MainService.process_user_message() call."""

    session_loaded: dict | None = None
    cards_add: list[dict] | None = None
    question_update: dict


# --- Color Mapping ---


CARD_TYPE_COLORS: dict[CardType, str] = {
    CardType.QUESTION: "#8B5CF6",  # Purple
    CardType.FACT: "#3B82F6",  # Blue
    CardType.PAIN: "#EF4444",  # Red
    CardType.RESOURCE: "#22C55E",  # Green
    CardType.HYPOTHESIS: "#EAB308",  # Yellow
}


# --- Phase Configuration ---


DEFAULT_QUESTIONS: dict[SessionPhase, tuple[str, str]] = {
    SessionPhase.QUESTION: (
        "What problem are you trying to solve?",
        "Describe the situation that is bothering you",
    ),
    SessionPhase.FACTS: (
        "What are the concrete facts of the situation?",
        "Numbers, dates, events - things that can be verified",
    ),
    SessionPhase.PAINS: (
        "What specifically hurts or bothers you?",
        "Be specific - not 'I feel bad' but 'I can't sleep before deadlines'",
    ),
    SessionPhase.RESOURCES: (
        "What resources do you have?",
        "People, skills, money, time - anything that can help",
    ),
    SessionPhase.GAPS: (
        "What might be missing from this picture?",
        "What haven't we talked about yet?",
    ),
    SessionPhase.CONNECTIONS: (
        "How do these things connect?",
        "What causes what? What blocks what?",
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
