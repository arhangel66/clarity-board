# TASK-FT010-01 Verification Evidence

## Commands
- `cd backend && uv run pytest tests/test_special_questions.py -v`
- `cd frontend && NODE_OPTIONS=--experimental-require-module pnpm test -- --run`
- `cd frontend && pnpm check`

## Evidence
- `total_questions_declared = 30`
- `total_questions_actual = 30`
- `reflector:1` localizes to `Ракурс` in RU and `Perspective` in EN through `SpecialQuestionsService`
- Pending special questions now carry `category_label` and render it in `CurrentQuestion`

## Result
- PASS
