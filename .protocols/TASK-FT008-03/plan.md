# TASK-FT008-03 Plan

## Goal
Exercise the remaining auth reliability path in Playwright so the dev-bypass harness proves users can log in, reload, and reopen the workspace without getting stranded.

## Steps
1. Reuse the existing auth fixture to avoid duplicated setup and keep the tests deterministic.
2. Extend `e2e/tests/auth.spec.ts` with real-board reload and browser-reopen flows.
3. Run `pnpm e2e -- --grep auth` and store the output summary in `.tasks/TASK-FT008-03/`.
4. Sync the FT-008 docs, backlog, and autonomous queue state.

## Expected touched files
- `e2e/tests/auth.spec.ts`
- `e2e/fixtures/auth.fixture.ts`
- `.tasks/TASK-FT008-03/verification-2026-03-08.md`

## Gates
- `pnpm e2e -- --grep auth`
