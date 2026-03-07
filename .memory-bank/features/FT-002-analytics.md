---
id: FT-002
title: Analytics & Event Tracking
status: draft
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
- `backend/app/events.py` (new — backend event logging)
- `backend/app/main.py` (event hooks)
