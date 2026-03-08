# TASK-FT003-02 Plan

## Goal
Turn the onboarding state model into a real guided walkthrough by gating progression on visible user milestones and exposing restart controls on both desktop and mobile surfaces.

## Steps
1. Create the task protocol bundle and promote `TASK-FT003-02` to `in_progress`.
2. Tighten onboarding progression so each step stays active until its expected milestone is reached.
3. Update the tooltip overlay to show action-oriented progress states instead of plain dismissible copy.
4. Add repeat-tutorial controls to `HelpOverlay.svelte` and `MobileDrawer.svelte`.
5. Add deterministic regression coverage for gated progression and the restart UI surfaces.
6. Run frontend gates, then verify and sync Memory Bank state if the slice passes.

## Expected touched files
- `.protocols/TASK-FT003-02/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT003-02/*`
- `.memory-bank/tasks/backlog.md`
- `frontend/src/lib/stores/onboarding.ts`
- `frontend/src/lib/components/TooltipOverlay.svelte`
- `frontend/src/lib/components/HelpOverlay.svelte`
- `frontend/src/lib/components/MobileDrawer.svelte`
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/**/*.test.ts`

## Gates
- `cd frontend && env NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`
