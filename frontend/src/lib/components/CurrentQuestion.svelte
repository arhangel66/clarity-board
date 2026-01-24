<script lang="ts">
  import { session, PHASE_LABELS } from '../stores/session';
  import type { SessionPhase } from '../types';

  let currentPhase = $state<SessionPhase>('question');
  let currentQuestion = $state('');
  let isActive = $state(false);
  let isAnimating = $state(false);
  let isAiThinking = $state(false);

  $effect(() => {
    const unsubscribe = session.subscribe((state) => {
      // Trigger animation when question changes
      if (state.currentQuestion !== currentQuestion && currentQuestion !== '') {
        isAnimating = true;
        setTimeout(() => {
          isAnimating = false;
        }, 300);
      }

      currentPhase = state.phase;
      currentQuestion = state.currentQuestion;
      isActive = state.isActive;
      isAiThinking = state.isAiThinking;
    });
    return unsubscribe;
  });

  function getPhaseNumber(phase: SessionPhase): string {
    const numbers: Record<SessionPhase, string> = {
      question: '1',
      facts: '2',
      pains: '3',
      resources: '4',
      gaps: '5',
      connections: '6'
    };
    return numbers[phase];
  }
</script>

{#if isActive}
  <div class="question-banner" class:animating={isAnimating}>
    <div class="phase-badge">
      <span class="phase-number">{getPhaseNumber(currentPhase)}</span>
      <span class="phase-label">{PHASE_LABELS[currentPhase]}</span>
    </div>

    <div class="question-text">
      {currentQuestion}
    </div>

    {#if isAiThinking}
      <div class="thinking-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    {/if}
  </div>
{/if}

<style>
  .question-banner {
    position: fixed;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;

    /* Wide pill shape */
    max-width: 700px;
    width: calc(100% - 200px);
    min-width: 400px;

    /* Layout */
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 12px 24px;

    /* Appearance */
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    box-shadow:
      0 4px 20px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(149, 117, 205, 0.2);

    transition: transform 0.3s ease, opacity 0.3s ease, box-shadow 0.2s ease, border-radius 0.2s ease;
  }

  .question-banner:hover {
    box-shadow:
      0 6px 24px rgba(0, 0, 0, 0.15),
      0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .question-banner.animating {
    animation: bannerPop 0.3s ease;
  }

  @keyframes bannerPop {
    0% {
      transform: translateX(-50%) translateY(-5px);
      opacity: 0.7;
    }
    100% {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
  }

  .phase-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 12px;
    background: rgba(149, 117, 205, 0.1);
    border-radius: 20px;
    flex-shrink: 0;
  }

  .phase-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    background: var(--question-purple);
    color: white;
    border-radius: 50%;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    font-size: 11px;
    font-weight: 600;
  }

  .phase-label {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }

  .question-text {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: var(--text-dark);
    line-height: 1.3;
    flex: 1;

    /* Truncate if too long */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    transition: all 0.2s ease;
  }

  /* Expand on hover */
  .question-banner:hover .question-text {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .thinking-dots {
    display: flex;
    gap: 4px;
    flex-shrink: 0;
    padding: 4px;
  }

  .thinking-dots span {
    width: 6px;
    height: 6px;
    background: var(--question-purple);
    border-radius: 50%;
    animation: dotPulse 1.4s ease-in-out infinite;
  }

  .thinking-dots span:nth-child(2) {
    animation-delay: 0.2s;
  }

  .thinking-dots span:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes dotPulse {
    0%, 60%, 100% {
      opacity: 0.3;
      transform: scale(0.8);
    }
    30% {
      opacity: 1;
      transform: scale(1);
    }
  }

  /* Responsive: smaller screens */
  @media (max-width: 768px) {
    .question-banner {
      width: calc(100% - 40px);
      min-width: unset;
      padding: 10px 16px;
      gap: 12px;
    }

    .phase-label {
      display: none;
    }

    .question-text {
      font-size: 14px;
    }
  }
</style>
