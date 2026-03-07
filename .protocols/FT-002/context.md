# FT-002 Context

## Loaded docs
- `.memory-bank/features/FT-002-analytics.md` — acceptance criteria
- `.memory-bank/tasks/backlog.md` — task in W1, status: planned
- `frontend/index.html` — no analytics scripts yet
- `frontend/src/lib/stores/websocket.ts` — all WS message types
- `frontend/src/lib/stores/cards.ts` — card CRUD
- `backend/app/main.py` — WebSocket handlers, REST endpoints
- `backend/app/services/main_service.py` — per-connection orchestrator
- `backend/app/construct.py` — DI container

## Current state
- Zero analytics code in the project
- Langsmith tracing exists for AI calls only
- Frontend: Svelte 5 SPA, no routing
- Backend: FastAPI + WebSocket, SQLite JSON blob storage
