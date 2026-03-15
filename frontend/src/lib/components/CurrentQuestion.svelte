<script lang="ts">
  import { session } from "../stores/session";
  import { strings } from "../stores/i18n";
  import { isMobile } from "../stores/mobile";
  import { openDrawer } from "../stores/drawer";
  import { websocket } from "../stores/websocket";

  let currentQuestion = $state("");
  let isActive = $state(false);
  let isAnimating = $state(false);
  let isAiThinking = $state(false);
  let pendingSpecialQuestion = $state<{
    id: string;
    category_id: string;
    category_label?: string;
    question: string;
    hint: string;
  } | null>(null);

  type VisibleType = "none" | "regular" | "special";
  type SpecialQuestionCategory = "reflector" | "constructor" | "centrist";
  let visibleType = $state<VisibleType>("none");
  let isWaitingForSpecial = $state(false);

  function isSpecialQuestionCategory(value: string): value is SpecialQuestionCategory {
    return value === "reflector" || value === "constructor" || value === "centrist";
  }

  function getSpecialCategoryLabel(
    prompt: typeof pendingSpecialQuestion,
    fallbackCategories: Record<SpecialQuestionCategory, string>
  ): string {
    if (!prompt) return "";
    if (prompt.category_label) return prompt.category_label;
    return isSpecialQuestionCategory(prompt.category_id)
      ? fallbackCategories[prompt.category_id]
      : "";
  }

  $effect(() => {
    const unsubscribe = session.subscribe((state) => {
      // Trigger animation when question changes
      if (state.currentQuestion !== currentQuestion && currentQuestion !== "") {
        isAnimating = true;
        setTimeout(() => {
          isAnimating = false;
        }, 300);
      }

      // Auto-show special question when it arrives
      if (isWaitingForSpecial && state.pendingSpecialQuestion) {
        visibleType = "special";
        isWaitingForSpecial = false;
      }

      if (!state.pendingSpecialQuestion && visibleType === "special") {
        visibleType = "none";
      }

      currentQuestion = state.currentQuestion;
      isActive = state.isActive;
      isAiThinking = state.isAiThinking;
      pendingSpecialQuestion = state.pendingSpecialQuestion;
    });
    return unsubscribe;
  });

  function handleMenuClick() {
    openDrawer();
  }

  function handleSpecialQuestion() {
    isWaitingForSpecial = true;
    websocket.requestSpecialQuestion();
  }

  function toggleVisible(type: VisibleType) {
    if (visibleType === type) {
      visibleType = "none";
    } else {
      visibleType = type;
      if (type === "special") isWaitingForSpecial = false;
    }
  }
</script>

{#if isActive}
  <div class="question-container">
    <div class="toggle-bar">
      {#if $isMobile}
        <button
          class="icon-btn menu-btn"
          onclick={handleMenuClick}
          aria-label="Open menu"
        >
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

      <div class="toggles">
        <!-- Regular Question Toggle -->
        <div class="toggle-item">
          <button
            class="toggle-btn"
            class:active={visibleType === "regular"}
            onclick={() => toggleVisible("regular")}
          >
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
              />
            </svg>
            <span class="btn-label">{$strings.canvas.legend.question}</span>
          </button>
          <div class="tooltip">{$strings.canvas.legend.question}</div>
        </div>

        <!-- Special Question Toggle/Request -->
        <div class="toggle-item">
          <button
            class="toggle-btn special"
            class:active={visibleType === "special"}
            class:has-pending={pendingSpecialQuestion !== null}
            onclick={() => {
              if (pendingSpecialQuestion) {
                toggleVisible("special");
              } else {
                handleSpecialQuestion();
              }
            }}
          >
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5z" /><path
                d="M2 17l10 5 10-5"
              /><path d="M2 12l10 5 10-5" />
            </svg>
            <span class="btn-label">{$strings.input.specialQuestionLabel}</span>
          </button>
          <div class="tooltip">
            {pendingSpecialQuestion
              ? $strings.input.specialQuestionLabel
              : $strings.input.specialQuestionButton}
          </div>
        </div>
      </div>

      {#if isAiThinking}
        <div class="thinking-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      {/if}
    </div>

    {#if visibleType !== "none"}
      <div class="question-content" class:animating={isAnimating}>
        {#if visibleType === "special" && pendingSpecialQuestion}
          <div class="special-question-active">
            <div class="special-label">
              <svg
                width="12"
                height="12"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="3"
              >
                <path d="M12 2L2 7l10 5 10-5-10-5z" /><path
                  d="M2 17l10 5 10-5"
                /><path d="M2 12l10 5 10-5" />
              </svg>
              {$strings.input.specialQuestionLabel}
              {#if getSpecialCategoryLabel(
                pendingSpecialQuestion,
                $strings.input.specialQuestionCategories
              )}
                <span class="special-category">
                  · {getSpecialCategoryLabel(
                    pendingSpecialQuestion,
                    $strings.input.specialQuestionCategories
                  )}
                </span>
              {/if}
            </div>
            <div class="special-text">{pendingSpecialQuestion.question}</div>
            {#if pendingSpecialQuestion.hint}
              <div class="special-hint">{pendingSpecialQuestion.hint}</div>
            {/if}
          </div>
        {:else if visibleType === "regular"}
          <div class="regular-question">
            {currentQuestion}
          </div>
        {/if}
      </div>
    {/if}
  </div>
{/if}

<style>
  .question-container {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    width: auto;
    max-width: 600px;
  }

  .toggle-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    background: var(--bg-input);
    backdrop-filter: blur(10px);
    border-radius: 999px;
    border: 1px solid var(--accent-purple-muted);
    box-shadow: var(--shadow-soft);
  }

  .toggles {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .toggle-item {
    position: relative;
  }

  .toggle-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border: none;
    background: transparent;
    color: var(--text-medium);
    border-radius: 999px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .toggle-btn:hover {
    background: rgba(149, 117, 205, 0.08);
    color: var(--question-purple);
  }

  .toggle-btn.active {
    background: var(--question-purple);
    color: white;
    box-shadow: 0 4px 12px rgba(149, 117, 205, 0.3);
  }

  .toggle-btn.special.unlocked {
    color: #16a34a;
  }

  .toggle-btn.special.active {
    background: #16a34a;
    color: white;
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
  }

  .toggle-btn.special.has-pending {
    background: #dcfce7;
    color: #16a34a;
  }

  .toggle-btn.special.has-pending.active {
    background: #16a34a;
    color: white;
  }

  .btn-label {
    display: inline-block;
  }

  .tooltip {
    position: absolute;
    top: calc(100% + 10px);
    left: 50%;
    transform: translateX(-50%) translateY(5px);
    background: #1e293b;
    color: white;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 11px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s ease;
    z-index: 200;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .toggle-item:hover .tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  .question-content {
    background: var(--bg-surface);
    padding: 16px 20px;
    border-radius: 16px;
    border: 1px solid var(--accent-purple-subtle);
    box-shadow: var(--shadow-elevated);
    width: 100%;
    animation: fadeInScale 0.2s ease-out;
  }

  @keyframes fadeInScale {
    from {
      opacity: 0;
      transform: scale(0.95) translateY(-5px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }

  .regular-question {
    font-size: 14px;
    line-height: 1.5;
    color: var(--text-dark);
    font-weight: 500;
    text-align: center;
  }

  .special-question-active {
    width: 100%;
  }

  .special-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    color: #166534;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
  }

  .special-category {
    color: var(--text-light);
    font-size: 12px;
    font-weight: 600;
    text-transform: none;
  }

  .special-text {
    font-size: 14px;
    color: var(--text-dark);
    font-weight: 500;
    line-height: 1.4;
  }

  .special-hint {
    font-size: 12px;
    color: var(--text-light);
    font-style: italic;
    margin-top: 6px;
  }

  .thinking-dots {
    display: flex;
    gap: 4px;
    padding-left: 8px;
    border-left: 1px solid var(--border-light);
  }

  .thinking-dots span {
    width: 5px;
    height: 5px;
    background: var(--question-purple);
    border-radius: 50%;
    animation: dotPulse 1.4s ease-in-out infinite;
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

  @media (max-width: 768px) {
    .btn-label {
      display: none;
    }
    .question-container {
      max-width: calc(100% - 32px);
    }
    .toggle-bar {
      padding: 4px 10px;
    }
  }
</style>
