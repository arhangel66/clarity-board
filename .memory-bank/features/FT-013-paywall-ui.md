---
id: FT-013
title: Paywall UI & Intent Tracking
status: draft
epic: EP-004
reqs: [REQ-032]
depends: [FT-012, FT-002]
---
# FT-013: Paywall UI & Intent Tracking

## Goal
Show pricing/upgrade screen when credits exhausted. No real payment — measure intent via click tracking.

## Acceptance criteria
- [ ] Paywall modal shown when user hits credit limit
- [ ] Pricing tiers displayed (free vs subscription comparison)
- [ ] "Upgrade" button click tracked as analytics event (FT-002)
- [ ] No real payment processor integration
- [ ] Credit balance indicator visible in app UI (header or sidebar)
- [ ] Friendly messaging ("You've used your free sessions — upgrade to continue")

## Touched files (expected)
- `frontend/src/lib/components/PaywallModal.svelte` (new)
- `frontend/src/lib/stores/credits.ts` (new — credit state)
- `frontend/src/lib/components/` (credit balance indicator)
- `frontend/src/lib/analytics.ts` (upgrade_clicked event)
