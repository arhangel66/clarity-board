---
description: Data layer and models scan report.
status: done
---
# Data Layer Analysis - Fact Card System

## Storage Strategy
**Document-oriented**: single SQLite table, entire session state as JSON blob.

### SQLite Schema
```sql
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  title TEXT,
  state_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX sessions_user_id_idx ON sessions(user_id);
```

### Benefits
- No N+1 queries (single read/write per session)
- Atomic state updates
- No migrations needed
- Simple backup (copy file)

### Trade-offs
- No relational queries across cards/connections
- Full state serialized on every save
- Not suitable for multi-user concurrent editing

## Core Models (Pydantic)

### Card
- id: str (generated)
- text: str (max 200 chars)
- type: CardType enum (question, fact, pain, resource, hypothesis, todo)
- emoji: str
- importance: float [0-1]
- confidence: float [0-1]
- x, y: float [0-1] (normalized canvas position)
- pinned: bool
- width, height: float | None
- custom_scale: float (default 1.0)

### Connection
- id: str
- from_id, to_id: str (card IDs)
- type: ConnectionType enum (causes, relates, contradicts, blocks)
- strength: float [0-1]
- label: str | None
- created_by: CreatedBy enum (user, ai)

### State
- session_id, user_id, locale: str
- question: str (central problem)
- phase: SessionPhase enum
- current_question, current_hint: str
- phase_index, puzzlement_turns: int
- cards: List[Card]
- connections: List[Connection]
- pending_special_question: SpecialQuestion | None
- special_questions_history: List[SpecialQuestionAnswer]

### SessionPhase (ordered)
QUESTION → FACTS → PAINS → RESOURCES → GAPS → CONNECTIONS

## Session Lifecycle
1. Create: generate ID → empty State → save JSON blob
2. Load: query by ID → deserialize JSON → hydrate Pydantic models
3. Modify: mutate State object → serialize → upsert
4. Delete: DELETE by ID + user_id ownership check
5. Reconnect: load existing session by ID, verify user ownership

## WebSocket Message Schemas

### Client → Server (13 types)
- init: {session_id?, auth_token, locale?}
- user_message: {text, special_question_id?}
- card_move: {card_id, x, y, pinned, width?, height?, custom_scale?}
- card_create: {text, type, x, y, emoji?, importance?, confidence?}
- card_delete: {card_id}
- card_update: {card_id, updates{}}
- connection_create: {from_id, to_id, type?, label?}
- connection_delete: {connection_id}
- special_question_request: {}
- set_locale: {locale}
- clear_session: {}

### Server → Client (11 types)
- session_loaded: {session: {id, question}}
- cards_add: {cards: [...]}
- cards_update: {updates: [...]}
- cards_delete: {card_ids: [...]}
- card_deleted: {card_id}
- connections_add: {connections: [...]}
- connection_deleted: {connection_id}
- question_update: {phase, question, hint, phaseIndex, special_questions_unlocked}
- special_question_prompt: {id, category_id, question, hint}
- session_cleared: {}
- error: {message}

## Validation Rules
- Card text: max 200 chars (frontend), 100/50 chars (AI decoder)
- importance/confidence: clamped [0, 1]
- Coordinates: clamped [0.05, 0.95] at decoder level
- Question card: protected from deletion
- Phase advancement: requires MIN_PUZZLEMENT_TURNS (3)
- User ownership: verified on session load

## Special Questions
- Source: backend/data/questions.json
- Structure: categories → questions (ru/en bilingual)
- Selection: random from unused, wraps around when exhausted
- History tracked in State.special_questions_history
