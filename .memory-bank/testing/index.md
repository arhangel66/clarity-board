---
description: Testing strategy, infrastructure, and quality gates.
status: active
---
# Testing & Verification

## Quality Gates
1. Local full gate: `./scripts/ci-gates.sh`
2. Local fast gate: `./scripts/ci-gates.sh --skip-e2e`
3. GitHub Actions smoke: `.github/workflows/ci-smoke.yml` validates repo wiring in under 2 minutes and opens the deploy path for a `push` to `main`
4. Deploy: `.github/workflows/deploy.yml` runs only after the `CI Smoke` workflow succeeds for a `push` to `main`

## Local Full Gate (`./scripts/ci-gates.sh`)
- Backend: `uv run pytest -q` (77 tests as of 2026-03-08)
- Frontend: `pnpm test -- --run` (37 tests as of 2026-03-08)
- Frontend build: `pnpm build`
- Frontend checks: `pnpm check`
- E2E: `pnpm e2e` (Playwright, Chromium, 16 tests as of 2026-03-08)

## GitHub Smoke (`.github/workflows/ci-smoke.yml`)
- Checkout only; no dependency install
- `bash -n scripts/ci-gates.sh`
- `python3 -m compileall backend/app backend/tests`
- File-presence smoke for backend/frontend/Playwright entrypoints
- Budget: `timeout-minutes: 2`

## Backend Tests (`backend/tests/`)
- **Framework:** pytest
- **Files:** 10 test files
- **Coverage:** endpoints, AI decoder, event logging, health check, MainService logic, WebSocket protocol, connections, special questions, phase transitions, validator
- **Mock:** MockAIService for deterministic responses
- **Auth:** dev-token fixture

## Frontend Tests
- **Framework:** vitest + @testing-library/svelte + jsdom
- **Files:** 14 test files / 37 tests
- **Notable coverage:** `src/lib/analytics.test.ts` verifies Yandex goal helper calls and payload shape; `src/lib/components/CurrentQuestion.test.ts` verifies visible special-question category labels and the i18n fallback path; `src/lib/stores/onboarding.test.ts` verifies ordered onboarding persistence, restart behavior, and gated progression; `src/lib/components/TooltipOverlay.test.ts`, `src/lib/components/HelpOverlay.test.ts`, and `src/lib/components/MobileDrawer.test.ts` lock the onboarding walkthrough surfaces
- **Gap:** coverage is stronger on critical surfaces, but still not exhaustive across the whole UI

## E2E Tests (`e2e/`)
- **Framework:** Playwright (Chromium only)
- **Pattern:** Page Object Model (CanvasPage, InputBarPage, SidebarPage)
- **Files:** 4 test files / 16 tests
- **Setup:** DEV_AUTH_BYPASS=true, AI_MOCK_MODE=true, E2E_UNLIMITED_ACCESS=true; Playwright boots an isolated frontend/backend pair on `127.0.0.1:4173` and `127.0.0.1:18000`, with backend state redirected to a clean temp data dir via `FACT_DATA_DIR`
- **CI:** 1 worker, 2 retries, trace/screenshot on first retry

## Pre-commit Hooks
- trailing whitespace, EOF fixer, YAML check, 1MB file limit
- Ruff: --fix + format check on `backend/` only

## Known Gaps
- Frontend unit test coverage is still shallower than backend coverage (37 vs 76 tests)
- No code coverage metrics
- WebSocket tests use arbitrary 500ms waits
- Single browser target (Chromium)
- No load/stress tests
- Frontend test runs currently emit existing Svelte compiler/a11y warnings even when green
- GitHub Actions smoke is intentionally lighter than the local full gate; local `./scripts/ci-gates.sh` remains the release-quality source of truth

## Anti-cheat
- Don't weaken assertions to green tests without approval
- If a test reveals a bug: log it, fix only with explicit scope
