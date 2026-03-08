---
description: Feature brief for pricing, paywall UI, and intent tracking.
id: FT-013
title: Pricing & Upgrade UI + Intent Tracking
status: done
epic: EP-004
reqs: [REQ-032]
depends: [FT-012, FT-002]
---
# FT-013: Pricing & Upgrade UI + Intent Tracking

## Goal
Show pricing/upgrade UI on the landing and in-app when free sessions are exhausted. No real payment initially — measure intent via click tracking.

## Acceptance criteria
- [x] Landing pricing section shows the public offer: 3 free sessions, $10/month unlimited, $100 lifetime
- [x] Paywall modal shown when user exhausts free sessions without a paid plan
- [x] Pricing tiers are displayed consistently across landing and in-app upgrade UI
- [x] "Upgrade" button click tracked as analytics event (FT-002)
- [x] No real payment processor integration
- [x] Session access indicator visible in app UI (header or sidebar)
- [x] Friendly messaging ("You've used your 3 free sessions — upgrade to continue")

## Current verified progress
- `TASK-FT013-01` is complete locally via verify-and-sync.
- `TASK-FT013-02` added `frontend/src/lib/components/PaywallModal.svelte` and mounted it in `frontend/src/App.svelte` for exhausted starter access.
- The paywall reuses `strings.landing.pricing.plans`, so the landing and in-app offers stay aligned.
- `TASK-FT013-03` added analytics-only `upgrade_clicked` tracking with stable plan IDs and no checkout redirect.
- Deterministic coverage now exists in `frontend/src/lib/stores/access.test.ts`, `frontend/src/lib/components/BoardsSidebar.test.ts`, `frontend/src/lib/components/PaywallModal.test.ts`, and `frontend/src/lib/analytics.test.ts`.

## Touched files (expected)
- `frontend/src/lib/components/PaywallModal.svelte` (new)
- `frontend/src/lib/stores/access.ts` (access/pricing state)
- `frontend/src/lib/components/LandingPage.svelte` (pricing section)
- `frontend/src/lib/components/` (session access indicator)
- `frontend/src/lib/analytics.ts` (upgrade_clicked event)
- `frontend/src/App.svelte` (authenticated paywall mount point)
