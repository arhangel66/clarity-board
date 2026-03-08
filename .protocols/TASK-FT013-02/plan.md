# TASK-FT013-02 Plan

## Goal
Deliver the paywall UI slice by showing a friendly in-app modal when starter sessions are exhausted while keeping the landing and modal pricing copy aligned.

## Steps
1. Add the task protocol and promote `TASK-FT013-02` to `in_progress` in the autonomous queue.
2. Implement a repo-local paywall modal that opens for exhausted starter access and reuses the landing pricing data.
3. Add deterministic frontend coverage for the exhausted-access paywall state and pricing copy.
4. Run the frontend gates, then verify the slice and sync Memory Bank state if it passes.

## Expected touched files
- `.protocols/TASK-FT013-02/{context,plan,progress,verification,handoff}.md`
- `.tasks/TASK-FT013-02/*`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.memory-bank/tasks/backlog.md`
- `frontend/src/App.svelte`
- `frontend/src/lib/components/PaywallModal.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/components/*.test.ts`

## Gates
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
