---
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
- [ ] Validate AI output: coordinates in bounds (0-1), text within 200 chars
- [ ] Detect and prevent duplicate cards
- [ ] Protect root card (question) from unwanted reformulation
- [ ] Log validation failures for analysis
- [ ] Collect 10+ real sessions and evaluate AI quality
- [ ] Tune model parameters based on evaluation

## Touched files (expected)
- `backend/app/decoder.py` (validation layer)
- `backend/app/ai_service.py` (parameter tuning)
- `backend/app/main_service.py` (root card protection)
