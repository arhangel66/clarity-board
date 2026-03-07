---
id: FT-004
title: Decision Memo Export
status: draft
epic: EP-002
reqs: [REQ-023]
depends: []
---
# FT-004: Decision Memo Export

## Goal
Tangible output from a thinking session that users can share or act on.

## Acceptance criteria
- [ ] AI generates structured summary at session end (or on demand)
- [ ] Markdown format: problem statement, key facts, insights, connections, action items
- [ ] Download as .md file
- [ ] Copy to clipboard
- [ ] Export button visible in session UI
- [ ] Works with current session data (cards + connections)

## Touched files (expected)
- `backend/app/ai_service.py` (summary prompt)
- `backend/app/main_service.py` (export handler)
- `backend/app/main.py` (REST endpoint or WS message)
- `frontend/src/lib/components/` (export button + modal)
