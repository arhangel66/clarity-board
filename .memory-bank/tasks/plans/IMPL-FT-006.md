---
description: Implementation plan for FT-006 AI output validation safeguards.
status: active
---
# IMPL-FT-006

## Goal
Keep AI-generated operations safe before they reach the canvas.

## Steps
- Maintain the validator boundary in `main_service`.
- Keep duplicate, bounds, root-card, and invalid-reference coverage in tests.
- Reconfirm failure logging remains observable for later analysis.

## Expected touched files
- `backend/app/services/validator.py`
- `backend/app/services/main_service.py`
- `backend/tests/test_validator.py`
- `backend/tests/test_main_service.py`

## Tests
- `cd backend && uv run pytest tests/test_validator.py -v`
- `cd backend && uv run pytest tests/test_main_service.py -v`

## Quality gates
- Reject invalid operations without breaking valid AI output.

## Verify / UAT
- Re-run validator coverage and confirm `REQ-025` remains complete.
