---
description: Feature brief for analytics instrumentation and event tracking.
id: FT-002
title: Analytics & Event Tracking
status: done
epic: EP-001
reqs: [REQ-021]
depends: []
---
# FT-002: Analytics & Event Tracking

## Goal
Instrumentation to measure user behavior, conversion funnel, and product usage before landing redesign ships.

## Acceptance criteria
- [x] Yandex Metrica counter installed (pageview tracking)
- [x] Webvisor and clickmap enabled in the client bootstrap
- [x] Conversion goals emitted for landing -> sign-up -> first session -> 5+ cards -> completed
- [x] Custom frontend events emitted: card_created, connection_created, phase_changed, special_question_used, session_exported, voice_input_used, text_input_used
- [x] Backend event logging captures session lifecycle, phase progress, card/connection creation, AI calls, and input mode
- [x] Analytics payloads exclude card text and other free-form user content

## Touched files (expected)
- `frontend/index.html` or `app.html` (Metrica script)
- `frontend/src/lib/analytics.ts` (new — event helpers)
- `frontend/src/lib/stores/websocket.ts` (emit events)
- `frontend/src/App.svelte` (landing and funnel analytics hooks)
- `backend/app/services/event_service.py` (structured backend event logging)
- `backend/app/services/main_service.py` (event hooks)

## Current verified implementation
- Yandex Metrica counter `107194444` is installed in `frontend/index.html` with `webvisor` and `clickmap` enabled.
- Frontend goal helpers exist in `frontend/src/lib/analytics.ts` and are called from `frontend/src/App.svelte`, `frontend/src/lib/components/InputBar.svelte`, and `frontend/src/lib/stores/websocket.ts`.
- Export analytics is emitted from `frontend/src/lib/components/BoardsSidebar.svelte` and `frontend/src/lib/components/SelectionToolbar.svelte`.
- Backend structured event logging exists via `backend/app/services/event_service.py` and is wired into `MainService`.
- Verification evidence lives in `.tasks/FT-002/verification-2026-03-08.md`.

## Operational follow-ups
- Yandex dashboard goal naming/reporting remains an operational setup step outside the repo.
- Legal/privacy copy changes should be handled as a separate launch-policy task if required.
