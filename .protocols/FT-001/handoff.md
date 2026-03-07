# FT-001 Handoff

## Summary
- Landing now communicates a sessions-based freemium offer instead of implying permanent free use.
- Added a dedicated pricing section with `3 free sessions total`, `$10/month unlimited`, and `$100 lifetime`.
- RU and EN copies are aligned across hero, trust, pricing, FAQ, and footer.

## Changed Areas
- `frontend/src/lib/components/LandingPage.svelte`
- `frontend/src/lib/stores/i18n.ts`
- `.memory-bank/features/FT-001-landing-redesign.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/changelog.md`

## Verification
- `cd frontend && pnpm check`
- `cd frontend && pnpm build`
- `cd frontend && pnpm test -- --run`
- `cd frontend && pnpm vite preview --host 127.0.0.1 --port 4173`
- Playwright desktop + mobile preview smoke-check

## Follow-ups
- Define exact runtime rule for when a session is considered consumed
- Decide when landing pricing should switch from intent tracking to real checkout
- Commit/push/deploy once the broader dirty worktree is reconciled
