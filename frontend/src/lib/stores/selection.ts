import { derived, writable } from 'svelte/store';

function createSelectionStore() {
  const { subscribe, set, update } = writable<Set<string>>(new Set());

  function normalize(next: Iterable<string>) {
    return new Set(next);
  }

  return {
    subscribe,
    set: (ids: Iterable<string>) => set(normalize(ids)),
    clear: () => set(new Set()),
    selectOnly: (cardId: string) => set(new Set([cardId])),
    add: (cardId: string) =>
      update((current) => {
        const next = new Set(current);
        next.add(cardId);
        return next;
      }),
    remove: (cardId: string) =>
      update((current) => {
        const next = new Set(current);
        next.delete(cardId);
        return next;
      }),
    toggle: (cardId: string) =>
      update((current) => {
        const next = new Set(current);
        if (next.has(cardId)) {
          next.delete(cardId);
        } else {
          next.add(cardId);
        }
        return next;
      })
  };
}

export const selectedCardIds = createSelectionStore();
export const selectedCardId = derived(selectedCardIds, ($ids) => $ids.values().next().value || null);
