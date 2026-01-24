# Backend Architecture Deep Dive

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Frontend (Svelte)                         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ WebSocket
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         main.py (FastAPI)                           │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │ConnectionManager│  │  SessionState    │  │ Message Handlers  │  │
│  │ (WS connections)│  │ (phase, question)│  │ (init, message,   │  │
│  └────────┬────────┘  └────────┬─────────┘  │  card_move)       │  │
│           │                    │            └─────────┬─────────┘  │
└───────────┼────────────────────┼──────────────────────┼────────────┘
            │                    │                      │
            │    ┌───────────────┴──────────────────────┘
            │    │
            ▼    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         construct.py (DI)                           │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ ai_service │  │card_service │  │embedding_svc │  │  database │  │
│  └──────┬─────┘  └──────┬──────┘  └──────┬───────┘  └─────┬─────┘  │
└─────────┼───────────────┼────────────────┼────────────────┼────────┘
          │               │                │                │
          ▼               ▼                ▼                ▼
    ┌──────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
    │OpenRouter│   │  Business  │   │  OpenAI    │   │   SQLite   │
    │ (Gemini) │   │   Logic    │   │ Embeddings │   │     DB     │
    └──────────┘   └────────────┘   └────────────┘   └────────────┘
```

---

## Classes

### 1. ConnectionManager (main.py:109)

**Purpose:** Manages WebSocket connections and session state.

```python
class ConnectionManager:
    active_connections: dict[str, WebSocket]  # connection_id -> WebSocket
    session_map: dict[str, str]               # connection_id -> session_id
    session_states: dict[str, SessionState]   # connection_id -> SessionState

    async def connect(ws, connection_id)      # Accept WS, store in active_connections
    def disconnect(connection_id)             # Remove from all dicts
    def set_session(connection_id, session_id)
    def get_session(connection_id) -> str | None
    def get_session_state(connection_id) -> SessionState | None
    def create_session_state(connection_id, phase) -> SessionState
    async def send_message(connection_id, message: dict)
```

**Key:** One global `manager` instance for all connections.

---

### 2. SessionState (main.py:55)

**Purpose:** In-memory state for guided flow (phase, current question).

```python
class SessionState:
    phase: SessionPhase          # QUESTION, FACTS, PAINS, RESOURCES, GAPS, CONNECTIONS
    current_question: str        # "What are the concrete facts?"
    current_hint: str            # "Numbers, dates, events..."
    phase_index: int             # 0-5
```

**Key:** Initialized from `DEFAULT_QUESTIONS[phase]`. Updated when AI says `question_action: "next"`.

---

### 3. AIService (services/ai_service.py:99)

**Purpose:** Send user message to LLM, parse response into operations.

```python
class AIService:
    client: OpenAI               # OpenRouter client
    model: str                   # "google/gemini-3-flash-preview"

    async def process_user_message(
        message: str,
        phase: SessionPhase,
        current_question: str,
        session_question: str,
        existing_cards_texts: list[str]
    ) -> AIResponse

    def _parse_response(content: str) -> AIResponse
```

**Flow:**
```
User text + context  ──►  LLM (Gemini)  ──►  JSON response  ──►  AIResponse
                          │
                          └── SYSTEM_PROMPT: "You are a fact-card therapy assistant..."
```

**Output:** `AIResponse` with:
- `operations`: list of create_card, create_connection, ask_question
- `question_action`: KEEP | NEXT | CLARIFY
- `next_question`, `next_hint`

---

### 4. CardService (services/card_service.py:22)

**Purpose:** CRUD for cards/sessions + processing AI response.

```python
class CardService:
    db: Database
    embedding_service: EmbeddingService

    # Session
    def create_session(question: str) -> Session
    def get_session(session_id: str) -> Session | None

    # Card
    async def create_card_from_ai_operation(session_id, operation, existing_cards) -> Card
    def update_card(update: CardUpdate)
    def get_cards_by_session(session_id) -> list[Card]

    # Connection
    def create_connection_from_ai_operation(session_id, operation, existing_cards) -> Connection | None

    # Main entry point for AI
    async def process_ai_response(session_id, ai_response) -> (new_cards, new_connections, questions)
```

**`process_ai_response` flow:**
```
AIResponse.operations ──► for each operation:
    create_card      ──► get embedding ──► calculate position ──► save to DB
    create_connection──► find cards by text ──► save to DB
    ask_question     ──► collect for UI
```

---

### 5. EmbeddingService (services/embedding_service.py:13)

**Purpose:** Generate embeddings + smart card positioning.

```python
class EmbeddingService:
    client: OpenAI               # OpenAI client for embeddings
    model: str                   # "text-embedding-3-small"

    async def get_embedding(text: str) -> list[float]  # 1536-dim vector
    def cosine_similarity(emb1, emb2) -> float
    def find_similar_cards(new_embedding, existing_cards, top_k=3) -> list[Card]
    def get_position_for_new_card(new_embedding, existing_cards) -> (x, y)
```

**Positioning algorithm:**
```
new card embedding ──► find 3 most similar cards ──► centroid of their positions
                                                      + random offset
                                                      + collision avoidance
```

---

### 6. Database (database.py:12)

**Purpose:** SQLite persistence.

```python
class Database:
    db_path: Path

    # Session
    def create_session(session: Session) -> Session
    def get_session(session_id) -> Session | None
    def update_session_phase(session_id, phase)
    def update_session_timestamp(session_id)

    # Card
    def create_card(session_id, card: Card) -> Card
    def get_cards_by_session(session_id) -> list[Card]
    def update_card(card_id, updates: dict)
    def get_card_by_id(card_id) -> Card | None
    def find_card_by_text(session_id, text) -> Card | None
    def get_root_card(session_id) -> Card | None

    # Connection
    def create_connection(session_id, connection) -> Connection
    def get_connections_by_session(session_id) -> list[Connection]
```

**Tables:**
- `sessions` (id, question, phase, created_at, updated_at)
- `cards` (id, session_id, text, type, emoji, x, y, ..., embedding)
- `connections` (id, session_id, from_id, to_id, type, strength)

---

## Dependency Injection (construct.py)

```python
# API Clients
openai_client = wrap_openai(OpenAI(api_key=OPENAI_API_KEY))
openrouter_client = wrap_openai(OpenAI(api_key=OPENROUTER_API_KEY, base_url="..."))

# Services
database = Database(db_path="fact_cards.db")
embedding_service = EmbeddingService(openai_client=openai_client)
ai_service = AIService(openrouter_client=openrouter_client)
card_service = CardService(database=database, embedding_service=embedding_service)
```

**Dependency Graph:**
```
openai_client ────────────────────────►  EmbeddingService
                                                │
openrouter_client ─────────────────────►  AIService
                                                │
Database ─────────────────────────────────────────────────►  CardService
                                         ▲                        │
                                         │                        │
                                   EmbeddingService ◄─────────────┘
```

---

## Data Flow: User Message

```
1. Frontend sends: { type: "user_text", payload: { text: "I work 60 hours" } }
                                    │
                                    ▼
2. main.py: handle_user_text(connection_id, payload)
   │
   ├── No session? ──► card_service.create_session(text) ──► DB
   │
   ├── Get existing cards: session.cards ──► existing_texts = ["card1", "card2"]
   │
   └── ai_service.process_user_message(
   │       message=text,
   │       phase=state.phase,           # FACTS
   │       current_question="What facts?",
   │       session_question="Work-life balance",
   │       existing_cards_texts=existing_texts
   │   )
   │           │
   │           ▼
   │   3. AIService: build context ──► LLM ──► parse JSON ──► AIResponse
   │       operations: [
   │           { type: "create_card", card: { text: "Work 60h/week", type: "fact" } }
   │           { type: "create_connection", connection: { from: "Work 60h", to: "root" } }
   │       ]
   │       question_action: "keep"
   │       next_question: "What else?"
   │           │
   │           ▼
   └── card_service.process_ai_response(session_id, ai_response)
           │
           ├── create_card_from_ai_operation:
           │       embedding_service.get_embedding("Work 60h/week") ──► OpenAI
           │       embedding_service.get_position_for_new_card(emb, existing)
           │       database.create_card(session_id, card)
           │
           └── create_connection_from_ai_operation:
                   _find_card_by_text(cards, "Work 60h")
                   _find_root_card(cards)
                   database.create_connection(session_id, connection)
                       │
                       ▼
4. main.py sends WebSocket messages:
   { type: "cards_add", payload: { cards: [...] } }
   { type: "connections_add", payload: { connections: [...] } }
   { type: "question_update", payload: { phase: "facts", question: "What else?" } }
```

---

## Phase Transitions

```
QUESTION ──► FACTS ──► PAINS ──► RESOURCES ──► GAPS ──► CONNECTIONS
   0           1         2           3           4           5
```

**Triggered by:** `ai_response.question_action == QuestionAction.NEXT`

```python
# main.py:441
if ai_response.question_action == QuestionAction.NEXT:
    current_index = PHASE_ORDER.index(state.phase)
    if current_index < len(PHASE_ORDER) - 1:
        next_phase = PHASE_ORDER[current_index + 1]
        state.phase = next_phase
        state.phase_index = current_index + 1
        state.current_question, state.current_hint = DEFAULT_QUESTIONS[next_phase]
        card_service.db.update_session_phase(session_id, next_phase.value)  # Persist
```

---

## Models (models.py)

### Core Entities

```python
class Session:
    id: str
    question: str           # Central problem
    phase: SessionPhase     # Current phase
    cards: list[Card]
    connections: list[Connection]

class Card:
    id: str
    text: str               # Summarized text (max 200 chars)
    type: CardType          # question, fact, pain, resource, hypothesis
    emoji: str
    color: str              # Derived from type
    importance: float       # 0-1
    confidence: float       # 0-1
    x, y: float             # Position 0-1
    target_x, target_y: float
    pinned: bool
    is_root: bool
    embedding: list[float]  # 1536-dim vector

class Connection:
    id: str
    from_id: str
    to_id: str
    type: ConnectionType    # causes, relates, contradicts, blocks
    strength: float         # 0-1
```

### AI Response Models

```python
class AIResponse:
    operations: list[AIOperationCreateCard | AIOperationCreateConnection | AIOperationAskQuestion]
    question_action: QuestionAction  # KEEP, NEXT, CLARIFY
    next_question: str | None
    next_hint: str | None

class AIOperationCreateCard:
    type: Literal["create_card"]
    card: CardCreate        # text, type, emoji, importance, confidence

class AIOperationCreateConnection:
    type: Literal["create_connection"]
    connection: ConnectionCreate  # from_text, to_text, type, strength
```

---

## WebSocket Protocol

### Client → Server

| Type | Payload | Handler |
|------|---------|---------|
| `session_init` | `{ session_id?: string }` | `handle_init` |
| `user_text` | `{ text: string }` | `handle_user_text` |
| `card_move` | `{ card_id, x, y, pinned }` | `handle_card_move` |

### Server → Client

| Type | Payload |
|------|---------|
| `session_loaded` | `{ session: { id, question } }` |
| `cards_add` | `{ cards: Card[] }` |
| `connections_add` | `{ connections: Connection[] }` |
| `cards_update` | `{ updates: CardUpdate[] }` |
| `question_update` | `{ phase, question, hint, phaseIndex }` |
| `error` | `{ message: string }` |

---

## File Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, WebSocket, handlers
│   ├── construct.py         # Dependency injection
│   ├── models.py            # Pydantic models, enums
│   ├── database.py          # SQLite operations
│   └── services/
│       ├── ai_service.py    # LLM integration
│       ├── card_service.py  # Business logic
│       └── embedding_service.py  # Embeddings & positioning
├── cli.py                   # CLI for testing AI logic
└── fact_cards.db            # SQLite database
```

---

## Call Graph (Simplified)

```
websocket_endpoint
    │
    ├── handle_init
    │       └── card_service.get_session
    │               └── database.get_session
    │
    └── handle_user_text
            │
            ├── card_service.create_session (if new)
            │       └── database.create_session
            │
            ├── ai_service.process_user_message
            │       └── openrouter_client.chat.completions.create
            │
            └── card_service.process_ai_response
                    │
                    ├── create_card_from_ai_operation
                    │       ├── embedding_service.get_embedding
                    │       │       └── openai_client.embeddings.create
                    │       ├── embedding_service.get_position_for_new_card
                    │       └── database.create_card
                    │
                    └── create_connection_from_ai_operation
                            ├── _find_card_by_text
                            └── database.create_connection
```
