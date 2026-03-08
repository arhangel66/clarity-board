# TASK-FT008-02 Context

## Task
- `TASK-FT008-02`
- Feature: `FT-008 Auth Reliability`
- REQs: `REQ-027`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-008-auth-reliability.md`
- `.memory-bank/tasks/plans/IMPL-FT-008.md`
- `.memory-bank/tasks/backlog.md`
- `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md`
- `.protocols/TASK-FT008-01/{context,plan,progress,verification,handoff}.md`

## Loaded code
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/auth.test.ts`
- `frontend/src/lib/stores/i18n.ts`
- `e2e/tests/auth.spec.ts`

## Scope for this task
- Differentiate revoked-session errors from transient Auth0/network failures.
- Tighten the auth recovery shell copy and make it directly testable.
- Add deterministic coverage for revoked-session init flows and the visible re-login shell.

## Out of scope
- Backend auth changes
- Long-duration reopen E2E beyond the local deterministic harness task
- Deploy or production auth configuration
