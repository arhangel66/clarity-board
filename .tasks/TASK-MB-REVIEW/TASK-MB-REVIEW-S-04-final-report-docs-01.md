# TASK-MB-REVIEW S-04 — Security, Privacy, Payment & Policy Risk Report

**Date:** 2026-03-08
**Reviewer:** Claude (autonomous review gate)
**Scope:** Autonomous backlog (W1–W3), PRD alignment, autonomy policy compliance

---

## 1. Security Risks

### 1.1 Auth Reliability (FT-008) — LOW risk
- TASK-FT008-01/02/03 deal with token refresh, revoked sessions, and re-login flows.
- All work is frontend-only (auth store, App.svelte, e2e tests). No backend auth changes.
- Risk: minimal — improvements to existing Auth0 integration, no new auth surfaces.
- The dev-bypass mode (`DEV_AUTH_BYPASS=true`) is already isolated to local dev; no backlog task exposes it to production.

### 1.2 Session Access & Limits (FT-012) — MEDIUM risk
- TASK-FT012-01/02 introduce `backend/app/access.py` — a new entitlement/access-control layer.
- **Concern:** Access enforcement logic is new server-side code that gates AI-assisted sessions. If implemented incorrectly, users could bypass limits or lose legitimate access.
- **Mitigation in backlog:** Task cards specify backend pytest coverage and verify that "free/monthly/lifetime access states persist per user and are enforced before AI-assisted session starts."
- **Recommendation:** Ensure access checks are applied at the WebSocket handler level (not just REST), since the core loop runs over WebSocket. The task card's `Touched files` includes `main.py` and `main_service.py`, which is correct.

### 1.3 No Secret Exposure Risks
- The autonomy policy explicitly excludes secret reads and prod writes.
- No task card touches `.env`, credentials, or API keys.
- `backend/data/events.jsonl` is untracked and explicitly marked as a user artifact not to be modified.

---

## 2. Privacy Risks

### 2.1 Analytics & Webvisor (FT-002) — MEDIUM risk
- FT-002 is already done (TASK-FT002-01 status: done).
- **Concern:** Yandex Metrica Webvisor records user sessions. The PRD acknowledges that "canvas card content may be visible in recordings" and says "add notice to ToS."
- **Current state:** No ToS update task exists in the backlog. The PRD treats this as a notice-level item, but recording personal thinking content (facts about relationships, career decisions, health) without explicit consent is a **real privacy risk**.
- **Recommendation:** Add a task to implement a cookie/tracking consent banner and update ToS before the landing redesign (FT-001) is deployed. This is **not blocking** for autonomous local work but **is blocking** for production deploy.

### 2.2 Backend Event Logging
- `backend/app/services/event_service.py` logs session events (duration, card count, phase).
- The verification artifact references "payload privacy constraints" — this is good.
- No PII appears to be logged in event payloads based on the task card scope.

### 2.3 Decision Memo Export (FT-004) — LOW risk
- Generates Markdown from session data. Download + clipboard = user-initiated, no external transmission.
- No server-side storage of exported memos mentioned.

---

## 3. Payment & Monetization Risks

### 3.1 Session Limits (FT-012) + Paywall UI (FT-013) — MEDIUM risk
- PRD Section 9 describes a "Freemium with Credits" model, but the backlog implements a simpler "3 free sessions" model (REQ-031).
- **Inconsistency:** PRD says "credits per action" (card creation = 1, voice = 2, etc.), but requirements.md says "3 free sessions total + plan access per user." The backlog follows requirements.md, not the PRD credit model.
- **This is acceptable** — the PRD explicitly states "No real payment processor at launch — measure intent only," and REQ-032 confirms "no real payment yet." The simpler session-count model is a reasonable MVP simplification.
- **Concern:** TASK-FT013-02 creates `PaywallModal.svelte` with upgrade buttons. If these buttons link to external payment pages or collect payment info, that would be a policy violation for autonomous execution. The task card says "confirm... no real payment integration exists," which is the correct guard.

### 3.2 No Financial Transaction Risk
- No Stripe, payment gateway, or billing integration in any task card.
- Upgrade clicks are tracked as analytics events only.

---

## 4. Policy Risks (Autonomy Compliance)

### 4.1 Deploy Tasks — CORRECTLY BLOCKED
- TASK-FT001-02 (landing deploy) is status `blocked`. This is correct per the autonomy policy: "secret reads / prod writes / deploys" are hard-stop categories.
- TASK-FT011-02/03 (domain cutover) are in W3 and `planned`, not `ready`. They involve DNS/SSL changes — correctly deferred.
- TASK-FT014-02 (publish LinkedIn article) — external action, correctly in W3/planned.

### 4.2 Queue Safety — CORRECT
- Only `TASK-FT008-01` is marked `ready`. It has no dependencies and is purely frontend local work (auth store improvements + tests).
- All other tasks respect dependency chains. No circular dependencies detected.
- Wave ordering is correct: W1 tasks complete before W2 starts; W2 before W3.

### 4.3 Manual/External Tasks — CORRECTLY DEFERRED
- FT-009 (Demand Validation): manual user research — W3, planned.
- FT-010-03 (Special Questions user testing): manual evidence — W2, depends on FT-010-02.
- FT-014/FT-016 (content publication): manual external actions — W3.
- None of these are marked `ready` or could accidentally run autonomously.

### 4.4 Failure Budget Compliance
- Budget: `max_retries: 2`, `max_consecutive_failures: 3`, `max_open_blockers: 3`, `max_files_changed: 12`.
- Current state: 0 failures, 1 blocker (TASK-FT001-02 deploy). Well within limits.

---

## 5. RTM Alignment

### 5.1 Requirements ↔ Backlog Consistency — GOOD
- Every REQ in requirements.md has corresponding task cards in backlog.md.
- RTM in requirements.md maps REQs to Epics, Features, and Tests.
- Two minor gaps:
  - REQ-020 (landing) maps to FT-001 which has `in_progress` in requirements.md but `done` in backlog (TASK-FT001-01). **Not a conflict** — the REQ covers both local implementation and deploy; local part is done, deploy is blocked.
  - REQ-025 (AI validation) and REQ-021 (analytics) show `done` in both places. Consistent.

### 5.2 PRD ↔ Requirements Drift — MINOR
- PRD uses "credits" model; requirements.md uses "sessions" model. Already addressed in Section 3.1.
- PRD references `P1-B2` through `P1-B11`; requirements.md captures these as `REQ-020` through `REQ-032`. Complete mapping.

---

## 6. Findings Summary

| # | Finding | Severity | Blocking? |
|---|---------|----------|-----------|
| F1 | No ToS/consent banner task for Webvisor tracking | Medium | No (blocks deploy, not local dev) |
| F2 | PRD credit model vs requirements session model inconsistency | Low | No (documented simplification) |
| F3 | FT-012 access enforcement must cover WebSocket path | Medium | No (task card already touches correct files) |
| F4 | PaywallModal must not include real payment integration | Medium | No (task card explicitly verifies this) |
| F5 | Deploy tasks correctly blocked by autonomy policy | Info | No |
| F6 | Only dependency-free `TASK-FT008-01` is marked ready | Info | No |

---

## 7. Recommendations

1. **Before deploy (TASK-FT001-02):** Add a tracking consent/ToS task. Not needed for autonomous local work.
2. **During FT-012 implementation:** Verify access checks at WebSocket `init` handler, not just REST endpoints.
3. **During FT-013 implementation:** Ensure PaywallModal upgrade buttons are analytics-only (no external payment redirect).
4. **Backlog hygiene:** Consider aligning PRD Section 9 with the actual session-count model to reduce confusion for future agents.

---

## 8. Conclusion

The autonomous backlog is well-structured for safe local execution. Deploy and external tasks are correctly blocked. The only `ready` task (TASK-FT008-01) is low-risk frontend auth improvement work with no security, privacy, or payment implications. Privacy concerns around Webvisor are real but only become blocking at deploy time, not during local development. No policy violations detected.

---

**VERDICT: APPROVE**
