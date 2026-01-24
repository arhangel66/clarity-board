"""FastAPI application with WebSocket endpoint for Fact Card System."""

import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.construct import ai_service, card_service
from app.models import CardUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Fact Card System backend starting...")
    yield
    logger.info("Fact Card System backend shutting down...")


app = FastAPI(
    title="Fact Card System",
    description="Backend for Kurpatov's Fact-Card methodology implementation",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """WebSocket connection manager."""

    def __init__(self) -> None:
        """Initialize connection manager."""
        self.active_connections: dict[str, WebSocket] = {}
        self.session_map: dict[str, str] = {}  # websocket_id -> session_id

    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        """Accept a new WebSocket connection.

        Args:
            websocket: WebSocket instance.
            connection_id: Unique connection ID.
        """
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        logger.info(f"WebSocket connected: {connection_id}")

    def disconnect(self, connection_id: str) -> None:
        """Remove a WebSocket connection.

        Args:
            connection_id: Connection ID to remove.
        """
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        if connection_id in self.session_map:
            del self.session_map[connection_id]
        logger.info(f"WebSocket disconnected: {connection_id}")

    def set_session(self, connection_id: str, session_id: str) -> None:
        """Associate a connection with a session.

        Args:
            connection_id: Connection ID.
            session_id: Session ID.
        """
        self.session_map[connection_id] = session_id

    def get_session(self, connection_id: str) -> str | None:
        """Get session ID for a connection.

        Args:
            connection_id: Connection ID.

        Returns:
            Session ID or None.
        """
        return self.session_map.get(connection_id)

    async def send_message(self, connection_id: str, message: dict[str, Any]) -> None:
        """Send a message to a specific connection.

        Args:
            connection_id: Connection ID.
            message: Message to send.
        """
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.send_json(message)


manager = ConnectionManager()


async def handle_new_session(connection_id: str, payload: dict[str, Any]) -> None:
    """Handle new_session message.

    Args:
        connection_id: WebSocket connection ID.
        payload: Message payload with 'question'.
    """
    question = payload.get("question", "")
    if not question:
        await manager.send_message(
            connection_id,
            {"type": "error", "payload": {"message": "Question is required"}},
        )
        return

    # Create session
    session = card_service.create_session(question)
    manager.set_session(connection_id, session.id)

    # Create root card
    root_card = await card_service.create_root_card(session.id, question)

    # Send session loaded response
    await manager.send_message(
        connection_id,
        {
            "type": "session_loaded",
            "payload": {
                "session": {
                    "id": session.id,
                    "question": session.question,
                }
            },
        },
    )

    # Send root card
    await manager.send_message(
        connection_id,
        {
            "type": "cards_add",
            "payload": {
                "cards": [_card_to_dict(root_card)],
            },
        },
    )

    logger.info(f"Created new session: {session.id}")


async def handle_user_message(connection_id: str, payload: dict[str, Any]) -> None:
    """Handle user_message.

    Args:
        connection_id: WebSocket connection ID.
        payload: Message payload with 'text'.
    """
    session_id = manager.get_session(connection_id)
    if not session_id:
        await manager.send_message(
            connection_id,
            {"type": "error", "payload": {"message": "No active session"}},
        )
        return

    text = payload.get("text", "")
    if not text:
        return

    # Get session for context
    session = card_service.get_session(session_id)
    if not session:
        await manager.send_message(
            connection_id,
            {"type": "error", "payload": {"message": "Session not found"}},
        )
        return

    # Get existing card texts for AI context
    existing_texts = [card.text for card in session.cards]

    # Process with AI
    ai_response = await ai_service.process_user_message(
        message=text,
        session_question=session.question,
        existing_cards_texts=existing_texts,
    )

    # Process AI operations
    new_cards, new_connections, questions = await card_service.process_ai_response(
        session_id, ai_response
    )

    # Send new cards
    if new_cards:
        await manager.send_message(
            connection_id,
            {
                "type": "cards_add",
                "payload": {
                    "cards": [_card_to_dict(card) for card in new_cards],
                },
            },
        )

    # Send new connections
    if new_connections:
        await manager.send_message(
            connection_id,
            {
                "type": "connections_add",
                "payload": {
                    "connections": [_connection_to_dict(conn) for conn in new_connections],
                },
            },
        )

    # Send AI questions
    for question in questions:
        await manager.send_message(
            connection_id,
            {
                "type": "ai_question",
                "payload": {"text": question},
            },
        )


async def handle_card_move(connection_id: str, payload: dict[str, Any]) -> None:
    """Handle card_move message.

    Args:
        connection_id: WebSocket connection ID.
        payload: Message payload with card_id, x, y, pinned.
    """
    session_id = manager.get_session(connection_id)
    if not session_id:
        return

    card_id = payload.get("card_id")
    if not card_id:
        return

    update = CardUpdate(
        id=card_id,
        x=payload.get("x"),
        y=payload.get("y"),
        pinned=payload.get("pinned"),
    )

    card_service.update_card(update)

    # Confirm the update
    await manager.send_message(
        connection_id,
        {
            "type": "cards_update",
            "payload": {
                "updates": [
                    {
                        "id": card_id,
                        "x": update.x,
                        "y": update.y,
                        "pinned": update.pinned,
                    }
                ],
            },
        },
    )


def _card_to_dict(card) -> dict[str, Any]:
    """Convert Card to dictionary for JSON serialization.

    Args:
        card: Card instance.

    Returns:
        Dictionary representation.
    """
    return {
        "id": card.id,
        "text": card.text,
        "type": card.type.value,
        "emoji": card.emoji,
        "color": card.color,
        "importance": card.importance,
        "confidence": card.confidence,
        "x": card.x,
        "y": card.y,
        "target_x": card.target_x,
        "target_y": card.target_y,
        "pinned": card.pinned,
        "is_root": card.is_root,
        "is_new": card.is_new,
        "created_at": card.created_at.isoformat(),
    }


def _connection_to_dict(connection) -> dict[str, Any]:
    """Convert Connection to dictionary for JSON serialization.

    Args:
        connection: Connection instance.

    Returns:
        Dictionary representation.
    """
    return {
        "id": connection.id,
        "from_id": connection.from_id,
        "to_id": connection.to_id,
        "type": connection.type.value,
        "strength": connection.strength,
        "label": connection.label,
        "created_by": connection.created_by.value,
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Main WebSocket endpoint.

    Args:
        websocket: WebSocket connection.
    """
    connection_id = str(id(websocket))
    await manager.connect(websocket, connection_id)

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                msg_type = message.get("type")
                payload = message.get("payload", {})

                logger.info(f"Received message type: {msg_type}")

                if msg_type == "new_session":
                    await handle_new_session(connection_id, payload)
                elif msg_type == "user_message":
                    await handle_user_message(connection_id, payload)
                elif msg_type == "card_move":
                    await handle_card_move(connection_id, payload)
                else:
                    logger.warning(f"Unknown message type: {msg_type}")

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {data}")
                await manager.send_message(
                    connection_id,
                    {"type": "error", "payload": {"message": "Invalid JSON"}},
                )

    except WebSocketDisconnect:
        manager.disconnect(connection_id)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status message.
    """
    return {"status": "ok", "service": "fact-card-backend"}


@app.get("/api/session/{session_id}")
async def get_session(session_id: str) -> dict[str, Any]:
    """Get session by ID.

    Args:
        session_id: Session ID.

    Returns:
        Session data or error.
    """
    session = card_service.get_session(session_id)
    if not session:
        return {"error": "Session not found"}

    return {
        "session": {
            "id": session.id,
            "question": session.question,
            "cards": [_card_to_dict(card) for card in session.cards],
            "connections": [_connection_to_dict(conn) for conn in session.connections],
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
        }
    }
