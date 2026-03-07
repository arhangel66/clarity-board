---
id: FT-008
title: Auth Reliability
status: draft
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
