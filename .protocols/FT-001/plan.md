# FT-001 Plan — Landing Page Redesign

## Changes

### 1. Hero section — pain-first rewrite
- **Current:** "Just talk. Your AI partner will organize the chaos" (feature-focused)
- **Target:** Lead with the pain/cost of bad decisions, then reveal the solution
- New headline examples: "Mistakes cost $50k. One hour of clarity costs nothing." / "Your head holds 3-4 thoughts. Your problem has 30 pieces."

### 2. Remove fake metrics bar
- **Current:** "10,000+ Sessions", "2,500+ Decisions Unlocked" — dishonest
- **Target:** Remove entire metrics bar section. Replace with nothing (honest absence > fake numbers)

### 3. Expand personas from 4 to 6
- Add: "Coach / Therapist" (structured client work)
- Add: "Student / Learner" (structured thinking habit)

### 4. Add social proof / testimonials section
- Structure ready with 2-3 placeholder slots
- Empty state: "Be among the first to try" or similar honest copy

### 5. Copy rewrite — transformation focus
- Focus on what user BECOMES, not what tool DOES
- "7 results you'll get" pattern from reference
- Rewrite result items to be more specific and transformational

### 6. Trust signals enhancement
- Add explicit: "No credit card", "Your data stays private", "Free to start"
- Visual trust badges near CTA

### 7. FAQ tuning
- Add objection-oriented questions: "Is AI deciding for me?", "What if I don't know my problem?"

## Files touched
- `frontend/src/lib/components/LandingPage.svelte` — structural changes
- `frontend/src/lib/stores/i18n.ts` — all landing copy (ru + en)

## Quality gates
- `cd frontend && pnpm build && pnpm check` — typecheck + build
- `cd frontend && pnpm test -- --run` — unit tests
- Visual check on localhost:5173
- Mobile responsive check (768px breakpoint)
