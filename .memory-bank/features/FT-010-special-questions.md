---
description: Feature brief for rewritten special questions.
id: FT-010
title: Special Questions Rewrite
status: in_progress
epic: EP-003
reqs: [REQ-029]
depends: []
---
# FT-010: Special Questions Rewrite

## Goal
Legally clean, high-quality probing questions with original formulations.

## Acceptance criteria
- [x] All questions rephrased to be original (no verbatim matches with sources)
- [x] Categories renamed from Reflector/Constructor/Centrist to new names
- [x] Questions generic enough for any domain (not just business)
- [x] 3-category structure preserved
- [ ] Tested with real users for clarity and impact

## Current verified progress
- `TASK-FT010-01` rewrote the RU/EN deck with 30 domain-neutral prompts and renamed visible category labels while preserving the legacy internal IDs.
- The special-question payload/history now carries a localized `category_label`, and `frontend/src/lib/components/CurrentQuestion.svelte` shows it with an i18n fallback.
- `TASK-FT010-02` added deterministic backend/frontend regression coverage for the rewritten deck metadata and visible labels.

## Open questions
- `TASK-FT010-03` still needs real-user review to confirm clarity and impact of the rewritten prompts.

## Touched files (expected)
- `backend/data/questions.json` (rewrite content)
- `backend/app/services/special_questions.py` (localized category label loading)
- `backend/tests/test_special_questions.py` (deck integrity + label regression coverage)
- `frontend/src/lib/stores/i18n.ts` (category name translations)
- `frontend/src/lib/components/CurrentQuestion.svelte` (visible category label)
- `frontend/src/lib/components/CurrentQuestion.test.ts` (visible label regression coverage)
