---
description: Feature brief for analytics instrumentation and event tracking.
id: FT-002
title: Analytics & Event Tracking
status: in_progress
epic: EP-001
reqs: [REQ-021]
depends: []
---
# FT-002: Analytics & Event Tracking

## Goal
Instrumentation to measure user behavior, conversion funnel, and product usage before landing redesign ships.

## Acceptance criteria
- [ ] Yandex Metrica counter installed (pageview tracking)
- [ ] Webvisor enabled (session recordings)
- [ ] Heatmaps + click maps on landing page
- [ ] Conversion goals configured: landing -> sign-up -> first session -> 5+ cards -> completed
- [ ] Custom frontend events: card_created, connection_created, phase_changed, special_question_used, session_exported
- [ ] Backend event logging: session duration, card count, phase reached, AI calls count
- [ ] In-app feedback form (post-session)
- [ ] Privacy: card content notice in ToS, EU-compliant mode

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
- Backend structured event logging exists via `backend/app/services/event_service.py` and is wired into `MainService`.
- Remaining gaps are dashboard-side goal configuration, post-session feedback, and privacy/compliance copy.
