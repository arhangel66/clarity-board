---
description: Requirements (REQ-IDs) + traceability matrix (RTM).
status: active
---
# Requirements

## Functional Requirements

### Core (MVP — done)
| REQ | Description | Status |
|---|---|---|
| REQ-001 | Real-time canvas with WebSocket sync | done |
| REQ-002 | Card CRUD (create, move, edit, delete, pin) with 6 types | done |
| REQ-003 | Connection CRUD (causes, relates, contradicts, blocks) | done |
| REQ-004 | AI-guided 6-phase session flow | done |
| REQ-005 | Auth0 authentication with Google provider | done |
| REQ-006 | Multi-session (boards) management | done |
| REQ-007 | Voice input via Whisper transcription | done |
| REQ-008 | i18n support (ru/en) | done |
| REQ-009 | Special questions deck (3 categories) | done |
| REQ-010 | Onboarding overlay with demo session | done |
| REQ-011 | Mobile-responsive UX with drawer | done |

### P1 Wave B — Product Launch
| REQ | Description | Status |
|---|---|---|
| REQ-020 | Landing page redesign (problem-first, transformations, segments) | planned |
| REQ-021 | Yandex Metrica + Webvisor + custom event tracking | planned |
| REQ-022 | Interactive onboarding tour with "repeat tutorial" button | planned |
| REQ-023 | Decision memo export (Markdown download + clipboard) | planned |
| REQ-024 | Blind spot analysis (gap detection, empty zone indication) | planned |
| REQ-025 | AI output validation (bounds, duplicates, root-card protection) | done |
| REQ-026 | TODO cards panel with done/undone toggle + export | planned |
| REQ-027 | Auth reliability (token refresh, edge cases, re-login fallback) | planned |
| REQ-028 | Demand validation (own sessions + external users + analytics) | planned |
| REQ-029 | Special questions rewrite (original formulations, renamed categories) | planned |
| REQ-030 | Own domain + branding (purchase, DNS, SSL, Auth0 update) | planned |
| REQ-031 | Usage credits/limits system (track consumption per user) | planned |
| REQ-032 | Paywall UI (show pricing, track click intent, no real payment) | planned |

### P2 Wave C — Growth
| REQ | Description | Status |
|---|---|---|
| REQ-040 | LinkedIn article + launch post | planned |
| REQ-041 | Mobile UX improvements (touch-friendly, chat-first mode) | planned |
| REQ-042 | Promo content (demo sessions, screenshots, ProductHunt) | planned |

## Out of scope
- Multi-user real-time collaboration (co-editing)
- Native mobile app (iOS/Android)
- Relational database / complex SQL queries
- Self-hosted / on-premise deployment
- Marketplace of templates or shared sessions
- Integration with external tools (Notion, Trello, etc.)

## Traceability (RTM)
| REQ | Epic | Feature | Test | Status |
|---|---|---|---|---|
| REQ-001 | EP-000 | — | e2e/canvas | done |
| REQ-002 | EP-000 | — | e2e/canvas, backend/test_cards | done |
| REQ-003 | EP-000 | — | e2e/canvas | done |
| REQ-004 | EP-000 | — | backend/test_ai | done |
| REQ-005 | EP-000 | — | backend/test_auth | done |
| REQ-006 | EP-000 | — | e2e/boards | done |
| REQ-007 | EP-000 | — | — | done |
| REQ-008 | EP-000 | — | frontend/i18n.test | done |
| REQ-009 | EP-000 | — | — | done |
| REQ-010 | EP-000 | — | — | done |
| REQ-011 | EP-000 | — | — | done |
| REQ-020 | EP-001 | FT-001 | — | planned |
| REQ-021 | EP-001 | FT-002 | — | planned |
| REQ-022 | EP-002 | FT-003 | — | planned |
| REQ-023 | EP-002 | FT-004 | — | planned |
| REQ-024 | EP-002 | FT-005 | — | planned |
| REQ-025 | EP-003 | FT-006 | — | planned |
| REQ-026 | EP-002 | FT-007 | — | planned |
| REQ-027 | EP-003 | FT-008 | — | planned |
| REQ-028 | EP-001 | FT-009 | — | planned |
| REQ-029 | EP-003 | FT-010 | — | planned |
| REQ-030 | EP-001 | FT-011 | — | planned |
| REQ-031 | EP-004 | FT-012 | — | planned |
| REQ-032 | EP-004 | FT-013 | — | planned |
| REQ-040 | EP-001 | FT-014 | — | planned |
| REQ-041 | EP-002 | FT-015 | — | planned |
| REQ-042 | EP-001 | FT-016 | — | planned |
