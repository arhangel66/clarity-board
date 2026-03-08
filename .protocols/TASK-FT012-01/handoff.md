# TASK-FT012-01 Handoff

## Summary
- Added `backend/app/access.py` as the code-facing source of truth for the launch access contract: `3 free sessions total`, `monthly`, and `lifetime`.
- Added `GET /api/access` in `backend/app/main.py` so the frontend has a stable backend surface for FT-012/FT-013.
- Access status currently reports usage as `estimated_from_sessions` by scanning existing started boards; irreversible metering and enforcement still belong to `TASK-FT012-02`.
- Added focused backend coverage in `backend/tests/test_access.py` plus integration coverage for the new endpoint.

## Follow-ups
- `TASK-FT012-02`: persist entitlements and enforce access before new AI-assisted sessions start
- `TASK-FT012-03`: expose the access state in the frontend without falling back to a credits UI
