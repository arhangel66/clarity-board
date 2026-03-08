---
description: Implementation plan for FT-015 mobile UX improvements.
status: active
---
# IMPL-FT-015

## Goal
Move from merely responsive mobile support to a deliberate mobile interaction model.

## Steps
- Decide the mobile mode boundary: chat-first assistance, simplified canvas, or hybrid.
- Implement the highest-value touch improvements for card creation, drag, and navigation.
- Add device-focused QA for narrow screens and real browsers.

## Expected touched files
- `frontend/src/App.svelte`
- `frontend/src/lib/components/MobileDrawer.svelte`
- `frontend/src/lib/components/Canvas.svelte`
- `frontend/src/lib/components/Card.svelte`
- `frontend/src/lib/stores/mobile.ts`

## Tests
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
- `pnpm e2e -- --grep mobile`

## Quality gates
- No critical workflow regressions below `768px`.

## Verify / UAT
- Exercise the core session flow on iOS Safari and Android Chrome viewports.
