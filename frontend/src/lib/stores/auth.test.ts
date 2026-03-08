import type { Auth0Client } from "@auth0/auth0-spa-js";
import { get } from "svelte/store";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { createAuthStore } from "./auth";

function setAuthEnv() {
  vi.stubEnv("VITE_AUTH0_DOMAIN", "example.auth0.com");
  vi.stubEnv("VITE_AUTH0_CLIENT_ID", "client-id");
  vi.stubEnv("VITE_AUTH0_AUDIENCE", "fact-api");
  vi.stubEnv("VITE_AUTH0_REDIRECT_URI", window.location.origin);
}

function clearAuthEnv() {
  vi.stubEnv("VITE_AUTH0_DOMAIN", "");
  vi.stubEnv("VITE_AUTH0_CLIENT_ID", "");
  vi.stubEnv("VITE_AUTH0_AUDIENCE", "");
  vi.stubEnv("VITE_AUTH0_REDIRECT_URI", "");
}

function createMockClient(overrides: Partial<Auth0Client> = {}): Auth0Client {
  return {
    handleRedirectCallback: vi.fn().mockResolvedValue(undefined),
    isAuthenticated: vi.fn().mockResolvedValue(false),
    getUser: vi.fn().mockResolvedValue(null),
    getTokenSilently: vi.fn().mockResolvedValue("token-1"),
    loginWithRedirect: vi.fn().mockResolvedValue(undefined),
    logout: vi.fn().mockResolvedValue(undefined),
    ...overrides,
  } as unknown as Auth0Client;
}

describe("auth store", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllEnvs();
    window.history.replaceState({}, "", "/");
  });

  it("uses the dev bypass without creating an Auth0 client", async () => {
    const createClient = vi.fn();
    const logger = { log: vi.fn(), warn: vi.fn(), error: vi.fn() };
    const store = createAuthStore({
      createClient,
      getWindow: () => window,
      isDev: true,
      logger,
    });

    window.history.replaceState({}, "", "/?dev=1");
    await store.init();

    expect(createClient).not.toHaveBeenCalled();
    expect(get(store)).toMatchObject({
      isLoading: false,
      isAuthenticated: true,
      token: "dev-token",
      error: null,
    });
  });

  it("falls back to a signed-out state when Auth0 config is missing", async () => {
    clearAuthEnv();

    const createClient = vi.fn();
    const store = createAuthStore({
      createClient,
      getWindow: () => window,
      isDev: false,
      logger: { log: vi.fn(), warn: vi.fn(), error: vi.fn() },
    });

    await store.init();

    expect(createClient).not.toHaveBeenCalled();
    expect(get(store)).toEqual({
      isLoading: false,
      isAuthenticated: false,
      user: null,
      token: null,
      error: null,
    });
  });

  it("handles the Auth0 redirect callback and hydrates the session", async () => {
    setAuthEnv();
    window.history.replaceState({}, "", "/?code=test-code&state=test-state");

    const client = createMockClient({
      isAuthenticated: vi.fn().mockResolvedValue(true),
      getUser: vi.fn().mockResolvedValue({ sub: "user-1", name: "User One" }),
      getTokenSilently: vi.fn().mockResolvedValue("token-1"),
    });
    const createClient = vi.fn().mockResolvedValue(client);
    const store = createAuthStore({
      createClient,
      getWindow: () => window,
      isDev: false,
      logger: { log: vi.fn(), warn: vi.fn(), error: vi.fn() },
    });

    await store.init();

    expect(createClient).toHaveBeenCalledOnce();
    expect(client.handleRedirectCallback).toHaveBeenCalledOnce();
    expect(window.location.search).toBe("");
    expect(get(store)).toMatchObject({
      isLoading: false,
      isAuthenticated: true,
      token: "token-1",
      error: null,
    });
  });

  it("clears the session and exposes a recoverable error when silent refresh fails during init", async () => {
    setAuthEnv();

    const client = createMockClient({
      isAuthenticated: vi.fn().mockResolvedValue(true),
      getUser: vi.fn().mockResolvedValue({ sub: "user-1" }),
      getTokenSilently: vi.fn().mockRejectedValue(new Error("expired")),
      logout: vi.fn().mockResolvedValue(undefined),
    });
    const store = createAuthStore({
      createClient: vi.fn().mockResolvedValue(client),
      getWindow: () => window,
      isDev: false,
      logger: { log: vi.fn(), warn: vi.fn(), error: vi.fn() },
    });

    await store.init();

    expect(client.logout).toHaveBeenCalledWith({ openUrl: false });
    expect(get(store)).toEqual({
      isLoading: false,
      isAuthenticated: false,
      user: null,
      token: null,
      error: "session_expired",
    });
  });

  it("returns null from refreshToken and marks the session expired when silent refresh fails later", async () => {
    setAuthEnv();

    const getTokenSilently = vi
      .fn()
      .mockResolvedValueOnce("token-1")
      .mockRejectedValueOnce(new Error("expired"));
    const client = createMockClient({
      isAuthenticated: vi.fn().mockResolvedValue(true),
      getUser: vi.fn().mockResolvedValue({ sub: "user-1" }),
      getTokenSilently,
      logout: vi.fn().mockResolvedValue(undefined),
    });
    const store = createAuthStore({
      createClient: vi.fn().mockResolvedValue(client),
      getWindow: () => window,
      isDev: false,
      logger: { log: vi.fn(), warn: vi.fn(), error: vi.fn() },
    });

    await store.init();
    const refreshedToken = await store.refreshToken();

    expect(refreshedToken).toBeNull();
    expect(client.logout).toHaveBeenCalledWith({ openUrl: false });
    expect(get(store)).toMatchObject({
      isAuthenticated: false,
      token: null,
      error: "session_expired",
    });
  });
});
