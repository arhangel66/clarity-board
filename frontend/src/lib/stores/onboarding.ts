import { writable } from 'svelte/store';

export type TooltipKey = 'inputbar' | 'cards_added' | 'connections_hint';

const STORAGE_KEY = 'fact_tips_seen';
const OLD_STORAGE_KEY = 'fact_onboarding_seen';

function loadSeenTips(): Set<TooltipKey> {
  try {
    // If user saw old onboarding, treat all tips as seen
    if (localStorage.getItem(OLD_STORAGE_KEY)) {
      return new Set<TooltipKey>(['inputbar', 'cards_added', 'connections_hint']);
    }
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      return new Set<TooltipKey>(JSON.parse(raw));
    }
  } catch {
    // ignore
  }
  return new Set<TooltipKey>();
}

function saveSeenTips(seen: Set<TooltipKey>) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...seen]));
  } catch {
    // ignore
  }
}

interface OnboardingState {
  activeTip: TooltipKey | null;
  seenTips: Set<TooltipKey>;
}

function createOnboardingStore() {
  const seenTips = loadSeenTips();
  const { subscribe, set, update } = writable<OnboardingState>({
    activeTip: null,
    seenTips
  });

  let dismissTimer: ReturnType<typeof setTimeout> | null = null;

  function clearTimer() {
    if (dismissTimer) {
      clearTimeout(dismissTimer);
      dismissTimer = null;
    }
  }

  return {
    subscribe,
    maybeShow: (tip: TooltipKey) => {
      update((state) => {
        if (state.seenTips.has(tip) || state.activeTip !== null) return state;
        clearTimer();
        dismissTimer = setTimeout(() => {
          update((s) => {
            if (s.activeTip !== tip) return s;
            const newSeen = new Set(s.seenTips);
            newSeen.add(tip);
            saveSeenTips(newSeen);
            return { activeTip: null, seenTips: newSeen };
          });
        }, 8000);
        return { ...state, activeTip: tip };
      });
    },
    dismiss: (tip: TooltipKey) => {
      clearTimer();
      update((state) => {
        if (state.activeTip !== tip) return state;
        const newSeen = new Set(state.seenTips);
        newSeen.add(tip);
        saveSeenTips(newSeen);
        return { activeTip: null, seenTips: newSeen };
      });
    },
    reset: () => {
      clearTimer();
      set({ activeTip: null, seenTips: new Set() });
    }
  };
}

export const onboarding = createOnboardingStore();
