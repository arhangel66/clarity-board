---
description: Feature brief for rewritten special questions.
id: FT-010
title: Special Questions Rewrite
status: draft
epic: EP-003
reqs: [REQ-029]
depends: []
---
# FT-010: Special Questions Rewrite

## Goal
Legally clean, high-quality probing questions with original formulations.

## Acceptance criteria
- [ ] All questions rephrased to be original (no verbatim matches with sources)
- [ ] Categories renamed from Reflector/Constructor/Centrist to new names
- [ ] Questions generic enough for any domain (not just business)
- [ ] 3-category structure preserved
- [ ] Tested with real users for clarity and impact

## Touched files (expected)
- `backend/data/questions.json` (rewrite content)
- `backend/app/special_questions.py` (update category names if needed)
- `frontend/src/lib/stores/i18n.ts` (category name translations)
