<script lang="ts">
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import Canvas from "./lib/components/Canvas.svelte";
  import CurrentQuestion from "./lib/components/CurrentQuestion.svelte";
  import HelpOverlay from "./lib/components/HelpOverlay.svelte";
  import DemoBanner from "./lib/components/DemoBanner.svelte";
  import TooltipOverlay from "./lib/components/TooltipOverlay.svelte";
  import InputBar from "./lib/components/InputBar.svelte";
  import MobileDrawer from "./lib/components/MobileDrawer.svelte";
  import CardDetailSheet from "./lib/components/CardDetailSheet.svelte";
  import LandingPage from "./lib/components/LandingPage.svelte";
  import BoardsSidebar from "./lib/components/BoardsSidebar.svelte";
  import { websocket } from "./lib/stores/websocket";
  import { auth } from "./lib/stores/auth";
  import { boards, isDemoBoard } from "./lib/stores/boards";
  import { cards, connections } from "./lib/stores/cards";
  import { onboarding } from "./lib/stores/onboarding";
  import { locale, strings } from "./lib/stores/i18n";
  import { WS_BASE } from "./lib/config";
  import type { Card, Connection } from "./lib/types";
  import demoData from "./lib/data/demo-session.json";
  import { trackLandingView, trackSignUp, trackCards5Plus } from "./lib/analytics";

  let hasInitialized = $state(false);
  let lastSessionId: string | null = null;
  let prevCardCount = $state(0);

  function loadDemoCards(loc: string) {
    const demoCards: Card[] = demoData.cards.map((c: any) => ({
      id: c.id,
      text: loc === "ru" ? c.text_ru : c.text_en,
      type: c.type,
      emoji: c.emoji,
      importance: c.importance,
      confidence: c.confidence,
      color: "",
      x: c.x,
      y: c.y,
      pinned: c.pinned ?? false,
      is_root: c.is_root ?? false,
      is_new: false,
    }));
    const demoConnections: Connection[] = demoData.connections.map(
      (c: any) => ({
        id: c.id,
        from_id: c.from_id,
        to_id: c.to_id,
        type: c.type,
        strength: c.strength,
        label: c.label,
        created_by: c.created_by,
      }),
    );
    cards.set(demoCards);
    connections.set(demoConnections);
  }

  async function initWorkspace(token: string) {
    await boards.fetchBoards(token);
    const state = get(boards);
    if (state.items.length === 0) {
      const loc = get(locale);
      boards.initDemoBoard(loc);
      loadDemoCards(loc);
    }
    const activeId = get(boards).activeId;
    if (activeId && activeId !== "demo") {
      websocket.connect(`${WS_BASE}/ws`, token, activeId);
    } else {
      websocket.connect(`${WS_BASE}/ws`, token);
    }
  }

  onMount(() => {
    auth.init();
    return () => {
      websocket.disconnect();
    };
  });

  // Analytics: track landing page view
  $effect(() => {
    if (!$auth.isLoading && !$auth.isAuthenticated) {
      trackLandingView();
    }
  });

  $effect(() => {
    if ($auth.isAuthenticated && $auth.token && !hasInitialized) {
      hasInitialized = true;
      trackSignUp();
      initWorkspace($auth.token);
    }
  });

  // Board switch: init session for real boards, load demo for demo board
  $effect(() => {
    if (
      $auth.isAuthenticated &&
      $boards.activeId &&
      $boards.activeId !== lastSessionId
    ) {
      lastSessionId = $boards.activeId;
      if ($boards.activeId === "demo") {
        const loc = get(locale);
        loadDemoCards(loc);
      } else {
        websocket.initSession($boards.activeId);
      }
    }
  });

  // Update demo cards when locale changes
  $effect(() => {
    const loc = $locale;
    if ($isDemoBoard) {
      loadDemoCards(loc);
    }
  });

  $effect(() => {
    if (!$auth.isAuthenticated && hasInitialized) {
      hasInitialized = false;
      lastSessionId = null;
      websocket.disconnect();
      boards.reset();
    }
  });

  $effect(() => {
    // Subscribe to cards for tooltip triggers
    const unsubscribe = cards.subscribe((cardList) => {
      if ($isDemoBoard) {
        prevCardCount = cardList.length;
        return;
      }

      // First real session, canvas empty -> show inputbar tip
      if (cardList.length === 0 && $boards.activeId) {
        onboarding.maybeShow("inputbar");
      }

      // Cards just appeared (from 0 to >0)
      if (cardList.length > 0 && prevCardCount === 0) {
        onboarding.maybeShow("cards_added");
      }

      // 3+ cards -> connections hint
      if (cardList.length >= 3) {
        onboarding.maybeShow("connections_hint");
      }

      // Analytics: 5+ cards milestone
      if (cardList.length >= 5 && prevCardCount < 5) {
        trackCards5Plus();
      }

      prevCardCount = cardList.length;
    });
    return unsubscribe;
  });
</script>

{#if $auth.isLoading}
  <div class="auth-state">{$strings.auth?.loading || "Loading..."}</div>
{:else if $auth.error}
  <div class="auth-state auth-state-error">
    <div class="auth-card">
      <p class="auth-kicker">Fact Cards</p>
      <h1 class="auth-title">
        {$auth.error === "session_expired"
          ? $strings.auth?.sessionExpiredTitle || "Your session expired"
          : $strings.auth?.errorTitle || "Sign-in needs another try"}
      </h1>
      <p class="auth-copy">
        {$auth.error === "session_expired"
          ? $strings.auth?.sessionExpiredBody ||
            "Please sign in again to continue where you left off."
          : $strings.auth?.errorBody ||
            "We could not restore your session. Retry or open sign-in again."}
      </p>
      <div class="auth-actions">
        <button class="auth-btn auth-btn-primary" onclick={() => void auth.retry()}>
          {$strings.auth?.retry || "Try again"}
        </button>
        <button class="auth-btn auth-btn-secondary" onclick={() => void auth.loginWithGoogle()}>
          {$strings.auth?.signInAgain || "Sign in again"}
        </button>
      </div>
    </div>
  </div>
{:else if !$auth.isAuthenticated}
  <LandingPage />
{:else}
  <main class="app">
    <BoardsSidebar />
    <section class="workspace">
      <Canvas />
      <CurrentQuestion />
      <HelpOverlay />
      {#if $isDemoBoard}
        <DemoBanner />
      {/if}
      <TooltipOverlay />
      <InputBar />
      <MobileDrawer />
      <CardDetailSheet />
    </section>
  </main>
{/if}

<style>
  .app {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    display: flex;
    background-color: #f7f1e7;
  }

  .workspace {
    position: relative;
    flex: 1;
    height: 100vh;
    overflow: hidden;
    transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .auth-state {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "DM Sans", sans-serif;
    color: var(--text-dark);
  }

  .auth-state-error {
    padding: 24px;
    background:
      radial-gradient(circle at top, rgba(255, 255, 255, 0.92), transparent 40%),
      linear-gradient(180deg, #efe5d1 0%, #f7f1e7 100%);
  }

  .auth-card {
    width: min(520px, 100%);
    padding: 28px;
    border-radius: 24px;
    border: 1px solid rgba(143, 87, 42, 0.14);
    background: rgba(255, 252, 246, 0.96);
    box-shadow: 0 22px 60px rgba(91, 53, 20, 0.12);
    text-align: center;
  }

  .auth-kicker {
    margin: 0 0 10px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(116, 71, 35, 0.72);
  }

  .auth-title {
    margin: 0;
    font-size: clamp(1.8rem, 2.4vw, 2.4rem);
    line-height: 1.1;
  }

  .auth-copy {
    margin: 14px 0 0;
    font-size: 1rem;
    line-height: 1.6;
    color: rgba(54, 39, 26, 0.82);
  }

  .auth-actions {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    margin-top: 22px;
  }

  .auth-btn {
    border: none;
    border-radius: 999px;
    padding: 12px 20px;
    font: inherit;
    font-weight: 700;
    cursor: pointer;
    transition:
      transform 0.18s ease,
      box-shadow 0.18s ease,
      background-color 0.18s ease;
  }

  .auth-btn:hover {
    transform: translateY(-1px);
  }

  .auth-btn-primary {
    background: #a44b1f;
    color: #fffdf8;
    box-shadow: 0 12px 26px rgba(164, 75, 31, 0.24);
  }

  .auth-btn-secondary {
    background: #efe4d6;
    color: #4f3521;
  }

  @media (max-width: 640px) {
    .auth-card {
      padding: 24px 20px;
    }

    .auth-actions {
      flex-direction: column;
    }

    .auth-btn {
      width: 100%;
    }
  }
</style>
