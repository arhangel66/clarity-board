# Clarity Board

A digital implementation of Kurpatov's "Fact-Card" methodology for externalizing thinking and revealing blind spots.

**Core principle:** One screen = one problem. No scrolling.

Users dump facts onto a single-screen canvas; AI assists in structuring, connecting, and finding patterns.

## Tech Stack

- **Backend:** FastAPI, Python 3.12, OpenAI API
- **Frontend:** Svelte 5, TypeScript, Vite
- **Database:** SQLite
- **Infrastructure:** Docker, nginx

## Quick Start

```bash
# Clone the repository
git clone git@github.com:mikhail/clarity-board.git
cd clarity-board

# Copy environment file and add your OpenAI API key
cp .env.example .env

# Run with Docker
docker-compose up --build
```

Access the application:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Development Setup

### Backend

```bash
cd backend
uv venv
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for AI-assisted card processing |

## Project Structure

```
clarity-board/
├── backend/           # FastAPI application
│   ├── app/           # Application code
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/          # Svelte application
│   ├── src/           # Source code
│   ├── Dockerfile
│   └── package.json
├── prototypes/        # HTML/JS visual prototypes
├── docker-compose.yml
└── .env.example
```

## Documentation

- `spec_fact_card.md` — Technical specification
- `card_data.md` — Methodology guide
- `example_session.md` — Step-by-step example session
- `ARCHITECTURE.md` — System architecture
