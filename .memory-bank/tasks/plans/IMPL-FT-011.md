---
description: Implementation plan for FT-011 own-domain and branding rollout.
status: active
---
# IMPL-FT-011

## Goal
Move the product to a dedicated domain with aligned branding and updated auth/network configuration.

## Steps
- Record the domain decision and repo-side config checklist first.
- Update repo-managed references, env examples, nginx config, and Auth0/CORS callback documentation.
- Treat domain purchase, DNS, SSL issuance, and traffic cutover as operator tasks outside unattended repo execution.

## Expected touched files
- `README.md`
- `.memory-bank/features/FT-011-own-domain.md`
- `.memory-bank/guides/dev-setup.md`
- deployment config files already in repo if the chosen domain changes them

## Tests
- Repo-side config review
- Post-cutover manual health check

## Quality gates
- No production hostname change should be attempted without an explicit operator decision.

## Verify / UAT
- Confirm the new domain serves the app and all callbacks/redirects work after manual cutover.
