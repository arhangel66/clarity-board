# TASK-FT012-01 Context

## Task
- `TASK-FT012-01`
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
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-03-final-report-docs-01.md`
- `.tasks/TASK-MB-REVIEW/TASK-MB-REVIEW-S-04-final-report-docs-01.md`

## Loaded code
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/auth.py`
- `backend/app/services/main_service.py`
- `backend/app/services/state_service.py`
- `backend/tests/test_integration_endpoints.py`
- `backend/tests/test_main_service.py`

## Scope for this task
- Replace the stale PRD `credits` framing with a code-facing `sessions + plans` contract for launch.
- Lock the session-consumption rule, paid-plan semantics, and API surface in backend code.
- Expose a deterministic backend endpoint that returns the access contract and the current pre-persistence status shape.
- Record non-blocking monetization assumptions explicitly for later FT-012 tasks.

## Out of scope
- Persisting entitlement rows or charging data in SQLite
- Enforcing limits on WebSocket init or first AI message
- Frontend access UI or paywall presentation
- Real billing, checkout, or deploy work
