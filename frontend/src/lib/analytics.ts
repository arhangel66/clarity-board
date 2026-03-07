/**
 * Yandex Metrica analytics wrapper.
 * Replace COUNTER_ID with your actual Yandex Metrica counter ID.
 */

const COUNTER_ID = 0; // TODO: replace with real counter ID

type YmParams = Record<string, string | number | boolean>;

declare global {
  interface Window {
    ym?: (counterId: number, method: string, ...args: unknown[]) => void;
  }
}

function isEnabled(): boolean {
  return COUNTER_ID > 0 && typeof window !== 'undefined' && typeof window.ym === 'function';
}

export function reachGoal(goal: string, params?: YmParams): void {
  if (!isEnabled()) return;
  window.ym!(COUNTER_ID, 'reachGoal', goal, params);
}

export function trackEvent(name: string, params?: YmParams): void {
  reachGoal(name, params);
}

// Conversion funnel goals
export function trackLandingView(): void {
  reachGoal('landing_view');
}

export function trackSignUp(): void {
  reachGoal('sign_up');
}

export function trackFirstSession(): void {
  reachGoal('first_session');
}

export function trackCards5Plus(): void {
  reachGoal('cards_5_plus');
}

export function trackSessionCompleted(): void {
  reachGoal('session_completed');
}

// Custom events
export function trackCardCreated(cardType: string): void {
  reachGoal('card_created', { card_type: cardType });
}

export function trackConnectionCreated(connectionType: string): void {
  reachGoal('connection_created', { connection_type: connectionType });
}

export function trackPhaseChanged(phase: string): void {
  reachGoal('phase_changed', { phase });
}

export function trackSpecialQuestionUsed(): void {
  reachGoal('special_question_used');
}

export function trackVoiceInput(): void {
  reachGoal('voice_input_used');
}

export function trackTextInput(): void {
  reachGoal('text_input_used');
}
