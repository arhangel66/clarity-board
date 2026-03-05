# Architecture Plan

## Scope

This document is the execution plan for architecture work. It complements:

- `ARCHITECTURE.md` (high-level)
- `backend/docs/ARCHITECTURE_DEEP.md` (deep dive)

As of 2026-03-05, this plan is the working source for architecture sequencing.

## Current Baseline (from code)

Backend runtime is centered around:

- `backend/app/main.py`: FastAPI + WebSocket transport layer
- `backend/app/services/main_service.py`: orchestration/business flow per connection
- `backend/app/services/state_service.py`: persistence of session state (SQLite JSON blob)
- `backend/app/services/ai_service.py`: LLM integration
- `backend/app/services/special_questions.py`: locale-aware question bank
- `backend/app/construct.py`: DI wiring + env setup + service instances

Key baseline notes:

- Session data is persisted in SQLite under backend `data/fact_cards.db` via `StateService`.
- Deployment currently follows the skill at `/Users/mikhail/w/learning/fact/.claude/skills/deploy`.
- Existing architecture docs still contain references to older modules (`database.py`, `card_service.py`, `embedding_service.py`).

## Problems To Solve

- Architecture docs are not aligned with current code paths.
- Module boundaries are implicit, not documented and not enforced.
- WebSocket contract evolution policy is not formalized.
- Migration and backup strategy is under-specified.
- Observability and operational diagnostics are minimal.

## Target Architecture Shape

- `transport`: FastAPI routes and WebSocket handlers in `main.py`
- `orchestration`: stateful flow logic in `MainService`
- `domain`: models/rules in `models.py` + pure domain helpers
- `persistence`: `StateService` + migrations + backup/restore
- `integrations`: AI provider clients and external auth dependencies

## Milestones

## A1. Documentation Sync (P0)

- Update `ARCHITECTURE.md` to reflect the current service graph.
- Update `backend/docs/ARCHITECTURE_DEEP.md` call graph and file map.
- Add canonical diagrams for message flow and persistence flow.

DoD:

- A new engineer can map request flow from client event to DB write using docs only.
- No references to removed backend modules remain in architecture docs.

## A2. Module Boundaries (P0)

- Document service responsibilities and forbidden dependencies.
- Define interfaces between transport/orchestration/persistence/integrations.
- Add lightweight checks (lint/test or review checklist) for dependency direction.

DoD:

- Dependency direction is explicit and reviewed in PRs.
- New features can be placed without architecture ambiguity.

## A3. WebSocket Contract Governance (P0)

- Add message schema versioning policy.
- Define backward-compatibility rules.
- Document error envelope and required fields for all message types.

DoD:

- Contract changes include version notes and compatibility statement.
- CI has contract-level test(s) for at least one old/new message compatibility scenario.

## A4. Persistence Reliability (P0)

- Replace ad-hoc migration approach with managed migration flow.
- Add backup and restore scripts for SQLite database.
- Add runbook for restore verification.

DoD:

- Restore drill succeeds on a clean environment.
- Schema changes are versioned and reproducible.

## A5. Observability Baseline (P1)

- Introduce structured logs for critical events.
- Define minimal operational metrics (session start/end, ws errors, auth failures).
- Add a documented debug checklist for incidents.

DoD:

- For top incident classes, there is a deterministic troubleshooting path.

## A6. ADR Discipline (P1)

- Add `docs/adr/` with numbered ADRs.
- Start with ADRs for storage model, websocket contract strategy, AI provider strategy.

DoD:

- Architecture-impacting changes link to ADR IDs.

## Execution Queue

- [x] A1.1 Update high-level architecture document
- [x] A1.2 Update deep architecture document
- [x] A1.3 Add transport->orchestration->persistence sequence diagram
- [x] A2.1 Document module boundaries
- [x] A3.1 Version websocket contract
- [x] A4.1 Migration pipeline
- [x] A4.2 Backup/restore scripts and runbook
- [ ] A5.1 Structured logs and metrics baseline
- [x] A6.1 ADR templates and initial ADR set
