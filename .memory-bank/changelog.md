---
description: Memory Bank changelog.
status: active
---
# Changelog

## [2026-03-08] FT-003: onboarding completion persistence verified end-to-end
- Added `buildCompletedOnboardingState()` in `frontend/src/lib/stores/onboarding.ts` so tests can seed the current onboarding persistence contract without relying on the legacy one-shot storage key
- Extended `e2e/tests/full-flow.spec.ts` with a targeted onboarding regression that completes the tour, reloads the app, and verifies the tutorial only returns after an explicit help-surface restart
- Updated `backend/app/construct.py` and `playwright.config.ts` so Playwright uses isolated frontend/backend ports plus a clean temp data dir, preventing local dev state from leaking into e2e access/session behavior
- Verified with `cd frontend && env NODE_OPTIONS=--experimental-require-module pnpm test -- --run`, `cd frontend && pnpm check`, and `pnpm exec playwright test --grep onboarding`
- Synced `FT-003`, `REQ-022`, the autonomous backlog (`TASK-FT003-03` done), and the autonomous run terminal state
## [2026-03-08] FT-003: guided walkthrough states and restart surfaces
- Tightened `frontend/src/lib/stores/onboarding.ts` so each onboarding step stays active until the required milestone is actually reached, using connection count and session phase as explicit advancement signals
- Updated `frontend/src/lib/components/TooltipOverlay.svelte` to show action-oriented prompts, waiting/ready states, and disabled primary controls until the current step is satisfied
- Added restart-tutorial surfaces in `frontend/src/lib/components/HelpOverlay.svelte` and `frontend/src/lib/components/MobileDrawer.svelte`, and wired live connection counts from `frontend/src/App.svelte`
- Extended `frontend/src/lib/stores/i18n.ts` with walkthrough action copy and added regression coverage in `frontend/src/lib/components/TooltipOverlay.test.ts`, `frontend/src/lib/components/HelpOverlay.test.ts`, `frontend/src/lib/components/MobileDrawer.test.ts`, and `frontend/src/lib/stores/onboarding.test.ts`
- Verified with `cd frontend && env NODE_OPTIONS=--experimental-require-module pnpm test -- --run`, `cd frontend && pnpm check`, and `cd frontend && pnpm build`
- Synced `FT-003`, `REQ-022`, the autonomous backlog (`TASK-FT003-02` done, `TASK-FT003-03` ready), and the autonomous run terminal state
## [2026-03-08] FT-003: onboarding state model and persistence
- Refactored `frontend/src/lib/stores/onboarding.ts` from one-shot tooltip memory into an ordered onboarding step model keyed by board/session signals
- Updated `frontend/src/App.svelte` and `frontend/src/lib/components/TooltipOverlay.svelte` to drive the onboarding overlay from `question`, `cards`, `connections`, and `blind_spots` progression
- Added deterministic coverage in `frontend/src/lib/stores/onboarding.test.ts` for persistence, restart behavior, and legacy-storage migration
- Verified with `cd frontend && env NODE_OPTIONS=--experimental-require-module pnpm test -- --run`, `cd frontend && pnpm check`, and `cd frontend && pnpm build`
- Synced `FT-003`, `REQ-022`, the autonomous backlog (`TASK-FT003-01` done), and the autonomous run terminal state

## [2026-03-08] FT-010: special-question rewrite and regression locks
- Rewrote `backend/data/questions.json` with 30 original, domain-neutral RU/EN prompts and renamed the visible category labels to `Ракурс / Perspective`, `Структура / Structure`, and `Контекст / Context`
- Extended `backend/app/models.py`, `backend/app/services/special_questions.py`, `backend/app/services/main_service.py`, `frontend/src/lib/types.ts`, and `frontend/src/lib/components/CurrentQuestion.svelte` so pending special questions carry and display a localized `category_label`
- Added regression coverage in `backend/tests/test_special_questions.py` and `frontend/src/lib/components/CurrentQuestion.test.ts`
- Verified with `cd backend && uv run pytest tests/test_special_questions.py -v`, `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run`, `cd frontend && pnpm check`, and `cd frontend && pnpm build`
- Synced `FT-010`, `REQ-029`, the autonomous backlog (`TASK-FT010-01` and `TASK-FT010-02` done), and the autonomous run terminal state

## [2026-03-08] FT-013: paywall modal and upgrade-intent tracking
- Added `frontend/src/lib/components/PaywallModal.svelte` and mounted it in `frontend/src/App.svelte` so exhausted starter users see an in-app pricing preview before any real billing exists
- Reused `strings.landing.pricing.plans` in the paywall and extended `frontend/src/lib/stores/i18n.ts` with friendly exhausted-access copy, keeping landing and in-app pricing aligned
- Added `trackUpgradeClicked` in `frontend/src/lib/analytics.ts` and wired paywall plan buttons to emit analytics-only `upgrade_clicked` events with stable `plan` and `surface` payloads
- Added deterministic coverage in `frontend/src/lib/components/PaywallModal.test.ts` and `frontend/src/lib/analytics.test.ts`
- Verified with `NODE_OPTIONS=--experimental-require-module cd frontend && pnpm test -- --run`, `cd frontend && pnpm check`, and `cd frontend && pnpm build`
- Synced `FT-013`, `REQ-032`, the autonomous backlog (`TASK-FT013-02` and `TASK-FT013-03` done), and the autonomous run terminal state

## [2026-03-08] FT-013: access-state slice verified and synced
- Closed `TASK-FT013-01` without product code changes because the FT-012 access-status implementation already satisfies the first FT-013 slice
- Verified the authenticated entitlement surface with `cd frontend && pnpm test -- --run` and `cd frontend && pnpm check`
- Recorded deterministic evidence in `.tasks/TASK-FT013-01/verification-2026-03-08.md` and updated the task protocol bundle
- Synced `FT-013`, `REQ-032`, the autonomous backlog (`TASK-FT013-01` done, `TASK-FT013-02` ready), and the autonomous run status

## [2026-03-08] FT-012: in-app access status surface
- Added `frontend/src/lib/stores/access.ts` and wired `frontend/src/App.svelte` to load/reset the authenticated `/api/access` snapshot
- Updated `frontend/src/lib/components/BoardsSidebar.svelte` to show starter sessions remaining or the active monthly/lifetime plan without credits language
- Extended `frontend/src/lib/stores/websocket.ts`, `frontend/src/lib/stores/i18n.ts`, and `frontend/src/lib/types.ts` so access state refreshes after the first blank-board AI turn and can hydrate from `access_exhausted` responses
- Added deterministic frontend coverage in `frontend/src/lib/stores/access.test.ts` and `frontend/src/lib/components/BoardsSidebar.test.ts`
- Verified with `cd frontend && pnpm test -- --run`, `cd frontend && pnpm check`, and `cd frontend && pnpm build`
- Synced `FT-012`, `REQ-031`, the autonomous backlog (`TASK-FT012-03` done), and the autonomous run terminal state

## [2026-03-08] FT-012: persistent metering and blank-session enforcement
- Extended `backend/app/access.py` to persist per-user entitlements and consumed-session rows, and to backfill tracked usage from already-started boards
- Wired the shared access service through `backend/app/construct.py`, `backend/app/main.py`, and `backend/app/services/main_service.py`
- Blocked the first AI-assisted message on a blank board when no free or paid access remains, while allowing existing started boards to continue
- Added deterministic coverage in `backend/tests/test_access.py`, `backend/tests/test_main_service.py`, and `backend/tests/test_integration_endpoints.py`
- Verified with `cd backend && uv run pytest tests/test_access.py tests/test_main_service.py tests/test_integration_endpoints.py -v`, `cd backend && uv run pytest -v`, and `./scripts/ci-gates.sh --skip-e2e`
- Synced `FT-012`, `REQ-031`, and the autonomous backlog (`TASK-FT012-02` done, `TASK-FT012-03` ready)

## [2026-03-08] FT-012: access contract and API surface
- Added `backend/app/access.py` to lock the launch monetization model as `3 free sessions total`, `monthly`, and `lifetime`
- Added authenticated `GET /api/access` in `backend/app/main.py`
- Added `backend/tests/test_access.py` plus endpoint coverage in `backend/tests/test_integration_endpoints.py`
- Recorded FT-012 assumptions in `.protocols/FT-012/decision-log.md`
- Verified with `cd backend && uv run pytest tests/test_access.py tests/test_integration_endpoints.py -v`, `cd backend && uv run pytest -v`, and `cd backend && uv run ruff check app/access.py app/main.py tests/test_access.py tests/test_integration_endpoints.py`
- Synced `FT-012`, `REQ-031`, and the autonomous backlog (`TASK-FT012-01` done, `TASK-FT012-02` ready)

## [2026-03-08] FT-008: auth reopen E2E coverage
- Extended `e2e/tests/auth.spec.ts` with authenticated real-board reload and browser-reopen flows using the local dev-bypass harness
- Verified the auth Playwright slice with `pnpm e2e -- --grep auth`
- Marked `FT-008` / `REQ-027` complete locally and synced the backlog (`TASK-FT008-03` done, no remaining ready tasks)

## [2026-03-08] FT-008: auth recovery paths and revoked-session UX
- Refined `frontend/src/lib/stores/auth.ts` so Auth0 recovery failures (`login_required`, `missing_refresh_token`, `invalid_grant`, related interactive-login codes) map to `session_expired`, while transient failures remain retryable
- Added `frontend/src/lib/components/AuthStateShell.svelte` and `frontend/src/lib/components/AuthStateShell.test.ts` to isolate and verify the auth recovery shell copy and actions
- Extended `frontend/src/lib/stores/auth.test.ts` to cover revoked-session init and retryable transient failures
- Updated auth recovery copy in `frontend/src/lib/stores/i18n.ts` to reassure users that their boards remain available after re-login
- Verified with `cd frontend && pnpm test -- --run` and `cd frontend && pnpm check`
- Synced `FT-008`, the autonomous run status, and the task backlog (`TASK-FT008-02` done, `TASK-FT008-03` ready)

## [2026-03-08] FT-008: auth reliability foundation
- Refactored `frontend/src/lib/stores/auth.ts` into a testable auth store with recoverable `auth_failed` and `session_expired` states
- Added `frontend/src/lib/stores/auth.test.ts` to cover dev bypass, missing config, redirect callback hydration, and silent refresh failures
- Updated `frontend/src/App.svelte` with localized retry and re-login actions for auth failures
- Added auth shell copy to `frontend/src/lib/stores/i18n.ts`
- Added a Playwright auth regression for surviving a page reload in `e2e/tests/auth.spec.ts`
- Verified with `cd frontend && pnpm test -- --run`, `cd frontend && pnpm check`, and `pnpm e2e -- --grep auth`
- Synced `FT-008`, `REQ-027`, the autonomous run status, and the task backlog (`TASK-FT008-01` done, `TASK-FT008-02` ready)

## [2026-03-08] Autonomous run: task-card backlog normalization
- Added `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md` plus `.tasks/TASK-AUTONOMOUS/README.md` to track the unattended run state
- Added `.memory-bank/tasks/index.md` and `.memory-bank/tasks/plans/index.md`
- Created per-feature implementation plans `IMPL-FT-001` through `IMPL-FT-016` under `.memory-bank/tasks/plans/`
- Replaced the old feature-only backlog with autonomous-ready `TASK-*` cards, queue states, dependencies, touched files, tests, verification steps, and docs targets
- Promoted `TASK-FT008-01` as the single current `ready` W1 task and recorded the remaining FT-001 deploy handoff as blocked by policy
- Synced `.memory-bank/index.md` planning links to the new task router

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
