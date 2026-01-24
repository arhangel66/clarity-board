<script lang="ts">
  import { onMount } from 'svelte';
  import Canvas from './lib/components/Canvas.svelte';
  import ChatPanel from './lib/components/ChatPanel.svelte';
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
  <ChatPanel />
</main>

<style>
  .app {
    display: flex;
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }
</style>
