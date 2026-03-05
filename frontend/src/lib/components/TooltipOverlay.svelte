<script lang="ts">
  import { onboarding, type TooltipKey } from "../stores/onboarding";
  import { strings } from "../stores/i18n";

  let activeTip = $state<TooltipKey | null>(null);

  $effect(() => {
    const unsubscribe = onboarding.subscribe((state) => {
      activeTip = state.activeTip;
    });
    return unsubscribe;
  });

  function dismiss() {
    if (activeTip) {
      onboarding.dismiss(activeTip);
    }
  }

  function getPositionClass(tip: TooltipKey): string {
    switch (tip) {
      case "inputbar":
        return "pos-inputbar";
      case "cards_added":
        return "pos-center";
      case "connections_hint":
        return "pos-bottom-right";
      default:
        return "pos-center";
    }
  }
</script>

{#if activeTip}
  <div
    class="tooltip-overlay {getPositionClass(activeTip)}"
    role="status"
    aria-live="polite"
  >
    <div class="tooltip-bubble">
      <span class="tooltip-text">{$strings.tooltips[activeTip]}</span>
      <button class="tooltip-close" onclick={dismiss} aria-label="Close">
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <path d="M18 6L6 18M6 6l12 12" />
        </svg>
      </button>
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
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(50, 30, 80, 0.92);
    backdrop-filter: blur(8px);
    border-radius: 14px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    pointer-events: auto;
  }

  .tooltip-text {
    font-size: 0.9em;
    color: white;
    font-weight: 500;
    line-height: 1.4;
  }

  .tooltip-close {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border: none;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 50%;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    flex-shrink: 0;
    transition: background 0.2s ease;
  }

  .tooltip-close:hover {
    background: rgba(255, 255, 255, 0.25);
    color: white;
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
    }
  }
</style>
