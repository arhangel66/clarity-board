---
description: Build, tooling, and CI scan report.
status: done
---
# S-01: Build & Tooling Configuration Report

## Backend (Python)
- **Package Manager**: `uv` (universal Python package manager)
- **Python Version**: 3.12+ required
- **Dependencies**: FastAPI 0.115.0+, uvicorn 0.34.0+, websockets 14.0, openai 1.60.0+, pydantic 2.10.0+, langsmith 0.6.4+
- **Dev Dependencies**: httpx 0.28.1+, pre-commit 4.5.1+, pytest 9.0.2+, ruff 0.14.14+
- **Linting**: Ruff (line-length=100, target py312) with E/W/F/I/B/C4/UP rules
- **Formatting**: Double quotes, 4-space indent via Ruff formatter
- **Build Tool**: Hatchling wheel backend

## Frontend (Node.js/TypeScript)
- **Package Manager**: pnpm v9 (verified in CI workflow)
- **Node Version**: 20 LTS (in CI workflow)
- **Build Tool**: Vite 6.0.7+
- **Framework**: Svelte 5.16.2+
- **TypeScript**: 5.7.3
- **CSS**: TailwindCSS 4.2.1+ via @tailwindcss/vite plugin
- **Testing**: Vitest 4.0.18 with @testing-library/svelte 5.3.1, jsdom environment
- **Type Checking**: svelte-check 4.1.4+
- **Auth**: @auth0/auth0-spa-js 2.1.3+

## Dependency Management
- **Backend**: uv.lock (frozen lockfile, deterministic builds)
- **Frontend**: pnpm-lock.yaml v9.0 (frozen-lockfile mode)
- **Root Level**: Single pnpm-lock.yaml for Playwright E2E tests (v9.0 format)

## Development Scripts (debug/)
- `start_all.sh` — Launches: Backend (port 8000, hot reload), Frontend (port 5173), Debug server (5656), Eval server (5657)
- `stop_all.sh` — Gracefully stops all services via pkill
- Logs written to `/tmp/` for inspection

## Docker Setup
- **Backend Dockerfile**: Python 3.12-slim, installs uv, builds with `uv sync --frozen --no-dev`, runs uvicorn on 8000
- **Frontend Dockerfile**: Multi-stage build (Node 20 Alpine -> nginx Alpine), pnpm install with frozen-lockfile, Vite build, nginx gzip compression
- **Compose**: Two services (backend, frontend) in shared `calend-network`, health checks enabled for backend
- **Volumes**: `fact_data` for SQLite persistence

## Nginx Configuration
- SPA routing (try_files -> index.html)
- API proxy to backend:8000/api/
- WebSocket support on /ws
- Gzip compression enabled
- Static asset caching (1 year, immutable)

## CI/CD Pipelines

### E2E Tests Workflow (.github/workflows/e2e.yml)
1. Checkout -> Node 20 setup -> pnpm 9
2. Install root + frontend dependencies
3. Python 3.12 setup -> install uv
4. Backend: `uv sync` -> `pytest -q`
5. Frontend: `pnpm test -- --run` -> `pnpm build` -> `pnpm check`
6. Install Playwright (Chromium only)
7. Run: `pnpm e2e` (with DEV_AUTH_BYPASS=true, AI_MOCK_MODE=true)
8. Upload artifacts on failure

### Deploy Workflow (.github/workflows/deploy.yml)
1. Triggered on E2E success, push to main
2. SSH rsync to 64.176.73.226:/opt/fact-card/
3. Create .env with production secrets
4. `docker compose down` -> `build --no-cache` -> `up -d`
5. Cleanup old images

## Playwright E2E Configuration
- Base URL: http://localhost:5173
- Test directory: ./e2e/tests
- Browser: Chromium only
- CI: 1 worker, 2 retries; Dev: parallel workers, no retries

## Pre-commit Hooks
- Standard: trailing whitespace, EOF fixer, YAML check, 1MB file limit, merge conflict check
- Ruff: --fix, format check on `backend/` files only

## Environment Variables
**Runtime**: OPENROUTER_API_KEY (required), OPENAI_API_KEY (optional Whisper), AUTH0_DOMAIN/AUDIENCE/ISSUER (prod auth), DEV_AUTH_BYPASS, AI_MOCK_MODE
**Frontend Build**: VITE_API_BASE, VITE_WS_BASE, VITE_AUTH0_* (passed as Docker build args)
