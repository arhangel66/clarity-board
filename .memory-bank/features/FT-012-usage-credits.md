---
description: Feature brief for session access and limits.
id: FT-012
title: Session Access & Limits System
status: done
epic: EP-004
reqs: [REQ-031]
depends: []
---
# FT-012: Session Access & Limits System

## Goal
Track free sessions and paid access per user without exposing a credit model in the product UI.

## Acceptance criteria
- [x] Each user starts with 3 free sessions total
- [x] Access states supported per user: free, monthly unlimited, lifetime
- [x] Session consumption is persisted per user
- [x] Backend tracks session usage and current access plan
- [x] API endpoint returns remaining free sessions or active paid plan
- [x] AI access is blocked when free sessions are exhausted and no paid plan is active

## Current verified progress
- `TASK-FT012-01` is complete locally.
- `TASK-FT012-02` is complete locally.
- `TASK-FT012-03` is complete locally.
- `backend/app/access.py` now persists per-user entitlements and consumed sessions in SQLite.
- `GET /api/access` returns tracked remaining free sessions or the active paid plan for FT-012 and FT-013.
- Session consumption is defined and enforced as the first AI-assisted message on a blank board.
- Existing started boards remain accessible after starter quota is exhausted.
- `frontend/src/lib/stores/access.ts` now hydrates the authenticated access snapshot and the sidebar surfaces starter sessions or the active paid plan without credits language.
- The frontend refreshes access status after the first successful AI-assisted turn on a blank board and hydrates server-provided `access_exhausted` snapshots.

## Open questions
- How monthly plan assignment and cancellation are represented before real billing exists

## Touched files (expected)
- `backend/app/access.py` (new — access/entitlement service)
- `backend/app/construct.py` (wire access/entitlement service)
- `backend/app/main_service.py` (check session access before AI session starts)
- `backend/app/main.py` (access/session limits REST endpoint)
- `frontend/src/lib/stores/access.ts` (authenticated access snapshot store)
- `frontend/src/App.svelte` (startup/reset wiring)
- `frontend/src/lib/components/BoardsSidebar.svelte` (in-app access status surface)
