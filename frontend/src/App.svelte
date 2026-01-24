<script lang="ts">
  import { onMount } from 'svelte';
  import Canvas from './lib/components/Canvas.svelte';
  import CurrentQuestion from './lib/components/CurrentQuestion.svelte';
  import HelpOverlay from './lib/components/HelpOverlay.svelte';
  import LanguageToggle from './lib/components/LanguageToggle.svelte';
  import OnboardingOverlay from './lib/components/OnboardingOverlay.svelte';
  import ZoomControls from './lib/components/ZoomControls.svelte';
  import InputBar from './lib/components/InputBar.svelte';
  import MobileDrawer from './lib/components/MobileDrawer.svelte';
  import CardDetailSheet from './lib/components/CardDetailSheet.svelte';
  import { websocket } from './lib/stores/websocket';

  onMount(() => {
    // Connect to WebSocket
    websocket.connect('ws://localhost:8000/ws');

    return () => {
      websocket.disconnect();
    };
  });
</script>

<main class="app">
  <Canvas />
  <CurrentQuestion />
  <HelpOverlay />
  <LanguageToggle />
  <ZoomControls />
  <OnboardingOverlay />
  <InputBar />
  <MobileDrawer />
  <CardDetailSheet />
</main>

<style>
  .app {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }
</style>
