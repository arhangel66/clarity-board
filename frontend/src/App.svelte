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
  import PaywallModal from "./lib/components/PaywallModal.svelte";
  import AuthStateShell from "./lib/components/AuthStateShell.svelte";
  import { websocket } from "./lib/stores/websocket";
  import { auth } from "./lib/stores/auth";
  import { access } from "./lib/stores/access";
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
    void access.refresh(token);
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
      access.reset();
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
  <div class="auth-loading">{$strings.auth?.loading || "Loading..."}</div>
{:else if $auth.error}
  <AuthStateShell
    error={$auth.error}
    onRetry={() => void auth.retry()}
    onRelogin={() => void auth.loginWithGoogle()}
  />
{:else if !$auth.isAuthenticated}
  <LandingPage />
{:else}
  <main class="app">
    <BoardsSidebar />
    <PaywallModal />
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

  .auth-loading {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "DM Sans", sans-serif;
    color: var(--text-dark);
  }
</style>
