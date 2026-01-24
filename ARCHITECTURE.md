# Fact Card System - Architecture Plan

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + WebSocket |
| Frontend | Svelte 5 + TypeScript + Vite |
| AI | OpenAI gpt-5-mini-2025-08-07 |
| Embeddings | OpenAI text-embedding-3-small + UMAP |
| Database | SQLite (via sqlite3) |
| Package Manager | uv (Python), pnpm (Node) |

---

## Project Structure

```
fact/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models.py            # Pydantic models (Card, Connection, etc)
│   │   ├── database.py          # SQLite connection & schema
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py    # OpenAI chat completions
│   │   │   ├── embedding_service.py  # Embeddings + UMAP projection
│   │   │   └── card_service.py  # Card/Connection CRUD
│   │   └── construct.py         # DI container (services instantiation)
│   ├── .env                     # OPENAI_API_KEY
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── Canvas.svelte       # Main canvas with cards
│   │   │   │   ├── Card.svelte         # Single draggable card
│   │   │   │   ├── ChatPanel.svelte    # Right panel for input
│   │   │   │   └── Connections.svelte  # SVG layer for lines
│   │   │   ├── stores/
│   │   │   │   ├── cards.ts            # Svelte store for cards state
│   │   │   │   └── websocket.ts        # WebSocket client
│   │   │   └── types.ts                # TypeScript interfaces
│   │   ├── App.svelte
│   │   └── main.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── prototypes/                  # Existing HTML prototypes (reference)
├── spec_fact_card.md           # Specification
└── CLAUDE.md
```

---

## Data Models

### Card
```python
class Card(BaseModel):
    id: str                      # UUID
    text: str                    # Max ~100 chars
    type: Literal["question", "fact", "pain", "resource", "hypothesis"]
    emoji: str                   # 1-2 emoji
    color: str                   # Hex color
    importance: float            # 0-1, affects size
    confidence: float            # 0-1, affects color intensity
    x: float                     # 0-1 normalized position
    y: float                     # 0-1 normalized position
    target_x: float              # From embedding projection
    target_y: float
    pinned: bool                 # User-positioned
    is_root: bool                # Central question
    is_new: bool                 # For highlight animation
    created_at: datetime
```

### Connection
```python
class Connection(BaseModel):
    id: str
    from_id: str
    to_id: str
    type: Literal["causes", "relates", "contradicts", "blocks"]
    strength: float              # 0-1
    label: str | None
    created_by: Literal["ai", "user"]
```

### Session
```python
class Session(BaseModel):
    id: str
    question: str                # Central problem
    cards: list[Card]
    connections: list[Connection]
    created_at: datetime
    updated_at: datetime
```

---

## WebSocket Protocol

### Client → Server

```typescript
// User sends a message
{
  "type": "user_message",
  "payload": {
    "text": "Я сплю по 5 часов"
  }
}

// User drags a card
{
  "type": "card_move",
  "payload": {
    "card_id": "card_001",
    "x": 0.35,
    "y": 0.42,
    "pinned": true
  }
}

// User starts a new session
{
  "type": "new_session",
  "payload": {
    "question": "Почему я работаю по 12 часов?"
  }
}
```

### Server → Client

```typescript
// Add new card(s)
{
  "type": "cards_add",
  "payload": {
    "cards": [Card, Card, ...]
  }
}

// Update existing card(s)
{
  "type": "cards_update",
  "payload": {
    "updates": [
      { "id": "card_001", "importance": 0.9, "x": 0.4 },
      ...
    ]
  }
}

// Add connection(s)
{
  "type": "connections_add",
  "payload": {
    "connections": [Connection, ...]
  }
}

// AI asks clarifying question (not a card, just chat)
{
  "type": "ai_question",
  "payload": {
    "text": "Это факт или ваше предположение?"
  }
}

// Recalculated positions (after UMAP)
{
  "type": "positions_update",
  "payload": {
    "positions": [
      { "id": "card_001", "target_x": 0.3, "target_y": 0.5 },
      ...
    ]
  }
}
```

---

## AI Prompt Strategy

### System Prompt (for card creation)

```
You are a fact-card therapy assistant based on Kurpatov's methodology.

Your role:
1. Convert user input into concrete FACTS, not abstractions
2. If user gives an abstraction ("I'm tired"), ask for specifics
3. For each valid fact, determine: type, emoji, importance, confidence
4. Propose connections between cards when you see relationships
5. Periodically ask about "empty zones" - what's missing?

Card types:
- fact (blue): Concrete, verifiable events/data
- pain (red): Problems, tensions, fears
- resource (green): Assets, helpers, opportunities
- hypothesis (yellow): Unverified assumptions

Output format: JSON with operations to perform.
```

### Response Format

```json
{
  "operations": [
    {
      "type": "create_card",
      "card": {
        "text": "Сплю 5 часов в сутки",
        "type": "fact",
        "emoji": "😴",
        "importance": 0.7,
        "confidence": 1.0
      }
    },
    {
      "type": "create_connection",
      "connection": {
        "from_text": "Сплю 5 часов",
        "to_text": "root",
        "type": "causes",
        "strength": 0.8
      }
    },
    {
      "type": "ask_question",
      "text": "Как давно это началось?"
    }
  ]
}
```

---

## Embedding & Positioning

### Key Principle
**Existing cards do NOT move when new card is added.**
Only the new card gets positioned. Existing cards stay where they are.

### Flow
1. When new card created → get embedding from OpenAI
2. Find semantically similar existing cards (cosine similarity)
3. Position new card near similar cards, avoiding collisions
4. Existing cards remain at their positions
5. Animate only the new card appearing

### Position Algorithm for New Card
```python
def get_position_for_new_card(new_embedding, existing_cards):
    if not existing_cards:
        # First card (root) goes to center
        return (0.5, 0.5)

    # Find top 3 similar cards by cosine similarity
    similar = find_similar_cards(new_embedding, existing_cards, top_k=3)

    # Calculate centroid of similar cards
    cx = mean([c.x for c in similar])
    cy = mean([c.y for c in similar])

    # Add offset to avoid overlap
    angle = random.uniform(0, 2*pi)
    offset = 0.1  # 10% of canvas

    new_x = clamp(cx + cos(angle) * offset, 0.05, 0.95)
    new_y = clamp(cy + sin(angle) * offset, 0.05, 0.95)

    # Collision detection - shift if overlaps
    return avoid_collisions(new_x, new_y, existing_cards)
```

### Python Dependencies
- `openai` - embeddings API
- `umap-learn` - dimensionality reduction
- `numpy` - array operations

---

## Implementation Phases

### Phase 1: Backend Foundation
- [x] Project structure
- [ ] SQLite schema & connection
- [ ] Pydantic models
- [ ] Basic WebSocket endpoint
- [ ] Card CRUD service

### Phase 2: AI Integration
- [ ] OpenAI client setup
- [ ] System prompt engineering
- [ ] Message → card operations parsing
- [ ] Embedding generation

### Phase 3: Frontend Core
- [ ] Svelte project setup with Vite
- [ ] WebSocket store
- [ ] Cards store
- [ ] Canvas component (from prototype 3)
- [ ] Card component with drag

### Phase 4: Integration
- [ ] Connect frontend ↔ backend
- [ ] Real-time card updates
- [ ] Connection rendering
- [ ] Position animations

### Phase 5: Positioning Engine
- [ ] UMAP integration
- [ ] Position recalculation on new cards
- [ ] Smooth animations to target positions

### Phase 6: Polish
- [ ] Error handling
- [ ] Loading states
- [ ] Session persistence
- [ ] Mobile responsiveness

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| WS | `/ws` | Main WebSocket connection |
| GET | `/api/session/{id}` | Load existing session |
| POST | `/api/session` | Create new session |
| GET | `/api/health` | Health check |

---

## Environment Variables

```env
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./fact_cards.db
```

---

## Run Commands

```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload

# Frontend
cd frontend
pnpm dev

# Full stack (with concurrently)
pnpm dev:all
```
