<script lang="ts">
  import { chatMessages, cards, connections } from '../stores/cards';
  import { websocket } from '../stores/websocket';
  import type { ConnectionStatus } from '../stores/websocket';
  import type { Card, CardType } from '../types';
  import demoData from '../data/demo-session.json';

  let inputText = $state('');
  let messagesContainer: HTMLDivElement;
  let connectionStatus = $state<ConnectionStatus>('disconnected');
  let isLoadingDemo = $state(false);

  const typeColors: Record<CardType, string> = {
    question: '#9575CD',
    fact: '#5B9BD5',
    pain: '#E57373',
    resource: '#81C784',
    hypothesis: '#FFB74D'
  };

  async function loadDemo() {
    if (isLoadingDemo) return;

    isLoadingDemo = true;

    // Clear existing cards and connections
    cards.clear();
    connections.clear();
    chatMessages.clear();

    chatMessages.addMessage('Loading demo session...', 'system');

    // Add cards one by one with delay for animation effect
    for (let i = 0; i < demoData.cards.length; i++) {
      const rawCard = demoData.cards[i];
      const card: Card = {
        id: rawCard.id,
        text: rawCard.text,
        type: rawCard.type as CardType,
        emoji: rawCard.emoji,
        color: typeColors[rawCard.type as CardType],
        importance: rawCard.importance,
        confidence: 1.0,
        // Coordinates are in 0-1 format, addCards will convert to 0-100
        x: rawCard.x,
        y: rawCard.y,
        target_x: rawCard.x,
        target_y: rawCard.y,
        pinned: rawCard.id === 'root_001',
        is_root: rawCard.id === 'root_001',
        is_new: true,
        created_at: new Date().toISOString()
      };

      cards.addCards([card]);

      // Small delay between cards for animation effect
      await new Promise(resolve => setTimeout(resolve, 150));

      // Clear new flag after animation
      setTimeout(() => {
        cards.clearNewFlag(card.id);
      }, 3000);
    }

    chatMessages.addMessage(`Demo loaded: ${demoData.cards.length} cards`, 'system');
    isLoadingDemo = false;
  }

  // Subscribe to websocket status
  $effect(() => {
    const unsubscribe = websocket.status.subscribe((status) => {
      connectionStatus = status;
    });
    return unsubscribe;
  });

  $effect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (messagesContainer && $chatMessages.length > 0) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  });

  function handleSend() {
    const text = inputText.trim();
    if (text) {
      websocket.sendUserMessage(text);
      inputText = '';
    }
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }
</script>

<div class="chat-panel">
  <div class="chat-header">
    <h2>Notes</h2>
    <p>thoughts and ideas</p>
    <div class="connection-status">
      {#if connectionStatus === 'connected'}
        <span class="status-dot connected"></span>
        <span class="status-text">Connected</span>
      {:else if connectionStatus === 'connecting'}
        <span class="status-dot connecting"></span>
        <span class="status-text">Connecting...</span>
      {:else}
        <span class="status-dot disconnected"></span>
        <span class="status-text">Disconnected</span>
      {/if}
    </div>
    <button class="load-demo-btn" onclick={loadDemo} disabled={isLoadingDemo}>
      {isLoadingDemo ? 'Loading...' : 'Load Demo'}
    </button>
  </div>

  <div class="chat-messages" bind:this={messagesContainer}>
    {#each $chatMessages as message (message.id)}
      <div class="chat-message {message.sender}">
        {message.text}
      </div>
    {/each}
  </div>

  <div class="chat-input-container">
    <textarea
      class="chat-input"
      placeholder="Add a thought or fact..."
      rows="2"
      bind:value={inputText}
      onkeydown={handleKeyDown}
    ></textarea>
    <button class="send-btn" onclick={handleSend}>Write</button>
  </div>
</div>

<style>
  .chat-panel {
    flex: 0 0 320px;
    min-width: 320px;
    max-width: 400px;
    height: 100vh;
    background: #fffef9;
    border-left: 1px solid #d4c5a9;
    display: flex;
    flex-direction: column;
    position: relative;

    /* Notepad paper texture */
    background-image: repeating-linear-gradient(transparent, transparent 27px, #e8dfd0 27px, #e8dfd0 28px),
      linear-gradient(90deg, #f5e6d3 0px, transparent 1px);
    background-size: 100% 28px, 100% 100%;
    background-position: 0 60px, 0 0;
  }

  /* Red margin line */
  .chat-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 40px;
    width: 2px;
    height: 100%;
    background: rgba(220, 100, 100, 0.3);
    z-index: 1;
  }

  /* Spiral binding holes */
  .chat-panel::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 30px;
    height: 100%;
    background-image: repeating-linear-gradient(
      to bottom,
      transparent 0px,
      transparent 20px,
      #c4b5a0 20px,
      #c4b5a0 28px,
      transparent 28px,
      transparent 48px
    );
    background-position: 10px 10px;
    z-index: 2;
  }

  .chat-header {
    padding: 16px 20px 16px 50px;
    border-bottom: none;
    background: transparent;
    position: relative;
    z-index: 3;
  }

  .chat-header h2 {
    font-family: 'Caveat', cursive;
    font-size: 1.6em;
    color: var(--text-dark);
    font-weight: 600;
  }

  .chat-header p {
    font-size: 0.85em;
    color: var(--text-medium);
    margin-top: 4px;
    font-style: italic;
  }

  .connection-status {
    display: flex;
    align-items: center;
    margin-top: 8px;
    font-size: 0.75em;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
  }

  .status-dot.connected {
    background: var(--resource-green);
  }

  .status-dot.connecting {
    background: var(--hypothesis-amber);
    animation: pulse 1s infinite;
  }

  .status-dot.disconnected {
    background: var(--pain-red);
  }

  .status-text {
    color: var(--text-light);
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px 16px 50px;
    position: relative;
    z-index: 3;
  }

  .chat-message {
    margin-bottom: 16px;
    font-size: 0.9em;
    line-height: 1.5;
    color: var(--text-dark);
  }

  .chat-message.system {
    font-style: italic;
    color: var(--text-medium);
  }

  .chat-message.user {
    color: #2c5282;
  }

  .chat-message.ai {
    color: #553c9a;
    font-weight: 500;
  }

  .chat-message::before {
    content: '>';
    margin-right: 8px;
    color: var(--text-light);
    font-family: 'Caveat', cursive;
  }

  .chat-message.ai::before {
    content: 'AI:';
    color: #553c9a;
  }

  .chat-input-container {
    padding: 16px 20px 20px 50px;
    border-top: 1px dashed #d4c5a9;
    background: rgba(255, 254, 249, 0.9);
    position: relative;
    z-index: 3;
  }

  .chat-input {
    width: 100%;
    padding: 12px;
    border: 1px solid #d4c5a9;
    border-radius: 4px;
    font-family: Georgia, serif;
    font-size: 0.9em;
    background: #fffef9;
    color: var(--text-dark);
    resize: none;
    min-height: 60px;
  }

  .chat-input:focus {
    outline: none;
    border-color: #b8a88a;
    box-shadow: 0 0 0 3px rgba(184, 168, 138, 0.2);
  }

  .chat-input::placeholder {
    color: var(--text-light);
    font-style: italic;
  }

  .send-btn {
    margin-top: 10px;
    width: 100%;
    padding: 10px;
    background: linear-gradient(135deg, #8b7355, #6b5344);
    color: white;
    border: none;
    border-radius: 4px;
    font-family: 'Caveat', cursive;
    font-size: 1.1em;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .send-btn:hover {
    background: linear-gradient(135deg, #9b8365, #7b6354);
    transform: translateY(-1px);
  }

  .load-demo-btn {
    margin-top: 12px;
    width: 100%;
    padding: 8px 12px;
    background: transparent;
    color: #8b7355;
    border: 1px dashed #b8a88a;
    border-radius: 4px;
    font-family: 'Caveat', cursive;
    font-size: 1em;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .load-demo-btn:hover:not(:disabled) {
    background: rgba(139, 115, 85, 0.1);
    border-color: #8b7355;
  }

  .load-demo-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
