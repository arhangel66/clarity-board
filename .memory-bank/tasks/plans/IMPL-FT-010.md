---
description: Implementation plan for FT-010 special questions rewrite.
status: active
---
# IMPL-FT-010

## Goal
Replace the current special-question deck with original, domain-neutral wording and a renamed category taxonomy.

## Steps
- Rewrite the JSON deck in Russian and English with original phrasing.
- Rename the three categories consistently in backend and frontend surfaces.
- Extend tests so deck loading and UI labels remain stable after the rename.
- Leave real-user clarity review as a follow-up validation task after the content lands.

## Expected touched files
- `backend/data/questions.json`
- `backend/app/services/special_questions.py`
- `backend/tests/test_special_questions.py`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/components/CurrentQuestion.test.ts`

## Tests
- `cd backend && uv run pytest tests/test_special_questions.py -v`
- `cd frontend && pnpm test -- --run`

## Quality gates
- No category names or prompts should reference the original source wording directly.

## Verify / UAT
- Load the special-question flow in RU and EN and confirm the renamed categories and rewritten prompts appear end-to-end.
