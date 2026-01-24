"""FastAPI application with WebSocket endpoint for Fact Card System."""

# Load environment variables FIRST, before any other imports
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(_env_path)
if not _env_path.exists():
    load_dotenv(Path(__file__).parent.parent / ".env")

import json  # noqa: E402
import logging  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI, WebSocket, WebSocketDisconnect  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from app.construct import ai_service, state_service  # noqa: E402
from app.services.main_service import MainService  # noqa: E402

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
    version="0.2.0",
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Main WebSocket endpoint.

    Args:
        websocket: WebSocket connection.
    """
    await websocket.accept()
    logger.info("WebSocket connected")

    # Create MainService for this connection
    service = MainService(
        state_service=state_service,
        ai_service=ai_service,
    )

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                msg_type = message.get("type")
                payload = message.get("payload", {})

                logger.info(f"Received message type: {msg_type}")

                if msg_type == "init":
                    await handle_init(websocket, service, payload)
                elif msg_type == "user_message":
                    await handle_user_message(websocket, service, payload)
                elif msg_type == "clear_session":
                    await handle_clear_session(websocket, service)
                elif msg_type == "card_move":
                    await handle_card_move(websocket, service, payload)
                else:
                    logger.warning(f"Unknown message type: {msg_type}")

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {data}")
                await websocket.send_json({"type": "error", "payload": {"message": "Invalid JSON"}})

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")


async def handle_init(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle init message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with optional session_id.
    """
    session_id = payload.get("session_id")
    result = service.init(session_id)

    if result.session_loaded:
        # Existing session - send all data
        await websocket.send_json(
            {
                "type": "session_loaded",
                "payload": {"session": result.session_loaded},
            }
        )

        if result.cards:
            await websocket.send_json(
                {
                    "type": "cards_add",
                    "payload": {"cards": result.cards},
                }
            )

        if result.question_update:
            await websocket.send_json(
                {
                    "type": "question_update",
                    "payload": result.question_update,
                }
            )

        logger.info(f"Loaded session: {result.session_loaded['id']}")
    else:
        # Ready for new session
        logger.info("Ready for new session")


async def handle_user_message(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle user_message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with text.
    """
    text = payload.get("text", "")
    if not text:
        return

    result = await service.process_user_message(text)

    # Send session_loaded if this is a new session
    if result.session_loaded:
        await websocket.send_json(
            {
                "type": "session_loaded",
                "payload": {"session": result.session_loaded},
            }
        )
        logger.info(f"Created session: {result.session_loaded['id']}")

    # Send new cards
    if result.cards_add:
        await websocket.send_json(
            {
                "type": "cards_add",
                "payload": {"cards": result.cards_add},
            }
        )

    # Send question update
    await websocket.send_json(
        {
            "type": "question_update",
            "payload": result.question_update,
        }
    )


async def handle_clear_session(websocket: WebSocket, service: MainService) -> None:
    """Handle clear_session message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
    """
    service.new_session()
    await websocket.send_json({"type": "session_cleared", "payload": {}})
    logger.info("Session cleared")


async def handle_card_move(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle card_move message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with card_id, x, y, pinned.
    """
    card_id = payload.get("card_id")
    if not card_id:
        return

    update = service.handle_card_move(
        card_id=card_id,
        x=payload.get("x", 0.5),
        y=payload.get("y", 0.5),
        pinned=payload.get("pinned", True),
    )

    if update:
        await websocket.send_json(
            {
                "type": "cards_update",
                "payload": {"updates": [update]},
            }
        )


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status message.
    """
    return {"status": "ok", "service": "fact-card-backend"}
