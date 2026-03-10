---
description: Implementation plan for FT-013 pricing and paywall UI.
status: active
---
# IMPL-FT-013

## Goal
Show consistent pricing and upgrade intent flows on the landing and in-app without introducing real payments yet.

## Steps
- Add frontend access state derived from `FT-012` backend entitlement data.
- Reuse the landing pricing copy and surface the same offer in a paywall modal plus session indicator.
- Track upgrade-intent clicks through the analytics layer from `FT-002`.
- Keep the paywall copy explicit that billing is not yet active if that remains true.
- Reopen the exhausted-access paywall only on entry to the exhausted state or on later blocked actions, not on every reload.
- Reuse the same non-billing explanation pattern from pricing surfaces so landing and in-app monetization copy stay honest.

## Expected touched files
- `frontend/src/lib/components/LandingPage.svelte`
- `frontend/src/lib/components/PaywallModal.svelte`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/stores/access.ts`
- `frontend/src/lib/analytics.ts`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/App.svelte`

## Tests
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`

## Quality gates
- Pricing copy must stay consistent across landing and app UI.

## Verify / UAT
- Exhaust the free-session state locally and confirm the upgrade flow, messaging, and analytics event.
