# Module Boundaries

Last updated: 2026-03-05

This document defines ownership and dependency direction for backend modules.

## Layers

- `transport`: HTTP/WebSocket endpoint handling (`backend/app/main.py`)
- `orchestration`: session flow and use-case logic (`backend/app/services/main_service.py`)
- `domain`: models/enums/validation rules (`backend/app/models.py`, decoder contracts)
- `persistence`: state storage (`backend/app/services/state_service.py`)
- `integrations`: external services (AI provider, auth provider, special question source)

## Allowed Dependency Direction

`transport` -> `orchestration` -> (`domain`, `persistence`, `integrations`)

`domain` must not depend on `transport`, `persistence`, or `integrations`.

`persistence` must not depend on `transport` or external AI/Auth integrations.

## Ownership Matrix

- `main.py` owns protocol endpoints, auth gate wiring, and response routing.
- `MainService` owns business workflow, mutation orchestration, and phase transitions.
- `StateService` owns DB schema compatibility and full-state persistence.
- `AIService` owns prompt construction and LLM invocation.
- `decoder.py` owns conversion from raw AI JSON to trusted operations.

## Forbidden Patterns

- No direct DB calls from `main.py` request handlers.
- No LLM calls from transport handlers.
- No persistence logic in UI-facing websocket handlers.
- No cross-layer imports that invert dependency direction.

## Change Checklist (for PR review)

- Does the change keep dependency direction intact?
- Is business logic in `MainService` (not in transport)?
- Are state mutations persisted through `StateService`?
- If protocol changed, is `docs/architecture/WEBSOCKET_CONTRACT.md` updated?
- If architecture changed, is an ADR added/updated under `docs/adr/`?
