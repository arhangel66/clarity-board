import { get, writable } from 'svelte/store';
import type { CardCreatePayload, ClientMessage, ServerMessage } from '../types';
import { cards, connections, chatMessages } from './cards';
import { session } from './session';
import { locale } from './i18n';

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

// Keep in sync with CSS animation in Card.svelte (cardFadeOut)
const CARD_DELETE_ANIMATION_MS = 500;

function createWebSocketStore() {
  const status = writable<ConnectionStatus>('disconnected');
  const hasSession = writable<boolean>(false);
  let ws: WebSocket | null = null;
  let authToken: string | null = null;
  let activeSessionId: string | null = null;
  let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  let reconnectAttempts = 0;
  const maxReconnectAttempts = 5;
  const reconnectDelay = 2000;
  const SESSION_STORAGE_KEY = 'fact_session_id';
  let activeLocale = get(locale);

  function clearStoredSessionId() {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem(SESSION_STORAGE_KEY);
    }
  }

  function connect(url: string = 'ws://localhost:8000/ws', token?: string, sessionId?: string) {
    if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) {
      return;
    }

    status.set('connecting');
    if (token) authToken = token;
    if (sessionId) activeSessionId = sessionId;
    console.log('[WebSocket] Connecting to', url);

    try {
      ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('[WebSocket] Connected');
        status.set('connected');
        reconnectAttempts = 0;

        // Send init with auth + session_id
        send({
          type: 'init',
          payload: {
            session_id: activeSessionId || undefined,
            auth_token: authToken || undefined,
            locale: activeLocale
          }
        });

        // Ensure backend locale is updated (no-op if already matching)
        send({
          type: 'set_locale',
          payload: { locale: activeLocale }
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
      case 'cards_add': {
        session.setThinking(false);
        const adjustedPositions = cards.addCards(message.payload.cards);
        if (adjustedPositions.length > 0) {
          setTimeout(() => {
            adjustedPositions.forEach((pos) => {
              sendCardMove(pos.id, pos.x, pos.y, false);
            });
          }, 80);
        }
        // Update board title if root card is added
        if (activeSessionId) {
          const rootCard = message.payload.cards.find((c) => c.is_root);
          if (rootCard && rootCard.text) {
            import('./boards').then(({ boards }) => {
              boards.updateBoardTitle(activeSessionId!, rootCard.text);
            });
          }
        }
        // Clear is_new flag after animation
        message.payload.cards.forEach((card) => {
          if (card.is_new) {
            setTimeout(() => {
              cards.clearNewFlag(card.id);
            }, 3000);
          }
        });
        break;
      }

      case 'cards_update':
        cards.updateCards(message.payload.updates);
        // Update board title if root card is updated
        if (activeSessionId) {
          const rootUpdate = message.payload.updates.find((u) => {
            if (!u.id) return false;
            const card = get(cards).find((c) => c.id === u.id);
            return card?.is_root && u.text;
          });
          if (rootUpdate && rootUpdate.text) {
            import('./boards').then(({ boards }) => {
              boards.updateBoardTitle(activeSessionId!, rootUpdate.text!);
            });
          }
        }
        break;

      case 'connections_add':
        connections.addConnections(message.payload.connections);
        break;

      case 'connection_deleted':
        console.log('[WebSocket] Connection deleted:', message.payload.connection_id);
        connections.deleteConnection(message.payload.connection_id);
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
        cards.clear();
        connections.clear();
        chatMessages.clear();
        session.startSession();
        activeSessionId = message.payload.session.id;
        break;

      case 'session_cleared':
        console.log('[WebSocket] Session cleared');
        hasSession.set(false);
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
          message.payload.phase,
          message.payload.special_questions_unlocked
        );
        break;

      case 'cards_delete':
        console.log('[WebSocket] Cards delete:', message.payload.card_ids);
        // Mark cards as deleting for fade-out animation
        message.payload.card_ids.forEach((id) => {
          cards.markDeleting(id);
        });
        // Remove cards after animation completes
        setTimeout(() => {
          cards.deleteCards(message.payload.card_ids);
        }, CARD_DELETE_ANIMATION_MS);
        break;

      case 'card_deleted':
        console.log('[WebSocket] Card deleted:', message.payload.card_id);
        cards.markDeleting(message.payload.card_id);
        setTimeout(() => {
          cards.deleteCard(message.payload.card_id);
        }, CARD_DELETE_ANIMATION_MS);
        break;

      case 'special_question_prompt':
        console.log('[WebSocket] Special question prompt:', message.payload);
        session.setPendingSpecialQuestion(message.payload);
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

  locale.subscribe((nextLocale) => {
    if (nextLocale === activeLocale) return;
    activeLocale = nextLocale;
    if (ws && ws.readyState === WebSocket.OPEN) {
      send({
        type: 'set_locale',
        payload: { locale: activeLocale }
      });
    }
  });

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

  function initSession(sessionId: string) {
    activeSessionId = sessionId;
    if (ws && ws.readyState === WebSocket.OPEN) {
      send({
        type: 'init',
        payload: {
          session_id: sessionId,
          auth_token: authToken || undefined
        }
      });
    }
  }

  function sendText(text: string) {
    session.setThinking(true);
    // Always send user_message - backend creates session if needed
    send({
      type: 'user_message',
      payload: { text }
    });
  }

  function sendTextWithSpecialQuestion(text: string, specialQuestionId: string) {
    session.setThinking(true);
    send({
      type: 'user_message',
      payload: { text, special_question_id: specialQuestionId }
    });
  }

  function sendCardMove(cardId: string, x: number, y: number, pinned: boolean = true, width?: number, height?: number, custom_scale?: number) {
    // Convert from 0-100 (frontend) to 0-1 (backend)
    send({
      type: 'card_move',
      payload: {
        card_id: cardId,
        x: x / 100,
        y: y / 100,
        pinned,
        width,
        height,
        custom_scale
      }
    });
  }

  function clearSession() {
    send({
      type: 'clear_session',
      payload: {}
    });
  }

  function sendCardDelete(cardId: string) {
    send({
      type: 'card_delete',
      payload: { card_id: cardId }
    });
  }

  function sendCardCreate(payload: CardCreatePayload) {
    send({
      type: 'card_create',
      payload
    });
  }

  function sendCardUpdate(
    cardId: string,
    updates: Partial<{ text: string; importance: number; confidence: number; emoji: string }>
  ) {
    send({
      type: 'card_update',
      payload: { card_id: cardId, updates }
    });
  }

  function requestSpecialQuestion() {
    send({
      type: 'special_question_request',
      payload: {}
    });
  }

  function sendConnectionCreate(fromId: string, toId: string, type: string = 'relates', label?: string) {
    send({
      type: 'connection_create',
      payload: { from_id: fromId, to_id: toId, type: type as any, label }
    });
  }

  function sendConnectionDelete(connectionId: string) {
    send({
      type: 'connection_delete',
      payload: { connection_id: connectionId }
    });
  }

  return {
    status: { subscribe: status.subscribe },
    hasSession: { subscribe: hasSession.subscribe },
    connect,
    disconnect,
    send,
    sendText,
    sendTextWithSpecialQuestion,
    sendCardMove,
    sendCardCreate,
    sendCardDelete,
    sendCardUpdate,
    requestSpecialQuestion,
    sendConnectionCreate,
    sendConnectionDelete,
    clearSession,
    initSession
  };
}

export const websocket = createWebSocketStore();
