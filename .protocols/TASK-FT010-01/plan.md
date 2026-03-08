# TASK-FT010-01 Plan

## Goal
Replace the current special-question copy with original, domain-neutral prompts and renamed category labels, then expose those labels in the live special-question payload/UI without breaking existing session history.

## Steps
1. Rewrite `backend/data/questions.json` with new RU/EN prompts, hints, and renamed category display names.
2. Extend the special-question models/service to carry localized category labels while preserving stable legacy category IDs.
3. Show the category label in the frontend special-question surface with an i18n fallback for older payloads.
4. Run the FT-010 task gates and record verification evidence.

## Expected touched files
- `.protocols/TASK-FT010-01/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT010-01/*`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.memory-bank/features/FT-010-special-questions.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/changelog.md`
- `backend/data/questions.json`
- `backend/app/models.py`
- `backend/app/services/special_questions.py`
- `backend/app/services/main_service.py`
- `frontend/src/lib/types.ts`
- `frontend/src/lib/components/CurrentQuestion.svelte`
- `frontend/src/lib/stores/i18n.ts`

## Gates
- `cd backend && uv run pytest tests/test_special_questions.py -v`
- `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`
