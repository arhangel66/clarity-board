---
id: FT-001
title: Landing Page Redesign
status: draft
epic: EP-001
reqs: [REQ-020]
depends: [FT-002]
---
# FT-001: Landing Page Redesign

## Goal
Problem-first landing page that converts visitors to sign-ups at >= 5% rate.

## Acceptance criteria
- [ ] Hero section leads with pain, not features ("Mistakes cost dearly", "Thoughts racing")
- [ ] 6 audience segments with specific use cases
- [ ] Before/After transformation section (fog -> clarity)
- [ ] Process visualization (animated or interactive session demo)
- [ ] Trust signals: privacy, no credit card, free sessions
- [ ] FAQ section addressing key objections
- [ ] No fake metrics (remove "10,000+ sessions" or replace with honest data)
- [ ] Social proof section (real testimonials — can be empty initially, structure ready)
- [ ] Mobile-responsive
- [ ] Yandex Metrica tracking active before launch (depends on FT-002)

## Reference
- https://lk.brain-games.ru/fc — structure and selling approach patterns

## Touched files (expected)
- `frontend/src/lib/components/LandingPage.svelte` (rewrite)
- `frontend/src/lib/stores/i18n.ts` (landing copy ru/en)
