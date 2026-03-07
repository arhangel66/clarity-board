# Fact Card System

Digital workspace for structured thinking based on the fact-card methodology. The product keeps one problem on one screen and uses AI to help users turn vague thoughts into cards, links, blind spots, and action items.

Live product: [fact.slotik.app](https://fact.slotik.app/)

## Status

- MVP is shipped and usable end-to-end
- Current focus is launch readiness, onboarding, reliability, and monetization experiments
- Canonical project docs live in `.memory-bank/`

## Tech Stack

- **Backend:** FastAPI, WebSocket, Python 3.12, `uv`
- **Frontend:** Svelte 5, TypeScript, Tailwind CSS v4, Vite, `pnpm`
- **Storage:** SQLite
- **AI:** OpenRouter for chat completions, OpenAI Whisper for transcription
- **Auth:** Auth0 with optional local dev bypass
- **Testing:** pytest, Vitest, Playwright
- **Infra:** Docker, nginx, GitHub Actions

## Repository Layout

```text
fact/
├── backend/        # FastAPI app, services, tests
├── frontend/       # Svelte app, stores, UI components
├── e2e/            # Playwright end-to-end tests
├── debug/          # Local multi-service dev scripts
├── .memory-bank/   # Product, architecture, backlog, guides
├── .protocols/     # Long-running plans and decision logs
└── docker-compose.yml
```

## Local Development

### Prerequisites

- Python 3.12+
- `uv`
- Node.js 20+
- `pnpm`

### Recommended setup

```bash
cp .env.example .env
./debug/start_all.sh
```

Then open:

- Frontend: `http://localhost:5173?dev=1`
- Backend API: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

`?dev=1` enables the frontend auth bypass. The backend side of that bypass is enabled by `DEV_AUTH_BYPASS=true`, which `./debug/start_all.sh` sets automatically.

### Manual startup

Backend:

```bash
cd backend
uv sync
DEV_AUTH_BYPASS=true uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend:

```bash
cd frontend
pnpm install
pnpm dev
```

## Environment

Core variables:

- `OPENROUTER_API_KEY`: required for backend startup in the current implementation
- `OPENAI_API_KEY`: optional, enables Whisper transcription endpoint
- `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, `AUTH0_ISSUER`: required when using real Auth0 instead of dev bypass

Useful local flags:

- `DEV_AUTH_BYPASS=true`: backend accepts the special `dev-token`
- `AI_MOCK_MODE=true`: uses `MockAIService` for deterministic responses
- `VITE_API_BASE`, `VITE_WS_BASE`: override frontend backend endpoints
- `VITE_AUTH0_DOMAIN`, `VITE_AUTH0_CLIENT_ID`, `VITE_AUTH0_AUDIENCE`, `VITE_AUTH0_REDIRECT_URI`: frontend Auth0 config

## Quality Gates

```bash
./debug/start_all.sh

cd backend && uv run pytest -v
cd frontend && pnpm test -- --run
cd frontend && pnpm build && pnpm check
pnpm e2e
cd backend && pre-commit run --all-files
```

## Docker

`docker-compose.yml` is currently deployment-oriented, not the easiest local entrypoint:

- it expects an external Docker network named `calend2_calend-network`
- it uses `expose`, not local `ports`, so services are not published to `localhost` by default

For day-to-day local work, prefer `./debug/start_all.sh`.

## Documentation

- `.memory-bank/index.md`: main documentation router
- `.memory-bank/product.md`: product brief
- `.memory-bank/architecture/overview.md`: system architecture
- `.memory-bank/guides/dev-setup.md`: development guide
- `prd.md`: current product requirements draft
