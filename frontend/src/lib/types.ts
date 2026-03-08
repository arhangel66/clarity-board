export type CardType = 'question' | 'fact' | 'pain' | 'resource' | 'hypothesis' | 'todo';
export type Locale = 'ru' | 'en';
export type AccessPlan = 'free' | 'monthly' | 'lifetime';
export type MeteringState = 'pending_persistence' | 'estimated_from_sessions' | 'tracked';
export type SessionConsumptionTrigger = 'first_ai_message_on_blank_session';

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
  width?: number;
  height?: number;
  custom_scale?: number;
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

export interface AccessContract {
  status_endpoint: string;
  pricing_unit: 'sessions';
  free_sessions_total: number;
  session_consumption_trigger: SessionConsumptionTrigger;
  blank_session_consumes: boolean;
  reopen_existing_session_consumes: boolean;
  deleting_session_restores_quota: boolean;
  supported_plans: AccessPlan[];
  monthly_requires_expires_at: boolean;
  lifetime_never_expires: boolean;
}

export interface AccessStatus {
  plan: AccessPlan;
  plan_expires_at: string | null;
  plan_active: boolean;
  free_sessions_total: number;
  free_sessions_used: number | null;
  free_sessions_remaining: number | null;
  can_start_ai_session: boolean;
  metering_state: MeteringState;
}

export interface AccessSnapshot {
  contract: AccessContract;
  status: AccessStatus;
}

// WebSocket message types - Client to Server
export interface InitPayload {
  session_id?: string;
  auth_token?: string;
  locale?: Locale;
}

export interface UserMessagePayload {
  text: string;
  special_question_id?: string;
}

export interface ClearSessionPayload { }

export interface CardMovePayload {
  card_id: string;
  x: number;
  y: number;
  pinned: boolean;
  width?: number;
  height?: number;
  custom_scale?: number;
}

export interface CardDeletePayload {
  card_id: string;
}

export interface CardUpdatePayload {
  card_id: string;
  updates: Partial<Pick<Card, 'text' | 'importance' | 'confidence' | 'emoji'>>;
}

export interface CardCreatePayload {
  text: string;
  type: CardType;
  x: number;
  y: number;
  emoji?: string;
  importance?: number;
  confidence?: number;
}

export interface ConnectionCreatePayload {
  from_id: string;
  to_id: string;
  type?: ConnectionType;
  label?: string;
}

export interface ConnectionDeletePayload {
  connection_id: string;
}

export interface SetLocalePayload {
  locale: Locale;
}

export type ClientMessage =
  | { type: 'init'; payload: InitPayload }
  | { type: 'user_message'; payload: UserMessagePayload }
  | { type: 'clear_session'; payload: ClearSessionPayload }
  | { type: 'card_move'; payload: CardMovePayload }
  | { type: 'card_create'; payload: CardCreatePayload }
  | { type: 'card_delete'; payload: CardDeletePayload }
  | { type: 'card_update'; payload: CardUpdatePayload }
  | { type: 'connection_create'; payload: ConnectionCreatePayload }
  | { type: 'connection_delete'; payload: ConnectionDeletePayload }
  | { type: 'set_locale'; payload: SetLocalePayload }
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
  code?: string;
  access?: AccessSnapshot;
}

export interface QuestionUpdatePayload {
  phase: SessionPhase;
  question: string;
  hint: string;
  phaseIndex: number;
  special_questions_unlocked?: boolean;
}

export interface SessionClearedPayload { }

export interface CardDeletedPayload {
  card_id: string;
}

export interface ConnectionDeletedPayload {
  connection_id: string;
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
  | { type: 'connection_deleted'; payload: ConnectionDeletedPayload }
  | { type: 'special_question_prompt'; payload: SpecialQuestionPromptPayload }
  | { type: 'error'; payload: ErrorPayload };

// Chat message for UI
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'system' | 'ai';
  timestamp: Date;
}
