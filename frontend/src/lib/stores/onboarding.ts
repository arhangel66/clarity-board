import { writable } from 'svelte/store';

function createOnboardingStore() {
  const { subscribe, set } = writable(false);

  return {
    subscribe,
    show: () => set(true),
    hide: () => set(false)
  };
}

export const onboarding = createOnboardingStore();
