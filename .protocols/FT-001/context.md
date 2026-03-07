# FT-001 Context

## Loaded docs
- `.memory-bank/features/FT-001-landing-redesign.md`
- `.memory-bank/product.md`
- `.memory-bank/architecture/frontend.md`
- `.protocols/FT-001/decision-log.md`
- `prd.md` (sections 7, 14)
- `frontend/src/lib/components/LandingPage.svelte` (current ~700 lines)
- `frontend/src/lib/stores/i18n.ts` (landing keys, ru/en)

## Key constraints
- Svelte 5, TailwindCSS v4, i18n (ru/en)
- Cork board aesthetic (warm palette, Fraunces/DM Sans/Caveat fonts)
- Must keep Google login flow (Auth0)
- Yandex Metrica already active (counter 107194444)
- Reference: https://lk.brain-games.ru/fc (Kurpatov course landing patterns)

## Commands used
- `pnpm check`
- `pnpm build`
- `pnpm test -- --run`
- `pnpm vite preview --host 127.0.0.1 --port 4173`
