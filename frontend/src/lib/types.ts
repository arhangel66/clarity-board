export type CardType = 'question' | 'fact' | 'pain' | 'resource' | 'hypothesis';

export type ConnectionType = 'causes' | 'relates' | 'contradicts' | 'blocks';

export interface Card {
  id: string;
  text: string;
  type: CardType;
  emoji: string;
  color: string;
  importance: number;
  confidence: number;
  x: number;
  y: number;
  target_x: number;
  target_y: number;
  pinned: boolean;
  is_root: boolean;
  is_new: boolean;
  created_at: string;
}

export interface Connection {
  id: string;
  from_id: string;
  to_id: string;
  type: ConnectionType;
  strength: number;
  label: string | null;
  created_by: 'ai' | 'user';
}

// WebSocket message types - Client to Server
export interface UserMessagePayload {
  text: string;
}

export interface CardMovePayload {
  card_id: string;
  x: number;
  y: number;
  pinned: boolean;
}

export interface NewSessionPayload {
  question: string;
}

export type ClientMessage =
  | { type: 'user_message'; payload: UserMessagePayload }
  | { type: 'card_move'; payload: CardMovePayload }
  | { type: 'new_session'; payload: NewSessionPayload };

// WebSocket message types - Server to Client
export interface CardsAddPayload {
  cards: Card[];
}

export interface CardsUpdatePayload {
  updates: Partial<Card>[];
}

export interface ConnectionsAddPayload {
  connections: Connection[];
}

export interface AiQuestionPayload {
  text: string;
}

export interface PositionsUpdatePayload {
  positions: { id: string; target_x: number; target_y: number }[];
}

export interface SessionLoadedPayload {
  session: {
    id: string;
    question: string;
  };
}

export interface ErrorPayload {
  message: string;
}

export type ServerMessage =
  | { type: 'cards_add'; payload: CardsAddPayload }
  | { type: 'cards_update'; payload: CardsUpdatePayload }
  | { type: 'connections_add'; payload: ConnectionsAddPayload }
  | { type: 'ai_question'; payload: AiQuestionPayload }
  | { type: 'positions_update'; payload: PositionsUpdatePayload }
  | { type: 'session_loaded'; payload: SessionLoadedPayload }
  | { type: 'error'; payload: ErrorPayload };

// Chat message for UI
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'system' | 'ai';
  timestamp: Date;
}
