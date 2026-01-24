import { writable } from 'svelte/store';

export const ZOOM_MIN = 0.6;
export const ZOOM_MAX = 1.6;
export const ZOOM_STEP = 0.1;

function clamp(value: number) {
  return Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, value));
}

function createZoomStore() {
  const { subscribe, set, update } = writable(1);

  return {
    subscribe,
    set: (value: number) => set(clamp(value)),
    zoomIn: () => update((value) => clamp(value + ZOOM_STEP)),
    zoomOut: () => update((value) => clamp(value - ZOOM_STEP)),
    reset: () => set(1)
  };
}

export const zoom = createZoomStore();
