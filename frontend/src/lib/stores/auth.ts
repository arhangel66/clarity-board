import { createAuth0Client, type Auth0Client, type User } from '@auth0/auth0-spa-js';
import { writable, type Readable } from 'svelte/store';

export type AuthErrorCode = 'auth_failed' | 'session_expired';

export interface AuthState {
  isLoading: boolean;
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  error: AuthErrorCode | null;
}

interface AuthStoreDeps {
  createClient?: typeof createAuth0Client;
  getWindow?: () => Window | undefined;
  isDev?: boolean;
  logger?: Pick<Console, 'error' | 'log' | 'warn'>;
}

interface AuthStore extends Readable<AuthState> {
  init: () => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<string | null>;
  retry: () => Promise<void>;
  clearError: () => void;
}

const INITIAL_STATE: AuthState = {
  isLoading: true,
  isAuthenticated: false,
  user: null,
  token: null,
  error: null
};

function createSignedOutState(error: AuthErrorCode | null = null): AuthState {
  return {
    isLoading: false,
    isAuthenticated: false,
    user: null,
    token: null,
    error
  };
}

function getConfig(currentWindow?: Window) {
  return {
    domain: import.meta.env.VITE_AUTH0_DOMAIN as string | undefined,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID as string | undefined,
    audience: import.meta.env.VITE_AUTH0_AUDIENCE as string | undefined,
    redirectUri:
      (import.meta.env.VITE_AUTH0_REDIRECT_URI as string | undefined) ||
      currentWindow?.location.origin ||
      ''
  };
}

export function createAuthStore(deps: AuthStoreDeps = {}): AuthStore {
  const createClient = deps.createClient ?? createAuth0Client;
  const getWindow = deps.getWindow ?? (() => (typeof window !== 'undefined' ? window : undefined));
  const isDev = deps.isDev ?? import.meta.env.DEV;
  const logger = deps.logger ?? console;
  const { subscribe, set, update } = writable<AuthState>(INITIAL_STATE);

  let auth0Client: Auth0Client | null = null;

  async function ensureClient(): Promise<Auth0Client | null> {
    if (auth0Client) {
      return auth0Client;
    }

    const currentWindow = getWindow();
    const { domain, clientId, audience, redirectUri } = getConfig(currentWindow);
    if (!domain || !clientId) {
      return null;
    }

    auth0Client = await createClient({
      domain,
      clientId,
      cacheLocation: 'localstorage',
      useRefreshTokens: true,
      authorizationParams: {
        redirect_uri: redirectUri,
        audience
      }
    });

    return auth0Client;
  }

  async function handleSessionExpired(error: unknown) {
    logger.warn('[AUTH] Token refresh failed, clearing session:', error);

    try {
      await auth0Client?.logout({ openUrl: false });
    } catch (logoutError) {
      logger.warn('[AUTH] Silent logout failed:', logoutError);
    }

    set(createSignedOutState('session_expired'));
  }

  async function init() {
    const currentWindow = getWindow();
    set(INITIAL_STATE);

    // DEV bypass: ?dev=1 in URL skips Auth0
    if (isDev && currentWindow) {
      const params = new URLSearchParams(currentWindow.location.search);
      if (params.get('dev') === '1') {
        logger.log('[AUTH] Dev bypass enabled');
        set({
          isLoading: false,
          isAuthenticated: true,
          user: { sub: 'dev-user', name: 'Dev User', email: 'dev@localhost' },
          token: 'dev-token',
          error: null
        });
        return;
      }
    }

    try {
      const client = await ensureClient();
      if (!client) {
        set(createSignedOutState());
        return;
      }

      if (currentWindow) {
        const search = currentWindow.location.search;
        if (search.includes('code=') && search.includes('state=')) {
          await client.handleRedirectCallback();
          currentWindow.history.replaceState(
            {},
            currentWindow.document.title,
            currentWindow.location.pathname,
          );
        }
      }

      const isAuthenticated = await client.isAuthenticated();
      let user: User | null = null;
      let token: string | null = null;

      if (isAuthenticated) {
        try {
          user = (await client.getUser()) || null;
          token = await client.getTokenSilently();
        } catch (error) {
          await handleSessionExpired(error);
          return;
        }
      }

      set({
        isLoading: false,
        isAuthenticated,
        user,
        token,
        error: null
      });
    } catch (error) {
      logger.error('[AUTH] Auth initialization failed:', error);
      set(createSignedOutState('auth_failed'));
    }
  }

  async function loginWithGoogle() {
    try {
      update((state) => ({ ...state, error: null }));
      const client = await ensureClient();
      if (!client) {
        set(createSignedOutState('auth_failed'));
        return;
      }

      const { audience } = getConfig(getWindow());
      await client.loginWithRedirect({
        authorizationParams: {
          connection: 'google-oauth2',
          audience
        }
      });
    } catch (error) {
      logger.error('[AUTH] Login redirect failed:', error);
      set(createSignedOutState('auth_failed'));
    }
  }

  function logout() {
    const { redirectUri } = getConfig(getWindow());
    auth0Client?.logout({
      logoutParams: {
        returnTo: redirectUri
      }
    });
  }

  async function refreshToken() {
    if (!auth0Client) {
      return null;
    }

    try {
      const token = await auth0Client.getTokenSilently();
      update((state) => ({ ...state, token, error: null }));
      return token;
    } catch (error) {
      await handleSessionExpired(error);
      return null;
    }
  }

  async function retry() {
    await init();
  }

  function clearError() {
    update((state) => ({ ...state, error: null }));
  }

  return {
    subscribe,
    init,
    loginWithGoogle,
    logout,
    refreshToken,
    retry,
    clearError
  };
}

export const auth = createAuthStore();
