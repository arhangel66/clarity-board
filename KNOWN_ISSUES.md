# Known Issues

Last updated: 2026-03-15

## Bugs

### BUG-001: `handle_card_move` does not include `id` in response

**Severity:** Medium
**Location:** `backend/app/services/main_service.py:378-385`

The `handle_card_move()` method returns an update dict without the `id` field.
The response is sent as `cards_update` with `payload.updates[]`, where each entry
must include `id` so the frontend can match it to the correct card.

Currently the frontend works around this because card_move updates are applied
optimistically on the client side, but the server echo is malformed.

```python
# Current (missing id):
return {
    "x": x, "y": y, "pinned": pinned,
    "width": ..., "height": ..., "custom_scale": ...,
}

# Should be:
return {
    "id": card_id,
    "x": x, "y": y, "pinned": pinned,
    "width": ..., "height": ..., "custom_scale": ...,
}
```

### BUG-002: `handle_card_move` accepts `width` but never applies it

**Severity:** Low
**Location:** `backend/app/services/main_service.py:349,373-376`

The method signature accepts `width: float | None = None`, and the response
returns `"width": getattr(card, "width", None)`, but the width is never
assigned to `card.width`. Both `height` and `custom_scale` are applied correctly.

```python
# height and custom_scale are applied:
if height is not None:
    card.height = height
if custom_scale is not None:
    card.custom_scale = custom_scale

# width is NOT applied — missing:
# if width is not None:
#     card.width = width
```

### BUG-003: `update_card` silently truncates text without notification

**Severity:** Low
**Location:** `backend/app/services/main_service.py:712-713`

Card text is silently truncated: question cards to 100 chars, others to 50 chars.
The frontend enforces 200 chars max. The backend truncation is stricter and happens
without any feedback to the user, leading to data loss.

```python
max_len = 100 if card.type == CardType.QUESTION else 50
card.text = str(updates["text"])[:max_len]
```

Note: The frontend `types.ts` does not define these limits. The frontend input bar
enforces 200 chars, so the mismatch can cause unexpected truncation.

---

## Security

### SEC-001: CORS allows all origins

**Severity:** High
**Location:** `backend/app/main.py:62-68`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # credentials + wildcard origin is a bad combination
    ...
)
```

Should restrict to `https://fact.slotik.app` in production.

### SEC-002: No security headers in nginx

**Severity:** Medium
**Location:** `frontend/nginx.conf`

Missing headers: `X-Frame-Options`, `X-Content-Type-Options`,
`Referrer-Policy`, `Content-Security-Policy`.

### SEC-003: No rate limiting

**Severity:** Medium
**Locations:** `backend/app/main.py` (WebSocket), `frontend/nginx.conf` (HTTP)

No rate limiting on WebSocket connections or HTTP endpoints.
A single client can open unlimited connections and send unlimited messages.

---

## Silent Failures

### SILENT-001: `handle_card_move` returns None without error

**Location:** `backend/app/main.py:362-368`, `backend/app/services/main_service.py:387`

If `card_id` is not found, `handle_card_move()` returns `None` and the WebSocket
handler silently skips the response. Client has no feedback.

### SILENT-002: `handle_card_update` returns without error on invalid input

**Location:** `backend/app/main.py:471-472`

If `card_id` is empty, `updates` is not a dict, or `updates` is empty,
the handler returns silently. No error is sent to the client.

### SILENT-003: `handle_card_delete` silent on failure

**Location:** `backend/app/main.py:447-454`

If `delete_card()` returns `False` (card not found), the client gets no response.

---

## Dead Code

### DEAD-001: Unused frontend message types

**Location:** `frontend/src/lib/types.ts:158-164, 214-215`

Two server message types are defined in TypeScript but never sent by the backend:

- `ai_question` with `AiQuestionPayload` — no backend handler sends this
- `positions_update` with `PositionsUpdatePayload` — no backend handler sends this

These appear to be remnants of a planned layout engine feature.

---

## Documentation Gaps

### DOC-001: WebSocket contract lacks payload schemas for server messages

**Location:** `docs/architecture/WEBSOCKET_CONTRACT.md:46-58`

Server -> Client messages are listed by name only, without payload schemas.
Client -> Server messages have payload details but server responses do not.

### DOC-002: Text length limits undocumented

The backend enforces different text limits per card type (question: 100, other: 50)
but this is not documented in the spec, ARCHITECTURE.md, or types.ts.
The frontend enforces 200 chars globally.

### DOC-003: REST API lacks response schemas

**Location:** `ARCHITECTURE.md:112-118`

REST endpoints are listed but response formats are not documented.

### DOC-004: init message missing fields in contract

**Location:** `docs/architecture/WEBSOCKET_CONTRACT.md:24`

The `init` message payload is documented as `{ session_id?, auth_token?, locale? }`
but the actual implementation also accepts `email?: string` and `name?: string`.
