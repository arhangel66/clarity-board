import { writable } from 'svelte/store';

function createSelectionStore() {
  const { subscribe, set } = writable<string | null>(null);

  return {
    subscribe,
    select: (cardId: string) => set(cardId),
    deselect: () => set(null),
    toggle: (cardId: string) => {
      let current: string | null = null;
      subscribe((v) => (current = v))();
      set(current === cardId ? null : cardId);
    }
  };
}

export const selectedCardId = createSelectionStore();
