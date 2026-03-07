---
description: Memory Bank changelog.
status: active
---
# Changelog

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
