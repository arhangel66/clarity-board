---
description: Implementation plan for FT-004 decision memo export.
status: active
---
# IMPL-FT-004

## Goal
Turn a session into a structured Markdown decision memo that can be copied or downloaded.

## Steps
- Define the export contract: problem statement, facts, insights, connections, and action items.
- Add backend summary generation or formatting support that works with current session data.
- Add an export surface in the frontend with copy/download actions and explicit success/error states.
- Reuse existing export analytics hooks where possible.

## Expected touched files
- `backend/app/services/ai_service.py`
- `backend/app/services/main_service.py`
- `backend/app/main.py`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/components/SelectionToolbar.svelte`
- `frontend/src/lib/stores/i18n.ts`

## Tests
- `cd backend && uv run pytest -v`
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`

## Quality gates
- Memo generation must tolerate sparse sessions and demo boards gracefully.

## Verify / UAT
- Generate a memo from a real session, copy it to the clipboard, and download the `.md` file.
