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

from fastapi import (  # noqa: E402
    Depends,
    FastAPI,
    Header,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from app.auth import AuthError, get_user_id  # noqa: E402
from app.construct import (  # noqa: E402
    ai_service,
    openai_client,
    special_questions_service,
    state_service,
)
from app.models import CardType  # noqa: E402
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
        special_questions_service=special_questions_service,
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
                elif msg_type == "set_locale":
                    await handle_set_locale(websocket, service, payload)
                elif msg_type == "clear_session":
                    await handle_clear_session(websocket, service)
                elif msg_type == "card_move":
                    await handle_card_move(websocket, service, payload)
                elif msg_type == "card_create":
                    await handle_card_create(websocket, service, payload)
                elif msg_type == "card_delete":
                    await handle_card_delete(websocket, service, payload)
                elif msg_type == "card_update":
                    await handle_card_update(websocket, service, payload)
                elif msg_type == "special_question_request":
                    await handle_special_question_request(websocket, service)
                elif msg_type == "connection_create":
                    await handle_connection_create(websocket, service, payload)
                elif msg_type == "connection_delete":
                    await handle_connection_delete(websocket, service, payload)
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
    token = payload.get("auth_token")
    try:
        user_id = get_user_id(token)
    except AuthError as exc:
        await websocket.send_json({"type": "error", "payload": {"message": str(exc)}})
        return

    result = service.init(session_id, user_id, locale=payload.get("locale"))

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

        if result.connections:
            await websocket.send_json(
                {
                    "type": "connections_add",
                    "payload": {"connections": result.connections},
                }
            )

        if result.question_update:
            await websocket.send_json(
                {
                    "type": "question_update",
                    "payload": result.question_update,
                }
            )

        if service.state and service.state.pending_special_question:
            await websocket.send_json(
                {
                    "type": "special_question_prompt",
                    "payload": service.state.pending_special_question.model_dump(),
                }
            )

        logger.info(f"Loaded session: {result.session_loaded['id']}")
    else:
        # Ready for new session
        logger.info("Ready for new session")


async def handle_set_locale(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle set_locale message."""
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    locale = payload.get("locale")
    if not locale:
        return

    result = await service.set_locale(locale)
    if not result:
        return

    question_update = result.get("question_update")
    if question_update:
        await websocket.send_json(
            {
                "type": "question_update",
                "payload": question_update,
            }
        )

    special_prompt = result.get("special_prompt")
    if special_prompt:
        await websocket.send_json(
            {
                "type": "special_question_prompt",
                "payload": special_prompt,
            }
        )


async def handle_user_message(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle user_message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with text.
    """
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    text = payload.get("text", "")
    if not text:
        return

    result = await service.process_user_message(
        text, special_question_id=payload.get("special_question_id")
    )

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

    # Send card updates
    if result.cards_update:
        await websocket.send_json(
            {
                "type": "cards_update",
                "payload": {"updates": result.cards_update},
            }
        )

    # Send card deletions
    if result.cards_delete:
        await websocket.send_json(
            {
                "type": "cards_delete",
                "payload": {"card_ids": result.cards_delete},
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
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

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
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    card_id = payload.get("card_id")
    if not card_id:
        return

    update = service.handle_card_move(
        card_id=card_id,
        x=payload.get("x", 0.5),
        y=payload.get("y", 0.5),
        pinned=payload.get("pinned", True),
        width=payload.get("width"),
        height=payload.get("height"),
        custom_scale=payload.get("custom_scale"),
    )

    if update:
        await websocket.send_json(
            {
                "type": "cards_update",
                "payload": {"updates": [update]},
            }
        )


async def handle_card_create(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle card_create message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with text, type, x, y.
    """
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    text = (payload.get("text") or "").strip()
    card_type = payload.get("type")
    if not text:
        await websocket.send_json(
            {"type": "error", "payload": {"message": "Card text is required"}}
        )
        return
    if not card_type:
        await websocket.send_json(
            {"type": "error", "payload": {"message": "Card type is required"}}
        )
        return
    try:
        CardType(card_type)
    except ValueError:
        await websocket.send_json({"type": "error", "payload": {"message": "Invalid card type"}})
        return

    card = service.create_manual_card(
        text=text,
        card_type=card_type,
        x=payload.get("x", 0.5),
        y=payload.get("y", 0.5),
        emoji=payload.get("emoji"),
        importance=payload.get("importance"),
        confidence=payload.get("confidence"),
    )

    if not card:
        await websocket.send_json(
            {"type": "error", "payload": {"message": "Failed to create card"}}
        )
        return

    await websocket.send_json(
        {
            "type": "cards_add",
            "payload": {"cards": [card]},
        }
    )


async def handle_card_delete(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle card_delete message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with card_id.
    """
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    card_id = payload.get("card_id")
    if not card_id:
        return

    if not service.state:
        await websocket.send_json({"type": "error", "payload": {"message": "No active session"}})
        return

    success = service.delete_card(card_id)

    if success:
        await websocket.send_json(
            {
                "type": "card_deleted",
                "payload": {"card_id": card_id},
            }
        )
        logger.info(f"Card deleted: {card_id}")


async def handle_card_update(websocket: WebSocket, service: MainService, payload: dict) -> None:
    """Handle card_update message.

    Args:
        websocket: WebSocket connection.
        service: MainService instance.
        payload: Message payload with card_id and updates.
    """
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    card_id = payload.get("card_id")
    updates = payload.get("updates", {})
    if not card_id or not isinstance(updates, dict) or not updates:
        return

    if not service.state:
        await websocket.send_json({"type": "error", "payload": {"message": "No active session"}})
        return

    update = service.update_card(card_id, updates)

    if update:
        await websocket.send_json(
            {
                "type": "cards_update",
                "payload": {"updates": [update]},
            }
        )


async def handle_special_question_request(websocket: WebSocket, service: MainService) -> None:
    """Handle special question request."""
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    if not service.state:
        await websocket.send_json({"type": "error", "payload": {"message": "No active session"}})
        return

    prompt = service.request_special_question()
    if not prompt:
        await websocket.send_json(
            {"type": "error", "payload": {"message": "Special questions unavailable"}}
        )
        return

    await websocket.send_json(
        {
            "type": "special_question_prompt",
            "payload": prompt,
        }
    )


async def handle_connection_create(
    websocket: WebSocket, service: MainService, payload: dict
) -> None:
    """Handle connection_create message."""
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    from_id = payload.get("from_id")
    to_id = payload.get("to_id")
    if not from_id or not to_id:
        return

    conn = service.create_connection(
        from_id=from_id,
        to_id=to_id,
        conn_type=payload.get("type", "relates"),
        label=payload.get("label"),
    )

    if conn:
        await websocket.send_json(
            {
                "type": "connections_add",
                "payload": {"connections": [conn]},
            }
        )


async def handle_connection_delete(
    websocket: WebSocket, service: MainService, payload: dict
) -> None:
    """Handle connection_delete message."""
    if not service.user_id:
        await websocket.send_json({"type": "error", "payload": {"message": "Unauthorized"}})
        return

    connection_id = payload.get("connection_id")
    if not connection_id:
        return

    success = service.delete_connection(connection_id)

    if success:
        await websocket.send_json(
            {
                "type": "connection_deleted",
                "payload": {"connection_id": connection_id},
            }
        )


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status message.
    """
    return {"status": "ok", "service": "fact-card-backend"}


def get_current_user_id(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization")
    token = authorization.split(" ", 1)[1].strip()
    try:
        return get_user_id(token)
    except AuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@app.get("/api/sessions")
async def list_sessions(user_id: str = Depends(get_current_user_id)) -> dict:
    return {"sessions": state_service.list_sessions(user_id)}


@app.post("/api/sessions")
async def create_session(user_id: str = Depends(get_current_user_id)) -> dict:
    service = MainService(
        state_service=state_service,
        ai_service=ai_service,
        special_questions_service=special_questions_service,
    )
    state = service.create_new_session(user_id)
    return {"session": {"id": state.session_id, "title": state_service._derive_title(state)}}


@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile, user_id: str = Depends(get_current_user_id)
) -> dict[str, str]:
    """Transcribe audio using OpenAI speech-to-text."""
    if openai_client is None:
        raise HTTPException(
            status_code=503, detail="Transcription not configured (OPENAI_API_KEY not set)"
        )

    if not file:
        raise HTTPException(status_code=400, detail="Missing audio file")

    try:
        result = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=(file.filename, file.file),
            response_format="json",
        )
    except Exception as exc:
        logger.exception("Transcription failed")
        raise HTTPException(status_code=500, detail="Transcription failed") from exc

    text = getattr(result, "text", "") or ""
    return {"text": text}
