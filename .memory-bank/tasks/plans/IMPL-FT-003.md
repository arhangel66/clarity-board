---
description: Implementation plan for FT-003 interactive onboarding tour.
status: active
---
# IMPL-FT-003

## Goal
Replace the current tooltip-only onboarding with a repeatable interactive tour that guides the first real session.

## Steps
- Audit the existing onboarding store, tooltip overlay, and mobile drawer entry points.
- Define a small tour state model: step progression, completion persistence, and repeat/reset action.
- Implement interactive steps around question entry, card creation, connections, and blind-spot guidance.
- Add regression coverage for persistence and the repeat-tutorial affordance.
- Replace the first-run `connections` milestone with a simpler visible `move a card` action.
- Make onboarding overlays freely draggable on pointer and touch input so they do not cover the cards being explained.
- Change `Skip` semantics from "complete the whole tour" to "skip the current step" unless the user explicitly dismisses the walkthrough.

## Expected touched files
- `frontend/src/lib/stores/onboarding.ts`
- `frontend/src/lib/components/TooltipOverlay.svelte`
- `frontend/src/lib/components/HelpOverlay.svelte`
- `frontend/src/lib/components/MobileDrawer.svelte`
- `frontend/src/App.svelte`

## Tests
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`

## Quality gates
- Desktop and mobile flows must both be usable.
- Existing tooltip triggers must not regress for returning users.

## Verify / UAT
- Complete the tour from a fresh session and confirm it stays hidden after completion until manually restarted.
