---
description: Memory Bank changelog.
status: active
---
# Changelog

## [2026-03-07] FT-001: landing pricing and session-based messaging
- Updated `frontend/src/lib/stores/i18n.ts` to remove “free forever” messaging in RU/EN
- Added landing pricing copy for `3 free sessions total`, `$10/month unlimited`, and `$100 lifetime`
- Updated `frontend/src/lib/components/LandingPage.svelte` with:
  - desktop anchor nav (`How it works` / `Pricing` / `FAQ`)
  - localized mockup labels in RU/EN
  - dedicated pricing section with three plans
  - trust and FAQ copy aligned to the sessions-based offer
- Verified locally with `pnpm check`, `pnpm build`, `pnpm test -- --run`, plus desktop/mobile preview smoke-check

## [2026-03-07] Docs: pricing model clarified for landing and monetization
- Recorded FT-001 pricing discussion in `.protocols/FT-001/decision-log.md`
- Updated Memory Bank from a `credits` framing to a `sessions + plans` framing
- Fixed free-tier definition to `3 free sessions total` (not monthly)
- Set public pricing direction to `$10/month unlimited` and `$100 lifetime`
- Added landing pricing section expectation to `FT-001`

## [2026-03-07] Garden sync: testing docs and RTM
- Updated `.memory-bank/testing/index.md` with verified test counts (57 backend, 7 frontend, 13 e2e listed)
- Fixed RTM drift in `.memory-bank/requirements.md` for `REQ-025` / `FT-006`
- Rechecked `.memory-bank/guides/dev-setup.md` against the current local setup and Docker caveats

## [2026-03-07] Docs: README and dev setup sync
- Rewrote `README.md` to match the current product name, stack, local startup flow, and quality gates
- Clarified that `docker-compose.yml` is deployment-oriented and does not publish localhost ports by default
- Updated `.memory-bank/guides/dev-setup.md` with the same local-run guidance and current env caveats

## [2026-03-07] T-001: Yandex Metrica counter ID
- Set real counter ID `107194444` in `frontend/index.html` and `frontend/src/lib/analytics.ts`
- Analytics tracking is now active in production

## [2026-03-07] FT-006: AI Output Validation (REQ-025)
- Added `backend/app/services/validator.py` — validation layer for AI-generated operations
- Duplicate card detection (SequenceMatcher, 80% threshold)
- Coordinate bounds re-validation (defense-in-depth after decoder)
- Text length enforcement (50 chars regular, 100 chars question)
- Root card protection (delete always blocked, update only in Phase 1)
- Invalid card_id reference detection
- Structured validation failure logging
- Integrated into `MainService.process_user_message` between decode and apply
- 16 new unit tests in `backend/tests/test_validator.py`
- All 57 backend tests pass

## [2026-03-06] Initial setup (cold-start, brownfield)
- Created Memory Bank skeleton
- Ran 5 parallel scan subagents (build, backend, frontend, data, tests)
- Synthesized: product.md, architecture/overview.md, architecture/frontend.md
- Created: guides/dev-setup.md, contracts/websocket-protocol.md
- Updated: testing/index.md with quality gates and known gaps
- Updated AGENTS.md as agent-facing project map
- Scan artifacts in .tasks/TASK-MB-MAP/
