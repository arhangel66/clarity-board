---
description: Epic brief for launch visibility, analytics, branding, and growth.
id: EP-001
title: Product Launch & Visibility
status: in_progress
wave: W1
reqs: [REQ-020, REQ-021, REQ-028, REQ-030, REQ-040, REQ-042]
---
# EP-001: Product Launch & Visibility

## Business value
Make the product discoverable, measurable, and professionally branded. Without this epic, the product exists but nobody finds it and we can't measure anything.

## Scope
- Landing page redesign (problem-first approach, 6 audience segments)
- Analytics infrastructure (Yandex Metrica, Webvisor, custom events)
- Own domain + branding
- Demand validation process
- Launch content (LinkedIn article, promo materials)

## Features
- FT-001: Landing page redesign
- FT-002: Analytics & event tracking
- FT-009: Demand validation
- FT-011: Own domain & branding
- FT-014: LinkedIn article (P2)
- FT-016: Promo content (P2)

## Success metrics
- Landing -> sign-up conversion >= 5%
- Yandex Metrica + Webvisor active with session recordings
- Own domain live with SSL
- >= 20 organic (non-invited) registrations

## Dependencies
- FT-002 (analytics) should ship before FT-001 (landing) goes live
- FT-011 (domain) before FT-014 (LinkedIn article)

## Current state
- FT-002 is done for MVP instrumentation: counter, funnel goals, product events, export tracking, and backend JSONL logging are verified locally.
- FT-001 is implemented locally and now only waits on deploy / launch sequencing.
