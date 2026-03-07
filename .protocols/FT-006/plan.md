# FT-006: AI Output Validation — Plan

## Goal
Add a validation layer that catches bad AI output (duplicates, out-of-bounds, root-card tampering) before it reaches the canvas. Log all validation failures for analysis.

## Non-goals
- Changing the AI prompt or model parameters (items 5-6 from AC are manual/operational)
- Adding a separate validation microservice
- Changing the frontend

## Approach

### 1. Add validation module `backend/app/services/validator.py`
A pure-function validator that checks decoded AI operations against current state:
- **Duplicate detection**: compare new card text against existing cards using normalized text similarity (case-insensitive, stripped). If similarity > 80% (simple ratio), log warning and skip.
- **Coordinate bounds**: re-validate x/y are in [0,1] (defense-in-depth after decoder)
- **Text length**: re-validate text within limits
- **Root card protection**: prevent delete/update of question card outside Phase 1
- **Invalid card_id references**: update/delete referencing non-existent card IDs

### 2. Add structured validation logging
- Create a `ValidationEvent` dataclass with: event_type, severity, details, session_id, timestamp
- Log to Python logger at WARNING level with structured JSON
- Optionally append to EventService for analytics

### 3. Integrate into MainService.process_user_message
- After `decode_ai_response()`, pass operations through `validate_operations()`
- Filter out invalid operations, log each rejection
- Continue with only valid operations

### 4. Tests
- `backend/tests/test_validator.py` — unit tests for all validation rules
- Update `backend/tests/test_main_service.py` — integration test for validation in flow

## Touched files
- `backend/app/services/validator.py` (NEW)
- `backend/app/services/main_service.py` (integrate validator)
- `backend/tests/test_validator.py` (NEW)
- `backend/tests/test_main_service.py` (add validation integration tests)

## Quality gates
- `cd backend && uv run ruff check .`
- `cd backend && uv run pytest -v`

## MB-SYNC
- Update backlog status FT-006 → done
- Update requirements.md REQ-025 → done
- Append changelog entry
