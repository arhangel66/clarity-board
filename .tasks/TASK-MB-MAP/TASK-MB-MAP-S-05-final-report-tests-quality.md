# Final Report: Test Infrastructure & Quality Gates

**Report Date:** 2026-03-06
**Repository:** /Users/mikhail/w/learning/fact
**Scope:** Complete inventory of testing frameworks, configuration, CI/CD gates, and code quality tooling

---

## 1. Test File Inventory

### 1.1 Backend Tests (pytest)
**Location:** `backend/tests/`
**Test Framework:** pytest 9.0.2+
**Count:** 7 test files

| File | Coverage | Key Tests |
|------|----------|-----------|
| `test_health.py` | HTTP endpoints | 1 test: health check |
| `test_decoder.py` | Pure function: AI JSON parsing | 5 tests: JSON parsing, invalid input handling, position normalization, text truncation, clamping |
| `test_main_service.py` | MainService business logic | 3 tests: card deletion rules, card creation, special question workflow |
| `test_integration_endpoints.py` | WebSocket + REST API | 21 tests: session CRUD, WebSocket init/auth, card operations (create/update/delete/move), connections, special questions, error handling |
| `test_connections.py` | Connection persistence | 1 test: create, retrieve, delete connections across service restarts |
| `test_special_questions.py` | Special questions service | 4 tests: unlock logic, pending state, locale support (ru/en), answer recording |
| `test_question_flow.py` | Phase transitions & card editing rules | 3 tests: question card update allowance by phase, phase transition delays |

**Total Backend Tests:** ~38 unit + integration tests

### 1.2 Frontend Tests (vitest + @testing-library/svelte)
**Location:** `frontend/src/`
**Test Framework:** vitest 4.0.18, @testing-library/svelte 5.3.1
**Environment:** jsdom, setupFiles: `src/test/setup.ts` (mocks ResizeObserver, matchMedia)
**Count:** 4 test files

| File | Coverage | Key Tests |
|------|----------|-----------|
| `App.test.ts` | App root component | 1 smoke test: renders without crash |
| `stores/cards.test.ts` | Svelte card store | 2 tests: position overlap avoidance, pinned card positioning |
| `components/CurrentQuestion.test.ts` | CurrentQuestion component | 2 tests: renders toggle bar, thinking indicator |
| `components/Connections.test.ts` | Connections SVG component | 2 tests: renders nothing when empty, draws line between cards |

**Total Frontend Tests:** ~7 unit tests

### 1.3 E2E Tests (Playwright)
**Location:** `e2e/`
**Test Framework:** Playwright Test (chromium only)
**Configuration:** `playwright.config.ts`
**Count:** 4 test files + 3 page objects + 1 auth fixture

#### Test Files
| File | Scenarios |
|------|-----------|
| `tests/auth.spec.ts` | 3 tests: landing page visibility, dev bypass auth, boards section access |
| `tests/card-crud.spec.ts` | 5 tests: create via text input, create via quick create, select, delete, root card protection |
| `tests/unified-flow.spec.ts` | 1 test: complete journey (auth → messages → card select → delete) |
| `tests/full-flow.spec.ts` | 4 tests: complete flow with unique test IDs, sidebar collapse/expand, input bar mode switching, lasso selection |

**Total E2E Tests:** ~13 test scenarios

#### Page Objects (POM Pattern)
- `pages/sidebar.page.ts` — BoardsSidebar: toggle, board selection, new board creation, delete button, user info
- `pages/canvas.page.ts` — Canvas: card selection, quick create, card count, wait for card by text
- `pages/input-bar.page.ts` — InputBar: text/voice mode switching, send text, send with Enter

#### Auth Fixture
**File:** `fixtures/auth.fixture.ts`
**Pattern:** Playwright test fixture extension
**Features:**
- Dev bypass: navigates to `/?dev=1`
- Onboarding skip: sets localStorage `fact_onboarding_seen=1`
- Board creation fallback: creates board via API if none exist
- Board selection: auto-selects first board
- WebSocket wait: 500ms delay for connection establishment

---

## 2. Testing Frameworks & Configuration

### 2.1 Backend: pytest

**Config Location:** `backend/pyproject.toml`

```toml
[dependency-groups]
dev = [
    "httpx>=0.28.1",
    "pre-commit>=4.5.1",
    "pytest>=9.0.2",
    "ruff>=0.14.14",
]
```

**No pytest.ini or conftest.py** — uses default discovery (test_*.py)

**Test Patterns:**
- AAA flow: Setup (Dummy*Service mocks), Act, Assert
- Dummy service pattern: Simple mock classes injected into services
- Monkeypatch for environment variables and service substitution
- FastAPI TestClient for HTTP testing
- WebSocket testing via TestClient.websocket_connect()
- tmp_path fixture for SQLite databases

**Run Command:**
```bash
cd backend && uv run pytest -v  # verbose
cd backend && uv run pytest -q  # quiet (CI)
```

### 2.2 Frontend: vitest

**Config Location:** `frontend/vite.config.ts`

```typescript
test: {
  environment: 'jsdom',
  globals: true,
  setupFiles: ['./src/test/setup.ts'],
}
```

**Setup File:** `frontend/src/test/setup.ts`
- `@testing-library/jest-dom/vitest` — provides jest matchers for vitest
- ResizeObserver mock
- matchMedia mock for mobile detection

**Test Patterns:**
- Svelte component rendering: `render()` from @testing-library/svelte
- Store testing: `get()` to extract current value
- `beforeEach`/`afterEach` for store cleanup
- Async operations: `await tick()` for Svelte reactivity

**Run Commands:**
```bash
cd frontend && pnpm test              # watch mode
cd frontend && pnpm test -- --run    # single run (CI)
cd frontend && pnpm test -- --run src/lib/stores/cards.test.ts  # single file
```

**TypeScript Config:** `frontend/tsconfig.json`
- `strict: true`, `checkJs: true`, `noUnusedLocals: true`, `noUnusedParameters: true`
- Target: ESNext, Module: ESNext

### 2.3 Frontend: svelte-check (Static Type Check)

**Run Command:**
```bash
cd frontend && pnpm check
```

Used in CI to catch Svelte component type errors

### 2.4 E2E: Playwright

**Config Location:** `playwright.config.ts`

**Key Settings:**
```typescript
testDir: './e2e/tests'
fullyParallel: true
forbidOnly: !!process.env.CI  // fail if test.only left in code
retries: process.env.CI ? 2 : 0
workers: process.env.CI ? 1 : undefined  // single worker on CI
reporter: [...] // HTML + GitHub
trace: 'on-first-retry'
screenshot: 'only-on-failure'
video: 'on-first-retry'
```

**Web Servers (auto-started):**
```typescript
webServer: [
  {
    command: 'cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000',
    url: 'http://localhost:8000/api/health',
    env: { DEV_AUTH_BYPASS: 'true', AI_MOCK_MODE: 'true' },
  },
  {
    command: 'cd frontend && pnpm dev --port 5173',
    url: 'http://localhost:5173',
  },
]
```

**Run Commands:**
```bash
pnpm e2e                        # run all E2E tests
pnpm e2e tests/auth.spec.ts   # single file
```

---

## 3. Code Quality Tools

### 3.1 Pre-Commit Hooks

**Config:** `.pre-commit-config.yaml`

**Hooks Configured:**
1. `trailing-whitespace` — remove trailing spaces
2. `end-of-file-fixer` — ensure newline at EOF
3. `check-yaml` — validate YAML syntax
4. `check-added-large-files` — block >1000KB files
5. `check-merge-conflict` — detect unresolved conflicts
6. **ruff** (v0.14.14) — linting + import sorting
7. **ruff-format** — code formatting

**Scope:** Backend only (`files: ^backend/`)

**Run Command:**
```bash
cd backend && pre-commit run --all-files
```

### 3.2 Backend: ruff

**Config:** `backend/pyproject.toml`

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]  # comprehensive
ignore = ["E501"]  # line too long (formatter handles)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Rules Active:**
- E/W: pycodestyle errors/warnings
- F: pyflakes (undefined names, unused imports)
- I: isort (import ordering)
- B: flake8-bugbear (common bugs)
- C4: flake8-comprehensions (list/dict comprehension style)
- UP: pyupgrade (modern Python syntax)

**Run Commands:**
```bash
cd backend && ruff check .
cd backend && ruff format .
```

### 3.3 Frontend: TypeScript Strict Mode

**Config:** `frontend/tsconfig.json`

**Strict Checks:**
- `strict: true` — enables all strict type checking options
- `noImplicitAny: true`
- `strictNullChecks: true`
- `noUnusedLocals: true`
- `noUnusedParameters: true`
- `noFallthroughCasesInSwitch: true`
- `checkJs: true` — check .js files too

**Run Command:**
```bash
cd frontend && pnpm check  # via svelte-check in CI
```

---

## 4. CI/CD Pipeline

### 4.1 E2E Tests Workflow

**File:** `.github/workflows/e2e.yml`
**Trigger:** Push to main + Pull requests to main
**Timeout:** 15 minutes

**Steps:**
1. Checkout code
2. Setup Node.js 20 + pnpm 9
3. Install dependencies (root + frontend)
4. Setup Python 3.12 + uv
5. **Install backend dependencies:** `cd backend && uv sync`
6. **Run backend tests:** `cd backend && uv run pytest -q` (quiet)
   - Env: `OPENROUTER_API_KEY=test-key-not-used-in-ci`
7. **Run frontend unit tests:** `cd frontend && pnpm test -- --run`
8. **Build frontend:** `cd frontend && pnpm build`
9. **Frontend type check:** `cd frontend && pnpm check` (svelte-check)
10. **Install Playwright:** `pnpm exec playwright install chromium`
11. **Create test .env:** Sets `OPENROUTER_API_KEY`, `DEV_AUTH_BYPASS=true`, `AI_MOCK_MODE=true`
12. **Run E2E tests:** `pnpm e2e`
    - Env: `DEV_AUTH_BYPASS=true`, `AI_MOCK_MODE=true`
13. **Upload artifacts on failure:**
    - playwright-report/ (7 days retention)
    - test-results/ (7 days retention)

### 4.2 Deploy Workflow

**File:** `.github/workflows/deploy.yml`
**Trigger:** E2E workflow completion (on main, on success)
**Condition:** Only deploys if E2E tests pass

**Process:**
1. Wait for E2E workflow success
2. SSH to production server
3. Sync code via rsync (exclude .git, .env, node_modules, __pycache__, .venv, *.db)
4. Build Docker containers: `docker compose build --no-cache`
5. Start services: `docker compose up -d`
6. Cleanup old images: `docker image prune -f`

---

## 5. Coverage Analysis & Gaps

### 5.1 Coverage by Layer

#### Backend Coverage: GOOD (~38 tests)
✓ Health check endpoint
✓ AI decoder (pure function, edge cases)
✓ MainService business logic
✓ WebSocket lifecycle (init, auth, message handling)
✓ Session management (CRUD)
✓ Card operations (create/update/delete/move)
✓ Connections (create/delete/persistence)
✓ Special questions workflow
✓ Question card editing rules
✓ Error handling (missing auth, invalid JSON, unauthorized)

**Gap:** No load/stress tests, no concurrent WebSocket tests

#### Frontend Coverage: MINIMAL (~7 tests)
✓ App renders without crash (smoke test)
✓ Card store: overlap detection, pinned positioning
✓ CurrentQuestion: toggle bar, thinking indicator
✓ Connections: SVG rendering with cards

**Gaps:**
- No InputBar tests
- No Canvas component tests
- No auth store tests
- No WebSocket store tests
- No i18n store tests
- No mobile store tests
- No zoom store tests
- No onboarding store tests
- No drawer/sidebar tests (only E2E)
- No error handling tests

#### E2E Coverage: GOOD (~13 scenarios)
✓ Auth bypass flow (dev param)
✓ Card creation via text + quick create
✓ Card selection + deletion
✓ Root card protection
✓ Sidebar collapse/expand
✓ Input bar mode switching (text/voice)
✓ Unified user journey (complete flow)
✓ Lasso selection (smoke test)
✓ Boards UI

**Gaps:**
- No voice input testing (requires audio mock)
- No special questions flow (E2E)
- No connection creation (E2E)
- No real Auth0 integration test
- No offline/network failure scenarios

### 5.2 Coverage Strategy Assessment

| Layer | Strategy | Strength | Weakness |
|-------|----------|----------|----------|
| Backend | Unit + Integration | Comprehensive service logic, WebSocket protocol | No load tests |
| Frontend | Minimal unit + E2E | E2E covers main flows | Store logic untested, component isolation weak |
| E2E | Happy paths + CRUD | Core user journeys | No edge cases, no real auth |

---

## 6. Test Infrastructure Quality & Reliability

### 6.1 Strengths

1. **Isolation:** Dummy mock services prevent external API calls
2. **Dev Auth Bypass:** `DEV_AUTH_BYPASS=true` allows testing without Auth0
3. **Mock AI Mode:** `AI_MOCK_MODE=true` makes E2E deterministic
4. **Fixtures:** Playwright auth fixture handles setup boilerplate
5. **Page Objects:** Clear separation of selectors from test logic
6. **Temp Databases:** pytest tmp_path isolates tests
7. **Monkeypatch:** Env vars and service swapping
8. **Artifact Capture:** Screenshots, videos, traces on failure
9. **Retry Logic:** E2E tests retry on CI (2x)
10. **Type Safety:** Frontend strict TypeScript, Python type hints

### 6.2 Weaknesses & Risks

1. **Frontend Unit Tests Sparse:** Most coverage is E2E (brittle)
2. **No conftest.py:** No shared pytest fixtures for backends
3. **Test-specific Mocks:** Mock AI service is hardcoded, not externalized
4. **LocalStorage Assumptions:** E2E fixture sets `fact_onboarding_seen` globally
5. **No Flake Detection:** No test retry strategy for local unit tests
6. **WebSocket Stability:** 500ms arbitrary wait in E2E fixture
7. **No Coverage Reports:** No pytest coverage plugin, no vitest coverage
8. **Single Browser:** Playwright config hardcoded to chromium only
9. **No Database Migration Tests:** No alembic test coverage
10. **Timeout Hard to Debug:** 10s timeouts in E2E but no detailed logs on failure

---

## 7. Commands & Workflows Reference

### 7.1 Run All Tests Locally

```bash
# Backend
cd backend && uv run pytest -v

# Frontend
cd frontend && pnpm test -- --run

# E2E (requires backend & frontend running)
pnpm e2e

# Type check
cd frontend && pnpm check
```

### 7.2 Pre-Commit Quality Gate

```bash
# Run all hooks
cd backend && pre-commit run --all-files

# Run specific hook
cd backend && pre-commit run ruff --all-files
```

### 7.3 CI Simulation Locally

```bash
# Simulate CI environment
export DEV_AUTH_BYPASS=true
export AI_MOCK_MODE=true
export OPENROUTER_API_KEY=test-key

# Backend
cd backend && uv sync && uv run pytest -q

# Frontend
cd frontend && pnpm install && pnpm test -- --run && pnpm check && pnpm build

# E2E (both services must be running)
pnpm e2e
```

---

## 8. Test Configuration Files Summary

| File | Purpose | Key Settings |
|------|---------|--------------|
| `backend/pyproject.toml` | Backend deps & ruff config | py312, line-length=100, ruff rules (E,W,F,I,B,C4,UP) |
| `frontend/vite.config.ts` | Vitest environment | jsdom, globals=true, setupFiles |
| `frontend/tsconfig.json` | TypeScript strict mode | strict=true, checkJs=true, noUnused* |
| `playwright.config.ts` | Playwright setup | webServers, testDir, workers, reporters |
| `.pre-commit-config.yaml` | Git hooks | ruff, trailing-whitespace, file checks |
| `e2e/fixtures/auth.fixture.ts` | Playwright auth helper | dev bypass, board creation, timeout waits |

---

## 9. Quality Gate Summary

### 9.1 Pre-Commit Gates
- ✓ Trailing whitespace removal
- ✓ File ending fixes
- ✓ YAML validation
- ✓ Large file detection (1MB limit)
- ✓ Merge conflict detection
- ✓ Ruff formatting + linting (backend)

### 9.2 CI Gates (E2E Workflow)
- ✓ Backend pytest (38 tests)
- ✓ Frontend vitest (7 tests)
- ✓ Frontend TypeScript check
- ✓ Frontend production build
- ✓ E2E tests (13 scenarios) with 2x retry on CI
- ✓ Deploy depends on E2E success

### 9.3 Deployment Gate
- ✗ Manual approval NOT required
- ✓ Automatic deploy on E2E pass + main branch
- ✓ Docker Compose managed deployment

---

## 10. Recommendations for Improvement

1. **Increase Frontend Unit Test Coverage**
   - Add tests for InputBar, Canvas, Sidebar components
   - Test store logic (auth, websocket, boards, selection)
   - Use vitest coverage plugin: `pnpm add -D @vitest/coverage-v8`

2. **Add pytest Fixtures & conftest.py**
   - Centralize Dummy*Service mocks
   - Create database fixture for StateService
   - Reduce test boilerplate

3. **Enable Coverage Reports**
   - Backend: `pytest --cov=app --cov-report=html`
   - Frontend: `vitest --coverage`
   - Set minimum coverage thresholds (80%+)

4. **Add More E2E Edge Cases**
   - Test special questions flow
   - Test connection creation/deletion
   - Test real Auth0 integration (separate workflow)
   - Test error scenarios (network failures, timeouts)

5. **Improve WebSocket Stability**
   - Replace 500ms wait with explicit event polling
   - Add WebSocket connection assertion in fixture
   - Log WebSocket errors in E2E tests

6. **Add Browser Compatibility**
   - Expand Playwright projects: chromium, firefox, webkit
   - Add separate mobile config for responsive tests

7. **Test Migration Changes**
   - Add alembic upgrade/downgrade tests
   - Test data integrity across migrations

8. **Performance Testing**
   - Load test WebSocket with concurrent connections
   - Profile card rendering with 100+ cards
   - Benchmark AI decoder speed

---

## 11. Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Backend Tests | 38 | Good |
| Frontend Unit Tests | 7 | Minimal |
| E2E Tests | 13 | Good |
| **Total Tests** | **58** | **Moderate** |
| Code Quality Tools | 7 (ruff, TypeScript, pre-commit, pytest, vitest, Playwright, svelte-check) | Comprehensive |
| Coverage Tools | 0 | **Gap** |
| CI Retry Strategy | 2x on CI | Configured |
| Pre-Commit Hooks | 7 | Active |
| Deploy Gate | E2E pass | Automated |

---

**Report Generated:** 2026-03-06
**Reviewed Test Stack:** Python 3.12 (pytest, ruff), Node 20 (vitest, Playwright, TypeScript)
**Status:** Testing infrastructure is solid for happy-path coverage; frontend unit testing and code coverage metrics need enhancement.
