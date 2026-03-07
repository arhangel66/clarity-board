---
description: Orchestrator plan for brownfield Memory Bank bootstrap.
status: in_progress
---
# TASK-MB-MAP: Brownfield Codebase Mapping

## Scenario
Brownfield — existing codebase, no PRD, no Memory Bank.

## Steps
1. [x] Create `.memory-bank/` skeleton (directories + core files)
2. [x] Create `.tasks/TASK-MB-MAP/` for scan artifacts
3. [x] Launch 5 parallel scan subagents:
   - S-01: Build/tooling/CI
   - S-02: Backend services
   - S-03: Frontend/UI
   - S-04: Data layer/models
   - S-05: Tests & quality gates
4. [x] Synthesize Memory Bank from scan reports:
   - product.md (what the system is today)
   - architecture/overview.md (C4 L1-L2, key invariants)
   - architecture/frontend.md (component tree, stores, canvas)
   - guides/dev-setup.md (setup, commands, testing, deploy)
   - contracts/websocket-protocol.md (WebSocket + REST API)
   - testing/index.md (quality gates, gaps)
   - index.md (annotated links)
5. [x] Update AGENTS.md
6. [ ] Ask user for PRD delta

## Non-overlapping file scopes
- S-01: pyproject.toml, package.json, docker-compose.yml, .github/, debug/, Dockerfile, .pre-commit-config.yaml, vite.config.ts, .env.example
- S-02: backend/app/**/*.py
- S-03: frontend/src/**/*
- S-04: backend/app/models.py, backend/data/, *.db, WebSocket schemas
- S-05: backend/tests/, frontend/src/**/*.test.*, e2e/, playwright.config.ts
