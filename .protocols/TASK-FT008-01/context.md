# TASK-FT008-01 Context

## Task
- `TASK-FT008-01`
- Feature: `FT-008 Auth Reliability`
- REQs: `REQ-027`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-008-auth-reliability.md`
- `.memory-bank/tasks/plans/IMPL-FT-008.md`
- `.memory-bank/tasks/backlog.md`
- `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md`
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-01-final-report-docs-01.md`
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-02-final-report-docs-01.md`
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-03-final-report-docs-01.md`
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-04-final-report-docs-01.md`
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-05-final-report-docs-01.md`

## Loaded code
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/App.svelte`
- `frontend/src/App.test.ts`
- `frontend/src/lib/analytics.test.ts`
- `frontend/src/lib/stores/cards.test.ts`
- `e2e/tests/auth.spec.ts`

## Scope for this task
- Add deterministic frontend coverage for auth-store init and refresh-failure states.
- Improve the app-shell auth fallback so failures are recoverable instead of a dead-end message.

## Out of scope
- Full Auth0 integration work
- Backend auth changes
- Long-duration reopen e2e and deploy work (covered by later FT-008 tasks)
