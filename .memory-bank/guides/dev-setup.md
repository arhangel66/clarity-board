---
description: HOW to set up and run the project locally.
status: active
---
# Development Setup Guide

See also: [architecture/overview.md](../architecture/overview.md) for WHAT/WHY.

## Prerequisites
- Python 3.12+, `uv` package manager
- Node.js 20 LTS, `pnpm` v9
- macOS / Linux

## Quick Start (all services)
```bash
./debug/start_all.sh    # Backend (8000), Frontend (5173), Debug (5656), Eval (5657)
./debug/stop_all.sh     # Stop all
```

## Backend
```bash
cd backend
uv sync                                    # Install deps
uv run uvicorn app.main:app --reload       # Dev server (port 8000)
```

## Frontend
```bash
cd frontend
pnpm install                               # Install deps
pnpm dev                                   # Dev server (port 5173)
```

## Docker (full stack)
```bash
docker-compose up --build                  # Frontend: 3000, Backend: 8000
```

## Environment (.env)
Required: `OPENROUTER_API_KEY`
Optional: `OPENAI_API_KEY`, `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, `DEV_AUTH_BYPASS=true`, `AI_MOCK_MODE=true`
Frontend: `VITE_API_BASE`, `VITE_WS_BASE`, `VITE_AUTH0_*`

## Dev Auth Bypass
Set `DEV_AUTH_BYPASS=true` on backend, use `?dev=1` URL param on frontend. Token: `"dev-token"`, user: `"dev-user"`.

## Linting
```bash
cd backend && pre-commit run --all-files   # Ruff (line-length=100, py312)
```

## Testing
```bash
# Backend
cd backend && uv run pytest -v

# Frontend
cd frontend && pnpm test -- --run

# E2E (requires DEV_AUTH_BYPASS=true, AI_MOCK_MODE=true)
pnpm e2e
```

## Deploy
Automatic via GitHub Actions: push to main → E2E pass → SSH rsync → docker compose rebuild on VPS.
