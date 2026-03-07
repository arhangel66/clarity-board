---
id: FT-007
title: TODO Cards as Action Plan
status: draft
epic: EP-002
reqs: [REQ-026]
depends: []
---
# FT-007: TODO Cards as Action Plan

## Goal
Bridge from insight to action — users leave with a concrete to-do list.

## Acceptance criteria
- [ ] Filter/panel showing only TODO-type cards
- [ ] Toggle done/undone on TODO cards
- [ ] Separate export of action items (Markdown list)
- [ ] TODO count badge visible in UI

## Touched files (expected)
- `frontend/src/lib/components/` (new TodoPanel component)
- `frontend/src/lib/stores/cards.ts` (done/undone state)
- `backend/app/` (persist done state in card data)
