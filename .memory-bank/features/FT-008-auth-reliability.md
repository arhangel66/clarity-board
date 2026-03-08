---
description: Feature brief for auth reliability improvements.
id: FT-008
title: Auth Reliability
status: in_progress
epic: EP-003
reqs: [REQ-027]
depends: []
---
# FT-008: Auth Reliability

## Goal
Zero auth-related user drop-off.

## Acceptance criteria
- [ ] E2E test: login -> close -> reopen after 24h (token refresh)
- [ ] Refresh token path verified and working
- [ ] Edge cases handled: revoked access, expired token, network error
- [ ] Clear re-login button + user-friendly error message
- [ ] Auth state survives page refresh

## Touched files (expected)
- `frontend/src/lib/stores/auth.ts` (token refresh logic)
- `backend/app/auth.py` (edge case handling)
- `e2e/` (auth reliability tests)

## Current verified progress
- `TASK-FT008-01` is complete locally.
- `TASK-FT008-02` is complete locally.
- Auth init and silent refresh paths are covered by `frontend/src/lib/stores/auth.test.ts`.
- Revoked-session and transient-auth failures now diverge into the correct recovery states.
- The auth recovery shell now shows localized retry and re-login actions with explicit “your boards are still here” messaging.
- `e2e/tests/auth.spec.ts` verifies dev-bypass auth survives a page reload.
- Remaining work stays in `TASK-FT008-03`.
