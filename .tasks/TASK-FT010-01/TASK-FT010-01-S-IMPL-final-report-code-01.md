# TASK-FT010-01 Final Report

## Summary
- Replaced the old special-question deck with 30 rewritten RU/EN prompts and hints.
- Renamed the visible taxonomy to `Ракурс / Perspective`, `Структура / Structure`, and `Контекст / Context`.
- Added `category_label` to special-question payload/history models and surfaced it in the pending special-question UI.

## Validation
- `cd backend && uv run pytest tests/test_special_questions.py -v`
- `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
