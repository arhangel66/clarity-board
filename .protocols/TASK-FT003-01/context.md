# TASK-FT003-01 Context

## Task
- `TASK-FT003-01`
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

## Loaded code
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/onboarding.ts`
- `frontend/src/lib/components/TooltipOverlay.svelte`
- `frontend/src/lib/components/HelpOverlay.svelte`
- `frontend/src/lib/components/MobileDrawer.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/stores/session.ts`
- `frontend/src/App.test.ts`

## Scope for this task
- Replace the one-shot tooltip storage with a persistent onboarding step model.
- Keep the current app triggers working while enforcing a stable step order.
- Add deterministic regression coverage for completion persistence and restart/reset behavior.

## Out of scope
- Full mobile/desktop tour walkthrough polish
- E2E onboarding coverage
- Reworking unrelated help or drawer UX beyond the minimum needed for restart plumbing
- Backend or deploy work
