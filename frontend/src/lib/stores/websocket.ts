import { writable } from 'svelte/store';
import type { ClientMessage, ServerMessage } from '../types';
import { cards, connections, chatMessages } from './cards';
import { session } from './session';

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

const SESSION_STORAGE_KEY = 'fact_session_id';

function getStoredSessionId(): string | null {
  try {
    return localStorage.getItem(SESSION_STORAGE_KEY);
  } catch {
    return null;
  }
}

function setStoredSessionId(sessionId: string) {
  try {
    localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
  } catch {
    console.error('[WebSocket] Failed to store session ID');
  }
}

function clearStoredSessionId() {
  try {
    localStorage.removeItem(SESSION_STORAGE_KEY);
  } catch {
    console.error('[WebSocket] Failed to clear session ID');
  }
}

function createWebSocketStore() {
  const status = writable<ConnectionStatus>('disconnected');
  const hasSession = writable<boolean>(false);
  let ws: WebSocket | null = null;
  let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  let reconnectAttempts = 0;
  const maxReconnectAttempts = 5;
  const reconnectDelay = 2000;

  function connect(url: string = 'ws://localhost:8000/ws') {
    if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) {
      return;
    }

    status.set('connecting');
    console.log('[WebSocket] Connecting to', url);

    try {
      ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('[WebSocket] Connected');
        status.set('connected');
        reconnectAttempts = 0;

        // Send init with stored session_id
        const sessionId = getStoredSessionId();
        send({
          type: 'init',
          payload: { session_id: sessionId || undefined }
        });
      };

      ws.onmessage = (event) => {
        try {
          const message: ServerMessage = JSON.parse(event.data);
          handleMessage(message);
        } catch (e) {
          console.error('[WebSocket] Failed to parse message:', e);
        }
      };

      ws.onclose = (event) => {
        console.log('[WebSocket] Disconnected:', event.code, event.reason);
        status.set('disconnected');
        ws = null;
        scheduleReconnect(url);
      };

      ws.onerror = (error) => {
        console.error('[WebSocket] Error:', error);
        status.set('error');
      };
    } catch (e) {
      console.error('[WebSocket] Failed to connect:', e);
      status.set('error');
      scheduleReconnect(url);
    }
  }

  function scheduleReconnect(url: string) {
    if (reconnectAttempts >= maxReconnectAttempts) {
      console.log('[WebSocket] Max reconnect attempts reached');
      return;
    }

    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout);
    }

    reconnectAttempts++;
    const delay = reconnectDelay * reconnectAttempts;
    console.log(`[WebSocket] Reconnecting in ${delay}ms (attempt ${reconnectAttempts})`);

    reconnectTimeout = setTimeout(() => {
      connect(url);
    }, delay);
  }

  function handleMessage(message: ServerMessage) {
    console.log('[WebSocket] Received:', message.type);

    switch (message.type) {
      case 'cards_add':
        session.setThinking(false);
        cards.addCards(message.payload.cards);
        // Clear is_new flag after animation
        message.payload.cards.forEach((card) => {
          if (card.is_new) {
            setTimeout(() => {
              cards.clearNewFlag(card.id);
            }, 3000);
          }
        });
        break;

      case 'cards_update':
        cards.updateCards(message.payload.updates);
        break;

      case 'connections_add':
        connections.addConnections(message.payload.connections);
        break;

      case 'ai_question':
        chatMessages.addMessage(message.payload.text, 'ai');
        break;

      case 'positions_update':
        cards.updatePositions(message.payload.positions);
        break;

      case 'session_loaded':
        console.log('[WebSocket] Session loaded:', message.payload.session.id);
        hasSession.set(true);
        session.startSession();
        // Store session ID for page reload persistence
        setStoredSessionId(message.payload.session.id);
        break;

      case 'session_cleared':
        console.log('[WebSocket] Session cleared');
        hasSession.set(false);
        clearStoredSessionId();
        cards.clear();
        connections.clear();
        chatMessages.clear();
        session.reset();
        break;

      case 'question_update':
        console.log('[WebSocket] Question update:', message.payload);
        session.setThinking(false);
        session.updateQuestion(
          message.payload.question,
          message.payload.hint,
          message.payload.phase
        );
        break;

      case 'error':
        console.error('[WebSocket] Server error:', message.payload.message);
        session.setThinking(false);
        // If session not found, clear localStorage
        if (message.payload.message === 'Session not found') {
          clearStoredSessionId();
          hasSession.set(false);
        }
        chatMessages.addMessage(`Error: ${message.payload.message}`, 'system');
        break;

      default:
        console.warn('[WebSocket] Unknown message type:', (message as ServerMessage).type);
    }
  }

  function send(message: ClientMessage) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
      console.log('[WebSocket] Sent:', message.type);
    } else {
      console.warn('[WebSocket] Cannot send - not connected');
    }
  }

  function disconnect() {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout);
      reconnectTimeout = null;
    }
    if (ws) {
      ws.close();
      ws = null;
    }
    status.set('disconnected');
  }

  function sendText(text: string) {
    session.setThinking(true);
    // Always send user_message - backend creates session if needed
    send({
      type: 'user_message',
      payload: { text }
    });
  }

  function sendCardMove(cardId: string, x: number, y: number, pinned: boolean = true) {
    // Convert from 0-100 (frontend) to 0-1 (backend)
    send({
      type: 'card_move',
      payload: {
        card_id: cardId,
        x: x / 100,
        y: y / 100,
        pinned
      }
    });
  }

  function clearSession() {
    send({
      type: 'clear_session',
      payload: {}
    });
  }

  return {
    status: { subscribe: status.subscribe },
    hasSession: { subscribe: hasSession.subscribe },
    connect,
    disconnect,
    send,
    sendText,
    sendCardMove,
    clearSession
  };
}

export const websocket = createWebSocketStore();
