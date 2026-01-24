<script lang="ts">
  import { session } from "../stores/session";
  import { strings } from "../stores/i18n";
  import { isMobile } from "../stores/mobile";
  import { openDrawer } from "../stores/drawer";
  import { websocket } from "../stores/websocket";
  import { cards } from "../stores/cards";
  import type { SessionPhase } from "../types";

  const SPECIAL_QUESTION_MIN_CARDS = 10;

  let currentPhase = $state<SessionPhase>("question");
  let currentQuestion = $state("");
  let isActive = $state(false);
  let isAnimating = $state(false);
  let isAiThinking = $state(false);
  let specialQuestionsUnlocked = $state(false);
  let nonQuestionCards = $state(0);
  let pendingSpecialQuestion = $state<{
    id: string;
    question: string;
    hint: string;
  } | null>(null);

  $effect(() => {
    const unsubscribe = session.subscribe((state) => {
      // Trigger animation when question changes
      if (state.currentQuestion !== currentQuestion && currentQuestion !== "") {
        isAnimating = true;
        setTimeout(() => {
          isAnimating = false;
        }, 300);
      }

      currentPhase = state.phase;
      currentQuestion = state.currentQuestion;
      isActive = state.isActive;
      isAiThinking = state.isAiThinking;
      specialQuestionsUnlocked = state.specialQuestionsUnlocked;
      pendingSpecialQuestion = state.pendingSpecialQuestion;
    });
    return unsubscribe;
  });

  $effect(() => {
    const unsubscribe = cards.subscribe((list) => {
      nonQuestionCards = list.filter((card) => card.type !== "question").length;
    });
    return unsubscribe;
  });

  function handleMenuClick() {
    openDrawer();
  }

  function handleSpecialQuestion() {
    websocket.requestSpecialQuestion();
  }

  function isSpecialQuestionEnabled(): boolean {
    return specialQuestionsUnlocked ||
      (currentPhase !== "question" && nonQuestionCards >= SPECIAL_QUESTION_MIN_CARDS);
  }
</script>

{#if isActive}
  <div class="question-banner" class:animating={isAnimating}>
    {#if $isMobile}
      <button class="menu-btn" onclick={handleMenuClick} aria-label="Open menu">
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    {/if}

    <button
      class="special-btn"
      class:unlocked={isSpecialQuestionEnabled()}
      class:has-pending={pendingSpecialQuestion !== null}
      disabled={!isSpecialQuestionEnabled()}
      onclick={handleSpecialQuestion}
      title={$strings.input.specialQuestionButton}
    >
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M9 18h6"></path>
        <path d="M10 22h4"></path>
        <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"></path>
      </svg>
    </button>

    <div class="question-text">
      {#if pendingSpecialQuestion}
        <div class="special-question-active">
          <div class="special-label">
            <svg
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            {$strings.input.specialQuestionLabel}
          </div>
          <div class="special-text">{pendingSpecialQuestion.question}</div>
          {#if pendingSpecialQuestion.hint}
            <div class="special-hint">{pendingSpecialQuestion.hint}</div>
          {/if}
        </div>
      {:else}
        {currentQuestion}
      {/if}
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

    transition:
      transform 0.3s ease,
      opacity 0.3s ease,
      box-shadow 0.2s ease,
      border-radius 0.2s ease;
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

  .menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: none;
    background: transparent;
    color: var(--text-medium);
    border-radius: 8px;
    cursor: pointer;
    flex-shrink: 0;
    transition: background 0.2s ease;
  }

  .menu-btn:hover {
    background: rgba(0, 0, 0, 0.05);
  }

  .special-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: none;
    border-radius: 50%;
    background: transparent;
    color: #94a3b8;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.2s ease;
  }

  .special-btn.unlocked {
    color: #16a34a;
  }

  .special-btn.unlocked:hover {
    background: #dcfce7;
  }

  .special-btn.has-pending {
    color: #16a34a;
    background: #dcfce7;
  }

  .special-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .question-text {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
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
    0%,
    60%,
    100% {
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
      gap: 10px;
    }

    .question-text {
      font-size: 14px;
    }
  }

  /* Special Question Styling */
  .special-question-active {
    width: 100%;
    animation: slideDown 0.3s ease;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .special-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #166534;
    font-weight: 700;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .special-text {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-dark);
    line-height: 1.4;
  }

  .special-hint {
    font-size: 12px;
    color: var(--text-light);
    margin-top: 4px;
    font-style: italic;
  }
</style>
