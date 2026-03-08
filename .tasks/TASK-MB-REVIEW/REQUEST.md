# TASK-MB-REVIEW Request

## Date
- `2026-03-08`

## Mode
- Autonomous run review gate before any new `TASK-*` execution

## Scope
- `.memory-bank/` after backlog normalization
- `.protocols/AUTONOMOUS-RUN/`
- Task planning docs in `.memory-bank/tasks/`

## Blocking concerns
- Task-card completeness and machine readability for `/autonomous`
- Wave ordering and whether only safe dependency-free work is marked `ready`
- RTM alignment between `requirements.md`, feature docs, and the new backlog
- Policy conflicts caused by deploy/prod-write steps that cannot run unattended
- Memory Bank navigation and MBB compliance after adding the new task routers/plans
