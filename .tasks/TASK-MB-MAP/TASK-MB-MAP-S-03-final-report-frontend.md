---
description: Frontend architecture scan report.
status: done
---
# Frontend Architecture - Fact Card System

**Scope:** `frontend/src/`
**Framework:** Svelte 5 + TypeScript + Tailwind CSS v4 + Vite

## Component Tree

```
App.svelte
├── LandingPage.svelte (when not authenticated)
└── Main workspace (authenticated)
    ├── BoardsSidebar (left, collapsible)
    └── workspace
        ├── Canvas.svelte (core, fullscreen)
        │   ├── Connections.svelte (SVG overlay)
        │   └── Card.svelte (per card)
        ├── CurrentQuestion.svelte (centered overlay)
        ├── HelpOverlay.svelte (modal)
        ├── DemoBanner.svelte
        ├── TooltipOverlay.svelte
        ├── InputBar.svelte (bottom, voice + text)
        ├── MobileDrawer.svelte (off-canvas menu)
        └── CardDetailSheet.svelte (mobile detail)
```

18 Svelte components + 14 TypeScript stores.

## Store Architecture

| Store | Purpose |
|-------|---------|
| `websocket` | WS connection, reconnect (exp backoff), message routing, send methods |
| `cards` | Card array, position clamping, collision detection |
| `connections` | Card relationships |
| `boards` | Board list, active board selection |
| `auth` | Auth0 JWT, user info, login state |
| `session` | Phase, AI thinking state, question flow |
| `i18n` | Locale (ru/en), 1000+ translation keys, localStorage |
| `selectedCardIds` | Set for bulk operations (lasso, delete, scale) |
| `zoom` | Canvas zoom 0.6x-1.6x |
| `isMobile` | MediaQuery 768px breakpoint |
| `onboarding` | Tooltip triggers, seen tips |
| `drawer` | Mobile drawer state |
| `cardDetail` | Card detail sheet (mobile) |
| `chatMessages` | AI conversation history |

## Data Flow
1. Auth → Boards: login → fetch boards via REST
2. Board → WebSocket: board selection → init message → server loads session
3. WebSocket → Stores: server messages update cards, connections, session
4. UI → WebSocket: user actions → send methods → server

## Card System
- 6 types: question (purple), fact (blue), pain (red), resource (green), hypothesis (amber), todo (teal)
- Scale: 0.7 + importance * 0.6 * custom_scale (0.7x to 1.3x)
- Rotation: hash-based stable (−3° to +3°) for handmade feel
- Animations: cardAppear (300ms), newCardPulse (8s glow), cardFadeOut (500ms)
- Drag: multi-touch + mouse, group selection, z-index stacking
- Edit: double-click inline (max 200 chars)

## Canvas
- Cork board background (SVG fractal noise + radial gradient)
- Zoom layer: CSS transform, smooth transition
- Lasso selection: rect select, Shift/Cmd+drag adds
- Quick card creation: double-click → type selector popover
- Keyboard: +/- importance, Delete/Backspace, Escape deselect, Cmd+A select all

## Coordinate System
- Backend: 0-1 normalized float
- Frontend: 0-100 percentage
- Clamping: 5-95% safe zone
- Collision detection: occupancy set + spiral search

## Mobile (768px breakpoint)
- MobileDrawer: slide-in from right (lang switch, boards, cards, zoom)
- CardDetailSheet: bottom sheet (sliders, connections, delete)
- Touch: drag, pinch resize, passive listeners

## i18n
- localStorage persistence (`fact_locale`)
- Browser lang detection → ru or en
- Flat keys: `translations.ru.canvas.legend.question`
- WebSocket notifies backend on locale change

## Styling (Tailwind v4)
- Fonts: Fraunces (display), DM Sans (body), Caveat (handwritten accent)
- Warm palette: cream to dark brown (cork board aesthetic)
- Card type colors: softened blue/red/green/amber/purple/teal
- Custom animations via @keyframes

## Auth Flow
1. Check `?dev=1` → dev-token bypass
2. Else Auth0 SPA client → silent token refresh
3. Handle redirect callback
4. Logout clears local state

## Key Files
| Path | Purpose |
|------|---------|
| `src/App.svelte` | Root, lifecycle, auth |
| `src/lib/types.ts` | Card, Connection, WS types |
| `src/lib/stores/websocket.ts` | WS client (402 lines) |
| `src/lib/stores/cards.ts` | Cards, connections, chat |
| `src/lib/stores/i18n.ts` | Translations (609 lines) |
| `src/lib/components/Canvas.svelte` | Canvas, zoom, lasso (487 lines) |
| `src/lib/components/Card.svelte` | Card rendering, drag |
| `src/app.css` | Theme, animations |
