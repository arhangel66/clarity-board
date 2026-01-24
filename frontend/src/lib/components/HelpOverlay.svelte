<script lang="ts">
  import { helpOverlay } from '../stores/help';

  let isOpen = $state(false);

  $effect(() => {
    const unsubscribe = helpOverlay.subscribe((value) => {
      isOpen = value;
    });
    return unsubscribe;
  });

  function toggleHelp() {
    helpOverlay.toggle();
  }

  function closeHelp() {
    helpOverlay.close();
  }
</script>

<button class="help-fab" onclick={toggleHelp} aria-label="Help">
  А-а
</button>

{#if isOpen}
  <div class="help-scrim" onclick={closeHelp}></div>
  <div class="help-panel" onclick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
    <div class="help-title">Как это работает</div>
    <p class="help-text">
      Вы сами решаете задачу. ИИ лишь немного направляет и аккуратно раскладывает карточки.
    </p>
    <ul class="help-list">
      <li>Сформулируйте, что самое важное вы хотите решить.</li>
      <li>Называйте факты, боли и ресурсы, связанные с задачей.</li>
      <li>Постепенно уточняйте формулировку центрального вопроса.</li>
    </ul>
    <button class="help-close" onclick={closeHelp}>Понятно</button>
  </div>
{/if}

<style>
  .help-fab {
    position: fixed;
    top: 16px;
    right: 20px;
    z-index: 120;

    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    cursor: pointer;

    background: rgba(255, 255, 255, 0.92);
    color: var(--text-dark);
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.4px;

    box-shadow:
      0 6px 18px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .help-fab:hover {
    transform: translateY(-1px);
    box-shadow:
      0 8px 22px rgba(0, 0, 0, 0.14),
      0 4px 10px rgba(0, 0, 0, 0.1);
  }

  .help-scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.25);
    z-index: 110;
  }

  .help-panel {
    position: fixed;
    top: 72px;
    right: 20px;
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
    .help-panel {
      right: 12px;
      top: 72px;
    }
  }
</style>
