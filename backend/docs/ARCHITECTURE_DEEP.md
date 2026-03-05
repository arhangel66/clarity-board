# Backend Architecture Deep Dive

Last updated: 2026-03-05

Architecture execution plan: `ARCHITECTURE_PLAN.md` (repository root).

## 1) High-Level Backend Graph

```text
Frontend (Svelte)
   │
   │ WebSocket /ws + REST /api/*
   ▼
main.py (transport + handlers)
   │
   ▼
MainService (orchestration, per connection)
   │              │
   │              ├── AIService (LLM call)
   │              └── SpecialQuestionsService (curated prompts)
   │
   ▼
StateService (SQLite, state_json blob)
```

## 2) Module Responsibilities

## `main.py`

- Owns API surface (WebSocket and REST)
- Validates basic request shape
- Applies auth checks (`get_user_id`)
- Delegates domain actions to `MainService`
- Emits websocket events back to client

## `MainService`

- Keeps connection-scoped state (`session_id`, `state`, `user_id`, `locale`)
- Handles session init/new-session/reset
- Orchestrates AI operations (create/update/delete cards)
- Applies phase/question transitions
- Persists every state mutation through `StateService`

## `StateService`

- Owns SQLite schema init and compatibility columns
- Stores session state as JSON blob (`state_json`)
- Supports load/list/delete/upsert operations
- Performs model serialization/deserialization

## `AIService`

- Builds prompt context from current state
- Calls OpenRouter model (`google/gemini-3-flash-preview`)
- Returns raw JSON for decoder stage

## `decoder.py`

- Converts raw AI JSON into trusted operation objects
- Provides a safe boundary between LLM output and domain mutation

## `special_questions.py`

- Returns locale-aware curated prompts
- Supports random selection with exclusion list

## 3) WebSocket Contract

## Client -> Server

- `init`
- `user_message`
- `set_locale`
- `clear_session`
- `card_move`
- `card_create`
- `card_delete`
- `card_update`
- `special_question_request`
- `connection_create`
- `connection_delete`

## Server -> Client

- `session_loaded`
- `cards_add`
- `cards_update`
- `cards_delete`
- `card_deleted`
- `connections_add`
- `connection_deleted`
- `question_update`
- `special_question_prompt`
- `session_cleared`
- `error`

## 4) REST Contract

- `GET /api/health`
- `GET /api/sessions` (auth required)
- `POST /api/sessions` (auth required)
- `DELETE /api/sessions/{session_id}` (auth required)
- `POST /api/transcribe` (auth required, requires `OPENAI_API_KEY`)

## 5) Session Lifecycle

## Init

1. Client sends `init` with optional `session_id` and `auth_token`.
2. Backend resolves `user_id` from token.
3. `MainService.init(...)` loads session or creates new state.
4. Backend returns `session_loaded` plus snapshot events.

## Message processing

1. Client sends `user_message`.
2. `MainService.process_user_message(...)` ensures state exists.
3. `AIService.generate_response(...)` returns raw JSON.
4. `decode_ai_response(...)` parses operations.
5. Service applies operations to cards/connections.
6. Service updates phase/question metadata.
7. Service saves state.
8. Backend emits delta events.

## Manual operations

- Card move/create/update/delete go directly through dedicated handlers and persist immediately.
- Connection create/delete similarly mutate and persist.

## 6) Persistence Details

SQLite table: `sessions`

- `id TEXT PRIMARY KEY`
- `user_id TEXT`
- `title TEXT`
- `state_json TEXT NOT NULL`
- `created_at TEXT NOT NULL`
- `updated_at TEXT NOT NULL`

Indexes:

- `sessions_user_id_idx ON sessions(user_id)`

State blob currently contains:

- question/phase/hint metadata
- full cards list
- full connections list
- locale
- pending special question
- special questions history

## 7) Auth Model

- WebSocket: token comes in payload (`auth_token`) on `init`
- REST: bearer token in `Authorization` header
- Backend uses `app.auth.get_user_id(...)`
- `StateService.get_for_user(...)` enforces ownership checks

## 8) Reliability Notes

Current strengths:

- Clear transport/orchestration split
- Persistent state on each mutation
- User-scoped session access checks

Current gaps:

- No formal websocket schema versioning policy
- No standardized migration framework (legacy ad-hoc scripts exist)
- Backup/restore runbook still missing
- Observability is log-centric; metrics and alerting are minimal

## 9) Operational Paths

## Health

- Liveness endpoint: `GET /api/health`

## Deploy path in practice

- Manual deploy workflow currently defined by:
  - `/Users/mikhail/w/learning/fact/.claude/skills/deploy`

## 10) Architecture Work Queue

See `ARCHITECTURE_PLAN.md` milestones A1-A6.
