import { get, writable } from 'svelte/store';
import type { SessionPhase, SpecialQuestionPromptPayload } from '../types';
import { locale, translations } from './i18n';
import type { Locale } from './i18n';

export interface SessionState {
  phase: SessionPhase;
  currentQuestion: string;
  currentHint: string;
  phaseIndex: number;
  isActive: boolean;
  isAiThinking: boolean;
  specialQuestionsUnlocked: boolean;
  pendingSpecialQuestion: SpecialQuestionPromptPayload | null;
}

const PHASE_ORDER: SessionPhase[] = ['question', 'facts', 'pains', 'resources', 'gaps', 'connections'];

function getDefaultQuestions(activeLocale: Locale) {
  return translations[activeLocale].session.defaultQuestions;
}

function buildInitialState(activeLocale: Locale): SessionState {
  const defaults = getDefaultQuestions(activeLocale);
  return {
    phase: 'question',
    currentQuestion: defaults.question.question,
    currentHint: defaults.question.hint,
    phaseIndex: 0,
    isActive: true, // Show question immediately on page load
    isAiThinking: false,
    specialQuestionsUnlocked: false,
    pendingSpecialQuestion: null
  };
}

function createSessionStore() {
  const initialLocale = get(locale);
  const initialState = buildInitialState(initialLocale);

  const { subscribe, set, update } = writable<SessionState>(initialState);
  let activeLocale = initialLocale;

  locale.subscribe((nextLocale) => {
    update((state) => {
      if (nextLocale === activeLocale) return state;
      const previousDefaults = getDefaultQuestions(activeLocale);
      const nextDefaults = getDefaultQuestions(nextLocale);
      const previous = previousDefaults[state.phase];
      const next = nextDefaults[state.phase];
      activeLocale = nextLocale;
      if (state.currentQuestion === previous.question && state.currentHint === previous.hint) {
        return {
          ...state,
          currentQuestion: next.question,
          currentHint: next.hint
        };
      }
      return state;
    });
  });

  return {
    subscribe,

    updateQuestion: (
      question: string,
      hint: string,
      phase?: SessionPhase,
      specialQuestionsUnlocked?: boolean
    ) => {
      update((state) => ({
        ...state,
        currentQuestion: question,
        currentHint: hint,
        phase: phase ?? state.phase,
        isActive: true,
        specialQuestionsUnlocked:
          specialQuestionsUnlocked ?? state.specialQuestionsUnlocked
      }));
    },

    setPhase: (phase: SessionPhase) => {
      const phaseIndex = PHASE_ORDER.indexOf(phase);
      const defaults = getDefaultQuestions(activeLocale)[phase];
      update((state) => ({
        ...state,
        phase,
        phaseIndex,
        currentQuestion: defaults.question,
        currentHint: defaults.hint,
        isActive: true
      }));
    },

    nextPhase: () => {
      update((state) => {
        const currentIndex = PHASE_ORDER.indexOf(state.phase);
        const nextIndex = Math.min(currentIndex + 1, PHASE_ORDER.length - 1);
        const nextPhase = PHASE_ORDER[nextIndex];
        const defaults = getDefaultQuestions(activeLocale)[nextPhase];
        return {
          ...state,
          phase: nextPhase,
          phaseIndex: nextIndex,
          currentQuestion: defaults.question,
          currentHint: defaults.hint
        };
      });
    },

    startSession: () => {
      set(buildInitialState(activeLocale));
    },

    reset: () => {
      set(buildInitialState(activeLocale));
    },

    setThinking: (thinking: boolean) => {
      update((state) => ({ ...state, isAiThinking: thinking }));
    },

    setSpecialQuestionsUnlocked: (unlocked: boolean) => {
      update((state) => ({ ...state, specialQuestionsUnlocked: unlocked }));
    },

    setPendingSpecialQuestion: (prompt: SpecialQuestionPromptPayload) => {
      update((state) => ({ ...state, pendingSpecialQuestion: prompt }));
    },

    clearPendingSpecialQuestion: () => {
      update((state) => ({ ...state, pendingSpecialQuestion: null }));
    },

    getPhaseLabel: (phase: SessionPhase) => translations[activeLocale].session.phaseLabels[phase]
  };
}

export const session = createSessionStore();
export { PHASE_ORDER };
