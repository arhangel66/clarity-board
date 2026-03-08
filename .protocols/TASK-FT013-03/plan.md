# TASK-FT013-03 Plan

## Goal
Finish FT-013 by wiring analytics-only upgrade intent tracking into the paywall modal without adding any payment integration.

## Steps
1. Add a dedicated analytics helper for paywall upgrade clicks.
2. Wire paywall plan buttons to the analytics helper while preserving the non-transactional preview flow.
3. Add deterministic analytics and paywall integration coverage.
4. Run the frontend test gate and close the feature if verification passes.

## Expected touched files
- `.protocols/TASK-FT013-03/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT013-03/*`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.memory-bank/tasks/backlog.md`
- `frontend/src/lib/analytics.ts`
- `frontend/src/lib/analytics.test.ts`
- `frontend/src/lib/components/PaywallModal.svelte`
- `frontend/src/lib/components/PaywallModal.test.ts`

## Gates
- `NODE_OPTIONS=--experimental-require-module cd frontend && pnpm test -- --run`
