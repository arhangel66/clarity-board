---
description: Implementation plan for FT-008 auth reliability.
status: active
---
# IMPL-FT-008

## Goal
Reduce auth-related drop-off by hardening refresh-token behavior, user-facing fallback states, and regression coverage.

## Steps
- Add targeted tests around `frontend/src/lib/stores/auth.ts` for refresh failure, page reload, and redirect handling.
- Preserve or recover auth state cleanly after silent-token refresh failures.
- Add a visible re-login path and friendlier error state in the app shell.
- Extend dev-bypass E2E coverage so refresh and re-open flows are exercised locally.

## Expected touched files
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `e2e/tests/auth.spec.ts`

## Tests
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
- `pnpm e2e -- --grep auth`

## Quality gates
- Auth failures must degrade to a recoverable UI state instead of a broken workspace.

## Verify / UAT
- Confirm login, reload, refresh-token failure fallback, and explicit re-login behavior with the dev bypass and mocked Auth0 client.
