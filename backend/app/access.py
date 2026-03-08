"""Access contract and entitlement helpers for session-based limits."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from app.models import State
from app.services.state_service import StateService

FREE_SESSION_LIMIT = 3
ACCESS_STATUS_ENDPOINT = "/api/access"


class AccessPlan(str, Enum):
    """Supported launch-era access plans."""

    FREE = "free"
    MONTHLY = "monthly"
    LIFETIME = "lifetime"


class MeteringState(str, Enum):
    """How trustworthy the usage counters are for the current response."""

    PENDING_PERSISTENCE = "pending_persistence"
    ESTIMATED_FROM_SESSIONS = "estimated_from_sessions"
    TRACKED = "tracked"


class SessionConsumptionTrigger(str, Enum):
    """When the product should treat a board as a consumed session."""

    FIRST_AI_MESSAGE_ON_BLANK_SESSION = "first_ai_message_on_blank_session"


class AccessContract(BaseModel):
    """Stable code-facing rules for the launch monetization model."""

    status_endpoint: str = ACCESS_STATUS_ENDPOINT
    pricing_unit: Literal["sessions"] = "sessions"
    free_sessions_total: int = FREE_SESSION_LIMIT
    session_consumption_trigger: SessionConsumptionTrigger = (
        SessionConsumptionTrigger.FIRST_AI_MESSAGE_ON_BLANK_SESSION
    )
    blank_session_consumes: bool = False
    reopen_existing_session_consumes: bool = False
    deleting_session_restores_quota: bool = False
    supported_plans: list[AccessPlan] = Field(
        default_factory=lambda: [AccessPlan.FREE, AccessPlan.MONTHLY, AccessPlan.LIFETIME]
    )
    monthly_requires_expires_at: bool = True
    lifetime_never_expires: bool = True


class UserEntitlement(BaseModel):
    """Persisted or implied access state for a user."""

    plan: AccessPlan = AccessPlan.FREE
    plan_expires_at: str | None = None


class AccessStatus(BaseModel):
    """User-facing status shape returned by the access endpoint."""

    plan: AccessPlan
    plan_expires_at: str | None = None
    plan_active: bool = True
    free_sessions_total: int = FREE_SESSION_LIMIT
    free_sessions_used: int | None = None
    free_sessions_remaining: int | None = None
    can_start_ai_session: bool = True
    metering_state: MeteringState = MeteringState.PENDING_PERSISTENCE


class AccessSnapshot(BaseModel):
    """Combined access contract + current user status."""

    contract: AccessContract
    status: AccessStatus


class AccessService:
    """Resolve session-based access rules without exposing a credits model."""

    def __init__(self, state_service: StateService | None = None) -> None:
        self.state_service = state_service

    def contract(self) -> AccessContract:
        return AccessContract()

    def should_consume_session(self, state: State | None) -> bool:
        """Return True when a new AI-assisted board should consume starter quota."""
        if state is None:
            return True
        return self._is_blank_session(state)

    def estimate_started_sessions(self, user_id: str) -> int:
        """Approximate starter-session usage from the current session store."""
        if self.state_service is None:
            return 0

        started_sessions = 0
        for session in self.state_service.list_sessions(user_id):
            state = self.state_service.get_for_user(session["id"], user_id)
            if state and not self._is_blank_session(state):
                started_sessions += 1
        return started_sessions

    def get_access_snapshot(
        self,
        user_id: str,
        entitlement: UserEntitlement | None = None,
    ) -> AccessSnapshot:
        """Return the current access response shape for the authenticated user."""
        free_sessions_used = None
        metering_state = MeteringState.PENDING_PERSISTENCE

        if self.state_service is not None:
            free_sessions_used = self.estimate_started_sessions(user_id)
            metering_state = MeteringState.ESTIMATED_FROM_SESSIONS

        return AccessSnapshot(
            contract=self.contract(),
            status=self.resolve_status(
                entitlement,
                free_sessions_used=free_sessions_used,
                metering_state=metering_state,
            ),
        )

    def resolve_status(
        self,
        entitlement: UserEntitlement | None = None,
        *,
        free_sessions_used: int | None = None,
        metering_state: MeteringState | None = None,
    ) -> AccessStatus:
        """Resolve the effective access status for the current contract."""
        entitlement = entitlement or UserEntitlement()
        metering_state = metering_state or self._default_metering_state(free_sessions_used)

        if entitlement.plan == AccessPlan.LIFETIME:
            return AccessStatus(
                plan=AccessPlan.LIFETIME,
                free_sessions_used=free_sessions_used,
                free_sessions_remaining=None,
                can_start_ai_session=True,
                metering_state=metering_state,
            )

        if entitlement.plan == AccessPlan.MONTHLY and self._plan_is_active(
            entitlement.plan_expires_at
        ):
            return AccessStatus(
                plan=AccessPlan.MONTHLY,
                plan_expires_at=entitlement.plan_expires_at,
                free_sessions_used=free_sessions_used,
                free_sessions_remaining=None,
                can_start_ai_session=True,
                metering_state=metering_state,
            )

        used_sessions = free_sessions_used if free_sessions_used is not None else 0
        remaining_sessions = max(0, FREE_SESSION_LIMIT - used_sessions)
        return AccessStatus(
            plan=AccessPlan.FREE,
            free_sessions_used=free_sessions_used,
            free_sessions_remaining=(
                remaining_sessions if free_sessions_used is not None else None
            ),
            can_start_ai_session=remaining_sessions > 0,
            metering_state=metering_state,
        )

    def _default_metering_state(self, free_sessions_used: int | None) -> MeteringState:
        if free_sessions_used is None:
            return MeteringState.PENDING_PERSISTENCE
        return MeteringState.TRACKED

    def _is_blank_session(self, state: State) -> bool:
        return not bool(state.question.strip())

    def _plan_is_active(self, plan_expires_at: str | None) -> bool:
        if not plan_expires_at:
            return False

        normalized = plan_expires_at.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized) > datetime.now(UTC)
