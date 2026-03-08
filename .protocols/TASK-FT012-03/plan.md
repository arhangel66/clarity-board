# TASK-FT012-03 Plan

## Goal
Expose the FT-012 access snapshot in the authenticated frontend so users can see starter sessions remaining or an active paid plan without seeing a credits model.

## Steps
1. Add a frontend access store with typed `/api/access` fetch, loading, reset, and snapshot-hydration helpers.
2. Load access status during authenticated app initialization and clear it when the user signs out.
3. Render an access-status card in the sidebar with localized copy for free, monthly, and lifetime states.
4. Refresh the access snapshot after the first successful AI-assisted turn on a blank board and hydrate it from `access_exhausted` WebSocket errors.
5. Add deterministic frontend coverage and record verification evidence.

## Expected touched files
- `frontend/src/lib/stores/access.ts`
- `frontend/src/App.svelte`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/stores/websocket.ts`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/types.ts`
- `frontend/src/lib/stores/access.test.ts`
- `frontend/src/lib/components/BoardsSidebar.test.ts`

## Gates
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`
