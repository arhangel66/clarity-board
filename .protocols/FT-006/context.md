# FT-006: AI Output Validation — Context

## Task
Implement validation layer for AI-generated card operations to catch bad output before it reaches the canvas.

## Driving specs
- Feature: `.memory-bank/features/FT-006-ai-validation.md`
- Requirement: REQ-025 (AI output validation: bounds, duplicates, root-card protection)
- Epic: EP-003 (Reliability & Quality)
- Backlog: W1 item #2

## Current state analysis

### Already implemented
1. **Coordinate clamping** in `decoder.py:_parse_card` — pixel→[0,1] normalization, clamped to 0.05–0.95
2. **Text truncation** in `decoder.py:_parse_card` — 50 chars regular, 100 chars question
3. **Question card delete protection** in `main_service.py:_delete_card` — refuses to delete question type
4. **Question card update protection** in `main_service.py:_update_card` — only allowed in Phase 1
5. **Question card create→update redirect** in `main_service.py:process_user_message` — if question card exists, update instead of creating duplicate
6. **Pydantic model validation** in `models.py:Card` — x/y ge=0 le=1, importance/confidence ge=0 le=1, text max_length=200

### Missing (to implement)
1. **Duplicate card detection** — AI can create cards with near-identical text to existing ones
2. **Structured validation failure logging** — no dedicated logging for validation events
3. **Formal validation layer** — validation is scattered across decoder.py and main_service.py, needs consolidation

## Key files
- `backend/app/services/decoder.py` — pure function AI response parser
- `backend/app/services/main_service.py` — orchestrator, applies operations
- `backend/app/models.py` — Pydantic models with field constraints
- `backend/tests/test_decoder.py` — existing decoder tests
- `backend/tests/test_main_service.py` — existing main_service tests
