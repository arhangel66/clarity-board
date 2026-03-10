---
description: Feature brief for the landing page redesign.
id: FT-001
title: Landing Page Redesign
status: in_progress
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
- [ ] Trust signals: privacy, no credit card to start, 3 free sessions
- [ ] Dedicated pricing section with honest public offer (3 free sessions total, $10/month unlimited, $100 lifetime)
- [ ] FAQ section addressing key objections
- [ ] No fake metrics (remove "10,000+ sessions" or replace with honest data)
- [ ] Social proof section (real testimonials — can be empty initially, structure ready)
- [ ] Mobile-responsive
- [ ] Yandex Metrica tracking active before launch (depends on FT-002)

## Status note (2026-03-10)
- `TASK-FT001-03` completed the repo-local landing polish pass for label contrast, kicker treatment, mobile wrapping, and featured pricing-card balance.
- Verification evidence lives in [.tasks/TASK-FT001-03/verification-2026-03-10.md](../../.tasks/TASK-FT001-03/verification-2026-03-10.md) plus the captured desktop/mobile screenshots in the same folder.
- `TASK-FT001-04` aligned landing pricing clicks with the in-app upgrade preview: every pricing card now uses informational `Start free` framing, still tracks intent, and shows explicit `payment is not live yet` guidance before sign-in.

## Open follow-up (2026-03-10 discuss)
- See [.protocols/DISCUSS-UX-POLISH-20260310/decision-log.md](../../.protocols/DISCUSS-UX-POLISH-20260310/decision-log.md): cross-feature UX polish decision log for landing, access, and onboarding.
- Resolved in `TASK-FT001-03`: stronger nav/section-label contrast, a shorter neutral kicker treatment (`Fact Cards` wordmark + compact supporting label), and a warm light featured-pricing highlight verified on desktop/mobile.
- Resolved in `TASK-FT001-04`: landing pricing CTAs now reuse the same explicit non-billing preview pattern as `FT-013` instead of pretending monthly/lifetime checkout already works.

## Reference
- https://lk.brain-games.ru/fc — structure and selling approach patterns

## Touched files (expected)
- `frontend/src/lib/components/LandingPage.svelte` (rewrite)
- `frontend/src/lib/stores/i18n.ts` (landing copy ru/en)
