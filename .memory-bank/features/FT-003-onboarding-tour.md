---
description: Feature brief for the interactive onboarding tour.
id: FT-003
title: Interactive Onboarding Tour
status: in_progress
epic: EP-002
reqs: [REQ-022]
depends: []
---
# FT-003: Interactive Onboarding Tour

## Goal
New users complete their first meaningful session without confusion. Replace/expand existing onboarding overlay with a step-by-step interactive tour.

## Acceptance criteria
- [ ] Step-by-step tour: problem -> cards -> connections -> blind spots
- [ ] Interactive (user performs actions, not just reads tips)
- [ ] "Repeat tutorial" button accessible from UI (e.g. help menu or settings)
- [x] Tour state persisted (don't show again after completion)
- [ ] Works on desktop and mobile
- [ ] Existing onboarding overlay replaced or integrated

## Current verified progress
- `TASK-FT003-01` replaced the tooltip-only memory with an ordered onboarding step model keyed by board/session state.
- The app now tracks `question`, `cards`, `connections`, and `blind_spots` progression in `frontend/src/lib/stores/onboarding.ts`.
- Deterministic regression coverage in `frontend/src/lib/stores/onboarding.test.ts` verifies persistence, restart behavior, and legacy-storage migration.

## Open follow-up
- `TASK-FT003-02` still needs the richer repeat-tutorial UI surface and the more guided desktop/mobile walkthrough.

## Touched files (expected)
- `frontend/src/lib/components/OnboardingOverlay.svelte` (rewrite)
- `frontend/src/lib/stores/onboarding.ts` (extend)
- `frontend/src/lib/components/` (new tour step components)
