# FT-002 Verification

## Status
- PASS (local, verified on 2026-03-08)

## Acceptance criteria check
- [x] Yandex Metrica counter installed (pageview tracking)
- [x] Webvisor + clickmap enabled in the client bootstrap
- [x] Conversion goals emitted for landing -> sign-up -> first session -> 5+ cards -> session completed
- [x] Custom frontend events firing for card/connection creation, phase changes, special questions, input mode, and exports
- [x] Backend event logging working
- [x] Privacy: no card content or free-form user text sent to analytics payloads

## Commands
- `cd backend && uv run pytest tests/test_event_service.py -v`
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`

## Evidence
- Verification artifact: `.tasks/FT-002/verification-2026-03-08.md`
- `uv run pytest tests/test_event_service.py -v` passed: `5 passed`
- `pnpm test -- --run` passed: `5` files / `10` tests
- `pnpm check` passed with `0 errors` and existing unrelated warnings
- `pnpm build` passed with existing unrelated warnings only
- `frontend/index.html` contains counter `107194444` with `webvisor:true` and `clickmap:true`
- `frontend/src/lib/analytics.ts` now includes `session_exported` in addition to the existing funnel and product events
- Export tracking is wired from both `BoardsSidebar.svelte` and `SelectionToolbar.svelte`
- `backend/app/services/event_service.py` and `backend/app/services/main_service.py` cover backend analytics logging

## Verdict
- PASS for FT-002 MVP instrumentation.
- Remaining Yandex UI configuration and legal copy are operational follow-ups, not blocking product code gaps.
