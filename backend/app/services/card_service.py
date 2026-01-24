"""Card service for CRUD operations and business logic."""

import uuid
from datetime import datetime

from app.database import Database
from app.models import (
    CARD_TYPE_COLORS,
    AIOperationCreateCard,
    AIOperationCreateConnection,
    AIResponse,
    Card,
    CardType,
    CardUpdate,
    Connection,
    CreatedBy,
    Session,
)
from app.services.embedding_service import EmbeddingService


class CardService:
    """Service for card and session operations."""

    def __init__(self, database: Database, embedding_service: EmbeddingService) -> None:
        """Initialize card service.

        Args:
            database: Database instance.
            embedding_service: Embedding service instance.
        """
        self.db = database
        self.embedding_service = embedding_service

    def generate_id(self, prefix: str = "card") -> str:
        """Generate a unique ID.

        Args:
            prefix: ID prefix.

        Returns:
            Unique ID string.
        """
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    # --- Session Operations ---

    def create_session(self, question: str) -> Session:
        """Create a new session with a root question card.

        Args:
            question: The central question.

        Returns:
            Created session.
        """
        session_id = self.generate_id("session")
        now = datetime.utcnow()

        session = Session(
            id=session_id,
            question=question,
            cards=[],
            connections=[],
            created_at=now,
            updated_at=now,
        )

        self.db.create_session(session)
        return session

    async def create_root_card(self, session_id: str, question: str) -> Card:
        """Create the root question card for a session.

        Args:
            session_id: Session ID.
            question: The question text.

        Returns:
            Created root card.
        """
        # Get embedding for the question
        embedding = await self.embedding_service.get_embedding(question)

        card = Card(
            id=self.generate_id("card"),
            text=question,
            type=CardType.QUESTION,
            emoji="",
            color=CARD_TYPE_COLORS[CardType.QUESTION],
            importance=1.0,
            confidence=1.0,
            x=0.5,
            y=0.5,
            target_x=0.5,
            target_y=0.5,
            pinned=True,  # Root card is always pinned at center
            is_root=True,
            is_new=True,
            created_at=datetime.utcnow(),
            embedding=embedding,
        )

        self.db.create_card(session_id, card)
        return card

    def get_session(self, session_id: str) -> Session | None:
        """Get a session by ID.

        Args:
            session_id: Session ID.

        Returns:
            Session or None if not found.
        """
        return self.db.get_session(session_id)

    # --- Card Operations ---

    async def create_card_from_ai_operation(
        self,
        session_id: str,
        operation: AIOperationCreateCard,
        existing_cards: list[Card],
    ) -> Card:
        """Create a card from AI operation.

        Args:
            session_id: Session ID.
            operation: AI create_card operation.
            existing_cards: Existing cards in session.

        Returns:
            Created card.
        """
        card_data = operation.card

        # Get embedding
        embedding = await self.embedding_service.get_embedding(card_data.text)

        # Calculate position based on embedding similarity
        x, y = self.embedding_service.get_position_for_new_card(
            embedding, existing_cards, is_root=False
        )

        # Get color for card type
        color = CARD_TYPE_COLORS.get(card_data.type, "#3B82F6")

        card = Card(
            id=self.generate_id("card"),
            text=card_data.text,
            type=card_data.type,
            emoji=card_data.emoji,
            color=color,
            importance=card_data.importance,
            confidence=card_data.confidence,
            x=x,
            y=y,
            target_x=x,
            target_y=y,
            pinned=False,
            is_root=False,
            is_new=True,
            created_at=datetime.utcnow(),
            embedding=embedding,
        )

        self.db.create_card(session_id, card)
        return card

    def update_card(self, update: CardUpdate) -> None:
        """Update a card.

        Args:
            update: Card update data.
        """
        updates = {}

        if update.x is not None:
            updates["x"] = update.x
        if update.y is not None:
            updates["y"] = update.y
        if update.target_x is not None:
            updates["target_x"] = update.target_x
        if update.target_y is not None:
            updates["target_y"] = update.target_y
        if update.pinned is not None:
            updates["pinned"] = update.pinned
        if update.importance is not None:
            updates["importance"] = update.importance
        if update.confidence is not None:
            updates["confidence"] = update.confidence
        if update.is_new is not None:
            updates["is_new"] = update.is_new

        if updates:
            self.db.update_card(update.id, updates)

    def get_cards_by_session(self, session_id: str) -> list[Card]:
        """Get all cards for a session.

        Args:
            session_id: Session ID.

        Returns:
            List of cards.
        """
        return self.db.get_cards_by_session(session_id)

    # --- Connection Operations ---

    def create_connection_from_ai_operation(
        self,
        session_id: str,
        operation: AIOperationCreateConnection,
        existing_cards: list[Card],
    ) -> Connection | None:
        """Create a connection from AI operation.

        Args:
            session_id: Session ID.
            operation: AI create_connection operation.
            existing_cards: Existing cards to match text against.

        Returns:
            Created connection or None if cards not found.
        """
        conn_data = operation.connection

        # Find source card by text
        from_card = self._find_card_by_text(existing_cards, conn_data.from_text)
        if not from_card:
            return None

        # Find target card (special handling for "root")
        if conn_data.to_text.lower() == "root":
            to_card = self._find_root_card(existing_cards)
        else:
            to_card = self._find_card_by_text(existing_cards, conn_data.to_text)

        if not to_card:
            return None

        # Don't create self-connections
        if from_card.id == to_card.id:
            return None

        connection = Connection(
            id=self.generate_id("conn"),
            from_id=from_card.id,
            to_id=to_card.id,
            type=conn_data.type,
            strength=conn_data.strength,
            label=conn_data.label,
            created_by=CreatedBy.AI,
        )

        self.db.create_connection(session_id, connection)
        return connection

    def _find_card_by_text(self, cards: list[Card], text: str) -> Card | None:
        """Find a card by partial text match.

        Args:
            cards: List of cards to search.
            text: Text to match.

        Returns:
            Matching card or None.
        """
        text_lower = text.lower()

        # First try exact match
        for card in cards:
            if card.text.lower() == text_lower:
                return card

        # Then try partial match
        for card in cards:
            if text_lower in card.text.lower() or card.text.lower() in text_lower:
                return card

        return None

    def _find_root_card(self, cards: list[Card]) -> Card | None:
        """Find the root card.

        Args:
            cards: List of cards.

        Returns:
            Root card or None.
        """
        for card in cards:
            if card.is_root:
                return card
        return None

    # --- Process AI Response ---

    async def process_ai_response(
        self,
        session_id: str,
        ai_response: AIResponse,
    ) -> tuple[list[Card], list[Connection], list[str]]:
        """Process all operations from AI response.

        Args:
            session_id: Session ID.
            ai_response: AI response with operations.

        Returns:
            Tuple of (new_cards, new_connections, questions).
        """
        new_cards: list[Card] = []
        new_connections: list[Connection] = []
        questions: list[str] = []

        # Get existing cards
        existing_cards = self.get_cards_by_session(session_id)

        for operation in ai_response.operations:
            if operation.type == "create_card":
                card = await self.create_card_from_ai_operation(
                    session_id, operation, existing_cards + new_cards
                )
                new_cards.append(card)

            elif operation.type == "create_connection":
                # Include newly created cards in the search
                all_cards = existing_cards + new_cards
                connection = self.create_connection_from_ai_operation(
                    session_id, operation, all_cards
                )
                if connection:
                    new_connections.append(connection)

            elif operation.type == "ask_question":
                questions.append(operation.text)

        # Update session timestamp
        self.db.update_session_timestamp(session_id)

        return new_cards, new_connections, questions
