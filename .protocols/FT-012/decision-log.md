# FT-012 Decision Log

## 2026-03-08

### Decision
Launch FT-012 on a `sessions + plans` model, not the older PRD `credits` model.

### Why
`REQ-031`, `FT-012`, and the landing/pricing copy already converged on `3 free sessions total`, `$10/month unlimited`, and `$100 lifetime`. Reintroducing per-action credits in code would recreate document drift instead of removing it.

### Decision
A session is consumed when a blank board receives its first AI-assisted user message.

### Why
Counting board creation would burn quota on empty placeholders, while counting every AI action would pull the product back toward a credits model. The first AI-assisted message matches the current board lifecycle and the "3 full sessions" positioning.

### Assumption
Deleting a board must not restore free-session quota.

### Why
Otherwise users could recycle the starter allowance indefinitely. Accurate irreversible tracking is deferred to `TASK-FT012-02`, so this task only locks the rule and API contract.

### Decision
`monthly` means unlimited AI-assisted sessions until an explicit expiry timestamp; `lifetime` means unlimited sessions with no expiry.

### Why
This keeps the paid-plan semantics precise before real billing exists and lets later tasks enforce access without inventing new plan types.

### Decision
The canonical API surface for this feature starts at `GET /api/access`.

### Why
`FT-012-03` needs a stable frontend-facing status endpoint, and `FT-013` depends on the same contract for upgrade UI decisions.

### Assumption
Until `TASK-FT012-02` adds persistent entitlements, `GET /api/access` may estimate starter-session usage from existing started boards and label that status as `estimated_from_sessions`.

### Why
This keeps the API shape stable today without pretending that quota consumption is already irreversible or fully enforced.
