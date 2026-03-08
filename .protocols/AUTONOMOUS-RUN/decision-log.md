# AUTONOMOUS-RUN Decision Log

## 2026-03-08

### Decision
Continue from the existing Memory Bank instead of re-running `/prd` from zero.

### Why
The repo already contains populated L1-L3 docs (`product`, `requirements`, `epics`, `features`) that match the root PRD closely enough for delta-based continuation.

### Assumption
Existing `FT-001`, `FT-002`, and `FT-006` protocol artifacts are trustworthy enough to seed backlog state, but not enough to treat undeployed work as shipped.

### Assumption
This run must remain repository-local. Deploy, secret reads, and production writes stay out of scope under the autonomy policy.

### Assumption
Untracked files that predate this run (`GEMINI.md`, `backend/data/events.jsonl`, `memobank/`, `prd.md`) are user or tool artifacts and must not be modified unless a later task explicitly requires it.

### Decision
Accept the `TASK-MB-REVIEW` results as the review gate for this autonomous run.

### Why
All five fresh-context review stages returned `APPROVE`; only non-blocking recommendations were raised.

### Decision
Stop this run in `HALT_BUDGET_EXCEEDED` after `TASK-FT008-01`.

### Why
The run already covered backlog normalization, review, and one verified W1 execution. The next tasks are queued safely (`TASK-FT008-02` is now `ready`), but continuing further in the same unattended session would trade away verification quality for throughput.

### Decision
Resume the run with `TASK-FT008-02` as the next scheduled task.

### Why
The earlier stop was a session-budget boundary, not a quality or policy blocker, and the review gate remained `APPROVE`.

### Decision
Treat Auth0 recovery errors (`login_required`, `missing_refresh_token`, `invalid_grant`, related interactive-login codes) as `session_expired`, while leaving transient/network failures in `auth_failed`.

### Why
`TASK-FT008-02` needs a clearer re-login path for revoked sessions without forcing the same UX for temporary provider/network issues.

### Decision
Stop this resumed run in `HALT_BUDGET_EXCEEDED` after `TASK-FT008-03`.

### Why
All currently ready FT-008 work is now verified and committed. The next candidate feature slice is outside the original auth scope and should start in a fresh unattended session.

### Decision
Promote `TASK-FT012-01` and execute it as the next safe W1 slice.

### Why
The latest review gate explicitly called out `TASK-FT012-01` as dependency-free, repo-local, and safe to promote from `planned` once FT-008 was complete.

### Assumption
The remaining ambiguity in FT-012 is non-blocking because the repo still has no real billing processor, checkout, or external payment contract.

### Why
The hard-stop categories cover real payment/compliance risk, not internal launch-contract wording. Locking the code-facing contract now reduces drift instead of increasing it.

### Decision
Use `estimated_from_sessions` as the temporary metering source for `GET /api/access`.

### Why
It gives FT-012 and FT-013 a stable response shape immediately, while leaving irreversible persistence and access enforcement to `TASK-FT012-02`.

### Decision
Stop this resumed run in `HALT_BUDGET_EXCEEDED` after `TASK-FT012-01`.

### Why
The next ready slice (`TASK-FT012-02`) changes backend persistence and WebSocket/session enforcement, which is materially riskier than the contract-only slice and should start with a fresh unattended session budget.

### Decision
Backfill existing started boards into tracked access metering instead of running a one-off migration.

### Why
The repo already contains local session data, and lazy backfill keeps quota accounting consistent without destructive migration work or external coordination.

### Decision
Only blank-board AI starts are blocked when starter quota is exhausted; previously started boards remain usable.

### Why
That keeps the launch model aligned with “3 full sessions” rather than a per-message credit system and avoids locking users out of boards they already began.

### Decision
Stop this resumed run in `HALT_BUDGET_EXCEEDED` after `TASK-FT012-02`.

### Why
`TASK-FT012-02` is fully verified, and the next ready slice (`TASK-FT012-03`) is a frontend status-surface task that should begin in a fresh unattended session with its own verification budget.
