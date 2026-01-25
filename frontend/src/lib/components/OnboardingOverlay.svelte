<script lang="ts">
  import { onMount } from 'svelte';
  import { onboarding } from '../stores/onboarding';
  import { strings } from '../stores/i18n';

  const STORAGE_KEY = 'fact_onboarding_seen';

  const steps = $derived($strings.onboarding.steps);

  let isOpen = $state(false);
  let stepIndex = $state(0);

  onMount(() => {
    try {
      const seen = localStorage.getItem(STORAGE_KEY);
      if (!seen) {
        isOpen = true;
      }
    } catch {
      isOpen = true;
    }

    const unsubscribe = onboarding.subscribe((shouldShow) => {
      if (shouldShow) {
        stepIndex = 0;
        isOpen = true;
        onboarding.hide();
      }4
    });

    return unsubscribe;
  });

  function close() {
    isOpen = false;
    try {
      localStorage.setItem(STORAGE_KEY, '1');
    } catch {
      // ignore
    }
  }

  function next() {
    if (stepIndex < steps.length - 1) {
      stepIndex += 1;
    } else {
      close();
    }
  }

  function prev() {
    if (stepIndex > 0) {
      stepIndex -= 1;
    }
  }
</script>

{#if isOpen}
  <div class="onboarding-scrim"></div>
  <div class="onboarding-panel" role="dialog" aria-modal="true">
    <div class="onboarding-kicker">{$strings.onboarding.kicker}</div>
    <div class="onboarding-title">{steps[stepIndex].title}</div>
    <div class="onboarding-body">{steps[stepIndex].body}</div>
    {#if stepIndex === 0}
      <div class="onboarding-ai">
        {$strings.onboarding.aiNote}
      </div>
    {/if}

    <div class="onboarding-footer">
      <button class="ghost-btn" onclick={prev} disabled={stepIndex === 0}>
        {$strings.onboarding.buttons.prev}
      </button>
      <div class="dots">
        {#each steps as _, i}
          <span class:active={i === stepIndex}></span>
        {/each}
      </div>
      <button class="primary-btn" onclick={next}>
        {stepIndex === steps.length - 1
          ? $strings.onboarding.buttons.start
          : $strings.onboarding.buttons.next}
      </button>
    </div>
    <button class="skip-btn" onclick={close}>{$strings.onboarding.buttons.skip}</button>
  </div>
{/if}

<style>
  .onboarding-scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.35);
    z-index: 150;
  }

  .onboarding-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 160;
    width: min(520px, calc(100% - 40px));
    padding: 22px 24px 18px;
    border-radius: 18px;
    background: #ffffff;
    box-shadow:
      0 18px 50px rgba(0, 0, 0, 0.2),
      0 6px 18px rgba(0, 0, 0, 0.12);
  }

  .onboarding-kicker {
    font-size: 11px;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    color: rgba(74, 46, 138, 0.7);
    font-weight: 700;
    margin-bottom: 8px;
  }

  .onboarding-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 10px;
  }

  .onboarding-body {
    font-size: 14px;
    line-height: 1.5;
    color: var(--text-medium);
    margin-bottom: 12px;
  }

  .onboarding-ai {
    font-size: 13px;
    color: var(--text-dark);
    background: rgba(149, 117, 205, 0.12);
    padding: 8px 10px;
    border-radius: 10px;
    margin-bottom: 16px;
  }

  .onboarding-footer {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 12px;
  }

  .dots {
    display: flex;
    gap: 6px;
    justify-content: center;
  }

  .dots span {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background: rgba(0, 0, 0, 0.15);
  }

  .dots span.active {
    background: rgba(149, 117, 205, 0.8);
  }

  .primary-btn,
  .ghost-btn,
  .skip-btn {
    border: none;
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
  }

  .primary-btn {
    background: var(--question-purple);
    color: white;
  }

  .ghost-btn {
    background: rgba(0, 0, 0, 0.06);
    color: var(--text-dark);
  }

  .ghost-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .skip-btn {
    margin-top: 12px;
    background: transparent;
    color: var(--text-light);
  }
</style>
