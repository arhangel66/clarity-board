import { writable } from 'svelte/store';
import type { SessionPhase } from '../types';

export interface SessionState {
  phase: SessionPhase;
  currentQuestion: string;
  currentHint: string;
  phaseIndex: number;
  isActive: boolean;
  isAiThinking: boolean;
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
    question: 'What problem are you trying to solve?',
    hint: 'Describe the situation that is bothering you'
  },
  facts: {
    question: 'What are the concrete facts of the situation?',
    hint: 'Numbers, dates, events - things that can be verified'
  },
  pains: {
    question: 'What specifically hurts or bothers you?',
    hint: 'Be specific - not "I feel bad" but "I can\'t sleep before deadlines"'
  },
  resources: {
    question: 'What resources do you have?',
    hint: 'People, skills, money, time - anything that can help'
  },
  gaps: {
    question: 'What might be missing from this picture?',
    hint: 'What haven\'t we talked about yet?'
  },
  connections: {
    question: 'How do these things connect?',
    hint: 'What causes what? What blocks what?'
  }
};

function createSessionStore() {
  const initialState: SessionState = {
    phase: 'question',
    currentQuestion: DEFAULT_QUESTIONS.question.question,
    currentHint: DEFAULT_QUESTIONS.question.hint,
    phaseIndex: 0,
    isActive: true,  // Show question immediately on page load
    isAiThinking: false
  };

  const { subscribe, set, update } = writable<SessionState>(initialState);

  return {
    subscribe,

    updateQuestion: (question: string, hint: string, phase?: SessionPhase) => {
      update((state) => ({
        ...state,
        currentQuestion: question,
        currentHint: hint,
        phase: phase ?? state.phase,
        isActive: true
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

    getPhaseLabel: (phase: SessionPhase) => PHASE_LABELS[phase]
  };
}

export const session = createSessionStore();
export { PHASE_LABELS, PHASE_ORDER };
