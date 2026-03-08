import { get } from "svelte/store";
import { describe, expect, it, vi } from "vitest";

import type { AccessSnapshot } from "../types";
import { createAccessStore } from "./access";

const starterSnapshot: AccessSnapshot = {
  contract: {
    status_endpoint: "/api/access",
    pricing_unit: "sessions",
    free_sessions_total: 3,
    session_consumption_trigger: "first_ai_message_on_blank_session",
    blank_session_consumes: false,
    reopen_existing_session_consumes: false,
    deleting_session_restores_quota: false,
    supported_plans: ["free", "monthly", "lifetime"],
    monthly_requires_expires_at: true,
    lifetime_never_expires: true,
  },
  status: {
    plan: "free",
    plan_expires_at: null,
    plan_active: true,
    free_sessions_total: 3,
    free_sessions_used: 1,
    free_sessions_remaining: 2,
    can_start_ai_session: true,
    metering_state: "tracked",
  },
};

describe("access store", () => {
  it("loads the access snapshot with the bearer token", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue(starterSnapshot),
    });
    const store = createAccessStore(fetchMock as unknown as typeof fetch);

    const snapshot = await store.refresh("token-123");

    expect(snapshot).toEqual(starterSnapshot);
    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/api/access", {
      headers: {
        Authorization: "Bearer token-123",
      },
    });
    expect(get(store)).toEqual({
      isLoading: false,
      snapshot: starterSnapshot,
      error: null,
    });
  });

  it("hydrates the snapshot and resets back to the initial state", () => {
    const store = createAccessStore(vi.fn() as unknown as typeof fetch);

    store.hydrate(starterSnapshot);
    expect(get(store).snapshot).toEqual(starterSnapshot);

    store.reset();
    expect(get(store)).toEqual({
      isLoading: false,
      snapshot: null,
      error: null,
    });
  });

  it("preserves the previous snapshot when refresh fails", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: vi.fn().mockResolvedValue(starterSnapshot),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 503,
      });
    const store = createAccessStore(fetchMock as unknown as typeof fetch);

    await store.refresh("token-123");
    const snapshot = await store.refresh("token-123");

    expect(snapshot).toBeNull();
    expect(get(store)).toEqual({
      isLoading: false,
      snapshot: starterSnapshot,
      error: "Failed to load access status: 503",
    });
  });
});
