# TASK-FT008-02 Plan

## Goal
Cover the remaining local auth edge cases so page reloads and revoked sessions lead to a clear re-login path instead of a generic failure state.

## Steps
1. Refine `frontend/src/lib/stores/auth.ts` so revoked/expired-session failures map to `session_expired` while transient issues stay retryable.
2. Extract or isolate the auth error shell so the copy and actions can be tested directly.
3. Add deterministic tests for revoked-session init behavior, transient auth failure behavior, and the visible auth recovery shell.
4. Run the frontend task gates and store verification evidence.

## Expected touched files
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/auth.test.ts`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/components/AuthStateShell.svelte`
- `frontend/src/lib/components/AuthStateShell.test.ts`

## Gates
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
