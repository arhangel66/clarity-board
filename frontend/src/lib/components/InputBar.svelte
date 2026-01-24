<script lang="ts">
  import { websocket } from '../stores/websocket';
  import { session } from '../stores/session';
  import { cards } from '../stores/cards';
  import { helpOverlay } from '../stores/help';
  import { zoom, ZOOM_MAX, ZOOM_MIN } from '../stores/zoom';
  import type { SessionPhase } from '../types';

  let inputText = $state('');
  let isFocused = $state(false);
  let specialQuestionsUnlocked = $state(false);
  let pendingSpecialQuestion = $state<{
    id: string;
    question: string;
    hint: string;
  } | null>(null);
  let currentPhase = $state<SessionPhase>('question');
  let nonQuestionCards = $state(0);

  const SPECIAL_QUESTION_MIN_CARDS = 10;

  const hasSession = websocket.hasSession;

  $effect(() => {
    const unsubscribe = session.subscribe((state) => {
      specialQuestionsUnlocked = state.specialQuestionsUnlocked;
      pendingSpecialQuestion = state.pendingSpecialQuestion;
      currentPhase = state.phase;
    });
    return unsubscribe;
  });

  $effect(() => {
    const unsubscribe = cards.subscribe((list) => {
      nonQuestionCards = list.filter((card) => card.type !== 'question').length;
    });
    return unsubscribe;
  });

  function handleSend() {
    const text = inputText.trim();
    if (!text) return;

    if (pendingSpecialQuestion) {
      websocket.sendTextWithSpecialQuestion(text, pendingSpecialQuestion.id);
      session.clearPendingSpecialQuestion();
    } else {
      websocket.sendText(text);
    }
    inputText = '';
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleMicClick() {
    // Placeholder for voice input
    console.log('Voice input not yet implemented');
  }

  function handleNewSession() {
    websocket.clearSession();
  }

  function handleSpecialQuestion() {
    websocket.requestSpecialQuestion();
  }

  function handleHelp() {
    helpOverlay.toggle();
  }

  function handleZoomIn() {
    zoom.zoomIn();
  }

  function handleZoomOut() {
    zoom.zoomOut();
  }
</script>

{#if pendingSpecialQuestion}
  <div class="special-question-banner">
    <div class="special-question-label">Особый вопрос</div>
    <div class="special-question-text">{pendingSpecialQuestion.question}</div>
    {#if pendingSpecialQuestion.hint}
      <div class="special-question-hint">{pendingSpecialQuestion.hint}</div>
    {/if}
  </div>
{/if}

<div class="input-dock">
  <div class="input-bar" class:focused={isFocused}>
    {#if $hasSession}
      <button class="new-session-btn" onclick={handleNewSession} title="Start new session">
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
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
    {/if}

    <button class="mic-btn" onclick={handleMicClick} title="Voice input (coming soon)">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
      </svg>
    </button>

    <input
      type="text"
      class="text-input"
      placeholder={pendingSpecialQuestion ? 'Ответ на особый вопрос...' : 'Type your answer...'}
      bind:value={inputText}
      onkeydown={handleKeyDown}
      onfocus={() => (isFocused = true)}
      onblur={() => (isFocused = false)}
    />

    <button class="send-btn" onclick={handleSend} disabled={!inputText.trim()} aria-label="Send answer">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <line x1="22" y1="2" x2="11" y2="13"></line>
        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
      </svg>
    </button>
  </div>

  <div class="action-panel">
    <button class="help-mini-btn" onclick={handleHelp} title="Help">
      Help
    </button>
    <button
      class="special-question-btn"
      onclick={handleSpecialQuestion}
      disabled={
        !!pendingSpecialQuestion ||
        (!specialQuestionsUnlocked &&
          (currentPhase === 'question' || nonQuestionCards < SPECIAL_QUESTION_MIN_CARDS))
      }
      title="Ask a special question"
    >
      Задать особый вопрос
    </button>
    <div class="zoom-panel" aria-label="Zoom controls">
      <button
        class="zoom-btn"
        onclick={handleZoomIn}
        disabled={$zoom >= ZOOM_MAX}
        title="Zoom in"
        aria-label="Zoom in"
      >
        +
      </button>
      <button
        class="zoom-btn"
        onclick={handleZoomOut}
        disabled={$zoom <= ZOOM_MIN}
        title="Zoom out"
        aria-label="Zoom out"
      >
        −
      </button>
    </div>
  </div>
</div>

<style>
  .input-dock {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;

    display: flex;
    align-items: center;
    gap: 12px;

    width: min(900px, calc(100% - 40px));
  }

  .input-bar {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;

    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 28px;
    padding: 8px 12px;
    box-shadow:
      0 4px 20px rgba(0, 0, 0, 0.1),
      0 2px 8px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.08);

    min-width: 0;
    transition:
      box-shadow 0.2s ease,
      border-color 0.2s ease;
  }

  .input-bar.focused {
    box-shadow:
      0 4px 24px rgba(0, 0, 0, 0.12),
      0 2px 12px rgba(0, 0, 0, 0.08);
    border-color: rgba(149, 117, 205, 0.3);
  }

  .text-input {
    flex: 1;
    border: none;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    font-size: 16px;
    color: var(--text-dark);
    outline: none;
    padding: 8px 4px;
  }

  .text-input::placeholder {
    color: var(--text-light);
  }

  .new-session-btn,
  .mic-btn,
  .send-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .new-session-btn {
    background: transparent;
    color: var(--text-light);
  }

  .new-session-btn:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .mic-btn {
    background: transparent;
    color: var(--text-light);
  }

  .mic-btn:hover {
    background: rgba(0, 0, 0, 0.05);
    color: var(--text-medium);
  }

  .send-btn {
    background: var(--question-purple);
    color: white;
  }

  .send-btn:hover:not(:disabled) {
    background: #7e57c2;
    transform: scale(1.05);
  }

  .send-btn:disabled {
    background: #d4d4d4;
    cursor: not-allowed;
  }

  .send-btn:active:not(:disabled) {
    transform: scale(0.95);
  }

  .special-question-banner {
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 99;

    max-width: 680px;
    width: calc(100% - 80px);
    padding: 12px 16px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(34, 197, 94, 0.25);
    box-shadow:
      0 6px 18px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .special-question-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: rgba(34, 197, 94, 0.8);
    font-weight: 600;
    margin-bottom: 4px;
  }

  .special-question-text {
    font-size: 14px;
    color: var(--text-dark);
    font-weight: 600;
    line-height: 1.3;
  }

  .special-question-hint {
    margin-top: 6px;
    font-size: 12px;
    color: var(--text-light);
  }

  .action-panel {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .help-mini-btn,
  .special-question-btn {
    border: none;
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 170px;
  }

  .help-mini-btn {
    background: rgba(149, 117, 205, 0.15);
    color: #4a2e8a;
  }

  .help-mini-btn:hover {
    background: rgba(149, 117, 205, 0.25);
  }

  .special-question-btn {
    background: rgba(34, 197, 94, 0.12);
    color: #166534;
  }

  .special-question-btn:hover:not(:disabled) {
    background: rgba(34, 197, 94, 0.2);
  }

  .special-question-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .zoom-panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }

  .zoom-btn {
    border: none;
    border-radius: 12px;
    padding: 6px 0;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    background: rgba(0, 0, 0, 0.06);
    color: var(--text-dark);
    transition: all 0.2s ease;
    min-width: 40px;
  }

  .zoom-btn:hover:not(:disabled) {
    background: rgba(0, 0, 0, 0.12);
  }

  .zoom-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  @media (max-width: 900px) {
    .input-dock {
      flex-direction: column;
      align-items: stretch;
      gap: 10px;
      width: calc(100% - 40px);
    }

    .action-panel {
      flex-direction: row;
      justify-content: center;
    }

    .help-mini-btn,
    .special-question-btn {
      min-width: 0;
      flex: 1;
    }

    .zoom-panel {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }
</style>
