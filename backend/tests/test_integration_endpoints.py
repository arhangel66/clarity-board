from fastapi.testclient import TestClient

import app.main as main
from app.models import Card, CardType, Connection, ConnectionType, SessionPhase, State
from app.services.state_service import StateService


def _auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer dev-token"}


class DummyAIService:
    async def generate_response(self, message: str, state: State) -> str:
        return '{"operations": [], "question_action": "keep"}'

    async def translate_question_hint(
        self, question: str, hint: str, locale: str
    ) -> tuple[str, str] | None:
        return None


def _setup_services(monkeypatch, tmp_path) -> StateService:
    monkeypatch.setenv("DEV_AUTH_BYPASS", "true")
    state_service = StateService(str(tmp_path / "test.db"))
    monkeypatch.setattr(main, "state_service", state_service)
    monkeypatch.setattr(main, "ai_service", DummyAIService())
    monkeypatch.setattr(main, "special_questions_service", None)
    return state_service


def _seed_state(
    state_service: StateService,
    *,
    session_id: str = "session_test",
    include_second_fact: bool = False,
    include_connection: bool = False,
) -> State:
    cards = [
        Card(
            id="card_q",
            text="Main problem",
            type=CardType.QUESTION,
            x=0.5,
            y=0.5,
            pinned=True,
        ),
        Card(
            id="card_1",
            text="First fact",
            type=CardType.FACT,
            x=0.1,
            y=0.2,
            pinned=False,
        ),
    ]

    if include_second_fact:
        cards.append(
            Card(
                id="card_2",
                text="Second fact",
                type=CardType.FACT,
                x=0.2,
                y=0.3,
                pinned=False,
            )
        )

    connections = []
    if include_connection:
        connections.append(
            Connection(
                id="conn_1",
                from_id="card_1",
                to_id="card_2" if include_second_fact else "card_q",
                type=ConnectionType.RELATES,
                label="relates to",
            )
        )

    state = State(
        session_id=session_id,
        user_id="dev-user",
        locale="ru",
        question="Main problem",
        phase=SessionPhase.FACTS,
        current_question="List facts",
        current_hint="Be specific",
        phase_index=1,
        puzzlement_turns=3,
        cards=cards,
        connections=connections,
    )
    state_service.save(state)
    return state


def _receive_init_messages(
    websocket,
    *,
    expect_cards: bool = True,
    expect_connections: bool = False,
    expect_question_update: bool = True,
) -> dict[str, dict]:
    expected = ["session_loaded"]
    if expect_cards:
        expected.append("cards_add")
    if expect_connections:
        expected.append("connections_add")
    if expect_question_update:
        expected.append("question_update")

    messages: dict[str, dict] = {}
    for _ in range(len(expected)):
        message = websocket.receive_json()
        messages[message["type"]] = message
    return messages


def test_sessions_create_and_list(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        create_response = client.post("/api/sessions", headers=_auth_headers())

        assert create_response.status_code == 200
        session_id = create_response.json()["session"]["id"]

        list_response = client.get("/api/sessions", headers=_auth_headers())

        assert list_response.status_code == 200
        sessions = list_response.json()["sessions"]
        assert session_id in {session["id"] for session in sessions}


def test_transcribe_returns_503_when_not_configured(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)
    monkeypatch.setattr(main, "openai_client", None)

    with TestClient(main.app) as client:
        response = client.post(
            "/api/transcribe",
            headers=_auth_headers(),
            files={"file": ("audio.wav", b"fake", "audio/wav")},
        )

        assert response.status_code == 503
        assert "Transcription not configured" in response.json()["detail"]


def test_websocket_init_and_card_updates(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)

    state = _seed_state(state_service)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "init",
                    "payload": {
                        "session_id": state.session_id,
                        "auth_token": "dev-token",
                    },
                }
            )

            init_messages = _receive_init_messages(websocket)
            assert init_messages["session_loaded"]["payload"]["session"]["id"] == state.session_id
            card_ids = {card["id"] for card in init_messages["cards_add"]["payload"]["cards"]}
            assert "card_1" in card_ids
            assert init_messages["question_update"]["payload"]["question"] == "List facts"

            websocket.send_json(
                {
                    "type": "card_update",
                    "payload": {"card_id": "card_1", "updates": {"text": "Updated"}},
                }
            )
            update_message = websocket.receive_json()
            assert update_message["type"] == "cards_update"
            assert update_message["payload"]["updates"][0]["id"] == "card_1"
            assert update_message["payload"]["updates"][0]["text"] == "Updated"

            websocket.send_json(
                {
                    "type": "card_move",
                    "payload": {
                        "card_id": "card_1",
                        "x": 0.3,
                        "y": 0.4,
                        "pinned": True,
                    },
                }
            )
            move_message = websocket.receive_json()
            assert move_message["type"] == "cards_update"
            assert move_message["payload"]["updates"][0]["x"] == 0.3
            assert move_message["payload"]["updates"][0]["y"] == 0.4


def test_websocket_error_on_missing_auth_token(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json({"type": "init", "payload": {}})

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Missing token"


def test_websocket_unauthorized_action_before_init(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "card_move",
                    "payload": {
                        "card_id": "card_1",
                        "x": 0.2,
                        "y": 0.2,
                        "pinned": True,
                    },
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Unauthorized"


def test_websocket_invalid_json_returns_error(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("not-json")

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Invalid JSON"


def test_websocket_clear_session(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "init",
                    "payload": {
                        "session_id": state.session_id,
                        "auth_token": "dev-token",
                    },
                }
            )
            _receive_init_messages(websocket)

            websocket.send_json({"type": "clear_session", "payload": {}})

            message = websocket.receive_json()
            assert message["type"] == "session_cleared"


def test_websocket_card_delete(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "init",
                    "payload": {
                        "session_id": state.session_id,
                        "auth_token": "dev-token",
                    },
                }
            )
            _receive_init_messages(websocket)

            websocket.send_json({"type": "card_delete", "payload": {"card_id": "card_1"}})

            message = websocket.receive_json()
            assert message["type"] == "card_deleted"
            assert message["payload"]["card_id"] == "card_1"


def test_websocket_connection_create_and_delete(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service, include_second_fact=True)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "init",
                    "payload": {
                        "session_id": state.session_id,
                        "auth_token": "dev-token",
                    },
                }
            )
            _receive_init_messages(websocket)

            websocket.send_json(
                {
                    "type": "connection_create",
                    "payload": {
                        "from_id": "card_1",
                        "to_id": "card_2",
                        "type": "causes",
                        "label": "leads to",
                    },
                }
            )

            created = websocket.receive_json()
            assert created["type"] == "connections_add"
            connection_id = created["payload"]["connections"][0]["id"]

            websocket.send_json(
                {
                    "type": "connection_delete",
                    "payload": {"connection_id": connection_id},
                }
            )

            deleted = websocket.receive_json()
            assert deleted["type"] == "connection_deleted"
            assert deleted["payload"]["connection_id"] == connection_id


def test_websocket_special_question_unavailable(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "init",
                    "payload": {
                        "session_id": state.session_id,
                        "auth_token": "dev-token",
                    },
                }
            )
            _receive_init_messages(websocket)

            websocket.send_json({"type": "special_question_request", "payload": {}})

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Special questions unavailable"
