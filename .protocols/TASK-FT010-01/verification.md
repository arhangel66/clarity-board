# TASK-FT010-01 Verification

## Status
- PASS

## Acceptance / checks
- [x] The special-question deck uses original, domain-neutral RU/EN wording
- [x] The three visible category names are renamed consistently
- [x] Pending special-question payloads carry the localized category label
- [x] The frontend special-question surface can show the renamed category label
- [x] `cd backend && uv run pytest tests/test_special_questions.py -v` passes
- [x] `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run` passes
- [x] `cd frontend && pnpm check` passes

## Evidence
- `backend/data/questions.json`
- `backend/app/models.py`
- `backend/app/services/special_questions.py`
- `backend/app/services/main_service.py`
- `frontend/src/lib/types.ts`
- `frontend/src/lib/components/CurrentQuestion.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `.tasks/TASK-FT010-01/TASK-FT010-01-S-IMPL-final-report-code-01.md`
- `.tasks/TASK-FT010-01/verification-2026-03-08.md`

## Verdict
- PASS
