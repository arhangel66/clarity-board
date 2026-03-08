import { writable, type Readable } from "svelte/store";

import { API_BASE } from "../config";
import type { AccessSnapshot } from "../types";

export interface AccessState {
  isLoading: boolean;
  snapshot: AccessSnapshot | null;
  error: string | null;
}

interface AccessStore extends Readable<AccessState> {
  refresh: (token: string) => Promise<AccessSnapshot | null>;
  hydrate: (snapshot: AccessSnapshot) => void;
  reset: () => void;
}

const INITIAL_STATE: AccessState = {
  isLoading: false,
  snapshot: null,
  error: null,
};

export function createAccessStore(fetchImpl: typeof fetch = fetch): AccessStore {
  const { subscribe, set, update } = writable<AccessState>(INITIAL_STATE);

  async function refresh(token: string): Promise<AccessSnapshot | null> {
    if (!token) {
      set(INITIAL_STATE);
      return null;
    }

    update((state) => ({ ...state, isLoading: true, error: null }));

    try {
      const response = await fetchImpl(`${API_BASE}/api/access`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`Failed to load access status: ${response.status}`);
      }

      const snapshot = (await response.json()) as AccessSnapshot;
      set({
        isLoading: false,
        snapshot,
        error: null,
      });
      return snapshot;
    } catch (error) {
      update((state) => ({
        ...state,
        isLoading: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load access status",
      }));
      return null;
    }
  }

  function hydrate(snapshot: AccessSnapshot) {
    set({
      isLoading: false,
      snapshot,
      error: null,
    });
  }

  function reset() {
    set(INITIAL_STATE);
  }

  return {
    subscribe,
    refresh,
    hydrate,
    reset,
  };
}

export const access = createAccessStore();
