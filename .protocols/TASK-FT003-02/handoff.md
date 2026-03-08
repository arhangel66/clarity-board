# TASK-FT003-02 Handoff

- Onboarding progression now stays on the current step until the user actually reaches that milestone, with `canAdvance` derived from live board, connection, and session-phase signals.
- `TooltipOverlay.svelte` now behaves like an action-oriented guide: it explains what to do next, shows waiting/ready status, disables the primary action until the milestone is met, and uses a dedicated finish label on the last step.
- Both `HelpOverlay.svelte` and `MobileDrawer.svelte` expose a restart-tutorial entry point that resets the walkthrough and closes the surface immediately.
- Deterministic regression coverage now includes the onboarding store plus desktop/mobile onboarding surfaces in `TooltipOverlay.test.ts`, `HelpOverlay.test.ts`, and `MobileDrawer.test.ts`.
- `TASK-FT003-03` remains the next follow-up for end-to-end completion, reload persistence, and explicit restart verification.
