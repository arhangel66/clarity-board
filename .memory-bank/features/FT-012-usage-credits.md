---
description: Feature brief for session access and limits.
id: FT-012
title: Session Access & Limits System
status: draft
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

## Open questions
- What exactly counts as a consumed session in product logic
- How monthly renewal/cancellation state is represented before real billing exists
- Whether session packs are needed later in addition to monthly/lifetime plans

## Touched files (expected)
- `backend/app/access.py` (new — access/entitlement service)
- `backend/app/construct.py` (wire access/entitlement service)
- `backend/app/main_service.py` (check session access before AI session starts)
- `backend/app/main.py` (access/session limits REST endpoint)
