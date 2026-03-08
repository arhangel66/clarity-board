# TASK-FT010-01 Handoff

- Rewrote the special-question deck with new domain-neutral RU/EN prompts and renamed visible category labels.
- Preserved legacy internal category IDs so saved session history and pending-question IDs stay compatible.
- Added localized `category_label` flow through the backend payload/history and surfaced it in `CurrentQuestion` with an i18n fallback.
- `TASK-FT010-02` is the immediate follow-up to lock this slice with regression coverage.
