# REST API Contract

Last updated: 2026-03-15

Base URL: `https://fact.slotik.app/api` (production), `http://localhost:8000/api` (dev)

## Authentication

All endpoints except `/api/health` require `Authorization: Bearer <token>` header.

- Production: Auth0 RS256 JWT
- Development: `DEV_AUTH_BYPASS=true` on backend, token = `"dev-token"`

---

## Endpoints

### `GET /api/health`

Health check. No auth required.

**Response** `200 OK`:

```json
{
  "status": "ok",
  "service": "clarify-board-backend"
}
```

---

### `GET /api/sessions`

List all sessions for the authenticated user.

**Response** `200 OK`:

```json
{
  "sessions": [
    {
      "id": "uuid",
      "user_id": "auth0|123",
      "title": "Session title or derived from first question",
      "created_at": "2026-03-15T10:00:00Z",
      "updated_at": "2026-03-15T10:05:00Z"
    }
  ]
}
```

Notes:
- Sessions without a cached title derive it from the state JSON (N+1 deserialization, see KNOWN_ISSUES.md).
- Sorted by `updated_at` descending.

---

### `POST /api/sessions`

Create a new empty session.

**Request body:** empty or `{}`

**Response** `200 OK`:

```json
{
  "session": {
    "id": "uuid",
    "title": ""
  }
}
```

---

### `DELETE /api/sessions/{session_id}`

Delete a session. Only the session owner can delete.

**Response** `200 OK`:

```json
{
  "status": "deleted"
}
```

**Response** `404 Not Found`:

```json
{
  "detail": "Session not found"
}
```

---

### `POST /api/transcribe`

Transcribe audio to text using OpenAI Whisper.

**Request:** `multipart/form-data` with field `file` (audio file).

**Response** `200 OK`:

```json
{
  "text": "transcribed text content"
}
```

**Response** `503 Service Unavailable`:

```json
{
  "detail": "Transcription service not configured"
}
```

Requires `OPENAI_API_KEY` environment variable.

---

### `GET /api/access`

Get access/billing status for the authenticated user.

**Response** `200 OK`:

```json
{
  "contract": {
    "status_endpoint": "/api/access",
    "pricing_unit": "sessions",
    "free_sessions_total": 3,
    "session_consumption_trigger": "first_ai_message_on_blank_session",
    "blank_session_consumes": false,
    "reopen_existing_session_consumes": false,
    "deleting_session_restores_quota": true,
    "supported_plans": ["free", "monthly", "lifetime"],
    "monthly_requires_expires_at": true,
    "lifetime_never_expires": true
  },
  "status": {
    "plan": "free",
    "plan_expires_at": null,
    "plan_active": true,
    "free_sessions_total": 3,
    "free_sessions_used": 1,
    "free_sessions_remaining": 2,
    "can_start_ai_session": true,
    "metering_state": "tracked"
  }
}
```
