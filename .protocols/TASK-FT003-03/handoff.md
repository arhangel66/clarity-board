# TASK-FT003-03 Handoff

- Added a Playwright onboarding regression that completes the guided flow on a real board, reloads the app, and verifies the tutorial only returns after an explicit desktop-help restart.
- `frontend/src/lib/stores/onboarding.ts` now exposes a canonical completed-tour payload helper so e2e setup can align with the current persistence contract instead of the legacy one-shot key.
- `playwright.config.ts` now boots an isolated frontend/backend pair on `127.0.0.1:4173` and `127.0.0.1:18000`, with the backend pointed at a clean temp data dir via `FACT_DATA_DIR`, so local dev state does not leak into Playwright access/session behavior.
- FT-003 is now fully verified for repo-local scope; the next autonomous promotion should come from the remaining planned W2 feature slices in a fresh budget.
