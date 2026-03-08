# TASK-FT010-02 Verification Evidence

## Commands
- `cd backend && uv run pytest tests/test_special_questions.py -v`
- `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`

## Evidence
- `backend/tests/test_special_questions.py` now verifies the real deck count, renamed category labels, and localized service output.
- `frontend/src/lib/components/CurrentQuestion.test.ts` now verifies both direct `category_label` rendering and the fallback-to-i18n path.
- Frontend build succeeds after the new category-label surface and tests.

## Result
- PASS
