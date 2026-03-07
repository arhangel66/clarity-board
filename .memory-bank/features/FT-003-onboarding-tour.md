---
description: Feature brief for the interactive onboarding tour.
id: FT-003
title: Interactive Onboarding Tour
status: draft
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
- [ ] Tour state persisted (don't show again after completion)
- [ ] Works on desktop and mobile
- [ ] Existing onboarding overlay replaced or integrated

## Touched files (expected)
- `frontend/src/lib/components/OnboardingOverlay.svelte` (rewrite)
- `frontend/src/lib/stores/onboarding.ts` (extend)
- `frontend/src/lib/components/` (new tour step components)
