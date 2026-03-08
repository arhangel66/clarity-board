<script lang="ts">
  import {
    ONBOARDING_STEP_ORDER,
    onboarding,
    type OnboardingStepId,
  } from "../stores/onboarding";
  import { strings } from "../stores/i18n";

  const STEP_INDEX: Record<OnboardingStepId, number> = {
    question: 0,
    cards: 1,
    connections: 2,
    blind_spots: 3,
  };

  let activeStep = $state<OnboardingStepId | null>(null);

  $effect(() => {
    const unsubscribe = onboarding.subscribe((state) => {
      activeStep = state.activeStep;
    });
    return unsubscribe;
  });

  function completeStep() {
    onboarding.complete();
  }

  function skipTour() {
    onboarding.skipTour();
  }

  function getPositionClass(step: OnboardingStepId): string {
    switch (step) {
      case "question":
        return "pos-inputbar";
      case "cards":
        return "pos-center";
      case "connections":
        return "pos-bottom-right";
      case "blind_spots":
        return "pos-center";
    }
  }

  function getPrimaryLabel(step: OnboardingStepId): string {
    return step === "question"
      ? $strings.onboarding.buttons.start
      : $strings.onboarding.buttons.next;
  }

  function getStepContent(step: OnboardingStepId) {
    return $strings.onboarding.steps[STEP_INDEX[step]];
  }
</script>

{#if activeStep}
  <div
    class="tooltip-overlay {getPositionClass(activeStep)}"
    role="dialog"
    aria-live="polite"
    aria-modal="false"
  >
    <div class="tooltip-bubble">
      <div class="tooltip-header">
        <span class="tooltip-kicker">{$strings.onboarding.kicker}</span>
        <span class="tooltip-progress"
          >{STEP_INDEX[activeStep] + 1} / {ONBOARDING_STEP_ORDER.length}</span
        >
      </div>
      <div class="tooltip-title">{getStepContent(activeStep).title}</div>
      <p class="tooltip-text">{getStepContent(activeStep).body}</p>
      <p class="tooltip-note">{$strings.onboarding.aiNote}</p>
      <div class="tooltip-actions">
        <button class="tooltip-btn secondary" onclick={skipTour}>
          {$strings.onboarding.buttons.skip}
        </button>
        <button class="tooltip-btn primary" onclick={completeStep}>
          {getPrimaryLabel(activeStep)}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .tooltip-overlay {
    position: fixed;
    z-index: 140;
    pointer-events: none;
    animation: tooltipFadeIn 0.3s ease-out;
  }

  .tooltip-bubble {
    min-width: min(360px, calc(100vw - 24px));
    max-width: 420px;
    padding: 16px 18px;
    background: rgba(27, 24, 34, 0.96);
    backdrop-filter: blur(8px);
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.28);
    pointer-events: auto;
  }

  .tooltip-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 10px;
  }

  .tooltip-kicker,
  .tooltip-progress {
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.62);
  }

  .tooltip-title {
    font-size: 16px;
    line-height: 1.2;
    font-weight: 500;
    color: white;
    margin-bottom: 8px;
  }

  .tooltip-text {
    font-size: 0.95em;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.4;
    margin: 0;
  }

  .tooltip-note {
    font-size: 12px;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.68);
    margin: 10px 0 0;
  }

  .tooltip-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 14px;
  }

  .tooltip-btn {
    border: none;
    border-radius: 999px;
    padding: 9px 14px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.2s ease, color 0.2s ease;
  }

  .tooltip-btn:hover {
    transform: translateY(-1px);
  }

  .tooltip-btn.secondary {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.88);
  }

  .tooltip-btn.primary {
    background: #f1c078;
    color: #24170a;
  }

  /* Position variants */
  .pos-inputbar {
    bottom: 110px;
    left: 50%;
    transform: translateX(-50%);
  }

  .pos-center {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .pos-bottom-right {
    bottom: 110px;
    right: 24px;
  }

  @keyframes tooltipFadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Override transform for positioned variants */
  .pos-inputbar {
    animation: tooltipFadeInCenter 0.3s ease-out;
  }

  .pos-center {
    animation: tooltipFadeInAbsolute 0.3s ease-out;
  }

  @keyframes tooltipFadeInCenter {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  @keyframes tooltipFadeInAbsolute {
    from {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
  }

  @media (max-width: 600px) {
    .tooltip-overlay {
      bottom: 100px !important;
      top: auto !important;
      left: 12px !important;
      right: 12px !important;
      transform: none !important;
      animation: tooltipFadeIn 0.3s ease-out !important;
    }

    .tooltip-bubble {
      width: 100%;
      min-width: 0;
    }
  }
</style>
