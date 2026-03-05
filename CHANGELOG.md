# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For releases with breaking changes, include a `### Migration Notes` section.

## [Unreleased] - 2026-03-05

### Added
- Added architecture-first execution plan with explicit P0/P1/P2 sequence in `ROADMAP.md`.
- Added formal note that current production deployment process is driven by `/Users/mikhail/w/learning/fact/.claude/skills/deploy`.
- Added explicit P0 tracks for architecture sync, CI quality gates, release discipline, and data reliability.
- Added `ARCHITECTURE_PLAN.md` with milestones A1-A6 and Definitions of Done.
- Added frontend `check` script (`svelte-check`) and wired it into CI quality steps.
- Added architecture governance docs:
  - `docs/architecture/MODULE_BOUNDARIES.md`
  - `docs/architecture/WEBSOCKET_CONTRACT.md`
  - ADR set under `docs/adr/0001..0003`
- Added release/operations docs:
  - `docs/release/RELEASE_CHECKLIST.md`
  - `docs/release/DATA_BACKUP_RESTORE.md`
- Added managed DB operations scripts:
  - `backend/scripts/migrate.py`
  - `backend/scripts/backup_db.sh`
  - `backend/scripts/restore_db.sh`
  - `backend/scripts/restore_smoke.sh`
- Added PR quality checklist template: `.github/pull_request_template.md`.
- Added demo-first onboarding building blocks:
  - `frontend/src/lib/data/demo-session.json`
  - `frontend/src/lib/components/DemoBanner.svelte`
  - `frontend/src/lib/components/TooltipOverlay.svelte`

### Changed
- Reorganized roadmap to a sequential execution model (`P0-A1` -> `P2-C2`) instead of a feature-only backlog.
- Prioritized architecture and engineering stability before new product surface area.
- Rewrote `ARCHITECTURE.md` to reflect current backend/runtime structure and protocol surface.
- Rewrote `backend/docs/ARCHITECTURE_DEEP.md` to reflect current services, flow, and storage model.
- Updated E2E auth test selectors to match the new landing page markup and removed CI skip.
- Expanded `.github/workflows/e2e.yml` with backend tests, frontend tests, build, and svelte-check before Playwright run.
- Updated deploy workflow to run only after successful `E2E Tests` workflow for pushes to `main`.
- Updated `MobileDrawer` onboarding integration to use `onboarding.maybeShow(...)` API.
- Updated app board/session flow to initialize demo board for first-time users and swap to real board on creation.

### Fixed
- Cleaned roadmap wording/typos and normalized terminology (blind spots, priorities, DoD).
