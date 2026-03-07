---
description: Feature brief for blind spot analysis on the canvas.
id: FT-005
title: Blind Spot Analysis
status: draft
epic: EP-002
reqs: [REQ-024]
depends: []
---
# FT-005: Blind Spot Analysis

## Goal
Core methodology value — help users see what they're NOT seeing.

## Acceptance criteria
- [ ] Gap analysis AI prompt fires after fact accumulation (>= N cards)
- [ ] UI indication of "empty zones" on canvas (areas lacking facts)
- [ ] Special questions targeting blind spots surfaced proactively
- [ ] Isolated cards highlighted (no connections)
- [ ] Missing link suggestions between related cards

## Touched files (expected)
- `backend/app/ai_service.py` (gap analysis prompt)
- `backend/app/main_service.py` (trigger logic)
- `frontend/src/lib/components/Canvas.svelte` (empty zone indicators)
- `frontend/src/lib/components/Card.svelte` (isolated card styling)
