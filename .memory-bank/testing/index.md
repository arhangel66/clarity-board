---
description: Testing strategy, infrastructure, and quality gates.
status: active
---
# Testing & Verification

## Quality Gates (CI Pipeline)
1. Backend: `uv run pytest -q` (76 tests as of 2026-03-08)
2. Frontend: `pnpm test -- --run` (30 tests as of 2026-03-08)
3. Frontend build: `pnpm build` + `pnpm check` (TypeScript)
4. E2E: `pnpm e2e` (Playwright, Chromium, 13 tests as of 2026-03-07)
5. Deploy: `.github/workflows/deploy.yml` runs only after the `E2E Tests` workflow succeeds for a `push` to `main`

## Backend Tests (`backend/tests/`)
- **Framework:** pytest
- **Files:** 10 test files
- **Coverage:** endpoints, AI decoder, event logging, health check, MainService logic, WebSocket protocol, connections, special questions, phase transitions, validator
- **Mock:** MockAIService for deterministic responses
- **Auth:** dev-token fixture

## Frontend Tests
- **Framework:** vitest + @testing-library/svelte + jsdom
- **Files:** 10 test files / 30 tests
- **Notable coverage:** `src/lib/analytics.test.ts` verifies Yandex goal helper calls and payload shape; `src/lib/components/CurrentQuestion.test.ts` verifies visible special-question category labels and the i18n fallback path
- **Gap:** coverage is stronger on critical surfaces, but still not exhaustive across the whole UI

## E2E Tests (`e2e/`)
- **Framework:** Playwright (Chromium only)
- **Pattern:** Page Object Model (CanvasPage, InputBarPage, SidebarPage)
- **Files:** 4 test files / 13 tests
- **Setup:** DEV_AUTH_BYPASS=true, AI_MOCK_MODE=true
- **CI:** 1 worker, 2 retries, trace/screenshot on first retry

## Pre-commit Hooks
- trailing whitespace, EOF fixer, YAML check, 1MB file limit
- Ruff: --fix + format check on `backend/` only

## Known Gaps
- Frontend unit test coverage is still shallower than backend coverage (30 vs 76 tests)
- No code coverage metrics
- WebSocket tests use arbitrary 500ms waits
- Single browser target (Chromium)
- No load/stress tests
- Frontend test runs currently emit existing Svelte compiler/a11y warnings even when green

## Anti-cheat
- Don't weaken assertions to green tests without approval
- If a test reveals a bug: log it, fix only with explicit scope
