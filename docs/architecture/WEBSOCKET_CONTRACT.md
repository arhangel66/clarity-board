# WebSocket Contract

Last updated: 2026-03-15

## Versioning Policy

- Current protocol version: `1`.
- Version is considered backward-compatible inside major version `1` when:
  - existing message types keep required fields unchanged,
  - added fields are optional,
  - added message types do not break unknown-message handling.
- Any removal or required-field change increments major version.

## Compatibility Rules

- Server must tolerate missing optional client fields.
- Client must ignore unknown server message types.
- Server error envelope remains stable:
  - `{ "type": "error", "payload": { "message": string } }`

## Message Envelope

All messages follow the format:

```json
{ "type": "<message_type>", "payload": { ... } }
```

## Client -> Server Messages

### `init`

Initialize or resume a session. First message after WebSocket connect.

```typescript
payload: {
  session_id?: string;    // Resume existing session; omit for new
  auth_token?: string;    // JWT (Auth0) or "dev-token" in dev mode
  locale?: "ru" | "en";   // UI language, default "ru"
  email?: string;         // User email (for analytics/display)
  name?: string;          // User display name
}
```

Server responds with `session_loaded` + `question_update`. If the session has
existing cards/connections, also sends `cards_add` and `connections_add`.

### `user_message`

Send text input for AI processing.

```typescript
payload: {
  text: string;                  // User input text (max 200 chars enforced by frontend)
  special_question_id?: string;  // If answering a special question
}
```

Server responds with a combination of: `session_loaded` (if new session created),
`cards_add`, `cards_update`, `cards_delete`, `question_update`.
May respond with `error` (code `access_exhausted`) if quota exceeded.

### `set_locale`

Change UI language. Triggers retranslation of question/hint.

```typescript
payload: {
  locale: "ru" | "en";
}
```

Server responds with `question_update` containing translated question and hint.

### `clear_session`

Reset the current session to blank state.

```typescript
payload: {}
```

Server responds with `session_cleared`.

### `card_move`

Update card position and visual properties.

```typescript
payload: {
  card_id: string;
  x: number;              // Normalized 0..1
  y: number;              // Normalized 0..1
  pinned: boolean;        // Lock card position
  width?: number;         // Card width (pixels)
  height?: number;        // Card height (pixels)
  custom_scale?: number;  // Scale multiplier (default 1.0)
}
```

Server responds with `cards_update` echoing the applied position.

### `card_create`

Create a card manually (user-initiated, not via AI).

```typescript
payload: {
  text: string;                                                  // Card text
  type: "question"|"fact"|"pain"|"resource"|"hypothesis"|"todo"; // Card type
  x: number;                                                     // Normalized 0..1
  y: number;                                                     // Normalized 0..1
  emoji?: string;                                                // Emoji icon
  importance?: number;                                           // 0..1 (default 0.5)
  confidence?: number;                                           // 0..1 (default 0.8)
}
```

Server responds with `cards_add` (single card) or `error`.

### `card_update`

Update card text or metadata.

```typescript
payload: {
  card_id: string;
  updates: {
    text?: string;        // New text (truncated: 100 chars for question, 50 for others)
    importance?: number;  // 0..1, clamped
    confidence?: number;  // 0..1, clamped
    emoji?: string;       // Max 4 chars
  }
}
```

Server responds with `cards_update` containing only changed fields + `id`.
Silent return if card not found or no valid updates (see KNOWN_ISSUES.md SILENT-002).

### `card_delete`

Delete a card and its connections.

```typescript
payload: {
  card_id: string;
}
```

Server responds with `card_deleted`. Silent if card not found (see KNOWN_ISSUES.md SILENT-003).

### `connection_create`

Create a link between two cards.

```typescript
payload: {
  from_id: string;                                         // Source card ID
  to_id: string;                                           // Target card ID
  type?: "causes"|"relates"|"contradicts"|"blocks";        // Default "relates"
  label?: string;                                          // Optional label
}
```

Server responds with `connections_add` (single connection) or `error`.
Rejects if duplicate (same from_id + to_id already exists).

### `connection_delete`

Delete a connection.

```typescript
payload: {
  connection_id: string;
}
```

Server responds with `connection_deleted` or `error`.

### `special_question_request`

Request a curated thinking question from the question deck.

```typescript
payload: {}
```

Server responds with `special_question_prompt` or `error` if unavailable.
Only available after `MIN_PUZZLEMENT_TURNS` (3) interactions in `question` phase.

---

## Server -> Client Messages

### `session_loaded`

Session initialized or resumed. Sent once after `init` or on first `user_message`.

```typescript
payload: {
  session: {
    id: string;        // Session UUID
    question: string;  // Central problem/question text
  }
}
```

### `cards_add`

New cards created (by AI or user).

```typescript
payload: {
  cards: Card[];  // Array of full Card objects
}
```

Card object:

```typescript
{
  id: string;
  text: string;
  type: "question"|"fact"|"pain"|"resource"|"hypothesis"|"todo";
  emoji: string;        // May be empty string
  color: string;        // Hex color, e.g. "#3B82F6"
  importance: number;   // 0..1
  confidence: number;   // 0..1
  x: number;            // 0..1
  y: number;            // 0..1
  pinned: boolean;
  width: number|null;
  height: number|null;
  custom_scale: number; // Default 1.0
  is_root: boolean;     // True if type === "question"
}
```

### `cards_update`

Cards modified (position, text, metadata).

```typescript
payload: {
  updates: Partial<Card & { id: string }>[];  // Each entry MUST include `id`
}
```

Note: BUG-001 — `card_move` handler currently omits `id` from updates.

### `cards_delete`

Multiple cards deleted (by AI).

```typescript
payload: {
  card_ids: string[];
}
```

### `card_deleted`

Single card deleted (by user via `card_delete`).

```typescript
payload: {
  card_id: string;
}
```

### `connections_add`

New connections created.

```typescript
payload: {
  connections: Connection[];
}
```

Connection object:

```typescript
{
  id: string;
  from_id: string;
  to_id: string;
  type: "causes"|"relates"|"contradicts"|"blocks";
  strength: number;         // 0..1
  label: string|null;
  created_by: "ai"|"user";
}
```

### `connection_deleted`

Connection removed.

```typescript
payload: {
  connection_id: string;
}
```

### `question_update`

Phase or question changed. Sent after every `user_message` processing and on `set_locale`.

```typescript
payload: {
  phase: "question"|"facts"|"pains"|"resources"|"gaps"|"connections";
  question: string;                   // Current phase question text
  hint: string;                       // Current phase hint text
  phaseIndex: number;                 // 0-based index in phase order
  special_questions_unlocked?: boolean;  // True when special questions become available
}
```

### `special_question_prompt`

Curated thinking question from the deck.

```typescript
payload: {
  id: string;              // Question ID
  category_id: string;     // Category identifier
  category_label?: string; // Human-readable category name
  question: string;        // Question text
  hint: string;            // Hint text
}
```

### `session_cleared`

Session was reset.

```typescript
payload: {}
```

### `error`

Error occurred.

```typescript
payload: {
  message: string;           // Human-readable error message
  code?: string;             // Machine-readable code (e.g. "access_exhausted")
  access?: AccessSnapshot;   // Present when code === "access_exhausted"
}
```

---

## Change Procedure

1. Update this file with exact message/field changes.
2. Add/adjust tests in backend/frontend for changed message shape.
3. If change is breaking, create ADR and mark migration notes in `CHANGELOG.md`.
