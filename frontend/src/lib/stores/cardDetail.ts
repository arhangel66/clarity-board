import { writable } from 'svelte/store';

export const detailCardId = writable<string | null>(null);

export function openCardDetail(cardId: string) {
  detailCardId.set(cardId);
}

export function closeCardDetail() {
  detailCardId.set(null);
}
