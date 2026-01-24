import { readable } from 'svelte/store';

const MOBILE_BREAKPOINT = 768;

function createMobileStore() {
  return readable(false, (set) => {
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT}px)`);
    set(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => set(e.matches);
    mediaQuery.addEventListener('change', handler);

    return () => mediaQuery.removeEventListener('change', handler);
  });
}

export const isMobile = createMobileStore();
