# TASK-FT012-01 Plan

## Goal
Turn the ambiguous monetization notes into a stable backend contract so later FT-012 work can implement persistence and enforcement without reopening the product rules.

## Steps
1. Create `backend/app/access.py` with explicit session-limit constants, access models, and helper logic for consumption and plan status.
2. Expose `GET /api/access` from `backend/app/main.py` so the contract has a stable API surface.
3. Add backend tests for the access rules and the new endpoint.
4. Record FT-012 assumptions in `.protocols/FT-012/decision-log.md` and store verification evidence.

## Expected touched files
- `backend/app/access.py`
- `backend/app/main.py`
- `backend/tests/test_access.py`
- `backend/tests/test_integration_endpoints.py`
- `.protocols/FT-012/decision-log.md`

## Gates
- `cd backend && uv run pytest tests/test_access.py tests/test_integration_endpoints.py -v`
- `cd backend && uv run pytest -v`
