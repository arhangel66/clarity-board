# WebSocket Contract

Last updated: 2026-03-05

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

## Client -> Server Messages

- `init`
  - payload: `{ session_id?: string, auth_token?: string, locale?: "ru" | "en" }`
- `user_message`
  - payload: `{ text: string, special_question_id?: string }`
- `set_locale`
  - payload: `{ locale: "ru" | "en" }`
- `clear_session`
  - payload: `{}`
- `card_move`
  - payload: `{ card_id, x, y, pinned, width?, height?, custom_scale? }`
- `card_create`
  - payload: `{ text, type, x, y, emoji?, importance?, confidence? }`
- `card_update`
  - payload: `{ card_id, updates }`
- `card_delete`
  - payload: `{ card_id }`
- `connection_create`
  - payload: `{ from_id, to_id, type?, label? }`
- `connection_delete`
  - payload: `{ connection_id }`
- `special_question_request`
  - payload: `{}`

## Server -> Client Messages

- `session_loaded`
- `session_cleared`
- `cards_add`
- `cards_update`
- `cards_delete`
- `card_deleted`
- `connections_add`
- `connection_deleted`
- `question_update`
- `special_question_prompt`
- `error`

## Change Procedure

1. Update this file with exact message/field changes.
2. Add/adjust tests in backend/frontend for changed message shape.
3. If change is breaking, create ADR and mark migration notes in `CHANGELOG.md`.
