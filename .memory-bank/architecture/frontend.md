---
description: Frontend architecture — component tree, stores, canvas system.
status: active
---
# Frontend Architecture

See also: [guides/dev-setup.md](../guides/dev-setup.md) for HOW.

## Component Hierarchy

```
App.svelte
├── LandingPage (unauthenticated)
└── Workspace (authenticated)
    ├── BoardsSidebar (left, collapsible)
    ├── Canvas (core)
    │   ├── Connections (SVG overlay, Bezier curves)
    │   └── Card (per card, draggable)
    ├── CurrentQuestion (centered overlay)
    ├── InputBar (bottom, voice + text)
    ├── HelpOverlay, DemoBanner, TooltipOverlay
    ├── MobileDrawer (off-canvas menu)
    └── CardDetailSheet (mobile bottom sheet)
```

## Store Architecture

Core data: `cards`, `connections`, `chatMessages`, `boards`, `session`, `auth`
UI state: `selectedCardIds`, `selectedCardId`, `zoom`, `drawer`, `cardDetail`, `helpOverlay`, `onboarding`
Infrastructure: `websocket`, `i18n`, `isMobile`

## Canvas System
- Cork board background (SVG noise + gradient)
- Zoom: CSS transform 0.6x-1.6x
- Lasso selection: rect select with Shift/Cmd modifier
- Quick create: double-click → type selector popover
- Collision detection: occupancy set + spiral search
- Coordinates: 0-100% with 5-95% safe zone clamping

## Card Visual System
- Scale: `(0.7 + importance * 0.6) * custom_scale`
- Rotation: hash-based stable ±3° for handmade feel
- 6 type colors: question (purple), fact (blue), pain (red), resource (green), hypothesis (amber), todo (teal)
- Animations: appear (300ms), pulse (8s glow), fadeOut (500ms)

## Mobile (768px breakpoint)
- MobileDrawer replaces sidebar
- CardDetailSheet replaces inline editing
- Touch drag/pinch supported

## i18n
- ru/en via localStorage, browser detection fallback
- 1000+ translation keys, flat structure
- WebSocket notifies backend on locale change
- Landing page copy and pricing content are localized in the same store

## Styling
- Tailwind CSS v4 with `@theme` design tokens
- Fonts: Fraunces (display), DM Sans (body), Caveat (handwritten)
- Warm cork board palette (cream → dark brown)
