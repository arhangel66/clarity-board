---
description: Feature brief for session access and limits.
id: FT-012
title: Session Access & Limits System
status: in_progress
epic: EP-004
reqs: [REQ-031]
depends: []
---
# FT-012: Session Access & Limits System

## Goal
Track free sessions and paid access per user without exposing a credit model in the product UI.

## Acceptance criteria
- [ ] Each user starts with 3 free sessions total
- [ ] Access states supported per user: free, monthly unlimited, lifetime
- [ ] Session consumption is persisted per user
- [ ] Backend tracks session usage and current access plan
- [ ] API endpoint returns remaining free sessions or active paid plan
- [ ] AI access is blocked or upsold when free sessions are exhausted and no paid plan is active

## Current verified progress
- `TASK-FT012-01` is complete locally.
- `backend/app/access.py` now defines the launch access contract in `sessions`, not `credits`.
- `GET /api/access` returns the authenticated contract/status shape for FT-012 and FT-013.
- Session consumption is now defined as the first AI-assisted message on a blank board.
- Usage counts are currently marked `estimated_from_sessions`; persistent entitlements and enforcement remain in `TASK-FT012-02`.

## Open questions
- How monthly plan assignment and cancellation are represented before real billing exists
- Whether launch needs any plan state beyond `free`, `monthly`, and `lifetime`

## Touched files (expected)
- `backend/app/access.py` (new — access/entitlement service)
- `backend/app/construct.py` (wire access/entitlement service)
- `backend/app/main_service.py` (check session access before AI session starts)
- `backend/app/main.py` (access/session limits REST endpoint)
