<script lang="ts">
  import { websocket } from '../stores/websocket';

  let inputText = $state('');
  let isFocused = $state(false);

  const hasSession = websocket.hasSession;

  function handleSend() {
    const text = inputText.trim();
    if (!text) return;

    websocket.sendText(text);
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
</script>

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
    placeholder="Type your answer..."
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

<style>
  .input-bar {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;

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

    width: 90%;
    max-width: 600px;

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
</style>
