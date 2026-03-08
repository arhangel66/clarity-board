# TASK-FT003-01 Plan

## Goal
Create the first reusable onboarding-tour slice: ordered step state, persistence, and repeat/reset primitives that later UI tasks can build on safely.

## Steps
1. Promote `TASK-FT003-01` to `in_progress` and create the task protocol bundle.
2. Refactor the onboarding store from ad hoc seen-tooltips state into ordered onboarding steps with durable completion data.
3. Update the app and tooltip overlay to use the new step model without regressing the existing trigger flow.
4. Add deterministic frontend tests for persistence, ordered progression, and restart behavior.
5. Run frontend gates, then verify and sync the Memory Bank if the slice passes.

## Expected touched files
- `.protocols/TASK-FT003-01/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT003-01/*`
- `.memory-bank/tasks/backlog.md`
- `frontend/src/lib/stores/onboarding.ts`
- `frontend/src/lib/components/TooltipOverlay.svelte`
- `frontend/src/App.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/stores/onboarding.test.ts`

## Gates
- `cd frontend && env NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`
