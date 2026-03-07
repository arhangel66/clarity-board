# PRD-BOOTSTRAP Decision Log

## Round 1 (2026-03-07)

### Q1: B1 vs B2 ordering
- **Answer:** Not critical; the PRD phrase "analytics before landing" is misleading
- **Decision:** B2 (Analytics) is still recommended before B1 launch, but not a hard blocker

### Q2: Decision Memo (B4) — scope
- **Answer:** Export only (Markdown download + clipboard). No email/profile storage.
- **Note:** Feature does NOT exist yet — confirmed by codebase search.

### Q3: Pricing model
- **Answer:** Freemium with credits/limits:
  - Every user starts with X free credits
  - Credits consumed on: voice recognition, card creation (AI calls)
  - Subscription increases or removes limits
  - MVP launch: no real payment integration needed
  - BUT: show payment UI (paywall screen) to measure intent (click tracking)
  - Track real usage per user to understand consumption patterns
- **Decision:** Add new roadmap item for pricing/limits infrastructure
- **PRD update needed:** Yes, add pricing section

### Q4: Own domain
- **Answer:** Not yet purchased. Need research + purchase + DNS/SSL setup.
- **Decision:** Include as task in Wave B

### Q5: Onboarding (B3)
- **Answer:** Rework and expand existing overlay into interactive tour
- **Addition:** Add "repeat tutorial" button for easy re-triggering and testing

## Open Questions
- Exact credit amounts (X free credits per user)
- Credit cost per action (voice vs card creation vs AI call)
- Subscription price point
- Domain name candidates (need availability check)
