# TASK-FT010-01 Context

## Task
- `TASK-FT010-01`
- Feature: `FT-010 Special Questions Rewrite`
- REQs: `REQ-029`

## Loaded docs
- `AGENTS.md`
- `prd.md`
- `.memory-bank/features/FT-010-special-questions.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/plans/IMPL-FT-010.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/commands/{autonomous,execute,verify,mb-sync,find-skills}.md`
- `.memory-bank/workflows/{autonomy-policy,mb-sync}.md`
- `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md`

## Loaded code
- `backend/data/questions.json`
- `backend/app/models.py`
- `backend/app/services/special_questions.py`
- `backend/app/services/main_service.py`
- `frontend/src/lib/types.ts`
- `frontend/src/lib/components/CurrentQuestion.svelte`
- `frontend/src/lib/stores/i18n.ts`

## Scope for this task
- Rewrite the special-question deck with original, domain-neutral RU/EN wording.
- Rename the visible category taxonomy while preserving legacy internal IDs for session compatibility.
- Surface localized category labels end-to-end for pending special questions without adding any external dependency.

## Out of scope
- Real-user clarity validation and wording interviews
- New payment, auth, or deploy work
- Feature slices outside `FT-010`
