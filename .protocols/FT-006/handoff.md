# FT-006: AI Output Validation — Handoff

## What changed
- New file: `backend/app/services/validator.py` — pure-function validation layer
- Modified: `backend/app/services/main_service.py` — integrated validator after decoder
- New file: `backend/tests/test_validator.py` — 16 unit tests

## How it works
After `decode_ai_response()` parses raw AI JSON, `validate_operations()` filters the operations list:
1. **create_card**: checks text non-empty, text length, coordinates in [0,1], duplicate detection
2. **update_card**: checks card_id exists, root card protection (Phase 1 only), text length
3. **delete_card**: checks card_id exists, root card never deletable

Invalid operations are dropped; fixable issues (coords, text length) are clamped/truncated.
All rejections logged via `_log_rejection()` at WARNING level.

## Open items
- AC items 5-6 (collect sessions, tune parameters) are operational — need real user sessions
- Duplicate threshold (80%) may need tuning after real-world data
