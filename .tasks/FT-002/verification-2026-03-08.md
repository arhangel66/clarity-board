# FT-002 Verification Evidence

Date: 2026-03-08

## Commands

- `cd backend && uv run pytest tests/test_event_service.py -v`
  - Result: `5 passed`
- `cd frontend && pnpm test -- --run`
  - Result: `5` test files, `10` tests passed
  - Includes `src/lib/analytics.test.ts` for the Yandex wrapper and export tracking helper
- `cd frontend && pnpm check`
  - Result: `0 errors`, `20 warnings`
  - Warnings are pre-existing Svelte/a11y issues outside FT-002 scope
- `cd frontend && pnpm build`
  - Result: success
  - Existing non-blocking warnings remain about CSS `@import` order and a dynamic-import chunk note

## Code Evidence

- `frontend/index.html`
  - Counter `107194444` installed
  - `webvisor:true` and `clickmap:true` enabled
- `frontend/src/lib/analytics.ts`
  - Goal helpers for `landing_view`, `sign_up`, `first_session`, `cards_5_plus`, `session_completed`
  - Custom events for card, connection, phase, special question, input mode, and `session_exported`
- `frontend/src/App.svelte`
  - Tracks landing view, sign-up, and 5-card milestone
- `frontend/src/lib/stores/websocket.ts`
  - Tracks first session, card/connection creation, phase change, session completion, special-question usage
- `frontend/src/lib/components/InputBar.svelte`
  - Tracks text vs voice input usage
- `frontend/src/lib/components/BoardsSidebar.svelte`
  - Tracks export actions from the main tools menu
- `frontend/src/lib/components/SelectionToolbar.svelte`
  - Tracks export actions from the selection toolbar
- `backend/app/services/event_service.py`
  - Structured JSONL logging for session start/end, AI calls, card/connection creation, phase changes, special questions, user message type
- `backend/app/services/main_service.py`
  - Emits backend analytics events during session lifecycle

## Privacy Check

- Frontend analytics sends only event names and metadata like `card_type`, `connection_type`, `phase`, `input_type`, and `export_type`
- No card text or free-form user content is passed to `ym(...)` in the tracked call sites above
- Webvisor form-input masking and dashboard goal setup remain operational settings in Yandex UI, not repository code
