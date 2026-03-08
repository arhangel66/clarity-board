# TASK-FT012-03 Context

## Task
- `TASK-FT012-03`
- Feature: `FT-012 Session Access & Limits System`
- REQs: `REQ-031`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-012-usage-credits.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/plans/IMPL-FT-012.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/commands/{autonomous,execute,verify,mb-sync}.md`
- `.protocols/AUTONOMOUS-RUN/{plan,status,decision-log}.md`
- `.protocols/FT-012/decision-log.md`
- `.protocols/TASK-FT012-02/{context,verification}.md`

## Loaded code
- `backend/app/access.py`
- `backend/app/main.py`
- `frontend/src/App.svelte`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/components/MobileDrawer.svelte`
- `frontend/src/lib/stores/auth.ts`
- `frontend/src/lib/stores/boards.ts`
- `frontend/src/lib/stores/websocket.ts`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/types.ts`

## Scope for this task
- Add a frontend store for the authenticated `/api/access` snapshot.
- Load the access snapshot during authenticated app startup and clear it on sign-out.
- Surface remaining free sessions or the active paid plan in-app without reintroducing credits terminology.
- Refresh or hydrate the status when the first AI-assisted turn on a blank board consumes starter access.

## Out of scope
- Billing, checkout, or plan purchase flows
- Backend access-rule changes
- Deployment or production writes
- FT-013 paywall/upgrade UI
