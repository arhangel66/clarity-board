export type CardType = 'question' | 'fact' | 'pain' | 'resource' | 'hypothesis' | 'todo';

export type ConnectionType = 'causes' | 'relates' | 'contradicts' | 'blocks';

export type SessionPhase = 'question' | 'facts' | 'pains' | 'resources' | 'gaps' | 'connections';

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
  pinned: boolean;
  // Optional fields for animations and state (computed on frontend)
  target_x?: number;
  target_y?: number;
  is_new?: boolean;
  is_root?: boolean;
  is_deleting?: boolean;
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
export interface InitPayload {
  session_id?: string;
  auth_token?: string;
}

export interface UserMessagePayload {
  text: string;
  special_question_id?: string;
}

export interface ClearSessionPayload {}

export interface CardMovePayload {
  card_id: string;
  x: number;
  y: number;
  pinned: boolean;
}

export interface CardDeletePayload {
  card_id: string;
}

export interface CardUpdatePayload {
  card_id: string;
  updates: Partial<Pick<Card, 'text' | 'importance' | 'confidence' | 'emoji'>>;
}

export type ClientMessage =
  | { type: 'init'; payload: InitPayload }
  | { type: 'user_message'; payload: UserMessagePayload }
  | { type: 'clear_session'; payload: ClearSessionPayload }
  | { type: 'card_move'; payload: CardMovePayload }
  | { type: 'card_delete'; payload: CardDeletePayload }
  | { type: 'card_update'; payload: CardUpdatePayload }
  | { type: 'special_question_request'; payload: {} };

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

export interface QuestionUpdatePayload {
  phase: SessionPhase;
  question: string;
  hint: string;
  phaseIndex: number;
  special_questions_unlocked?: boolean;
}

export interface SessionClearedPayload {}

export interface CardDeletedPayload {
  card_id: string;
}

export interface SpecialQuestionPromptPayload {
  id: string;
  category_id: string;
  question: string;
  hint: string;
}

export interface CardsDeletePayload {
  card_ids: string[];
}

export type ServerMessage =
  | { type: 'cards_add'; payload: CardsAddPayload }
  | { type: 'cards_update'; payload: CardsUpdatePayload }
  | { type: 'cards_delete'; payload: CardsDeletePayload }
  | { type: 'connections_add'; payload: ConnectionsAddPayload }
  | { type: 'ai_question'; payload: AiQuestionPayload }
  | { type: 'positions_update'; payload: PositionsUpdatePayload }
  | { type: 'session_loaded'; payload: SessionLoadedPayload }
  | { type: 'session_cleared'; payload: SessionClearedPayload }
  | { type: 'question_update'; payload: QuestionUpdatePayload }
  | { type: 'card_deleted'; payload: CardDeletedPayload }
  | { type: 'special_question_prompt'; payload: SpecialQuestionPromptPayload }
  | { type: 'error'; payload: ErrorPayload };

// Chat message for UI
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'system' | 'ai';
  timestamp: Date;
}
