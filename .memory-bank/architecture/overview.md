---
description: System architecture overview (C4 L1-L2) — containers, services, data flow.
status: active
---
# Architecture Overview

See also: [guides/dev-setup.md](../guides/dev-setup.md) for HOW to run locally.

## C4 L1: System Context

```
[User] → [Fact Card App (fact.slotik.app)]
                │
                ├── [Auth0] (authentication)
                ├── [OpenRouter/Gemini] (AI chat completions)
                └── [OpenAI Whisper] (voice transcription, optional)
```

## C4 L2: Containers

```
┌─────────────────────────────────────────────────┐
│                  nginx (reverse proxy)           │
│  SPA routing, /api/ proxy, /ws proxy, gzip      │
├────────────────────┬────────────────────────────┤
│  Frontend (Svelte) │  Backend (FastAPI)          │
│  Port 3000 (prod)  │  Port 8000                  │
│  Port 5173 (dev)   │                             │
│                    │  ┌─────────────────────┐    │
│  Stores:           │  │ MainService (per-WS) │   │
│  - websocket       │  │ AIService (singleton) │   │
│  - cards           │  │ StateService (SQLite)  │  │
│  - auth            │  │ SpecialQuestions       │  │
│  - boards          │  └─────────────────────┘    │
│  - i18n            │                             │
│  - session         │  SQLite: fact_cards.db      │
└────────────────────┴────────────────────────────┘
```

## Service Architecture (Backend)

- **MainService** — per-WebSocket-connection orchestrator. Handles user messages, card operations, phase progression. NOT a singleton.
- **AIService** — singleton. Calls OpenRouter (Gemini) for chat completions. Returns raw JSON. Switchable to MockAIService via AI_MOCK_MODE.
- **StateService** — singleton. SQLite wrapper. Stores entire session state as JSON blob. CRUD for sessions.
- **SpecialQuestionsService** — singleton. Loads question deck from JSON file. Random selection with exclusion.
- **decoder.py** — pure function. Parses AI JSON response, normalizes coordinates (pixels → 0-1), clamps values, enforces text limits.

## Key Invariants
- One MainService instance per WebSocket connection (no shared mutable state)
- All state mutations go through StateService.save() (atomic JSON blob upsert)
- AI output passes through decoder before domain mutation (trust boundary)
- Session ownership verified on every load (user_id check)
- Phase cannot advance before MIN_PUZZLEMENT_TURNS (3) in question phase

## Data Flow (Main Loop)
```
User input → WebSocket → MainService.process_user_message()
  → AIService.generate_response() → OpenRouter API
  → decoder.decode_ai_response() → AIResponse (trusted)
  → Apply operations (create/update/delete cards)
  → Phase advancement check
  → StateService.save() → SQLite
  → WebSocket responses → Frontend stores → UI update
```

## Coordinate System
- **AI prompt**: absolute pixels (1920x1080 canvas model)
- **Backend storage**: normalized [0, 1]
- **Decoder**: converts pixels → [0, 1], clamps to [0.05, 0.95]
- **Frontend**: 0-100 percentage (multiply by 100)
