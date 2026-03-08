---
description: Autonomous-ready backlog with task cards, queue states, and wave ordering.
status: active
---
# Backlog

## Scheduler notes
- `TASK-FT012-02` is done; `TASK-FT012-03` is now the next `ready` task for the in-app access status UI.
- `FT-001` repo-local work is complete; deployment handoff remains blocked by autonomy policy.
- `FT-002` and `FT-006` remain done and serve as completed prerequisites for later work.
- `FT-008` repo-local auth reliability work is complete.

## Wave status
| Wave | Status | Notes |
|---|---|---|
| W1 | in_progress | Landing deploy handoff remains blocked; FT-012 backend enforcement is done and the access-status UI is the next safe local task. |
| W2 | planned | Feature plans and task cards are ready, but W2 should stay queued until W1 is cleared. |
| W3 | planned | Contains external research/ops/marketing work and later UX polish. |

## W1

### FT-001 Landing Page Redesign
TASK-ID: TASK-FT001-01
Status: done
Wave: W1
Feature: FT-001
REQs: REQ-020
Depends on: TASK-FT002-01
Touched files: `frontend/src/lib/components/LandingPage.svelte`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`; `cd frontend && pnpm build`
Verify: Match the landing against FT-001 AC on desktop/mobile and keep local evidence in `.protocols/FT-001/verification.md`
Docs: Update `FT-001`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT001-02
Status: blocked
Wave: W1
Feature: FT-001
REQs: REQ-020
Depends on: TASK-FT001-01
Touched files: `.protocols/FT-001/handoff.md`, deployment runbooks if explicitly allowed later
Tests: manual launch smoke-check after deploy
Verify: Confirm the live landing matches the verified local build and analytics remain active
Docs: Update `FT-001`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-002 Analytics & Event Tracking
TASK-ID: TASK-FT002-01
Status: done
Wave: W1
Feature: FT-002
REQs: REQ-021
Depends on: none
Touched files: `frontend/index.html`, `frontend/src/lib/analytics.ts`, `frontend/src/App.svelte`, `frontend/src/lib/stores/websocket.ts`, `backend/app/services/event_service.py`, `backend/app/services/main_service.py`
Tests: `cd backend && uv run pytest tests/test_event_service.py -v`; `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`; `cd frontend && pnpm build`
Verify: Reconfirm the event map and payload privacy constraints recorded in `.tasks/FT-002/verification-2026-03-08.md`
Docs: Update `FT-002`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-006 AI Output Validation
TASK-ID: TASK-FT006-01
Status: done
Wave: W1
Feature: FT-006
REQs: REQ-025
Depends on: none
Touched files: `backend/app/services/validator.py`, `backend/app/services/main_service.py`, `backend/tests/test_validator.py`, `backend/tests/test_main_service.py`
Tests: `cd backend && uv run pytest tests/test_validator.py -v`; `cd backend && uv run pytest tests/test_main_service.py -v`
Verify: Re-run validator coverage and confirm invalid AI operations are filtered before apply
Docs: Update `FT-006`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-008 Auth Reliability
TASK-ID: TASK-FT008-01
Status: done
Wave: W1
Feature: FT-008
REQs: REQ-027
Depends on: none
Touched files: `frontend/src/lib/stores/auth.ts`, `frontend/src/App.svelte`, `frontend/src/lib/stores/i18n.ts`, `e2e/tests/auth.spec.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Add deterministic frontend coverage for init/refresh failure states and confirm the app exposes a recoverable auth shell state
Docs: Update `FT-008`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT008-02
Status: done
Wave: W1
Feature: FT-008
REQs: REQ-027
Depends on: TASK-FT008-01
Touched files: `frontend/src/lib/stores/auth.ts`, `frontend/src/App.svelte`, `frontend/src/lib/components/AuthStateShell.svelte`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Confirm refresh failures, revoked sessions, and page refreshes land on a clear re-login path with helpful copy
Docs: Update `FT-008`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT008-03
Status: done
Wave: W1
Feature: FT-008
REQs: REQ-027
Depends on: TASK-FT008-02
Touched files: `e2e/tests/auth.spec.ts`, `e2e/fixtures/auth.fixture.ts`
Tests: `pnpm e2e -- --grep auth`
Verify: Exercise login, refresh, and re-open flows with the dev-bypass harness and store the run output in `.tasks/TASK-FT008-03/`
Docs: Update `FT-008`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-012 Session Access & Limits System
TASK-ID: TASK-FT012-01
Status: done
Wave: W1
Feature: FT-012
REQs: REQ-031
Depends on: none
Touched files: `backend/app/access.py`, `backend/app/main.py`, `.protocols/FT-012/decision-log.md`
Tests: `cd backend && uv run pytest -v`
Verify: Lock the entitlement rules in code-facing terms and record any remaining assumptions explicitly
Docs: Update `FT-012`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT012-02
Status: done
Wave: W1
Feature: FT-012
REQs: REQ-031
Depends on: TASK-FT012-01
Touched files: `backend/app/access.py`, `backend/app/construct.py`, `backend/app/services/main_service.py`, `backend/app/services/state_service.py`, `backend/app/main.py`, `backend/tests/test_access.py`, `backend/tests/test_integration_endpoints.py`, `backend/tests/test_main_service.py`
Tests: `cd backend && uv run pytest -v`
Verify: Confirm free/monthly/lifetime access states persist per user and are enforced before AI-assisted session starts
Docs: Update `FT-012`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT012-03
Status: ready
Wave: W1
Feature: FT-012
REQs: REQ-031
Depends on: TASK-FT012-02
Touched files: `frontend/src/lib/stores/access.ts`, `frontend/src/App.svelte`, `frontend/src/lib/components/BoardsSidebar.svelte`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Show remaining free sessions or active plan status in-app without exposing a credits model
Docs: Update `FT-012`, `requirements.md`, `backlog.md`, `changelog.md`

## W2

### FT-003 Interactive Onboarding Tour
TASK-ID: TASK-FT003-01
Status: planned
Wave: W2
Feature: FT-003
REQs: REQ-022
Depends on: TASK-FT008-03
Touched files: `frontend/src/lib/stores/onboarding.ts`, `frontend/src/lib/components/TooltipOverlay.svelte`, `frontend/src/App.svelte`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Define the interactive tour state model, repeat action, and persistence strategy without regressing existing help cues
Docs: Update `FT-003`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT003-02
Status: planned
Wave: W2
Feature: FT-003
REQs: REQ-022
Depends on: TASK-FT003-01
Touched files: `frontend/src/lib/components/TooltipOverlay.svelte`, `frontend/src/lib/components/HelpOverlay.svelte`, `frontend/src/lib/components/MobileDrawer.svelte`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Walk through the tour on desktop and mobile and confirm users perform the expected actions instead of only reading tips
Docs: Update `FT-003`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT003-03
Status: planned
Wave: W2
Feature: FT-003
REQs: REQ-022
Depends on: TASK-FT003-02
Touched files: `frontend/src/lib/stores/onboarding.ts`, `e2e/tests/full-flow.spec.ts`
Tests: `cd frontend && pnpm test -- --run`; `pnpm e2e -- --grep onboarding`
Verify: Finish the tour, refresh, and confirm it stays hidden until the user explicitly restarts it
Docs: Update `FT-003`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-004 Decision Memo Export
TASK-ID: TASK-FT004-01
Status: planned
Wave: W2
Feature: FT-004
REQs: REQ-023
Depends on: TASK-FT008-03
Touched files: `backend/app/services/ai_service.py`, `backend/app/services/main_service.py`, `backend/app/main.py`
Tests: `cd backend && uv run pytest -v`
Verify: Define and validate the memo payload for sparse and fully populated sessions
Docs: Update `FT-004`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT004-02
Status: planned
Wave: W2
Feature: FT-004
REQs: REQ-023
Depends on: TASK-FT004-01
Touched files: `frontend/src/lib/components/BoardsSidebar.svelte`, `frontend/src/lib/components/SelectionToolbar.svelte`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Generate, copy, and download a Markdown memo from the session UI
Docs: Update `FT-004`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT004-03
Status: planned
Wave: W2
Feature: FT-004
REQs: REQ-023
Depends on: TASK-FT004-02
Touched files: `frontend/src/lib/analytics.ts`, `frontend/src/lib/components/BoardsSidebar.svelte`, `frontend/src/lib/components/SelectionToolbar.svelte`
Tests: `cd frontend && pnpm test -- --run`
Verify: Confirm memo export analytics are emitted with the final export surface
Docs: Update `FT-004`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-005 Blind Spot Analysis
TASK-ID: TASK-FT005-01
Status: planned
Wave: W2
Feature: FT-005
REQs: REQ-024
Depends on: TASK-FT004-03
Touched files: `backend/app/services/ai_service.py`, `backend/app/services/main_service.py`
Tests: `cd backend && uv run pytest -v`
Verify: Define trigger rules and gap-analysis response shape after fact accumulation
Docs: Update `FT-005`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT005-02
Status: planned
Wave: W2
Feature: FT-005
REQs: REQ-024
Depends on: TASK-FT005-01
Touched files: `frontend/src/lib/components/Canvas.svelte`, `frontend/src/lib/components/Card.svelte`, `frontend/src/lib/stores/cards.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Render empty-zone hints and isolated-card emphasis without breaking drag/edit interactions
Docs: Update `FT-005`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT005-03
Status: planned
Wave: W2
Feature: FT-005
REQs: REQ-024
Depends on: TASK-FT005-02
Touched files: `backend/app/services/main_service.py`, `frontend/src/lib/components/CurrentQuestion.svelte`
Tests: `cd backend && uv run pytest -v`; `cd frontend && pnpm test -- --run`
Verify: Confirm proactive blind-spot prompts and missing-link suggestions appear at the right time
Docs: Update `FT-005`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-007 TODO Cards as Action Plan
TASK-ID: TASK-FT007-01
Status: planned
Wave: W2
Feature: FT-007
REQs: REQ-026
Depends on: TASK-FT004-03
Touched files: `backend/app/models.py`, `backend/app/services/main_service.py`, `frontend/src/lib/stores/cards.ts`
Tests: `cd backend && uv run pytest -v`; `cd frontend && pnpm test -- --run`
Verify: Persist TODO done/undone state without regressing other card types
Docs: Update `FT-007`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT007-02
Status: planned
Wave: W2
Feature: FT-007
REQs: REQ-026
Depends on: TASK-FT007-01
Touched files: `frontend/src/lib/components/BoardsSidebar.svelte`, `frontend/src/lib/components/SelectionToolbar.svelte`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Use the TODO panel/filter, badge, and dedicated export flow from a real session
Docs: Update `FT-007`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-010 Special Questions Rewrite
TASK-ID: TASK-FT010-01
Status: planned
Wave: W2
Feature: FT-010
REQs: REQ-029
Depends on: TASK-FT008-03
Touched files: `backend/data/questions.json`, `backend/app/services/special_questions.py`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd backend && uv run pytest tests/test_special_questions.py -v`; `cd frontend && pnpm test -- --run`
Verify: Confirm the deck loads with renamed categories and rewritten prompts in RU and EN
Docs: Update `FT-010`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT010-02
Status: planned
Wave: W2
Feature: FT-010
REQs: REQ-029
Depends on: TASK-FT010-01
Touched files: `backend/tests/test_special_questions.py`, `frontend/src/lib/components/CurrentQuestion.test.ts`
Tests: `cd backend && uv run pytest tests/test_special_questions.py -v`; `cd frontend && pnpm test -- --run`
Verify: Lock renamed categories and deck integrity into regression tests
Docs: Update `FT-010`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT010-03
Status: planned
Wave: W2
Feature: FT-010
REQs: REQ-029
Depends on: TASK-FT010-02
Touched files: `.tasks/TASK-FT010-03/*`, `.protocols/FT-010/*`
Tests: manual evidence collection
Verify: Review the rewritten deck with real users and record wording follow-ups
Docs: Update `FT-010`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-013 Pricing & Upgrade UI + Intent Tracking
TASK-ID: TASK-FT013-01
Status: planned
Wave: W2
Feature: FT-013
REQs: REQ-032
Depends on: TASK-FT012-02, TASK-FT002-01
Touched files: `frontend/src/lib/stores/access.ts`, `frontend/src/lib/components/BoardsSidebar.svelte`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Show the current access state in-app using backend entitlement data
Docs: Update `FT-013`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT013-02
Status: planned
Wave: W2
Feature: FT-013
REQs: REQ-032
Depends on: TASK-FT013-01
Touched files: `frontend/src/lib/components/PaywallModal.svelte`, `frontend/src/lib/components/LandingPage.svelte`, `frontend/src/lib/stores/i18n.ts`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Trigger the paywall after free-session exhaustion and confirm landing/in-app pricing stay aligned
Docs: Update `FT-013`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT013-03
Status: planned
Wave: W2
Feature: FT-013
REQs: REQ-032
Depends on: TASK-FT013-02
Touched files: `frontend/src/lib/analytics.ts`, `frontend/src/lib/components/PaywallModal.svelte`
Tests: `cd frontend && pnpm test -- --run`
Verify: Confirm upgrade-click events fire with the new paywall UI and no real payment integration exists
Docs: Update `FT-013`, `requirements.md`, `backlog.md`, `changelog.md`

## W3

### FT-009 Demand Validation
TASK-ID: TASK-FT009-01
Status: planned
Wave: W3
Feature: FT-009
REQs: REQ-028
Depends on: TASK-FT002-01
Touched files: `.protocols/FT-009/plan.md`, `.tasks/TASK-FT009-01/*`
Tests: manual evidence collection
Verify: Define the research template, target cohorts, and evidence bundle before interviews/sessions start
Docs: Update `FT-009`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT009-02
Status: planned
Wave: W3
Feature: FT-009
REQs: REQ-028
Depends on: TASK-FT009-01
Touched files: `.protocols/FT-009/verification.md`, `.tasks/TASK-FT009-02/*`
Tests: manual evidence collection
Verify: Capture own sessions, external observations, Webvisor review, and the resulting go/no-go decision
Docs: Update `FT-009`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-011 Own Domain & Branding
TASK-ID: TASK-FT011-01
Status: planned
Wave: W3
Feature: FT-011
REQs: REQ-030
Depends on: none
Touched files: `.protocols/FT-011/decision-log.md`, `README.md`, `.memory-bank/features/FT-011-own-domain.md`
Tests: repo-side config review
Verify: Record the domain decision and the repo-managed cutover checklist before any operator action
Docs: Update `FT-011`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT011-02
Status: planned
Wave: W3
Feature: FT-011
REQs: REQ-030
Depends on: TASK-FT011-01
Touched files: deployment config files already in repo, `.memory-bank/guides/dev-setup.md`, `README.md`
Tests: manual config review
Verify: Update all repo-side hostnames, Auth0 callbacks, and docs for the chosen domain
Docs: Update `FT-011`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT011-03
Status: planned
Wave: W3
Feature: FT-011
REQs: REQ-030
Depends on: TASK-FT011-02
Touched files: `.tasks/TASK-FT011-03/*`
Tests: manual health check after cutover
Verify: Confirm the new domain serves the app and the old one redirects after operator-run DNS/SSL changes
Docs: Update `FT-011`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-014 LinkedIn Article & Launch Post
TASK-ID: TASK-FT014-01
Status: planned
Wave: W3
Feature: FT-014
REQs: REQ-040
Depends on: TASK-FT011-03
Touched files: `.protocols/FT-014/plan.md`, `.tasks/TASK-FT014-01/*`
Tests: manual editorial review
Verify: Draft the article/post package with screenshots and the live own-domain URL
Docs: Update `FT-014`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT014-02
Status: planned
Wave: W3
Feature: FT-014
REQs: REQ-040
Depends on: TASK-FT014-01
Touched files: `.tasks/TASK-FT014-02/*`
Tests: manual publication checklist
Verify: Publish and cross-post the launch package, then record outcome links and early signals
Docs: Update `FT-014`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-015 Mobile UX Improvements
TASK-ID: TASK-FT015-01
Status: planned
Wave: W3
Feature: FT-015
REQs: REQ-041
Depends on: TASK-FT003-03
Touched files: `frontend/src/lib/stores/mobile.ts`, `frontend/src/App.svelte`, `.protocols/FT-015/decision-log.md`
Tests: `cd frontend && pnpm check`
Verify: Decide the mobile mode boundary and record the chosen interaction model
Docs: Update `FT-015`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT015-02
Status: planned
Wave: W3
Feature: FT-015
REQs: REQ-041
Depends on: TASK-FT015-01
Touched files: `frontend/src/lib/components/Canvas.svelte`, `frontend/src/lib/components/Card.svelte`, `frontend/src/lib/components/MobileDrawer.svelte`
Tests: `cd frontend && pnpm test -- --run`; `cd frontend && pnpm check`
Verify: Confirm touch-friendly creation/manipulation works on narrow viewports without critical regressions
Docs: Update `FT-015`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT015-03
Status: planned
Wave: W3
Feature: FT-015
REQs: REQ-041
Depends on: TASK-FT015-02
Touched files: `e2e/tests/*`, `.tasks/TASK-FT015-03/*`
Tests: `pnpm e2e -- --grep mobile`
Verify: Store iOS Safari and Android Chrome evidence for the core session flow under `.tasks/TASK-FT015-03/`
Docs: Update `FT-015`, `requirements.md`, `backlog.md`, `changelog.md`

### FT-016 Promo & Distribution Content
TASK-ID: TASK-FT016-01
Status: planned
Wave: W3
Feature: FT-016
REQs: REQ-042
Depends on: TASK-FT011-03
Touched files: `.tasks/TASK-FT016-01/*`, `.protocols/FT-016/plan.md`
Tests: manual editorial review
Verify: Assemble the demo session, screenshots, and base promo pack against the live domain and pricing
Docs: Update `FT-016`, `requirements.md`, `backlog.md`, `changelog.md`

TASK-ID: TASK-FT016-02
Status: planned
Wave: W3
Feature: FT-016
REQs: REQ-042
Depends on: TASK-FT016-01
Touched files: `.tasks/TASK-FT016-02/*`
Tests: manual publication checklist
Verify: Finalize the Reddit, LinkedIn, blog, and Product Hunt content variants and log the feedback loop
Docs: Update `FT-016`, `requirements.md`, `backlog.md`, `changelog.md`
