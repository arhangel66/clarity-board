---
description: Feature brief for the interactive onboarding tour.
id: FT-003
title: Interactive Onboarding Tour
status: done
epic: EP-002
reqs: [REQ-022]
depends: []
---
# FT-003: Interactive Onboarding Tour

## Goal
New users complete their first meaningful session without confusion. Replace/expand existing onboarding overlay with a step-by-step interactive tour.

## Acceptance criteria
- [x] Step-by-step tour: problem -> cards -> connections -> blind spots
- [x] Interactive (user performs actions, not just reads tips)
- [x] "Repeat tutorial" button accessible from UI (e.g. help menu or settings)
- [x] Tour state persisted (don't show again after completion)
- [x] Works on desktop and mobile
- [x] Existing onboarding overlay replaced or integrated

## Current verified progress
- `TASK-FT003-01` replaced the tooltip-only memory with an ordered onboarding step model keyed by board/session state.
- The app now tracks `question`, `cards`, `connections`, and `blind_spots` progression in `frontend/src/lib/stores/onboarding.ts`.
- Deterministic regression coverage in `frontend/src/lib/stores/onboarding.test.ts` verifies persistence, restart behavior, and legacy-storage migration.
- `TASK-FT003-02` tightened the progression gates so steps stay visible until the user reaches the required milestone, added action-oriented overlay states, and exposed restart controls in both the desktop help popover and the mobile drawer.
- Deterministic UI coverage now locks the walkthrough surfaces in `frontend/src/lib/components/TooltipOverlay.test.ts`, `frontend/src/lib/components/HelpOverlay.test.ts`, and `frontend/src/lib/components/MobileDrawer.test.ts`.
- `TASK-FT003-03` adds Playwright coverage for completing the tour, reloading the app, and explicitly restarting it from help on an isolated test stack.

## Open follow-up
- None for the repo-local onboarding scope; FT-003 is now verified through unit, component, and targeted Playwright coverage.

## Touched files (expected)
- `frontend/src/lib/components/OnboardingOverlay.svelte` (rewrite)
- `frontend/src/lib/stores/onboarding.ts` (extend)
- `frontend/src/lib/components/` (new tour step components)
