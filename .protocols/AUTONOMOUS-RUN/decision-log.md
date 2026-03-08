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

### Decision
Resume the autonomous run with `TASK-FT012-03` as the active task.

### Why
The review gate is still `APPROVE`, `TASK-FT012-03` is the only ready dependency-cleared slice, and it stays within the repo-local frontend scope allowed by the autonomy policy.

### Decision
Stop this resumed run in `HALT_POLICY_VIOLATION` after `TASK-FT012-03`.

### Why
`TASK-FT012-03` is verified, but the only remaining W1 item is the FT-001 deploy handoff, and continuing into deploy/prod writes would violate the autonomy policy. W2 intentionally remains queued until W1 is cleared.

### Decision
Resume the autonomous run with `TASK-FT013-01` as the next repo-local task even though `TASK-FT001-02` stays blocked.

### Why
`TASK-FT001-02` is an operator-only deploy handoff, not a repository-local prerequisite for the W2 pricing/access UI work. Promoting the first FT-013 slice keeps the run inside repo-local scope without violating the autonomy policy.

### Assumption
`TASK-FT013-01` may close as a verification-and-sync task if the FT-012 access-status implementation already satisfies the slice.

### Decision
Close `TASK-FT013-01` as `done` without product code edits.

### Why
The existing FT-012 implementation already loads backend entitlement data through `frontend/src/lib/stores/access.ts`, resets it in `frontend/src/App.svelte`, and surfaces starter and paid-plan states in `frontend/src/lib/components/BoardsSidebar.svelte`. The task only required verification, protocol artifacts, and Memory Bank sync.

### Decision
Stop this resumed run in `HALT_BUDGET_EXCEEDED` after `TASK-FT013-01`.

### Why
The next ready slice, `TASK-FT013-02`, adds a new paywall modal and pricing-alignment UI. That is a materially larger frontend change than this verification-only closure and should start with a fresh unattended session budget.

### Decision
Resume the autonomous run with `TASK-FT013-02` as the active task.

### Why
The review gate is still `APPROVE`, there are no blocking questions, and `TASK-FT013-02` is the only dependency-cleared ready slice in the backlog.

### Assumption
The in-app paywall can stay repo-local and non-transactional in this slice by previewing plans and messaging without any external checkout or payment redirect.

### Why
That keeps the work inside the autonomy policy while delivering the required paywall UI surface ahead of the separate analytics-only upgrade-intent slice.

### Decision
Close `TASK-FT013-02` as `done` and promote `TASK-FT013-03` immediately.

### Why
The paywall modal, friendly exhausted-access messaging, and shared pricing preview now pass local frontend validation, and the next FT-013 slice is a narrow analytics-only follow-up touching the same repo-local surface.

### Decision
Close `TASK-FT013-03` as `done` and halt this autopilot run in `HALT_DEPENDENCY_DEADLOCK`.

### Why
FT-013 is now fully verified, but the backlog has no remaining `ready` tasks. The only unfinished W1 slice is still blocked by deploy policy, and the rest of W2/W3 remain `planned`, so the queue cannot advance automatically under the autopilot selection rule.

### Decision
Use only already-installed project skills for the resumed FT-010 work.

### Why
The PRD mentions several tools and CLIs, but the repo already has the needed local skills (`autonomous`, `execute`, `verify`, `mb-sync`, and `add-tests`). No marketplace installation is required for the next repo-local slices.

### Decision
Promote `TASK-FT010-01` and `TASK-FT010-02` as the next safe FT-010 slices.

### Why
They are repo-local, dependency-cleared after `TASK-FT008-03`, and smaller than the remaining W2 product slices. Closing the implementation slice and its regression-lock slice together keeps the special-question rewrite internally consistent.

### Decision
Keep the legacy special-question category IDs (`reflector`, `constructor`, `centrist`) while renaming only the visible labels.

### Why
Existing session history and pending-question IDs already reference those identifiers. Preserving them avoids breaking localization lookups or duplicating old prompts in saved sessions.

### Decision
Stop this resumed run in `HALT_BUDGET_EXCEEDED` after `TASK-FT010-02`.

### Why
The FT-010 rewrite and regression locks are verified. The remaining follow-up (`TASK-FT010-03`) is manual real-user validation work, and any new W2 repo-local feature promotion should begin in a fresh unattended execution budget.

### Decision
Promote `TASK-FT003-01` as the next safe onboarding slice.

### Why
It is dependency-cleared after `TASK-FT008-03`, stays fully repo-local, and is smaller than the export and blind-spot feature work still queued in W2.

### Decision
Close `TASK-FT003-01` as `done` and halt this run in `HALT_BUDGET_EXCEEDED`.

### Why
The ordered onboarding state, persistence, and regression coverage are verified locally. The next slice (`TASK-FT003-02`) is the richer desktop/mobile UI walkthrough and should start in a fresh unattended execution budget.
