# TASK-FT008-03 Context

## Task
- `TASK-FT008-03`
- Feature: `FT-008 Auth Reliability`
- REQs: `REQ-027`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-008-auth-reliability.md`
- `.memory-bank/tasks/plans/IMPL-FT-008.md`
- `.memory-bank/tasks/backlog.md`
- `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md`
- `.protocols/TASK-FT008-01/handoff.md`
- `.protocols/TASK-FT008-02/{handoff,verification}.md`

## Loaded code
- `e2e/tests/auth.spec.ts`
- `e2e/fixtures/auth.fixture.ts`
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/App.svelte`

## Scope for this task
- Extend Playwright auth coverage for login, reload, and reopen flows using the local dev-bypass harness.
- Record reproducible E2E evidence under `.tasks/TASK-FT008-03/`.

## Out of scope
- Real Auth0 end-to-end integration
- 24h time-travel or external auth-provider testing
- Backend auth changes or deploy work
