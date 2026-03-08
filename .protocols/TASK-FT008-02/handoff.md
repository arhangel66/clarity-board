# TASK-FT008-02 Handoff

## Summary
- `frontend/src/lib/stores/auth.ts` now distinguishes interactive re-login failures (`login_required`, `missing_refresh_token`, `invalid_grant`, related Auth0 recovery codes) from transient auth failures.
- `frontend/src/lib/components/AuthStateShell.svelte` owns the user-facing auth recovery shell so the copy and actions are testable in isolation.
- `frontend/src/lib/stores/auth.test.ts` covers revoked-session init, retryable transient failures, and later refresh failure handling.
- `frontend/src/lib/components/AuthStateShell.test.ts` verifies the localized recovery copy plus retry and re-login actions.

## Follow-ups
- `TASK-FT008-03`: extend Playwright auth coverage for reopen/refresh flows with the dev-bypass harness
