# FT-002 Implementation Plan

## Scope
Analytics & Event Tracking — Yandex Metrica + custom events + backend logging.

## Steps

### Step 1: Yandex Metrica (frontend)
- [ ] Add Yandex Metrica counter script to `frontend/index.html`
- [ ] Enable Webvisor, heatmaps, click maps in counter settings (done in Metrica UI, script just needs correct config)
- [ ] Create `frontend/src/lib/analytics.ts` — wrapper for `ym()` calls with type safety

### Step 2: Frontend custom events
- [ ] Track conversion funnel goals via `ym('reachGoal', ...)`:
  - `landing_view` — landing page shown
  - `sign_up` — auth completed
  - `first_session` — first board/session created
  - `cards_5_plus` — 5+ cards in session
  - `session_completed` — reached connections phase
- [ ] Track custom events:
  - `card_created` — with card type
  - `connection_created` — with connection type
  - `phase_changed` — with new phase name
  - `special_question_used`
  - `voice_input_used` / `text_input_used`
- [ ] Integration points:
  - `App.svelte` — landing_view, sign_up
  - `websocket.ts` — card/connection/phase events (on server response)
  - `InputBar.svelte` — input mode tracking
  - `boards.ts` — first_session

### Step 3: Backend event logging
- [ ] Create `backend/app/services/event_service.py` — structured event logger
  - Logs to structured JSON (file-based, simple)
  - Events: session_start, session_end, card_count, phase_reached, ai_call
- [ ] Add EventService to `construct.py`
- [ ] Hook into `MainService` for event emission
- [ ] Track: session duration, card count per session, max phase reached, AI calls count

### Step 4: Privacy
- [ ] Add cookie consent notice for Yandex Metrica (simple banner)
- [ ] Yandex Metrica configured to NOT record form inputs (Webvisor setting)
- [ ] No card content sent to analytics — only event names and card types

### Step 5: Tests
- [ ] Unit test for `analytics.ts` (mock ym function)
- [ ] Unit test for `EventService`
- [ ] Verify no card content leaks to analytics

## Out of scope (deferred)
- In-app feedback form (separate task — requires UI design)
- ToS page update (legal review needed)
- Session export tracking (export feature doesn't exist yet)

## Files touched
- `frontend/index.html` — Metrica script
- `frontend/src/lib/analytics.ts` — NEW
- `frontend/src/App.svelte` — funnel events
- `frontend/src/lib/stores/websocket.ts` — card/connection/phase events
- `frontend/src/lib/components/InputBar.svelte` — input mode tracking
- `frontend/src/lib/stores/boards.ts` — first_session event
- `backend/app/services/event_service.py` — NEW
- `backend/app/construct.py` — add EventService
- `backend/app/services/main_service.py` — emit events
- `backend/app/main.py` — pass EventService to MainService
