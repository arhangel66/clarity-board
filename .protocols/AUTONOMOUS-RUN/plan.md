# AUTONOMOUS-RUN Plan

## Objective
- Continue the existing PRD-backed repository through the local autonomous workflow.
- Normalize backlog/task metadata so `/autonomous` can schedule work safely.
- Run review and then execute the next safe task if the review gate passes.

## Run scope
- In scope: `.memory-bank/`, `.protocols/`, `.tasks/`, repository-local code and tests.
- Out of scope: deploy, production writes, secret reads, infrastructure changes outside the repo.

## Preflight summary
- `.memory-bank/` exists and is populated.
- `prd.md` exists in the repo root and is dated `2026-03-07`.
- Both local executors are available: `codex` and `claude`.
- `.memory-bank/workflows/autonomy-policy.md` exists.
- The repository already contains substantial code and an existing brownfield baseline, so this run continues from the current Memory Bank instead of rebuilding it from scratch.

## Existing state carried into this run
- L1-L3 product docs already exist in `.memory-bank/`.
- `FT-002` and `FT-006` are documented as done.
- `FT-001` has local implementation and verification artifacts but is not deployed.
- `.memory-bank/tasks/backlog.md` is still feature-level and must be converted into task cards before autonomous scheduling.

## Failure budgets
- `max_retries_per_task: 2`
- `max_consecutive_failures: 3`
- `max_open_blockers: 3`
- `max_files_changed_per_task: 12`

## Execution phases
1. Initialize autonomous-run artifacts and assumptions.
2. Create autonomous-ready implementation plans and task cards.
3. Run Memory Bank review and fix blocking doc issues.
4. Execute the next safe `ready` task, verify it, and sync Memory Bank state.
5. Stop only in an explicit terminal state.
