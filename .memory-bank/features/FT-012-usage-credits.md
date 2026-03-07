---
id: FT-012
title: Usage Credits & Limits System
status: draft
epic: EP-004
reqs: [REQ-031]
depends: []
---
# FT-012: Usage Credits & Limits System

## Goal
Track AI usage per user with a credit system. Enable data-driven pricing decisions.

## Acceptance criteria
- [ ] Each user has a credit balance (starts with X free credits)
- [ ] Credits deducted on AI-powered actions:
  - Voice recognition (Whisper call)
  - Card creation via AI (chat completion call)
  - Blind spot analysis
  - Decision memo generation
- [ ] Credit balance persisted per user (extend SQLite or add user table)
- [ ] Backend tracks: action type, credit cost, timestamp, user_id
- [ ] API endpoint to check remaining credits
- [ ] Actions blocked when credits exhausted (with friendly message)

## Open questions
- Free tier credit amount
- Credit cost per action type
- Reset period (monthly? never?)

## Touched files (expected)
- `backend/app/credits.py` (new — credit service)
- `backend/app/construct.py` (wire credit service)
- `backend/app/main_service.py` (check credits before AI calls)
- `backend/app/main.py` (credits REST endpoint)
