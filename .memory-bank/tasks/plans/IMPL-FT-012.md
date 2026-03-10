---
description: Implementation plan for FT-012 session access and limits.
status: active
---
# IMPL-FT-012

## Goal
Track free-session usage and paid entitlement state per user so the product can gate AI access without exposing a credits model.

## Steps
- Lock the entitlement rules in code-facing terms: what consumes a session, what monthly/lifetime mean before billing, and which API surface exposes status.
- Implement a backend access service and persistence model tied to user/session lifecycle.
- Expose remaining free sessions and current plan to the frontend.
- Enforce limits before AI-assisted work starts while keeping existing sessions readable.
- Keep the no-reset rule explicit: deleting boards does not restore spent starter access.
- Add regression coverage that exhausted users can still continue on already-started boards while blank boards remain blocked.
- Tighten the in-app access surface so it explains blocked `New board` behavior without occupying disproportionate sidebar space.

## Expected touched files
- `backend/app/access.py`
- `backend/app/construct.py`
- `backend/app/services/main_service.py`
- `backend/app/main.py`
- `backend/tests/*access*`

## Tests
- `cd backend && uv run pytest -v`

## Quality gates
- Existing sessions must remain accessible even when new AI sessions are blocked.

## Verify / UAT
- Create users across `free`, `monthly`, and `lifetime` states and confirm the returned access status matches expectations.
