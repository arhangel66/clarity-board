# TASK-FT003-02 Context

## Task
- `TASK-FT003-02`
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
- `.protocols/TASK-FT003-01/{context,verification,handoff}.md`

## Loaded code
- `frontend/src/lib/stores/onboarding.ts`
- `frontend/src/lib/components/TooltipOverlay.svelte`
- `frontend/src/lib/components/HelpOverlay.svelte`
- `frontend/src/lib/components/MobileDrawer.svelte`
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/stores/help.ts`
- `frontend/src/lib/stores/drawer.ts`

## Scope for this task
- Tighten onboarding progression so steps advance only after the expected user-facing milestones are met.
- Add repeat-tutorial entry points to both the desktop help popover and the mobile drawer.
- Improve the tooltip copy/states so the walkthrough asks users to act, not just dismiss tips.

## Out of scope
- E2E persistence coverage (`TASK-FT003-03`)
- Broader mobile UX redesign outside the tutorial affordance
- Backend or deploy work
