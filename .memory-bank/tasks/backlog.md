---
description: Backlog and execution plan (waves).
status: active
---
# Backlog

## Conventions
Each task should include: goal, touched files, tests, verification steps, docs-first update.

## Task state model
- `Status: planned|ready|in_progress|blocked|done|failed`
- `Wave: W1|W2|W3`
- `Depends on: TASK-... | none`

## Wave structure

### W1: Foundation (analytics + reliability + credits)
Priority: ship instrumentation and quality before new features.

| # | Feature | Epic | Priority | Status |
|---|---|---|---|---|
| 1 | FT-002 Analytics & Event Tracking | EP-001 | P1 | done |
| 2 | FT-006 AI Output Validation | EP-003 | P1 | done |
| 3 | FT-008 Auth Reliability | EP-003 | P1 | planned |
| 4 | FT-012 Usage Credits & Limits | EP-004 | P1 | planned |

### W2: Core value (UX + methodology + landing)
Priority: deliver the product value and make it discoverable.

| # | Feature | Epic | Priority | Status |
|---|---|---|---|---|
| 5 | FT-003 Interactive Onboarding Tour | EP-002 | P1 | planned |
| 6 | FT-004 Decision Memo Export | EP-002 | P1 | planned |
| 7 | FT-005 Blind Spot Analysis | EP-002 | P1 | planned |
| 8 | FT-007 TODO Cards Panel | EP-002 | P1 | planned |
| 9 | FT-001 Landing Page Redesign | EP-001 | P1 | planned |
| 10 | FT-010 Special Questions Rewrite | EP-003 | P1 | planned |
| 11 | FT-013 Paywall UI & Intent Tracking | EP-004 | P1 | planned |

### W3: Launch & growth
Priority: go public, validate demand, iterate.

| # | Feature | Epic | Priority | Status |
|---|---|---|---|---|
| 12 | FT-011 Own Domain & Branding | EP-001 | P1 | planned |
| 13 | FT-009 Demand Validation | EP-001 | P1 | planned |
| 14 | FT-014 LinkedIn Article | EP-001 | P2 | planned |
| 15 | FT-015 Mobile UX Improvements | EP-002 | P2 | planned |
| 16 | FT-016 Promo Content | EP-001 | P2 | planned |

## Follow-up tasks

| # | Task | Priority | Status |
|---|------|----------|--------|
| T-001 | Replace Yandex Metrica placeholder counter ID (0) with real ID in `frontend/index.html` and `frontend/src/lib/analytics.ts` | P1 | planned |

## Task generation
Tasks are generated per-feature using `/prd-to-tasks FT-<NNN>`.
Plans stored in `tasks/plans/IMPL-FT-<NNN>.md`.
