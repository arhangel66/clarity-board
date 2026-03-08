# TASK-FT003-01 Handoff

- Replaced the tooltip-only onboarding memory with a signal-driven step model for question, cards, connections, and blind-spot guidance.
- The app now syncs onboarding state from the active board, card count, and session phase instead of one-off `maybeShow()` calls.
- Deterministic regression coverage locks persistence, legacy-storage migration, and restart behavior in `frontend/src/lib/stores/onboarding.test.ts`.
- `TASK-FT003-02` remains the next follow-up for the actual repeat-tutorial UI surface and the richer desktop/mobile walkthrough.
