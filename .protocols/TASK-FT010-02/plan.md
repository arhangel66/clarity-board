# TASK-FT010-02 Plan

## Goal
Lock the FT-010 rewrite into deterministic tests so category names, localized labels, and deck integrity do not drift silently.

## Steps
1. Add backend tests that verify the real deck metadata, localized category labels, and question-count integrity.
2. Add frontend tests that verify the renamed category label renders for pending special questions, including the i18n fallback path.
3. Update testing docs and run the task gates.

## Expected touched files
- `.protocols/TASK-FT010-02/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT010-02/*`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.memory-bank/features/FT-010-special-questions.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/testing/index.md`
- `.memory-bank/changelog.md`
- `backend/tests/test_special_questions.py`
- `frontend/src/lib/components/CurrentQuestion.test.ts`

## Gates
- `cd backend && uv run pytest tests/test_special_questions.py -v`
- `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
