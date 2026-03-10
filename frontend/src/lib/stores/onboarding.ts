import { writable } from "svelte/store";

import type { SessionPhase } from "../types";

export type OnboardingStepId =
  | "question"
  | "cards"
  | "move_card"
  | "blind_spots";

export interface OnboardingSignals {
  hasActiveBoard: boolean;
  cardCount: number;
  connectionCount: number;
  hasMovedCard?: boolean;
  phase: SessionPhase;
  isDemoBoard: boolean;
}

interface PersistedOnboardingState {
  completedSteps: OnboardingStepId[];
  isTourComplete: boolean;
}

interface StorageLike {
  getItem(key: string): string | null;
  removeItem(key: string): void;
  setItem(key: string, value: string): void;
}

export interface OnboardingState {
  activeStep: OnboardingStepId | null;
  completedSteps: Set<OnboardingStepId>;
  canAdvance: boolean;
  isTourComplete: boolean;
}

export const ONBOARDING_STORAGE_KEY = "fact_onboarding_state";
export const LEGACY_TIPS_STORAGE_KEY = "fact_tips_seen";
export const LEGACY_ONBOARDING_STORAGE_KEY = "fact_onboarding_seen";
export const ONBOARDING_STEP_ORDER: OnboardingStepId[] = [
  "question",
  "cards",
  "move_card",
  "blind_spots",
];

const COMPLETED_TOUR = new Set(ONBOARDING_STEP_ORDER);
const INITIAL_SIGNALS: OnboardingSignals = {
  hasActiveBoard: false,
  cardCount: 0,
  connectionCount: 0,
  phase: "question",
  isDemoBoard: false,
};

export function buildCompletedOnboardingState(): PersistedOnboardingState {
  return {
    completedSteps: [...ONBOARDING_STEP_ORDER],
    isTourComplete: true,
  };
}

function getDefaultStorage(): StorageLike | null {
  if (typeof localStorage === "undefined") {
    return null;
  }
  return localStorage;
}

function isOnboardingStepId(value: string): value is OnboardingStepId {
  return ONBOARDING_STEP_ORDER.includes(value as OnboardingStepId);
}

function normalizePersistedStepId(value: string): OnboardingStepId | null {
  if (value === "connections") {
    return "move_card";
  }
  return isOnboardingStepId(value) ? value : null;
}

function isStepEligible(step: OnboardingStepId, signals: OnboardingSignals): boolean {
  if (signals.isDemoBoard || !signals.hasActiveBoard) {
    return false;
  }

  switch (step) {
    case "question":
      return true;
    case "cards":
      return signals.cardCount > 0;
    case "move_card":
      return signals.cardCount >= 3;
    case "blind_spots":
      return signals.phase === "gaps" || signals.phase === "connections";
  }
}

function canAdvanceStep(step: OnboardingStepId, signals: OnboardingSignals): boolean {
  switch (step) {
    case "question":
      return signals.cardCount > 0;
    case "cards":
      return signals.cardCount >= 3;
    case "move_card":
      return signals.hasMovedCard ?? false;
    case "blind_spots":
      return signals.phase === "gaps" || signals.phase === "connections";
  }
}

function getNextEligibleStep(
  completedSteps: Set<OnboardingStepId>,
  signals: OnboardingSignals,
): OnboardingStepId | null {
  for (const step of ONBOARDING_STEP_ORDER) {
    if (completedSteps.has(step)) {
      continue;
    }
    if (isStepEligible(step, signals)) {
      return step;
    }
  }
  return null;
}

function cloneState(state: OnboardingState): OnboardingState {
  return {
    activeStep: state.activeStep,
    completedSteps: new Set(state.completedSteps),
    canAdvance: state.canAdvance,
    isTourComplete: state.isTourComplete,
  };
}

function buildCompletedState(): OnboardingState {
  return {
    activeStep: null,
    completedSteps: new Set(COMPLETED_TOUR),
    canAdvance: false,
    isTourComplete: true,
  };
}

function buildFreshState(): OnboardingState {
  return {
    activeStep: null,
    completedSteps: new Set(),
    canAdvance: false,
    isTourComplete: false,
  };
}

function finalizeStep(
  state: OnboardingState,
  targetStep: OnboardingStepId,
  signals: OnboardingSignals,
  options: { allowSkip?: boolean } = {},
): OnboardingState {
  if (
    targetStep !== state.activeStep ||
    state.completedSteps.has(targetStep) ||
    (!options.allowSkip && !canAdvanceStep(targetStep, signals))
  ) {
    return state;
  }

  const nextState = cloneState(state);
  nextState.completedSteps.add(targetStep);
  nextState.isTourComplete =
    nextState.completedSteps.size === ONBOARDING_STEP_ORDER.length;
  return nextState;
}

function loadState(storage: StorageLike | null): OnboardingState {
  if (!storage) {
    return buildFreshState();
  }

  try {
    if (storage.getItem(LEGACY_ONBOARDING_STORAGE_KEY)) {
      return buildCompletedState();
    }

    const legacyTips = storage.getItem(LEGACY_TIPS_STORAGE_KEY);
    if (legacyTips) {
      const parsed = JSON.parse(legacyTips);
      if (
        Array.isArray(parsed) &&
        parsed.includes("inputbar") &&
        parsed.includes("cards_added") &&
        parsed.includes("connections_hint")
      ) {
        return buildCompletedState();
      }
    }

    const raw = storage.getItem(ONBOARDING_STORAGE_KEY);
    if (!raw) {
      return buildFreshState();
    }

    const parsed = JSON.parse(raw) as PersistedOnboardingState;
    const completedSteps = new Set(
      Array.isArray(parsed.completedSteps)
        ? parsed.completedSteps
            .map((value) => normalizePersistedStepId(String(value)))
            .filter((value): value is OnboardingStepId => value !== null)
        : [],
    );

    if (parsed.isTourComplete) {
      return buildCompletedState();
    }

    return {
      activeStep: null,
      completedSteps,
      canAdvance: false,
      isTourComplete: completedSteps.size === ONBOARDING_STEP_ORDER.length,
    };
  } catch {
    return buildFreshState();
  }
}

function saveState(storage: StorageLike | null, state: OnboardingState): void {
  if (!storage) {
    return;
  }

  try {
    storage.removeItem(LEGACY_ONBOARDING_STORAGE_KEY);
    storage.removeItem(LEGACY_TIPS_STORAGE_KEY);
    const payload: PersistedOnboardingState = state.isTourComplete
      ? buildCompletedOnboardingState()
      : {
          completedSteps: [...state.completedSteps],
          isTourComplete: false,
        };
    storage.setItem(ONBOARDING_STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // ignore write failures
  }
}

export function createOnboardingStore(storage: StorageLike | null = getDefaultStorage()) {
  const { subscribe, set, update } = writable<OnboardingState>(loadState(storage));
  let latestSignals = INITIAL_SIGNALS;

  function syncWithSignals(state: OnboardingState): OnboardingState {
    const nextState = cloneState(state);
    if (nextState.isTourComplete) {
      nextState.activeStep = null;
      nextState.canAdvance = false;
      return nextState;
    }
    nextState.activeStep = getNextEligibleStep(nextState.completedSteps, latestSignals);
    nextState.canAdvance = nextState.activeStep
      ? canAdvanceStep(nextState.activeStep, latestSignals)
      : false;
    return nextState;
  }

  return {
    subscribe,
    sync: (signals: OnboardingSignals) => {
      latestSignals = signals;
      update((state) => syncWithSignals(state));
    },
    complete: (step?: OnboardingStepId) => {
      update((state) => {
        const targetStep = step ?? state.activeStep;
        if (!targetStep) {
          return syncWithSignals(state);
        }

        const nextState = finalizeStep(state, targetStep, latestSignals);
        const syncedState = syncWithSignals(nextState);
        saveState(storage, syncedState);
        return syncedState;
      });
    },
    skipTour: () => {
      update((state) => {
        if (!state.activeStep) {
          return syncWithSignals(state);
        }

        const nextState = finalizeStep(state, state.activeStep, latestSignals, {
          allowSkip: true,
        });
        const syncedState = syncWithSignals(nextState);
        saveState(storage, syncedState);
        return syncedState;
      });
    },
    restart: () => {
      const resetState = syncWithSignals(buildFreshState());
      saveState(storage, resetState);
      set(resetState);
    },
    reset: () => {
      const resetState = buildFreshState();
      saveState(storage, resetState);
      set(resetState);
    },
  };
}

export const onboarding = createOnboardingStore();
