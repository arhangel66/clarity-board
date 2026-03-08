# TASK-FT012-01 Verification Evidence

## Commands
- `cd backend && uv run pytest tests/test_access.py tests/test_integration_endpoints.py -v`
- `cd backend && uv run pytest -v`
- `cd backend && uv run ruff check app/access.py app/main.py tests/test_access.py tests/test_integration_endpoints.py`

## Results
- Targeted backend slice passed: `26` tests.
- Full backend suite passed: `65` tests.
- Ruff passed on the touched backend files with `0` issues.
- Existing backend warnings remain limited to pre-existing `datetime.utcnow()` deprecations outside this task's scope.

## Code Evidence
- `backend/app/access.py`
  - Defines the launch access contract, supported plans, metering-state semantics, and the session-consumption trigger.
- `backend/app/main.py`
  - Adds authenticated `GET /api/access` returning the contract plus the current status payload.
- `backend/tests/test_access.py`
  - Verifies session-consumption rules, free-limit behavior, paid-plan semantics, and estimated session counting.
- `backend/tests/test_integration_endpoints.py`
  - Verifies the new endpoint requires auth and returns the expected contract/status shape.
- `.protocols/FT-012/decision-log.md`
  - Records the session-based launch model and the temporary `estimated_from_sessions` assumption.

## User-visible outcome
- The backend now exposes a stable access contract for `3 free sessions total`, `monthly`, and `lifetime` plans without reintroducing a credits model.
- Follow-up tasks can implement persistence and enforcement against the same API shape instead of redefining monetization rules again.
