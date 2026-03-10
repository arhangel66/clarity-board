---
description: Implementation plan for FT-001 landing page redesign.
status: active
---
# IMPL-FT-001

## Goal
Ship the landing page redesign with honest pricing, problem-first positioning, and launch-ready verification.

## Steps
- Confirm the current implementation still covers all `REQ-020` acceptance criteria after recent pricing/copy changes.
- Keep the remaining landing work limited to polish, responsive QA, and launch handoff.
- Separate deployment/publish work from already-verified repo-local implementation so autonomous execution can reason about state cleanly.
- Run a landing readability pass: contrast, typography tone, and mobile wrapping around the kicker/nav labels.
- Keep landing pricing CTAs informational while billing is offline, aligned with the in-app non-billing preview behavior from `FT-013`.

## Expected touched files
- `frontend/src/lib/components/LandingPage.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `frontend/src/app.css`
- `.protocols/FT-001/*`

## Tests
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`

## Quality gates
- Desktop and mobile smoke-check for the landing route
- Analytics and pricing copy still aligned with `FT-002` and monetization docs

## Verify / UAT
- Validate all landing sections against the FT-001 acceptance checklist.
- Capture remaining non-repo launch work as a separate handoff item.
