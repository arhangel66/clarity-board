# TASK-FT012-02 Plan

## Goal
Turn the FT-012 contract into a durable backend system with persistent usage counts, stored entitlements, and blank-session gating.

## Steps
1. Extend backend persistence for access entitlements and consumed sessions.
2. Teach `AccessService` to read/write tracked state and to backfill from existing started boards.
3. Wire `MainService` to block the first AI-assisted message on a blank board when no access remains, while allowing already-started boards to continue.
4. Update backend tests for tracked snapshots, entitlement states, and WebSocket enforcement.
5. Record FT-012 decisions/evidence and sync the Memory Bank state.

## Expected touched files
- `backend/app/access.py`
- `backend/app/construct.py`
- `backend/app/main.py`
- `backend/app/services/main_service.py`
- `backend/app/services/state_service.py`
- `backend/tests/test_access.py`
- `backend/tests/test_integration_endpoints.py`
- `backend/tests/test_main_service.py`
- `.protocols/FT-012/decision-log.md`

## Gates
- `cd backend && uv run pytest tests/test_access.py tests/test_main_service.py tests/test_integration_endpoints.py -v`
- `cd backend && uv run pytest -v`
