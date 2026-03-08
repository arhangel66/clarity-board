---
description: Implementation plan for FT-005 blind-spot analysis.
status: active
---
# IMPL-FT-005

## Goal
Surface gaps, isolated cards, and missing relationships so the canvas exposes blind spots instead of just storing facts.

## Steps
- Define when blind-spot analysis should trigger and what payload it returns.
- Add backend logic for gap prompts, isolated-card detection, and link suggestions.
- Add lightweight frontend rendering for empty-zone hints and isolated-card emphasis.
- Ensure the hints feel advisory rather than noisy.

## Expected touched files
- `backend/app/services/ai_service.py`
- `backend/app/services/main_service.py`
- `frontend/src/lib/components/Canvas.svelte`
- `frontend/src/lib/components/Card.svelte`
- `frontend/src/lib/stores/cards.ts`

## Tests
- `cd backend && uv run pytest -v`
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`

## Quality gates
- Blind-spot hints must not break normal card drag/edit interactions.

## Verify / UAT
- Load a session with disconnected clusters and verify the app surfaces missing links and sparse zones.
