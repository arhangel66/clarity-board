# TASK-FT003-03 Plan

## Goal
Lock the onboarding tour's completion persistence with an end-to-end test that finishes the flow, reloads the app, and confirms the tutorial returns only after an explicit restart.

## Steps
1. Create the task protocol bundle and promote `TASK-FT003-03` to `in_progress`.
2. Align the e2e setup helper with the current onboarding persistence contract instead of the legacy one-shot key.
3. Add a Playwright onboarding regression that completes the guided flow on a fresh board, reloads, and restarts it from help.
4. Run the targeted frontend and e2e gates, then verify and sync Memory Bank if the slice passes.

## Expected touched files
- `.protocols/TASK-FT003-03/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT003-03/*`
- `.memory-bank/tasks/backlog.md`
- `backend/app/construct.py`
- `playwright.config.ts`
- `frontend/src/lib/stores/onboarding.ts`
- `e2e/tests/full-flow.spec.ts`

## Gates
- `cd frontend && env NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
- `pnpm exec playwright test --grep onboarding`
