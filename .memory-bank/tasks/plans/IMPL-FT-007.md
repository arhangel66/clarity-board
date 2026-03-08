---
description: Implementation plan for FT-007 TODO cards as an action plan.
status: active
---
# IMPL-FT-007

## Goal
Let users treat TODO cards as a lightweight action tracker instead of a generic card subtype only.

## Steps
- Extend the card model with done/undone state in a backwards-compatible way.
- Add a TODO-only panel or filter with badge/count visibility.
- Reuse the existing export surfaces for dedicated action-item export.
- Keep persistence consistent across reloads and sessions.

## Expected touched files
- `backend/app/models.py`
- `backend/app/services/main_service.py`
- `frontend/src/lib/stores/cards.ts`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/components/SelectionToolbar.svelte`

## Tests
- `cd backend && uv run pytest -v`
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`

## Quality gates
- Existing card CRUD and export paths must keep working for non-TODO cards.

## Verify / UAT
- Mark TODO cards complete/incomplete, refresh the app, and export the action list.
