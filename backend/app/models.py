"""Pydantic models for Fact Card System."""

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class CardType(str, Enum):
    """Types of cards in the system."""

    QUESTION = "question"
    FACT = "fact"
    PAIN = "pain"
    RESOURCE = "resource"
    HYPOTHESIS = "hypothesis"


class ConnectionType(str, Enum):
    """Types of connections between cards."""

    CAUSES = "causes"
    RELATES = "relates"
    CONTRADICTS = "contradicts"
    BLOCKS = "blocks"


class CreatedBy(str, Enum):
    """Who created the entity."""

    AI = "ai"
    USER = "user"


# --- Card Models ---


class Card(BaseModel):
    """A card representing a fact, pain, resource, or hypothesis."""

    id: str
    text: str = Field(max_length=200)
    type: CardType
    emoji: str = ""
    color: str = "#3B82F6"
    importance: float = Field(default=0.5, ge=0, le=1)
    confidence: float = Field(default=0.8, ge=0, le=1)
    x: float = Field(default=0.5, ge=0, le=1)
    y: float = Field(default=0.5, ge=0, le=1)
    target_x: float = Field(default=0.5, ge=0, le=1)
    target_y: float = Field(default=0.5, ge=0, le=1)
    pinned: bool = False
    is_root: bool = False
    is_new: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    embedding: list[float] | None = None


class CardCreate(BaseModel):
    """Data for creating a new card (from AI response)."""

    text: str
    type: CardType
    emoji: str = ""
    importance: float = Field(default=0.5, ge=0, le=1)
    confidence: float = Field(default=0.8, ge=0, le=1)


class CardUpdate(BaseModel):
    """Partial update for a card."""

    id: str
    x: float | None = None
    y: float | None = None
    target_x: float | None = None
    target_y: float | None = None
    pinned: bool | None = None
    importance: float | None = None
    confidence: float | None = None
    is_new: bool | None = None


# --- Connection Models ---


class Connection(BaseModel):
    """A connection between two cards."""

    id: str
    from_id: str
    to_id: str
    type: ConnectionType
    strength: float = Field(default=0.5, ge=0, le=1)
    label: str | None = None
    created_by: CreatedBy = CreatedBy.AI


class ConnectionCreate(BaseModel):
    """Data for creating a connection (from AI response)."""

    from_text: str  # Text to match existing card
    to_text: str  # "root" or text to match
    type: ConnectionType
    strength: float = Field(default=0.5, ge=0, le=1)
    label: str | None = None


# --- Session Models ---


class Session(BaseModel):
    """A fact-card session."""

    id: str
    question: str
    cards: list[Card] = []
    connections: list[Connection] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# --- WebSocket Message Models ---


class WSMessageUserMessage(BaseModel):
    """User sends a message."""

    type: Literal["user_message"] = "user_message"
    payload: dict  # {"text": "..."}


class WSMessageCardMove(BaseModel):
    """User moves a card."""

    type: Literal["card_move"] = "card_move"
    payload: dict  # {"card_id": "...", "x": 0.5, "y": 0.5, "pinned": True}


class WSMessageNewSession(BaseModel):
    """User starts a new session."""

    type: Literal["new_session"] = "new_session"
    payload: dict  # {"question": "..."}


class WSMessageCardsAdd(BaseModel):
    """Server adds new cards."""

    type: Literal["cards_add"] = "cards_add"
    payload: dict  # {"cards": [...]}


class WSMessageCardsUpdate(BaseModel):
    """Server updates existing cards."""

    type: Literal["cards_update"] = "cards_update"
    payload: dict  # {"updates": [...]}


class WSMessageConnectionsAdd(BaseModel):
    """Server adds connections."""

    type: Literal["connections_add"] = "connections_add"
    payload: dict  # {"connections": [...]}


class WSMessageAIQuestion(BaseModel):
    """AI asks a clarifying question."""

    type: Literal["ai_question"] = "ai_question"
    payload: dict  # {"text": "..."}


class WSMessagePositionsUpdate(BaseModel):
    """Server updates card positions."""

    type: Literal["positions_update"] = "positions_update"
    payload: dict  # {"positions": [...]}


class WSMessageError(BaseModel):
    """Server sends an error."""

    type: Literal["error"] = "error"
    payload: dict  # {"message": "..."}


class WSMessageSessionLoaded(BaseModel):
    """Server sends loaded session data."""

    type: Literal["session_loaded"] = "session_loaded"
    payload: dict  # {"session": {...}}


# --- AI Operation Models ---


class AIOperationCreateCard(BaseModel):
    """AI operation to create a card."""

    type: Literal["create_card"] = "create_card"
    card: CardCreate


class AIOperationCreateConnection(BaseModel):
    """AI operation to create a connection."""

    type: Literal["create_connection"] = "create_connection"
    connection: ConnectionCreate


class AIOperationAskQuestion(BaseModel):
    """AI operation to ask a clarifying question."""

    type: Literal["ask_question"] = "ask_question"
    text: str


class AIResponse(BaseModel):
    """Parsed AI response containing operations."""

    operations: list[AIOperationCreateCard | AIOperationCreateConnection | AIOperationAskQuestion]


# --- Color Mapping ---


CARD_TYPE_COLORS: dict[CardType, str] = {
    CardType.QUESTION: "#8B5CF6",  # Purple
    CardType.FACT: "#3B82F6",  # Blue
    CardType.PAIN: "#EF4444",  # Red
    CardType.RESOURCE: "#22C55E",  # Green
    CardType.HYPOTHESIS: "#EAB308",  # Yellow
}
