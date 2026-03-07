---
description: Backend architecture scan report.
status: done
---
# Backend Architecture Analysis - Fact Card System

**Scope:** `backend/app/`
**Framework:** FastAPI, Python 3.12, SQLite, OpenRouter API

## Service Architecture

```
FastAPI main.py (WebSocket /ws + REST /api/*)
  │ Auth guard (get_user_id)
  ▼
MainService (per-connection instance)
  │ init(), process_user_message(), handle_card_*, create/delete_connection
  ├──► StateService (singleton, SQLite)
  │     get/save/delete/list sessions
  ├──► AIService (singleton, OpenRouter / MockAIService)
  │     generate_response(), translate_q_hint()
  └──► SpecialQuestionsService (singleton)
        random_question(), get_question_by_id()

decoder.py (pure function)
  decode_ai_response() — parses AI JSON, normalizes coords, clamps values
```

## Key Data Models (Pydantic)

- **State**: session_id, user_id, locale, question, phase, cards[], connections[], pending_special_question, special_questions_history[]
- **Card**: id, text (max 200), type (6 enums), emoji, importance/confidence [0-1], x/y [0-1], pinned, width/height, custom_scale
- **Connection**: id, from_id, to_id, type (4 enums), strength [0-1], label, created_by
- **SessionPhase**: QUESTION → FACTS → PAINS → RESOURCES → GAPS → CONNECTIONS
- **CardType**: question, fact, pain, resource, hypothesis, todo
- **ConnectionType**: causes, relates, contradicts, blocks

## WebSocket Protocol

### Client → Server (11 types)
init, user_message, set_locale, clear_session, card_move, card_create, card_delete, card_update, special_question_request, connection_create, connection_delete

### Server → Client (11 types)
session_loaded, cards_add, cards_update, cards_delete, card_deleted, connections_add, connection_deleted, question_update, special_question_prompt, session_cleared, error

## REST API
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/health` | GET | No | Health check |
| `/api/sessions` | GET | Yes | List user sessions |
| `/api/sessions` | POST | Yes | Create session |
| `/api/sessions/{id}` | DELETE | Yes | Delete session |
| `/api/transcribe` | POST | Yes | Whisper transcription |

## AI Integration
- Model: google/gemini-3-flash-preview via OpenRouter
- System prompt: Kurpatov's Fact-Map methodology, Solar System positioning (1920x1080 canvas)
- Decoder normalizes: pixels → [0,1], text limits (100/50 chars), importance/confidence clamping
- MockAIService for E2E tests (AI_MOCK_MODE=true)
- Langsmith tracing on all AI calls

## Authentication
- Auth0 RS256 JWT (production): JWKS cached 1hr, verify audience/issuer
- Dev bypass: DEV_AUTH_BYPASS=true + token "dev-token" → user "dev-user"

## State Persistence
- SQLite table `sessions`: id, user_id, title, state_json (full State as JSON blob), created_at, updated_at
- JSON blob strategy: entire session state serialized/deserialized on each save/load
- No migrations, no relational schema for cards/connections

## Dependency Injection (construct.py)
- Singletons: state_service, ai_service (or mock), special_questions_service
- Per-connection: MainService instance created per WebSocket connection
- Environment-driven switching: AI_MOCK_MODE, DEV_AUTH_BYPASS

## Phase Progression Rules
- MIN_PUZZLEMENT_TURNS (3) before leaving QUESTION phase
- AI decides question_action: keep/next/clarify
- Phase order: QUESTION → FACTS → PAINS → RESOURCES → GAPS → CONNECTIONS

## Key Architectural Decisions
- Per-connection MainService (no shared mutable state)
- Pure function decoder boundary between LLM and domain
- JSON blob storage (simplicity over relational)
- Coordinate normalization at decoder level
