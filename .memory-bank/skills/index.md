---
description: Registry of available skills in this repository.
status: active
---
# Skills

## Installed
- [../../.agents/skills/add-tests/SKILL.md](../../.agents/skills/add-tests/SKILL.md): Add focused unit, integration, or e2e coverage.
- [../../.agents/skills/autonomous/SKILL.md](../../.agents/skills/autonomous/SKILL.md): Run a full autonomous PRD-to-execution loop.
- [../../.agents/skills/autopilot/SKILL.md](../../.agents/skills/autopilot/SKILL.md): Process backlog tasks in clean agent sessions.
- [../../.agents/skills/cold-start/SKILL.md](../../.agents/skills/cold-start/SKILL.md): Bootstrap or route repository work from a cold start.
- [../../.agents/skills/discuss/SKILL.md](../../.agents/skills/discuss/SKILL.md): Clarify ambiguities and keep a decision log before implementation.
- [../../.agents/skills/execute/SKILL.md](../../.agents/skills/execute/SKILL.md): Execute one `TASK-*` with plan, gates, verify, and MB sync.
- [../../.agents/skills/find-skill/SKILL.md](../../.agents/skills/find-skill/SKILL.md): Find one relevant skill for the current task.
- [../../.agents/skills/find-skills/SKILL.md](../../.agents/skills/find-skills/SKILL.md): Find several relevant skills for the current task.
- [../../.agents/skills/map-codebase/SKILL.md](../../.agents/skills/map-codebase/SKILL.md): Map an existing codebase into Memory Bank form.
- [../../.agents/skills/mb/SKILL.md](../../.agents/skills/mb/SKILL.md): Prime context from the Memory Bank before work.
- [../../.agents/skills/mb-execute/SKILL.md](../../.agents/skills/mb-execute/SKILL.md): Alias for the Memory Bank execution flow.
- [../../.agents/skills/mb-from-prd/SKILL.md](../../.agents/skills/mb-from-prd/SKILL.md): Alias for the PRD-to-Memory-Bank flow.
- [../../.agents/skills/mb-garden/SKILL.md](../../.agents/skills/mb-garden/SKILL.md): Maintain and de-drift the Memory Bank.
- [../../.agents/skills/mb-harness/SKILL.md](../../.agents/skills/mb-harness/SKILL.md): Set up deterministic harness commands and profiles.
- [../../.agents/skills/mb-init/SKILL.md](../../.agents/skills/mb-init/SKILL.md): Initialize the Memory Bank skeleton.
- [../../.agents/skills/mb-map-codebase/SKILL.md](../../.agents/skills/mb-map-codebase/SKILL.md): Alias for the brownfield mapping flow.
- [../../.agents/skills/mb-review/SKILL.md](../../.agents/skills/mb-review/SKILL.md): Alias for fresh-context Memory Bank review.
- [../../.agents/skills/mb-sync/SKILL.md](../../.agents/skills/mb-sync/SKILL.md): Sync indexes, RTM, and changelog after changes.
- [../../.agents/skills/mb-verify/SKILL.md](../../.agents/skills/mb-verify/SKILL.md): Alias for Memory Bank task verification.
- [../../.agents/skills/prd/SKILL.md](../../.agents/skills/prd/SKILL.md): Turn a PRD into requirements, epics, and features.
- [../../.agents/skills/prd-to-tasks/SKILL.md](../../.agents/skills/prd-to-tasks/SKILL.md): Decompose a feature into implementation tasks.
- [../../.agents/skills/review/SKILL.md](../../.agents/skills/review/SKILL.md): Run a multi-expert review pass.
- [../../.agents/skills/verify/SKILL.md](../../.agents/skills/verify/SKILL.md): Verify one task against acceptance criteria.

## When to use
- Prime or route work: `mb`, `cold-start`, `find-skill`, `find-skills`
- Plan or map: `prd`, `mb-from-prd`, `prd-to-tasks`, `discuss`, `map-codebase`, `mb-map-codebase`
- Execute or test: `execute`, `mb-execute`, `add-tests`, `verify`, `mb-verify`
- Review or maintain: `review`, `mb-review`, `mb-sync`, `mb-garden`, `mb-harness`, `mb-init`
- Orchestrate autonomously: `autonomous`, `autopilot`
