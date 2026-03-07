---
id: FT-013
title: Pricing & Upgrade UI + Intent Tracking
status: draft
epic: EP-004
reqs: [REQ-032]
depends: [FT-012, FT-002]
---
# FT-013: Pricing & Upgrade UI + Intent Tracking

## Goal
Show pricing/upgrade UI on the landing and in-app when free sessions are exhausted. No real payment initially — measure intent via click tracking.

## Acceptance criteria
- [ ] Landing pricing section shows the public offer: 3 free sessions, $10/month unlimited, $100 lifetime
- [ ] Paywall modal shown when user exhausts free sessions without a paid plan
- [ ] Pricing tiers are displayed consistently across landing and in-app upgrade UI
- [ ] "Upgrade" button click tracked as analytics event (FT-002)
- [ ] No real payment processor integration
- [ ] Session access indicator visible in app UI (header or sidebar)
- [ ] Friendly messaging ("You've used your 3 free sessions — upgrade to continue")

## Touched files (expected)
- `frontend/src/lib/components/PaywallModal.svelte` (new)
- `frontend/src/lib/stores/access.ts` (new — access/pricing state)
- `frontend/src/lib/components/LandingPage.svelte` (pricing section)
- `frontend/src/lib/components/` (session access indicator)
- `frontend/src/lib/analytics.ts` (upgrade_clicked event)
