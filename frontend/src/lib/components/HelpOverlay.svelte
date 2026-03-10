<script lang="ts">
  import { helpOverlay } from "../stores/help";
  import {
    ONBOARDING_STEP_ORDER,
    onboarding,
    type OnboardingStepId,
  } from "../stores/onboarding";
  import { strings } from "../stores/i18n";

  const STEP_INDEX: Record<OnboardingStepId, number> = {
    question: 0,
    cards: 1,
    move_card: 2,
    blind_spots: 3,
  };

  let isOpen = $state(false);
  let activeStep = $state<OnboardingStepId | null>(null);
  let isTourComplete = $state(false);

  $effect(() => {
    const unsubscribe = helpOverlay.subscribe((value) => {
      isOpen = value;
    });
    return unsubscribe;
  });

  function closeHelp() {
    helpOverlay.close();
  }

  $effect(() => {
    const unsubscribe = onboarding.subscribe((state) => {
      activeStep = state.activeStep;
      isTourComplete = state.isTourComplete;
    });
    return unsubscribe;
  });

  function restartTutorial() {
    onboarding.restart();
    closeHelp();
  }

  function getStepTitle(step: OnboardingStepId | null): string {
    if (!step) {
      return $strings.onboarding.completed;
    }
    return $strings.onboarding.steps[STEP_INDEX[step]].title;
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
      <div class="help-tour">
        <div class="help-tour-label">{$strings.onboarding.panelTitle}</div>
        <div class="help-tour-summary">
          {#if activeStep}
            {getStepTitle(activeStep)} · {STEP_INDEX[activeStep] + 1}/{ONBOARDING_STEP_ORDER.length}
          {:else if isTourComplete}
            {$strings.onboarding.completed}
          {:else}
            {getStepTitle("question")}
          {/if}
        </div>
        <button class="help-restart" onclick={restartTutorial}>
          {$strings.onboarding.buttons.restart}
        </button>
      </div>
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

  .help-tour {
    margin-bottom: 16px;
    border-radius: 14px;
    background: rgba(79, 70, 229, 0.06);
    border: 1px solid rgba(79, 70, 229, 0.12);
    padding: 12px 14px;
  }

  .help-tour-label {
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b5fc7;
    font-weight: 700;
    margin-bottom: 6px;
  }

  .help-tour-summary {
    font-size: 13px;
    line-height: 1.5;
    color: var(--text-dark);
    margin-bottom: 10px;
  }

  .help-close:hover {
    background: rgba(149, 117, 205, 0.25);
  }

  .help-restart {
    border: none;
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background: #4f46e5;
    color: white;
    transition: background 0.2s;
  }

  .help-restart:hover {
    background: #4338ca;
  }

  @media (max-width: 900px) {
    .help-popover {
      display: none;
    }
  }
</style>
