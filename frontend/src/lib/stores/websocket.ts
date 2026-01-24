import { writable } from 'svelte/store';
import type { ClientMessage, ServerMessage } from '../types';
import { cards, connections, chatMessages } from './cards';

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

function createWebSocketStore() {
  const status = writable<ConnectionStatus>('disconnected');
  const hasSession = writable<boolean>(false);
  let ws: WebSocket | null = null;
  let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  let reconnectAttempts = 0;
  let _hasSession = false;
  const maxReconnectAttempts = 5;
  const reconnectDelay = 2000;

  hasSession.subscribe((value) => {
    _hasSession = value;
  });

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
        break;

      case 'error':
        console.error('[WebSocket] Server error:', message.payload.message);
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

  function sendUserMessage(text: string) {
    chatMessages.addMessage(text, 'user');

    // If no session exists, create one with this message as the question
    if (!_hasSession) {
      sendNewSession(text);
    } else {
      send({
        type: 'user_message',
        payload: { text }
      });
    }
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

  function sendNewSession(question: string) {
    cards.clear();
    connections.clear();
    // Don't clear chatMessages - keep the user's message visible
    send({
      type: 'new_session',
      payload: { question }
    });
  }

  return {
    status: { subscribe: status.subscribe },
    hasSession: { subscribe: hasSession.subscribe },
    connect,
    disconnect,
    send,
    sendUserMessage,
    sendCardMove,
    sendNewSession
  };
}

export const websocket = createWebSocketStore();
