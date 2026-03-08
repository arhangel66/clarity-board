# TASK-FT012-02 Context

## Task
- `TASK-FT012-02`
- Feature: `FT-012 Session Access & Limits System`
- REQs: `REQ-031`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-012-usage-credits.md`
- `.memory-bank/epics/EP-004-monetization.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/plans/IMPL-FT-012.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/commands/{autonomous,execute,verify,review,mb-sync}.md`
- `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md`
- `.protocols/FT-012/decision-log.md`
- `.protocols/TASK-FT012-01/{context,plan,progress,verification}.md`

## Loaded code
- `backend/app/access.py`
- `backend/app/construct.py`
- `backend/app/main.py`
- `backend/app/services/main_service.py`
- `backend/app/services/state_service.py`
- `backend/tests/test_access.py`
- `backend/tests/test_integration_endpoints.py`
- `backend/tests/test_main_service.py`

## Scope for this task
- Persist free-session consumption per user so quota survives deletes and restarts.
- Persist per-user entitlement state for `free`, `monthly`, and `lifetime`.
- Enforce the access rules before the first AI-assisted message on a blank board.
- Keep existing started sessions accessible even when starter quota is exhausted.
- Return tracked access status from `GET /api/access`.

## Out of scope
- Frontend access UI and upgrade surfaces
- Real billing or checkout integration
- Deploy or production writes
- W2/W3 monetization work
