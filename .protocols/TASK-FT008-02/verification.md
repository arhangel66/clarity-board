# TASK-FT008-02 Verification

## Status
- PASS

## Acceptance / checks
- [x] Revoked and expired-session Auth0 failures resolve to a clear re-login state
- [x] Transient auth failures stay retryable instead of forcing a silent logout
- [x] The auth recovery shell renders helpful localized copy and both recovery actions
- [x] `cd frontend && pnpm test -- --run` passes
- [x] `cd frontend && pnpm check` passes

## Evidence
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/lib/stores/auth.test.ts`
- `frontend/src/lib/components/AuthStateShell.svelte`
- `frontend/src/lib/components/AuthStateShell.test.ts`
- `frontend/src/lib/stores/i18n.ts`
- `.tasks/TASK-FT008-02/verification-2026-03-08.md`

## Verdict
- PASS
