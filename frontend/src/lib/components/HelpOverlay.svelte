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
  <div class="help-popover" role="dialog" aria-modal="true">
    <div class="popover-arrow"></div>
    <div class="help-content">
      <div class="help-title">{$strings.help.title}</div>
      <p class="help-text">
        {$strings.help.text}
      </p>
      <ul class="help-list">
        {#each $strings.help.list as item}
          <li>{item}</li>
        {/each}
      </ul>
      <button class="help-close" onclick={closeHelp}
        >{$strings.help.close}</button
      >
    </div>
  </div>
{/if}

<style>
  .help-popover {
    position: absolute;
    top: 50%;
    left: calc(100% + 20px);
    transform: translateY(-50%);
    z-index: 200;
    width: 320px;
    filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.16));
    animation: slideIn 0.2s ease-out;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-50%) translateX(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(-50%) translateX(0);
    }
  }

  .popover-arrow {
    position: absolute;
    top: 50%;
    left: -8px;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-right: 8px solid rgba(255, 255, 255, 0.98);
  }

  .help-content {
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(149, 117, 205, 0.2);
    border-radius: 16px;
    padding: 20px;
  }

  .help-title {
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 8px;
    color: var(--text-dark);
    font-family: inherit;
  }

  .help-text {
    font-size: 13px;
    line-height: 1.5;
    color: var(--text-medium);
    margin-bottom: 12px;
  }

  .help-list {
    margin: 0 0 16px 18px;
    padding: 0;
    font-size: 13px;
    color: var(--text-dark);
    line-height: 1.5;
  }

  .help-list li {
    margin-bottom: 8px;
  }

  .help-close {
    border: none;
    border-radius: 999px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background: rgba(149, 117, 205, 0.15);
    color: #4a2e8a;
    transition: background 0.2s;
  }

  .help-close:hover {
    background: rgba(149, 117, 205, 0.25);
  }

  @media (max-width: 900px) {
    .help-popover {
      display: none;
    }
  }
</style>
