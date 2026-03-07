---
description: Product brief (C4 L1) — what it is, audience, core value, constraints.
status: active
---
# Product: Fact Card System

## What this is
A digital tool for structured thinking: users externalize complex problems onto a single-screen canvas where AI assists in structuring facts, revealing connections, and surfacing blind spots. Based on fact-card methodology principles.

Live at: https://fact.slotik.app/ (will migrate to dedicated domain)

## Core value
**One screen = one problem.** No scrolling. All facts visible at once on a spatial canvas, with AI guiding the user through a structured thinking process (Question -> Facts -> Pains -> Resources -> Gaps -> Connections).

**Transformation:** fog of thoughts -> visual clarity -> concrete action plan.

## Audience
| Segment | Priority |
|---|---|
| People stuck on tough decisions (career, relationship, life) | Primary |
| Entrepreneurs/leaders making strategic bets | Primary |
| Creatives developing new products/projects | Primary |
| Coaches and psychologists (structured client work) | Secondary |
| Students and learners (structured thinking habit) | Secondary |
| Personal development seekers | Secondary |

**Languages:** Russian, English (bilingual i18n).

## Primary user flow
1. User opens app -> authenticates (Auth0 / Google)
2. Creates/selects a board (session)
3. States a central problem — the "puzzlement" (question phase)
4. AI asks probing questions to convert abstractions into concrete facts
5. User dumps facts; AI creates typed cards (fact, pain, resource, hypothesis, todo)
6. User drags, edits, connects cards spatially
7. AI advances through phases: Question -> Facts -> Pains -> Resources -> Gaps -> Connections
8. AI surfaces patterns: causation chains, contradictions, blind spots
9. User reaches insight and formulates action items (TODO cards)
10. User exports result as decision memo (Markdown)

## Business model
- **Freemium with credits:** every user starts with X free credits
- Credits consumed on AI-powered actions (voice recognition, card creation)
- Subscription increases or removes limits
- Launch phase: no real payment, but show paywall UI + track intent clicks

## Current state (MVP shipped)
- WebSocket real-time canvas with AI-guided 6-phase flow
- Auth0 + dev bypass, multi-session boards, card/connection CRUD
- Special questions deck (ru/en), voice input (Whisper)
- i18n, onboarding overlay, mobile drawer, zoom, selection toolbar
- CI quality gates (pytest, vitest, svelte-check, build, e2e smoke)
- Landing page, Docker + nginx deploy

## Constraints
- **Tech stack:** FastAPI + WebSocket (Python 3.12), Svelte 5 + TypeScript (frontend), SQLite (storage), OpenRouter/Gemini (AI), Auth0 (auth)
- **Package managers:** uv (Python), pnpm (Node)
- **Infrastructure:** Docker + nginx on VPS, CI via GitHub Actions
- **Non-goals:** Multi-user collaboration, native mobile app, relational DB, self-hosted, marketplace of templates, external integrations (Notion, Trello)

## Key decisions
| Decision | Rationale | Status |
|---|---|---|
| JSON blob in SQLite | Simplicity over relational; session is atomic unit | active |
| Per-connection MainService | No shared mutable state between sessions | active |
| Pure decoder function | Clear boundary between LLM output and domain | active |
| OpenRouter + Gemini | Cost-effective, fast, good at structured JSON output | active |
| Svelte 5 runes | Fine-grained reactivity for canvas performance | active |
| Cork board aesthetic | Warm, handmade feel matching methodology spirit | active |
| Dev bypass auth | Fast local development without Auth0 setup | active |
| Freemium credits model | Measure demand before building billing | planned |
