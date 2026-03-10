<script lang="ts">
  import { onMount } from "svelte";

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

  interface TooltipPosition {
    left: number;
    top: number;
  }

  let activeStep = $state<OnboardingStepId | null>(null);
  let canAdvance = $state(false);
  let bubbleEl = $state<HTMLDivElement | null>(null);
  let position = $state<TooltipPosition>({ left: 24, top: 24 });
  let hasManualPosition = $state(false);
  let positionedStep = $state<OnboardingStepId | null>(null);
  let dragPointerId = $state<number | null>(null);

  let dragStartX = 0;
  let dragStartY = 0;
  let dragOrigin: TooltipPosition = { left: 24, top: 24 };

  $effect(() => {
    const unsubscribe = onboarding.subscribe((state) => {
      activeStep = state.activeStep;
      canAdvance = state.canAdvance;
    });
    return unsubscribe;
  });

  onMount(() => {
    function handleResize() {
      if (!activeStep) return;
      position = hasManualPosition
        ? clampPosition(position)
        : getDefaultPosition(activeStep);
    }

    window.addEventListener("resize", handleResize);
    return () => {
      stopDragging();
      window.removeEventListener("resize", handleResize);
    };
  });

  $effect(() => {
    if (!activeStep) {
      positionedStep = null;
      stopDragging();
      return;
    }

    const currentStep = activeStep;
    const shouldResetManualPosition =
      currentStep === "question" && positionedStep !== "question";

    const frame = requestAnimationFrame(() => {
      if (!bubbleEl || currentStep !== activeStep) {
        return;
      }

      if (shouldResetManualPosition) {
        hasManualPosition = false;
      }

      if (!hasManualPosition) {
        position = getDefaultPosition(currentStep);
      }

      positionedStep = currentStep;
    });

    return () => cancelAnimationFrame(frame);
  });

  function getViewportPadding(): number {
    if (typeof window === "undefined") {
      return 24;
    }
    return window.innerWidth <= 600 ? 12 : 24;
  }

  function getBubbleSize() {
    if (bubbleEl) {
      const rect = bubbleEl.getBoundingClientRect();
      return {
        width: rect.width,
        height: rect.height,
      };
    }

    if (typeof window === "undefined") {
      return { width: 360, height: 260 };
    }

    const padding = getViewportPadding();
    return {
      width: Math.min(420, Math.max(280, window.innerWidth - padding * 2)),
      height: 260,
    };
  }

  function clampPosition(next: TooltipPosition): TooltipPosition {
    if (typeof window === "undefined") {
      return next;
    }

    const size = getBubbleSize();
    const padding = getViewportPadding();
    const maxLeft = Math.max(padding, window.innerWidth - size.width - padding);
    const maxTop = Math.max(padding, window.innerHeight - size.height - padding);

    return {
      left: Math.min(Math.max(padding, next.left), maxLeft),
      top: Math.min(Math.max(padding, next.top), maxTop),
    };
  }

  function getDefaultPosition(step: OnboardingStepId): TooltipPosition {
    if (typeof window === "undefined") {
      return { left: 24, top: 24 };
    }

    const size = getBubbleSize();
    const padding = getViewportPadding();
    const centeredLeft = (window.innerWidth - size.width) / 2;
    const bottomAlignedTop = window.innerHeight - size.height - 110;
    const centeredTop = (window.innerHeight - size.height) / 2;

    switch (step) {
      case "question":
        return clampPosition({
          left: centeredLeft,
          top: bottomAlignedTop,
        });
      case "cards":
        return clampPosition({
          left: centeredLeft,
          top: centeredTop,
        });
      case "move_card":
        return clampPosition({
          left: window.innerWidth - size.width - padding,
          top: window.innerHeight - size.height - 120,
        });
      case "blind_spots":
        return clampPosition({
          left: centeredLeft,
          top: Math.max(padding, centeredTop - 40),
        });
    }
  }

  function stopDragging() {
    if (typeof window === "undefined") {
      dragPointerId = null;
      return;
    }

    dragPointerId = null;
    window.removeEventListener("pointermove", handleDragMove);
    window.removeEventListener("pointerup", handleDragEnd);
    window.removeEventListener("pointercancel", handleDragEnd);
  }

  function handleDragStart(event: PointerEvent) {
    if (!bubbleEl) return;
    if (event.pointerType !== "touch" && event.button !== 0) return;

    dragPointerId = event.pointerId;
    dragStartX = event.clientX;
    dragStartY = event.clientY;
    dragOrigin = { ...position };
    hasManualPosition = true;

    window.addEventListener("pointermove", handleDragMove);
    window.addEventListener("pointerup", handleDragEnd);
    window.addEventListener("pointercancel", handleDragEnd);
    event.preventDefault();
  }

  function handleDragMove(event: PointerEvent) {
    if (event.pointerId !== dragPointerId) return;

    position = clampPosition({
      left: dragOrigin.left + event.clientX - dragStartX,
      top: dragOrigin.top + event.clientY - dragStartY,
    });
  }

  function handleDragEnd(event: PointerEvent) {
    if (event.pointerId !== dragPointerId) return;
    stopDragging();
  }

  function completeStep() {
    if (!canAdvance) return;
    onboarding.complete();
  }

  function skipStep() {
    onboarding.skipTour();
  }

  function getPrimaryLabel(step: OnboardingStepId): string {
    if (step === "question") return $strings.onboarding.buttons.start;
    if (step === "blind_spots") return $strings.onboarding.buttons.finish;
    return $strings.onboarding.buttons.next;
  }

  function getStepContent(step: OnboardingStepId) {
    return $strings.onboarding.steps[STEP_INDEX[step]];
  }

  function getActionContent(step: OnboardingStepId) {
    return $strings.onboarding.actions[step];
  }
</script>

{#if activeStep}
  <div
    class="tooltip-overlay"
    class:dragging={dragPointerId !== null}
    role="dialog"
    aria-live="polite"
    aria-modal="false"
    data-active-step={activeStep}
    style={`left:${position.left}px; top:${position.top}px;`}
  >
    <div bind:this={bubbleEl} class="tooltip-bubble">
      <div class="tooltip-header" onpointerdown={handleDragStart}>
        <span class="tooltip-grip" aria-hidden="true"></span>
        <div class="tooltip-header-meta">
          <span class="tooltip-kicker">{$strings.onboarding.kicker}</span>
          <span class="tooltip-progress"
            >{STEP_INDEX[activeStep] + 1} / {ONBOARDING_STEP_ORDER.length}</span
          >
        </div>
      </div>
      <div class="tooltip-title">{getStepContent(activeStep).title}</div>
      <p class="tooltip-text">{getStepContent(activeStep).body}</p>
      <p class="tooltip-action">{getActionContent(activeStep).prompt}</p>
      <div class:ready={canAdvance} class="tooltip-status">
        {canAdvance
          ? getActionContent(activeStep).ready
          : getActionContent(activeStep).waiting}
      </div>
      <p class="tooltip-note">{$strings.onboarding.aiNote}</p>
      <div class="tooltip-actions">
        <button class="tooltip-btn secondary" onclick={skipStep}>
          {$strings.onboarding.buttons.skip}
        </button>
        <button
          class="tooltip-btn primary"
          disabled={!canAdvance}
          onclick={completeStep}
        >
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
  }

  .tooltip-overlay.dragging {
    user-select: none;
  }

  .tooltip-bubble {
    width: min(420px, calc(100vw - 24px));
    padding: 16px 18px;
    background: rgba(27, 24, 34, 0.96);
    backdrop-filter: blur(8px);
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.28);
    pointer-events: auto;
    animation: tooltipFadeIn 0.3s ease-out;
  }

  .tooltip-header {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 10px;
    cursor: grab;
    touch-action: none;
  }

  .tooltip-overlay.dragging .tooltip-header {
    cursor: grabbing;
  }

  .tooltip-grip {
    align-self: center;
    width: 44px;
    height: 4px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
  }

  .tooltip-header-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
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

  .tooltip-action {
    font-size: 13px;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.88);
    margin: 12px 0 0;
  }

  .tooltip-status {
    display: inline-flex;
    align-items: center;
    margin-top: 10px;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.76);
  }

  .tooltip-status.ready {
    background: rgba(144, 238, 144, 0.14);
    color: #b8f1b7;
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

  .tooltip-btn:disabled {
    cursor: not-allowed;
    opacity: 0.6;
    transform: none;
  }

  .tooltip-btn.secondary {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.88);
  }

  .tooltip-btn.primary {
    background: #f1c078;
    color: #24170a;
  }

  @keyframes tooltipFadeIn {
    from {
      opacity: 0;
      transform: scale(0.96);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  @media (max-width: 600px) {
    .tooltip-bubble {
      width: calc(100vw - 24px);
      max-width: none;
    }
  }
</style>
