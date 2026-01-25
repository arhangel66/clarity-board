<script lang="ts">
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import Canvas from "./lib/components/Canvas.svelte";
  import CurrentQuestion from "./lib/components/CurrentQuestion.svelte";
  import HelpOverlay from "./lib/components/HelpOverlay.svelte";
  import OnboardingOverlay from "./lib/components/OnboardingOverlay.svelte";
  import InputBar from "./lib/components/InputBar.svelte";
  import MobileDrawer from "./lib/components/MobileDrawer.svelte";
  import CardDetailSheet from "./lib/components/CardDetailSheet.svelte";
  import LandingPage from "./lib/components/LandingPage.svelte";
  import BoardsSidebar from "./lib/components/BoardsSidebar.svelte";
  import { websocket } from "./lib/stores/websocket";
  import { auth } from "./lib/stores/auth";
  import { boards } from "./lib/stores/boards";
  import { WS_BASE } from "./lib/config";

  let hasInitialized = $state(false);
  let lastSessionId: string | null = null;

  async function initWorkspace(token: string) {
    await boards.fetchBoards(token);
    const activeId = get(boards).activeId;
    websocket.connect(`${WS_BASE}/ws`, token, activeId || undefined);
  }

  onMount(() => {
    auth.init();
    return () => {
      websocket.disconnect();
    };
  });

  $effect(() => {
    if ($auth.isAuthenticated && $auth.token && !hasInitialized) {
      hasInitialized = true;
      initWorkspace($auth.token);
    }
  });

  $effect(() => {
    if (
      $auth.isAuthenticated &&
      $boards.activeId &&
      $boards.activeId !== lastSessionId
    ) {
      lastSessionId = $boards.activeId;
      websocket.initSession($boards.activeId);
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
</script>

{#if $auth.isLoading}
  <div class="auth-state">Loading...</div>
{:else if $auth.error}
  <div class="auth-state">{$auth.error}</div>
{:else if !$auth.isAuthenticated}
  <LandingPage />
{:else}
  <main class="app">
    <BoardsSidebar />
    <section class="workspace">
      <Canvas />
      <CurrentQuestion />
      <HelpOverlay />
      <OnboardingOverlay />
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
</style>
