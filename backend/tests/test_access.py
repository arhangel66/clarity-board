from datetime import UTC, datetime, timedelta

from app.access import (
    AccessPlan,
    AccessService,
    MeteringState,
    SessionConsumptionTrigger,
    UserEntitlement,
)
from app.models import State
from app.services.state_service import StateService


def _make_state(*, session_id: str, user_id: str, question: str) -> State:
    return State(session_id=session_id, user_id=user_id, question=question)


def test_should_consume_session_only_for_blank_boards() -> None:
    service = AccessService()

    blank_state = _make_state(session_id="session_blank", user_id="user_1", question="")
    started_state = _make_state(
        session_id="session_started",
        user_id="user_1",
        question="How do I decide what to do next?",
    )

    assert service.should_consume_session(None) is True
    assert service.should_consume_session(blank_state) is True
    assert service.should_consume_session(started_state) is False


def test_access_contract_keeps_no_refund_and_existing_board_rules() -> None:
    contract = AccessService().contract()

    assert contract.session_consumption_trigger == (
        SessionConsumptionTrigger.FIRST_AI_MESSAGE_ON_BLANK_SESSION
    )
    assert contract.blank_session_consumes is False
    assert contract.reopen_existing_session_consumes is False
    assert contract.deleting_session_restores_quota is False


def test_resolve_status_tracks_remaining_free_sessions() -> None:
    service = AccessService()

    status = service.resolve_status(
        free_sessions_used=2,
        metering_state=MeteringState.TRACKED,
    )

    assert status.plan == AccessPlan.FREE
    assert status.free_sessions_total == 3
    assert status.free_sessions_used == 2
    assert status.free_sessions_remaining == 1
    assert status.can_start_ai_session is True
    assert status.metering_state == MeteringState.TRACKED


def test_resolve_status_blocks_free_plan_after_limit() -> None:
    service = AccessService()

    status = service.resolve_status(
        free_sessions_used=3,
        metering_state=MeteringState.TRACKED,
    )

    assert status.plan == AccessPlan.FREE
    assert status.free_sessions_remaining == 0
    assert status.can_start_ai_session is False


def test_resolve_status_keeps_paid_plans_unlimited() -> None:
    service = AccessService()
    future_expiry = (datetime.now(UTC) + timedelta(days=30)).isoformat()

    monthly = service.resolve_status(
        UserEntitlement(plan=AccessPlan.MONTHLY, plan_expires_at=future_expiry),
        free_sessions_used=3,
        metering_state=MeteringState.TRACKED,
    )
    lifetime = service.resolve_status(
        UserEntitlement(plan=AccessPlan.LIFETIME),
        free_sessions_used=9,
        metering_state=MeteringState.TRACKED,
    )

    assert monthly.plan == AccessPlan.MONTHLY
    assert monthly.plan_expires_at == future_expiry
    assert monthly.free_sessions_remaining is None
    assert monthly.can_start_ai_session is True

    assert lifetime.plan == AccessPlan.LIFETIME
    assert lifetime.free_sessions_remaining is None
    assert lifetime.can_start_ai_session is True


def test_expired_monthly_plan_falls_back_to_free_status() -> None:
    service = AccessService()
    past_expiry = (datetime.now(UTC) - timedelta(days=1)).isoformat()

    status = service.resolve_status(
        UserEntitlement(plan=AccessPlan.MONTHLY, plan_expires_at=past_expiry),
        free_sessions_used=3,
        metering_state=MeteringState.TRACKED,
    )

    assert status.plan == AccessPlan.FREE
    assert status.free_sessions_remaining == 0
    assert status.can_start_ai_session is False


def test_estimate_started_sessions_ignores_blank_boards(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    state_service.save(_make_state(session_id="session_blank", user_id="user_1", question=""))
    state_service.save(
        _make_state(
            session_id="session_started",
            user_id="user_1",
            question="How do I fix this decision?",
        )
    )

    service = AccessService(state_service=state_service)

    assert service.estimate_started_sessions("user_1") == 1


def test_get_access_snapshot_uses_tracked_persistence(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    state_service.save(
        _make_state(
            session_id="session_started",
            user_id="user_1",
            question="How do I fix this decision?",
        )
    )
    state_service.save(_make_state(session_id="session_blank", user_id="user_1", question=""))

    service = AccessService(state_service=state_service)
    snapshot = service.get_access_snapshot("user_1")

    assert snapshot.status.plan == AccessPlan.FREE
    assert snapshot.status.free_sessions_used == 1
    assert snapshot.status.free_sessions_remaining == 2
    assert snapshot.status.metering_state == MeteringState.TRACKED


def test_recorded_session_usage_survives_session_delete(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    state_service.save(
        _make_state(
            session_id="session_started",
            user_id="user_1",
            question="How do I fix this decision?",
        )
    )

    service = AccessService(state_service=state_service)
    service.record_session_consumed("user_1", "session_started")

    assert state_service.delete_session("session_started", "user_1") is True

    snapshot = service.get_access_snapshot("user_1")
    assert snapshot.status.free_sessions_used == 1
    assert snapshot.status.free_sessions_remaining == 2


def test_get_access_snapshot_reads_persisted_paid_plan(tmp_path) -> None:
    state_service = StateService(str(tmp_path / "test.db"))
    service = AccessService(state_service=state_service)
    expiry = (datetime.now(UTC) + timedelta(days=30)).isoformat()

    service.set_entitlement(
        "user_1",
        UserEntitlement(plan=AccessPlan.MONTHLY, plan_expires_at=expiry),
    )

    snapshot = service.get_access_snapshot("user_1")

    assert snapshot.status.plan == AccessPlan.MONTHLY
    assert snapshot.status.plan_expires_at == expiry
    assert snapshot.status.free_sessions_remaining is None
    assert snapshot.status.can_start_ai_session is True


def test_dev_bypass_user_gets_implicit_unlimited_access(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("E2E_UNLIMITED_ACCESS", "true")
    state_service = StateService(str(tmp_path / "test.db"))
    service = AccessService(state_service=state_service)

    snapshot = service.get_access_snapshot("dev-user")

    assert snapshot.status.plan == AccessPlan.LIFETIME
    assert snapshot.status.free_sessions_remaining is None
    assert snapshot.status.can_start_ai_session is True
