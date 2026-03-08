"""Access contract and entitlement helpers for session-based limits."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from app.models import State
from app.services.state_service import StateService

FREE_SESSION_LIMIT = 3
ACCESS_STATUS_ENDPOINT = "/api/access"
ACCESS_ENTITLEMENTS_TABLE = "access_entitlements"
ACCESS_SESSION_USAGE_TABLE = "access_session_usage"


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


class AccessBlockedError(RuntimeError):
    """Raised when a blank AI-assisted session cannot start."""

    def __init__(self, snapshot: AccessSnapshot) -> None:
        self.snapshot = snapshot
        super().__init__("Access exhausted")


class AccessService:
    """Resolve session-based access rules without exposing a credits model."""

    def __init__(self, state_service: StateService | None = None) -> None:
        self.state_service = state_service
        self._init_schema()

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

    def set_entitlement(self, user_id: str, entitlement: UserEntitlement) -> None:
        """Persist a launch-era entitlement for a user."""
        if self.state_service is None:
            return

        normalized_expiry = entitlement.plan_expires_at
        if entitlement.plan == AccessPlan.MONTHLY and not normalized_expiry:
            raise ValueError("Monthly access requires plan_expires_at")
        if entitlement.plan != AccessPlan.MONTHLY:
            normalized_expiry = None

        conn = self.state_service._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {ACCESS_ENTITLEMENTS_TABLE} (user_id, plan, plan_expires_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                plan = excluded.plan,
                plan_expires_at = excluded.plan_expires_at,
                updated_at = excluded.updated_at
            """,
            (
                user_id,
                entitlement.plan.value,
                normalized_expiry,
                datetime.now(UTC).isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def get_entitlement(self, user_id: str) -> UserEntitlement:
        """Load the persisted entitlement for a user."""
        implicit_entitlement = self._get_implicit_entitlement(user_id)
        if implicit_entitlement is not None:
            return implicit_entitlement

        if self.state_service is None:
            return UserEntitlement()

        conn = self.state_service._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT plan, plan_expires_at FROM {ACCESS_ENTITLEMENTS_TABLE} WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return UserEntitlement()

        return UserEntitlement(plan=AccessPlan(row["plan"]), plan_expires_at=row["plan_expires_at"])

    def _get_implicit_entitlement(self, user_id: str) -> UserEntitlement | None:
        """Grant unlimited access to the local dev-bypass identity."""
        if os.getenv("E2E_UNLIMITED_ACCESS", "").lower() == "true" and user_id == "dev-user":
            return UserEntitlement(plan=AccessPlan.LIFETIME)
        return None

    def record_session_consumed(self, user_id: str, session_id: str) -> None:
        """Persist that a session has consumed one starter-session slot."""
        if self.state_service is None:
            return

        conn = self.state_service._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {ACCESS_SESSION_USAGE_TABLE} (session_id, user_id, consumed_at)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO NOTHING
            """,
            (session_id, user_id, datetime.now(UTC).isoformat()),
        )
        conn.commit()
        conn.close()

    def sync_metering(self, user_id: str) -> int:
        """Backfill tracked usage from already-started sessions and return the count."""
        if self.state_service is None:
            return 0

        for session in self.state_service.list_sessions(user_id):
            state = self.state_service.get_for_user(session["id"], user_id)
            if state and not self._is_blank_session(state):
                self.record_session_consumed(user_id, state.session_id)

        conn = self.state_service._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT COUNT(*) AS count FROM {ACCESS_SESSION_USAGE_TABLE} WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return int(row["count"]) if row else 0

    def ensure_can_start_ai_session(self, user_id: str, state: State | None) -> None:
        """Block blank-board AI starts when no access remains."""
        if not self.should_consume_session(state):
            return

        snapshot = self.get_access_snapshot(user_id)
        if snapshot.status.can_start_ai_session:
            return
        raise AccessBlockedError(snapshot)

    def get_access_snapshot(
        self,
        user_id: str,
        entitlement: UserEntitlement | None = None,
    ) -> AccessSnapshot:
        """Return the current access response shape for the authenticated user."""
        free_sessions_used = None
        metering_state = MeteringState.PENDING_PERSISTENCE
        effective_entitlement = entitlement or self.get_entitlement(user_id)

        if self.state_service is not None:
            free_sessions_used = self.sync_metering(user_id)
            metering_state = MeteringState.TRACKED

        return AccessSnapshot(
            contract=self.contract(),
            status=self.resolve_status(
                effective_entitlement,
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

    def _init_schema(self) -> None:
        if self.state_service is None:
            return

        conn = self.state_service._get_connection()
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS {ACCESS_ENTITLEMENTS_TABLE} (
                user_id TEXT PRIMARY KEY,
                plan TEXT NOT NULL,
                plan_expires_at TEXT,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS {ACCESS_SESSION_USAGE_TABLE} (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                consumed_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS access_session_usage_user_id_idx
                ON {ACCESS_SESSION_USAGE_TABLE}(user_id);
            """
        )
        conn.commit()
        conn.close()

    def _is_blank_session(self, state: State) -> bool:
        return not bool(state.question.strip())

    def _plan_is_active(self, plan_expires_at: str | None) -> bool:
        if not plan_expires_at:
            return False

        normalized = plan_expires_at.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized) > datetime.now(UTC)
