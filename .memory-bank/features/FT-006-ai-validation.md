---
description: Feature brief for AI output validation safeguards.
id: FT-006
title: AI Output Validation
status: done
epic: EP-003
reqs: [REQ-025]
depends: []
---
# FT-006: AI Output Validation

## Goal
Reliable, trustworthy AI behavior — catch bad output before it reaches the canvas.

## Acceptance criteria
- [x] Validate AI output: coordinates are clamped, text is capped, and invalid card references are rejected
- [x] Detect and prevent duplicate cards
- [x] Protect the root card (question) from unwanted reformulation or deletion outside Phase 1
- [x] Log validation failures for analysis

## Follow-up
- Collect 10+ real sessions and evaluate AI quality
- Tune model parameters based on evaluation

## Touched files (expected)
- `backend/app/services/validator.py` (post-decode validation layer)
- `backend/app/services/main_service.py` (validation hook and root-card protection)
- `backend/tests/test_validator.py` (validator coverage)
