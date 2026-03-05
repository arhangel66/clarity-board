# ADR-0002: WebSocket Contract Versioning Policy

- Status: Accepted
- Date: 2026-03-05
- Deciders: project maintainers

## Context

Frontend and backend evolve independently and communicate via websocket events. Uncoordinated breaking payload changes can silently break runtime behavior.

## Decision

Adopt major-version compatibility policy for websocket contract.

- Current major version: 1.
- Non-breaking changes: optional fields and additive message types.
- Breaking changes: required field changes/removals or semantic changes to existing required fields.

Contract source of truth is `docs/architecture/WEBSOCKET_CONTRACT.md`.

## Consequences

### Positive

- Predictable protocol evolution.
- Clear trigger for migration notes and compatibility tests.

### Negative

- Slight overhead for documenting each protocol change.

## Alternatives Considered

- No explicit versioning (implicit compatibility).
- Tight lockstep frontend/backend releases.
