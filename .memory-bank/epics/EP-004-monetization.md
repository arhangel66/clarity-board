---
id: EP-004
title: Monetization Infrastructure
status: draft
wave: W1
reqs: [REQ-031, REQ-032]
---
# EP-004: Monetization Infrastructure

## Business value
Validate willingness to pay before building real billing. Track usage patterns to inform pricing decisions. Show paywall to measure intent.

## Scope
- Session access/limits system (backend tracking per user)
- Pricing and upgrade UI (landing + in-app, no real payment processor initially)
- Usage analytics (sessions used per user, plan selection, upgrade intent)

## Features
- FT-012: Session access & limits system
- FT-013: Pricing & upgrade UI + intent tracking

## Success metrics
- Free-session consumption tracked per user
- Upgrade UI shown when free sessions are exhausted
- Click-through rate on "upgrade" measured
- Usage distribution data available for pricing decisions

## Open questions
- What exactly counts as a consumed session
- Whether launch starts with real checkout or intent tracking only
- Whether monthly unlimited and lifetime remain the only public plans
