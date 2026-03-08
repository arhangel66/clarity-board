---
description: Implementation plan for FT-002 analytics and event tracking.
status: active
---
# IMPL-FT-002

## Goal
Maintain verified analytics coverage across landing, funnel, export, and backend session events.

## Steps
- Keep Yandex Metrica bootstrap and event helper coverage intact.
- Keep backend event logging structured and free of user-generated card text.
- Treat Yandex dashboard naming/reporting as an operational follow-up outside the repo.

## Expected touched files
- `frontend/index.html`
- `frontend/src/lib/analytics.ts`
- `frontend/src/App.svelte`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/components/SelectionToolbar.svelte`
- `frontend/src/lib/stores/websocket.ts`
- `backend/app/services/event_service.py`
- `backend/app/services/main_service.py`

## Tests
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`
- `cd backend && uv run pytest tests/test_event_service.py -v`

## Quality gates
- No card text or free-form user content leaves the app through analytics payloads.

## Verify / UAT
- Reconfirm the event list against `REQ-021`.
