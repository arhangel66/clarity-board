# TASK-FT008-01 Plan

## Goal
Make auth init failures testable and user-recoverable without expanding beyond the first FT-008 foundation task.

## Steps
1. Refactor `frontend/src/lib/stores/auth.ts` just enough to support deterministic mocking in Vitest.
2. Add unit tests for dev bypass, missing config, redirect callback handling, and silent-token refresh failure.
3. Replace the plain auth error shell in `frontend/src/App.svelte` with a recoverable state that offers a re-login action.
4. Run frontend quality gates for the touched area.

## Expected touched files
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/App.svelte`
- `frontend/src/App.test.ts`
- `frontend/src/lib/stores/auth.test.ts`
- `frontend/src/lib/stores/i18n.ts`

## Gates
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
