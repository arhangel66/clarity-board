<script lang="ts">
  import { helpOverlay } from "../stores/help";
  import { strings } from "../stores/i18n";

  let isOpen = $state(false);

  $effect(() => {
    const unsubscribe = helpOverlay.subscribe((value) => {
      isOpen = value;
    });
    return unsubscribe;
  });

  function closeHelp() {
    helpOverlay.close();
  }
</script>

{#if isOpen}
  <div class="help-scrim" onclick={closeHelp}></div>
  <div
    class="help-panel"
    onclick={(e) => e.stopPropagation()}
    role="dialog"
    aria-modal="true"
  >
    <div class="help-title">{$strings.help.title}</div>
    <p class="help-text">
      {$strings.help.text}
    </p>
    <ul class="help-list">
      {#each $strings.help.list as item}
        <li>{item}</li>
      {/each}
    </ul>
    <button class="help-close" onclick={closeHelp}>{$strings.help.close}</button
    >
  </div>
{/if}

<style>
  .help-scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.25);
    z-index: 110;
  }

  .help-panel {
    position: fixed;
    top: 70px;
    right: 76px;
    z-index: 120;
    width: 320px;
    max-width: calc(100% - 32px);
    padding: 16px 18px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.98);
    box-shadow:
      0 10px 30px rgba(0, 0, 0, 0.16),
      0 4px 12px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(149, 117, 205, 0.18);
  }

  .help-title {
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 8px;
    color: var(--text-dark);
  }

  .help-text {
    font-size: 13px;
    line-height: 1.4;
    color: var(--text-medium);
    margin-bottom: 10px;
  }

  .help-list {
    margin: 0 0 12px 16px;
    padding: 0;
    font-size: 13px;
    color: var(--text-dark);
    line-height: 1.4;
  }

  .help-list li {
    margin-bottom: 6px;
  }

  .help-close {
    border: none;
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background: rgba(149, 117, 205, 0.15);
    color: #4a2e8a;
  }

  @media (max-width: 768px) {
    .help-fab,
    .help-scrim,
    .help-panel {
      display: none;
    }
  }
</style>
