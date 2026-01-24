import { writable } from 'svelte/store';
import type { SessionPhase, SpecialQuestionPromptPayload } from '../types';

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

const PHASE_LABELS: Record<SessionPhase, string> = {
  question: 'Defining the Problem',
  facts: 'Gathering Facts',
  pains: 'Identifying Pains',
  resources: 'Discovering Resources',
  gaps: 'Finding Gaps',
  connections: 'Making Connections'
};

const DEFAULT_QUESTIONS: Record<SessionPhase, { question: string; hint: string }> = {
  question: {
    question: 'Что самое важное вы хотите сейчас решить?',
    hint: 'Сформулируйте коротко.'
  },
  facts: {
    question: 'List concrete facts.',
    hint: 'Dates, numbers, actions.'
  },
  pains: {
    question: 'What hurts most, specifically?',
    hint: 'Concrete symptoms only.'
  },
  resources: {
    question: 'What resources are available?',
    hint: 'People, skills, time, money.'
  },
  gaps: {
    question: 'What\'s missing here?',
    hint: 'Unknowns, blind spots.'
  },
  connections: {
    question: 'What connects these items?',
    hint: 'Causes, blockers, dependencies.'
  }
};

function createSessionStore() {
  const initialState: SessionState = {
    phase: 'question',
    currentQuestion: DEFAULT_QUESTIONS.question.question,
    currentHint: DEFAULT_QUESTIONS.question.hint,
    phaseIndex: 0,
    isActive: true,  // Show question immediately on page load
    isAiThinking: false,
    specialQuestionsUnlocked: false,
    pendingSpecialQuestion: null
  };

  const { subscribe, set, update } = writable<SessionState>(initialState);

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
      const defaults = DEFAULT_QUESTIONS[phase];
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
        const defaults = DEFAULT_QUESTIONS[nextPhase];
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
      set({
        ...initialState,
        isActive: true
      });
    },

    reset: () => {
      set(initialState);
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

    getPhaseLabel: (phase: SessionPhase) => PHASE_LABELS[phase]
  };
}

export const session = createSessionStore();
export { PHASE_LABELS, PHASE_ORDER };
