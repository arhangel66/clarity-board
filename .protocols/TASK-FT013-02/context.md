# TASK-FT013-02 Context

## Task
- `TASK-FT013-02`
- Feature: `FT-013 Pricing & Upgrade UI + Intent Tracking`
- REQs: `REQ-032`

## Loaded docs
- `AGENTS.md`
- `.memory-bank/features/FT-013-paywall-ui.md`
- `.memory-bank/features/FT-012-usage-credits.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/plans/IMPL-FT-013.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/commands/{autopilot,execute,verify}.md`
- `.memory-bank/workflows/{autonomy-policy,mb-sync}.md`
- `.protocols/AUTONOMOUS-RUN/{status,decision-log}.md`
- `.protocols/TASK-FT013-01/{context,verification}.md`

## Loaded code
- `frontend/src/App.svelte`
- `frontend/src/lib/components/LandingPage.svelte`
- `frontend/src/lib/components/BoardsSidebar.svelte`
- `frontend/src/lib/stores/access.ts`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/lib/components/BoardsSidebar.test.ts`
- `frontend/src/App.test.ts`

## Scope for this task
- Add the first in-app paywall modal for exhausted free-session users.
- Keep landing and in-app pricing aligned from the same translated offer.
- Preserve the no-payment/no-redirect constraint for unattended execution.

## Out of scope
- Analytics wiring for upgrade clicks
- Real checkout, billing, or partner integrations
- Backend access-contract changes
- Deploy or production writes
