# FT-002 Context

## Loaded docs
- `.memory-bank/features/FT-002-analytics.md` — acceptance criteria
- `.memory-bank/requirements.md` — REQ-021 lifecycle
- `.memory-bank/tasks/backlog.md` — W1 priority and lifecycle
- `frontend/index.html` — Metrica bootstrap
- `frontend/src/lib/analytics.ts` — frontend analytics wrapper
- `frontend/src/App.svelte` — landing and funnel tracking
- `frontend/src/lib/stores/websocket.ts` — session/card/phase tracking
- `frontend/src/lib/components/InputBar.svelte` — input mode tracking
- `frontend/src/lib/components/BoardsSidebar.svelte` — export tracking
- `frontend/src/lib/components/SelectionToolbar.svelte` — export tracking
- `backend/app/services/main_service.py` — backend event emission
- `backend/app/services/event_service.py` — JSONL analytics logging
- `backend/tests/test_event_service.py` — backend verification

## Current state
- Yandex Metrica counter `107194444` is installed and initialized with `webvisor` and `clickmap`.
- Frontend emits conversion goals and custom analytics events for landing, auth, session progress, input mode, and exports.
- Backend writes structured analytics events to JSONL via `EventService`.
- The remaining work for close-out was verification + Memory Bank sync, not missing product code.
