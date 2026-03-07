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
- Usage credits/limits system (backend tracking per user)
- Paywall UI (frontend, no real payment processor)
- Usage analytics (credits consumed per user, per action type)

## Features
- FT-012: Usage credits & limits system
- FT-013: Paywall UI & intent tracking

## Success metrics
- Every AI action tracked with credit cost
- Paywall shown when credits exhausted
- Click-through rate on "upgrade" measured
- Usage distribution data available for pricing decisions

## Open questions
- Exact credit amounts per user (free tier)
- Credit cost per action type (voice vs card vs AI call)
- Subscription price point
