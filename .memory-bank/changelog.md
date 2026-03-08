---
description: Memory Bank changelog.
status: active
---
# Changelog

## [2026-03-08] FT-002: analytics verification and MB sync
- Added `frontend/src/lib/analytics.test.ts` to verify Yandex goal helper calls and payloads
- Added `session_exported` tracking in `frontend/src/lib/components/BoardsSidebar.svelte` and `frontend/src/lib/components/SelectionToolbar.svelte`
- Verified FT-002 with `pytest tests/test_event_service.py -v`, `pnpm test -- --run`, `pnpm check`, and `pnpm build`
- Synced `.protocols/FT-002/*`, marked `REQ-021` and the W1 backlog item as `done`, and attached evidence in `.tasks/FT-002/verification-2026-03-08.md`

## [2026-03-07] Garden sync: routers, statuses, and architecture drift
- Added missing routers: `.memory-bank/epics/index.md` and `.memory-bank/features/index.md`
- Added required `description:` frontmatter coverage to EP/FT docs
- Synced `.memory-bank/testing/index.md` with the current test inventory: 57 backend tests in 9 files, 7 frontend tests in 4 files, 13 Playwright tests in 4 files
- Updated architecture docs to reflect `EventService`, `validator.py`, JSONL analytics logging, and the current frontend store layout
- Corrected lifecycle drift for `EP-001`, `FT-002`, `REQ-020`, `REQ-021`, and the backlog entry for FT-002
- Refreshed `.memory-bank/skills/index.md` to match the local `.agents/skills/` registry

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
