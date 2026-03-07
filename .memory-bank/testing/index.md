---
description: Testing strategy, infrastructure, and quality gates.
status: active
---
# Testing & Verification

## Quality Gates (CI Pipeline)
1. Backend: `uv run pytest -q` (57 tests as of 2026-03-07)
2. Frontend: `pnpm test -- --run` (~7 tests)
3. Frontend build: `pnpm build` + `pnpm check` (TypeScript)
4. E2E: `pnpm e2e` (Playwright, Chromium, 13 scenarios as of 2026-03-07)
5. Deploy: auto on E2E pass + push to main

## Backend Tests (`backend/tests/`)
- **Framework:** pytest
- **Files:** 7 test files
- **Coverage:** endpoints, AI decoder, MainService logic, WebSocket protocol, connections, special questions, phase transitions
- **Mock:** MockAIService for deterministic responses
- **Auth:** dev-token fixture

## Frontend Tests
- **Framework:** vitest + @testing-library/svelte + jsdom
- **Files:** 4 test files (~7 tests)
- **Gap:** minimal coverage, mostly smoke tests

## E2E Tests (`e2e/`)
- **Framework:** Playwright (Chromium only)
- **Pattern:** Page Object Model (CanvasPage, InputBarPage, SidebarPage)
- **Files:** 4 test files, ~13 scenarios
- **Setup:** DEV_AUTH_BYPASS=true, AI_MOCK_MODE=true
- **CI:** 1 worker, 2 retries, trace/screenshot on first retry

## Pre-commit Hooks
- trailing whitespace, EOF fixer, YAML check, 1MB file limit
- Ruff: --fix + format check on `backend/` only

## Known Gaps
- Frontend unit test coverage (7 vs 57 backend tests)
- No code coverage metrics
- WebSocket tests use arbitrary 500ms waits
- Single browser target (Chromium)
- No load/stress tests
- Frontend test runs currently emit existing Svelte compiler/a11y warnings even when green

## Anti-cheat
- Don't weaken assertions to green tests without approval
- If a test reveals a bug: log it, fix only with explicit scope
