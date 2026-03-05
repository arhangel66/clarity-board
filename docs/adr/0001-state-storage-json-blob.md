# ADR-0001: State Storage as SQLite JSON Blob

- Status: Accepted
- Date: 2026-03-05
- Deciders: project maintainers

## Context

The application evolves session state quickly (cards, connections, locale, phase, special-question metadata). Frequent schema changes are expected during product discovery.

## Decision

Persist the full session as a JSON blob (`state_json`) in SQLite `sessions` table, with minimal indexed metadata (`id`, `user_id`, `title`, timestamps).

## Consequences

### Positive

- Low friction for state evolution.
- Faster iteration without frequent relational migrations.
- Full session can be atomically persisted/reloaded.

### Negative

- Harder analytics queries directly in SQL.
- Requires careful app-level validation for state integrity.

## Alternatives Considered

- Fully normalized relational schema.
- Hybrid schema with selected denormalized JSON fields.
