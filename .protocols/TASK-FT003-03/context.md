# TASK-FT003-03 Context

## Task
- `TASK-FT003-03`
- Feature: `FT-003 Interactive Onboarding Tour`
- REQs: `REQ-022`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-003-onboarding-tour.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/plans/IMPL-FT-003.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/commands/{autonomous,execute,verify,mb-sync}.md`
- `.memory-bank/workflows/{autonomy-policy,execute-loop,mb-sync}.md`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.protocols/TASK-FT003-02/{verification,handoff}.md`

## Loaded code
- `frontend/src/lib/stores/onboarding.ts`
- `e2e/tests/full-flow.spec.ts`
- `e2e/fixtures/auth.fixture.ts`
- `e2e/pages/{canvas,input-bar,sidebar}.page.ts`
- `backend/app/construct.py`
- `playwright.config.ts`
- `frontend/src/lib/components/TooltipOverlay.svelte`
- `frontend/src/lib/components/HelpOverlay.svelte`

## Scope for this task
- Add deterministic Playwright coverage for completing the onboarding flow on a fresh board.
- Verify the finished tour stays hidden after a reload.
- Verify the user can re-open it only by explicitly restarting from the help surface.

## Out of scope
- More onboarding copy/UI redesign beyond the already verified walkthrough surfaces
- Backend/session model changes outside what the existing dev harness already provides
- Mobile-specific E2E coverage
