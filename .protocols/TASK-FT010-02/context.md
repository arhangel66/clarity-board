# TASK-FT010-02 Context

## Task
- `TASK-FT010-02`
- Feature: `FT-010 Special Questions Rewrite`
- REQs: `REQ-029`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-010-special-questions.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/plans/IMPL-FT-010.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/testing/index.md`
- `.memory-bank/commands/{execute,verify,mb-sync,add-tests}.md`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.protocols/TASK-FT010-01/{context,plan,progress,verification}.md`

## Loaded code
- `backend/data/questions.json`
- `backend/app/services/special_questions.py`
- `backend/tests/test_special_questions.py`
- `frontend/src/lib/components/CurrentQuestion.svelte`
- `frontend/src/lib/components/CurrentQuestion.test.ts`
- `frontend/src/lib/stores/i18n.ts`

## Scope for this task
- Add backend regression coverage for the rewritten deck metadata and localized category labels.
- Add frontend regression coverage for the visible renamed category label on pending special questions.
- Update testing docs to mention the strengthened FT-010 checks.

## Out of scope
- Additional special-question copy rewrites
- Real-user validation work from `TASK-FT010-03`
