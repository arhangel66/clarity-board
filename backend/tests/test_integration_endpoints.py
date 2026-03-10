from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

import app.main as main
from app.access import AccessPlan, AccessService, UserEntitlement
from app.models import Card, CardType, Connection, ConnectionType, SessionPhase, State
from app.services.state_service import StateService


def _auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer dev-token"}


class DummyAIService:
    def __init__(self, response_json: str | None = None) -> None:
        self._response_json = response_json
        self.call_count = 0

    async def generate_response(self, message: str, state: State) -> str:
        self.call_count += 1
        if self._response_json is not None:
            return self._response_json
        return '{"operations": [], "question_action": "keep"}'

    async def translate_question_hint(
        self, question: str, hint: str, locale: str
    ) -> tuple[str, str] | None:
        return None


def _setup_services(monkeypatch, tmp_path, ai_response_json: str | None = None) -> StateService:
    monkeypatch.setenv("DEV_AUTH_BYPASS", "true")
    state_service = StateService(str(tmp_path / "test.db"))
    monkeypatch.setattr(main, "state_service", state_service)
    monkeypatch.setattr(main, "ai_service", DummyAIService(ai_response_json))
    monkeypatch.setattr(main, "access_service", AccessService(state_service=state_service))
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


def test_sessions_delete(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service)

    with TestClient(main.app) as client:
        # Verify session exists
        list_response = client.get("/api/sessions", headers=_auth_headers())
        sessions_before = list_response.json()["sessions"]
        assert state.session_id in {s["id"] for s in sessions_before}

        # Delete the session
        delete_response = client.delete(
            f"/api/sessions/{state.session_id}", headers=_auth_headers()
        )
        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "deleted"

        # Verify session is gone
        list_response = client.get("/api/sessions", headers=_auth_headers())
        sessions_after = list_response.json()["sessions"]
        assert state.session_id not in {s["id"] for s in sessions_after}


def test_sessions_delete_does_not_restore_starter_access(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service)
    main.access_service.record_session_consumed("dev-user", state.session_id)

    with TestClient(main.app) as client:
        delete_response = client.delete(
            f"/api/sessions/{state.session_id}",
            headers=_auth_headers(),
        )
        assert delete_response.status_code == 200

        access_response = client.get("/api/access", headers=_auth_headers())
        assert access_response.status_code == 200

        status = access_response.json()["status"]
        assert status["free_sessions_used"] == 1
        assert status["free_sessions_remaining"] == 2


def test_sessions_delete_not_found(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        delete_response = client.delete("/api/sessions/nonexistent", headers=_auth_headers())
        assert delete_response.status_code == 404
        assert delete_response.json()["detail"] == "Session not found"


def test_access_requires_auth(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        response = client.get("/api/access")

        assert response.status_code == 401
        assert response.json()["detail"] == "Missing authorization"


def test_access_returns_contract_and_tracked_status(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    _seed_state(state_service, session_id="session_started")
    state_service.save(
        State(
            session_id="session_blank",
            user_id="dev-user",
            locale="ru",
            question="",
            phase=SessionPhase.QUESTION,
            current_question="",
            current_hint="",
            phase_index=0,
            puzzlement_turns=0,
            cards=[],
            connections=[],
        )
    )

    with TestClient(main.app) as client:
        response = client.get("/api/access", headers=_auth_headers())

        assert response.status_code == 200

        payload = response.json()
        assert payload["contract"]["status_endpoint"] == "/api/access"
        assert payload["contract"]["pricing_unit"] == "sessions"
        assert payload["contract"]["free_sessions_total"] == 3
        assert payload["contract"]["session_consumption_trigger"] == (
            "first_ai_message_on_blank_session"
        )
        assert payload["contract"]["blank_session_consumes"] is False
        assert payload["contract"]["reopen_existing_session_consumes"] is False
        assert payload["contract"]["deleting_session_restores_quota"] is False

        status = payload["status"]
        assert status["plan"] == "free"
        assert status["free_sessions_used"] == 1
        assert status["free_sessions_remaining"] == 2
        assert status["can_start_ai_session"] is True
        assert status["metering_state"] == "tracked"


def test_access_returns_persisted_paid_plan(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)
    expiry = (datetime.now(UTC) + timedelta(days=30)).isoformat()
    main.access_service.set_entitlement(
        "dev-user",
        UserEntitlement(plan=AccessPlan.MONTHLY, plan_expires_at=expiry),
    )

    with TestClient(main.app) as client:
        response = client.get("/api/access", headers=_auth_headers())

        assert response.status_code == 200
        status = response.json()["status"]
        assert status["plan"] == "monthly"
        assert status["plan_expires_at"] == expiry
        assert status["free_sessions_remaining"] is None
        assert status["can_start_ai_session"] is True


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


def test_websocket_blocks_new_session_after_free_limit(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)
    for session_id in ("used_1", "used_2", "used_3"):
        main.access_service.record_session_consumed("dev-user", session_id)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json({"type": "init", "payload": {"auth_token": "dev-token"}})
            _receive_init_messages(websocket, expect_cards=False, expect_question_update=False)

            websocket.send_json(
                {
                    "type": "user_message",
                    "payload": {"text": "Need help with a new decision"},
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["code"] == "access_exhausted"
            assert message["payload"]["access"]["status"]["free_sessions_remaining"] == 0
            assert main.ai_service.call_count == 0


def test_websocket_blocks_blank_existing_session_after_free_limit(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state_service.save(
        State(
            session_id="session_blank",
            user_id="dev-user",
            locale="ru",
            question="",
            phase=SessionPhase.QUESTION,
            current_question="",
            current_hint="",
            phase_index=0,
            puzzlement_turns=0,
            cards=[],
            connections=[],
        )
    )
    for session_id in ("used_1", "used_2", "used_3"):
        main.access_service.record_session_consumed("dev-user", session_id)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "init",
                    "payload": {
                        "session_id": "session_blank",
                        "auth_token": "dev-token",
                    },
                }
            )
            _receive_init_messages(websocket, expect_cards=False, expect_question_update=False)

            websocket.send_json(
                {
                    "type": "user_message",
                    "payload": {"text": "Try to start this blank board"},
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["code"] == "access_exhausted"
            assert message["payload"]["access"]["status"]["free_sessions_remaining"] == 0
            assert main.ai_service.call_count == 0


def test_websocket_allows_existing_started_session_after_limit(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service, session_id="session_started")
    for session_id in ("used_1", "used_2", "used_3"):
        main.access_service.record_session_consumed("dev-user", session_id)

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
                    "type": "user_message",
                    "payload": {"text": "Continue the existing board"},
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "question_update"
            assert main.ai_service.call_count == 1


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


def test_websocket_card_create_success(monkeypatch, tmp_path) -> None:
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

            websocket.send_json(
                {
                    "type": "card_create",
                    "payload": {
                        "text": "New todo",
                        "type": "todo",
                        "x": 0.2,
                        "y": 0.3,
                    },
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "cards_add"
            card = message["payload"]["cards"][0]
            assert card["text"] == "New todo"
            assert card["type"] == "todo"


def test_websocket_card_create_unauthorized(monkeypatch, tmp_path) -> None:
    _setup_services(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json(
                {
                    "type": "card_create",
                    "payload": {
                        "text": "New fact",
                        "type": "fact",
                        "x": 0.2,
                        "y": 0.3,
                    },
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Unauthorized"


def test_websocket_card_create_invalid_type(monkeypatch, tmp_path) -> None:
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

            websocket.send_json(
                {
                    "type": "card_create",
                    "payload": {
                        "text": "New card",
                        "type": "invalid",
                        "x": 0.2,
                        "y": 0.3,
                    },
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Invalid card type"


def test_websocket_card_create_empty_text(monkeypatch, tmp_path) -> None:
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

            websocket.send_json(
                {
                    "type": "card_create",
                    "payload": {
                        "text": "   ",
                        "type": "fact",
                        "x": 0.2,
                        "y": 0.3,
                    },
                }
            )

            message = websocket.receive_json()
            assert message["type"] == "error"
            assert message["payload"]["message"] == "Card text is required"


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


def test_websocket_user_message_creates_cards(monkeypatch, tmp_path) -> None:
    ai_response = (
        "{"
        '"operations": [{"type": "create_card", "card": {"text": "Fact A", "type": "fact",'
        ' "x": 600, "y": 300}}], '
        '"question_action": "clarify", '
        '"next_question": "Next step?", '
        '"next_hint": "Short hint"'
        "}"
    )
    _setup_services(monkeypatch, tmp_path, ai_response_json=ai_response)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json({"type": "init", "payload": {"auth_token": "dev-token"}})

            init_message = websocket.receive_json()
            assert init_message["type"] == "session_loaded"

            websocket.send_json({"type": "user_message", "payload": {"text": "User input"}})

            session_loaded = websocket.receive_json()
            assert session_loaded["type"] == "session_loaded"

            cards_add = websocket.receive_json()
            assert cards_add["type"] == "cards_add"
            assert cards_add["payload"]["cards"][0]["text"] == "Fact A"

            question_update = websocket.receive_json()
            assert question_update["type"] == "question_update"
            assert question_update["payload"]["question"] == "Next step?"
            assert question_update["payload"]["hint"] == "Short hint"


def test_websocket_init_with_connections(monkeypatch, tmp_path) -> None:
    state_service = _setup_services(monkeypatch, tmp_path)
    state = _seed_state(state_service, include_second_fact=True, include_connection=True)

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

            messages = _receive_init_messages(websocket, expect_connections=True)
            connections = messages["connections_add"]["payload"]["connections"]
            assert len(connections) == 1
            assert connections[0]["id"] == "conn_1"
