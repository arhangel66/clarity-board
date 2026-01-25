from app.models import State
from app.services.main_service import MainService
from app.services.state_service import StateService


class DummyAIService:
    async def generate_response(self, message: str, state: State) -> str:
        return '{"operations": [], "question_action": "keep"}'


def test_connection_creation_and_persistence(tmp_path):
    db_path = tmp_path / "test.db"
    state_service = StateService(str(db_path))
    service = MainService(state_service=state_service, ai_service=DummyAIService())

    # Initialize session
    init_res = service.init(None, "user_1")
    session_id = init_res.session_loaded["id"]

    # Create two cards
    card1_data = {"text": "Card 1", "type": "fact", "x": 0.1, "y": 0.1}
    card2_data = {"text": "Card 2", "type": "fact", "x": 0.2, "y": 0.2}

    card1 = service._create_card(card1_data)
    card2 = service._create_card(card2_data)
    service.state.cards.extend([card1, card2])
    state_service.save(service.state)

    # Create connection
    conn = service.create_connection(card1.id, card2.id, "causes", "leads to")
    assert conn is not None
    assert conn["from_id"] == card1.id
    assert conn["to_id"] == card2.id
    assert conn["type"] == "causes"
    assert conn["label"] == "leads to"

    # Verify persistence
    new_service = MainService(state_service=state_service, ai_service=DummyAIService())
    reloaded = new_service.init(session_id, "user_1")

    assert len(reloaded.connections) == 1
    assert reloaded.connections[0]["id"] == conn["id"]
    assert reloaded.connections[0]["from_id"] == card1.id

    # Delete connection
    success = new_service.delete_connection(conn["id"])
    assert success is True
    assert len(new_service.state.connections) == 0

    # Verify deletion persisted
    final_service = MainService(state_service=state_service, ai_service=DummyAIService())
    final_reloaded = final_service.init(session_id, "user_1")
    assert len(final_reloaded.connections) == 0
