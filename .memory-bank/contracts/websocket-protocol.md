---
description: WebSocket protocol contract — message types, payloads, flow.
status: active
---
# WebSocket Protocol

Endpoint: `/ws`

## Client → Server

| Type | Payload | Description |
|---|---|---|
| `init` | `{session_id?, auth_token, locale?}` | Initialize/resume session |
| `user_message` | `{text, special_question_id?}` | User input for AI processing |
| `set_locale` | `{locale}` | Switch language (ru/en) |
| `clear_session` | `{}` | Reset current session |
| `card_move` | `{card_id, x, y, pinned, width?, height?, custom_scale?}` | Card repositioned |
| `card_create` | `{text, type, x, y, emoji?, importance?, confidence?}` | Manual card creation |
| `card_delete` | `{card_id}` | Delete card |
| `card_update` | `{card_id, updates{}}` | Update card properties |
| `special_question_request` | `{}` | Request special question from deck |
| `connection_create` | `{from_id, to_id, type?, label?}` | Create card relationship |
| `connection_delete` | `{connection_id}` | Remove relationship |

## Server → Client

| Type | Payload | When |
|---|---|---|
| `session_loaded` | `{session: {id, question}}` | Session initialized |
| `cards_add` | `{cards: [...]}` | New cards created |
| `cards_update` | `{updates: [...]}` | Cards modified |
| `cards_delete` | `{card_ids: [...]}` | Cards removed (batch) |
| `card_deleted` | `{card_id}` | Single card removed (user action) |
| `connections_add` | `{connections: [...]}` | New connections |
| `connection_deleted` | `{connection_id}` | Connection removed |
| `question_update` | `{phase, question, hint, phaseIndex, special_questions_unlocked}` | Phase/question changed |
| `special_question_prompt` | `{id, category_id, question, hint}` | Special question delivered |
| `session_cleared` | `{}` | Session reset confirmed |
| `error` | `{message}` | Error condition |

## REST Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/health` | GET | No | Health check |
| `/api/sessions` | GET | Bearer | List user sessions |
| `/api/sessions` | POST | Bearer | Create session |
| `/api/sessions/{id}` | DELETE | Bearer | Delete session |
| `/api/transcribe` | POST | Bearer | Whisper transcription |
