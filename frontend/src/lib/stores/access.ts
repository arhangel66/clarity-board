import { writable, type Readable } from "svelte/store";

import { API_BASE } from "../config";
import type { AccessContract, AccessSnapshot } from "../types";

export interface AccessState {
  isLoading: boolean;
  snapshot: AccessSnapshot | null;
  error: string | null;
  paywallPromptCount: number;
}

export interface AccessSummaryLabels {
  loadingTitle: string;
  loadingBody: string;
  unavailableTitle: string;
  unavailableBody: string;
  starterTitle: string;
  starterRemaining: string;
  starterUsedUp: string;
  starterUsedUpBody: string;
  starterBlankBoardBody: string;
  starterDeleteDoesNotRestoreBody: string;
  monthlyTitle: string;
  monthlyBody: string;
  lifetimeTitle: string;
  lifetimeBody: string;
  activeUntil: string;
}

export interface AccessSummary {
  title: string;
  detail: string;
  note: string | null;
  tone: "loading" | "error" | "starter" | "warning" | "paid";
  remaining: number | null;
  total: number | null;
}

export interface AccessPaywallGate {
  key: string;
  shouldShow: boolean;
  total: number;
}

interface AccessStore extends Readable<AccessState> {
  refresh: (token: string) => Promise<AccessSnapshot | null>;
  hydrate: (snapshot: AccessSnapshot) => void;
  requestPaywallPrompt: () => void;
  reset: () => void;
}

const INITIAL_STATE: AccessState = {
  isLoading: false,
  snapshot: null,
  error: null,
  paywallPromptCount: 0,
};

function buildStarterRuleNote(
  contract: AccessContract,
  labels: AccessSummaryLabels,
): string {
  if (contract.deleting_session_restores_quota === false) {
    return labels.starterDeleteDoesNotRestoreBody;
  }

  return "";
}

export function summarizeAccessState(
  state: AccessState,
  labels: AccessSummaryLabels,
  currentLocale: string,
): AccessSummary {
  if (state.isLoading && !state.snapshot) {
    return {
      title: labels.loadingTitle,
      detail: labels.loadingBody,
      note: null,
      tone: "loading",
      remaining: null,
      total: null,
    };
  }

  if (!state.snapshot) {
    return {
      title: labels.unavailableTitle,
      detail: labels.unavailableBody,
      note: state.error,
      tone: "error",
      remaining: null,
      total: null,
    };
  }

  const { contract, status } = state.snapshot;
  if (status.plan === "free") {
    const total = contract.free_sessions_total ?? status.free_sessions_total ?? 3;
    const remaining = Math.max(0, status.free_sessions_remaining ?? total);
    const note = buildStarterRuleNote(contract, labels) || null;

    return {
      title: remaining > 0 ? labels.starterTitle : labels.starterUsedUp,
      detail:
        remaining > 0
          ? labels.starterRemaining
              .replace("{count}", String(remaining))
              .replace("{total}", String(total))
          : labels.starterUsedUpBody,
      note,
      tone: remaining > 0 ? "starter" : "warning",
      remaining,
      total,
    };
  }

  const formattedExpiry =
    status.plan_expires_at && !Number.isNaN(Date.parse(status.plan_expires_at))
      ? new Intl.DateTimeFormat(currentLocale, {
          month: "short",
          day: "numeric",
          year: "numeric",
        }).format(new Date(status.plan_expires_at))
      : null;

  return {
    title: status.plan === "monthly" ? labels.monthlyTitle : labels.lifetimeTitle,
    detail: status.plan === "monthly" ? labels.monthlyBody : labels.lifetimeBody,
    note:
      status.plan === "monthly" && formattedExpiry
        ? labels.activeUntil.replace("{date}", formattedExpiry)
        : null,
    tone: "paid",
    remaining: null,
    total: null,
  };
}

export function getAccessPaywallGate(snapshot: AccessSnapshot | null): AccessPaywallGate {
  if (!snapshot) {
    return {
      key: "none",
      shouldShow: false,
      total: 3,
    };
  }

  const total = snapshot.contract.free_sessions_total ?? snapshot.status.free_sessions_total ?? 3;
  const remaining = Math.max(
    0,
    snapshot.status.free_sessions_remaining ?? (snapshot.status.can_start_ai_session ? total : 0),
  );
  const shouldShow =
    snapshot.status.plan === "free" &&
    (remaining === 0 || snapshot.status.can_start_ai_session === false);

  return {
    key: `${snapshot.status.plan}:${remaining}:${snapshot.status.can_start_ai_session}`,
    shouldShow,
    total,
  };
}

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
      update((state) => ({
        ...state,
        isLoading: false,
        snapshot,
        error: null,
      }));
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
    update((state) => ({
      ...state,
      isLoading: false,
      snapshot,
      error: null,
    }));
  }

  function requestPaywallPrompt() {
    update((state) => {
      if (!getAccessPaywallGate(state.snapshot).shouldShow) {
        return state;
      }

      return {
        ...state,
        paywallPromptCount: state.paywallPromptCount + 1,
      };
    });
  }

  function reset() {
    set(INITIAL_STATE);
  }

  return {
    subscribe,
    refresh,
    hydrate,
    requestPaywallPrompt,
    reset,
  };
}

export const access = createAccessStore();
