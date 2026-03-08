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

### W1: Foundation (analytics + reliability + landing)
Priority: ship instrumentation, quality, and the front door.

| # | Feature | Epic | Priority | Status |
|---|---|---|---|---|
| 1 | FT-002 Analytics & Event Tracking | EP-001 | P1 | done |
| 2 | FT-006 AI Output Validation | EP-003 | P1 | done |
| 3 | FT-001 Landing Page Redesign | EP-001 | P1 | in_progress |
| 4 | FT-008 Auth Reliability | EP-003 | P1 | planned |
| 5 | FT-012 Session Access & Limits | EP-004 | P1 | planned |

### W2: Core value (UX + methodology)
Priority: deliver the product value.

| # | Feature | Epic | Priority | Status |
|---|---|---|---|---|
| 6 | FT-003 Interactive Onboarding Tour | EP-002 | P1 | planned |
| 7 | FT-004 Decision Memo Export | EP-002 | P1 | planned |
| 8 | FT-005 Blind Spot Analysis | EP-002 | P1 | planned |
| 9 | FT-007 TODO Cards Panel | EP-002 | P1 | planned |
| 10 | FT-010 Special Questions Rewrite | EP-003 | P1 | planned |
| 11 | FT-013 Pricing & Upgrade UI + Intent Tracking | EP-004 | P1 | planned |

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
| T-001 | Yandex Metrica counter ID set to 107194444 | P1 | done |

## Task generation
Tasks are generated per-feature using `/prd-to-tasks FT-<NNN>`.
Plans stored in `tasks/plans/IMPL-FT-<NNN>.md`.
