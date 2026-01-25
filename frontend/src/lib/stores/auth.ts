import { createAuth0Client, type Auth0Client, type User } from '@auth0/auth0-spa-js';
import { writable } from 'svelte/store';

interface AuthState {
  isLoading: boolean;
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  error: string | null;
}

const { subscribe, set, update } = writable<AuthState>({
  isLoading: true,
  isAuthenticated: false,
  user: null,
  token: null,
  error: null
});

let auth0Client: Auth0Client | null = null;

function getConfig() {
  return {
    domain: import.meta.env.VITE_AUTH0_DOMAIN as string | undefined,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID as string | undefined,
    audience: import.meta.env.VITE_AUTH0_AUDIENCE as string | undefined,
    redirectUri: (import.meta.env.VITE_AUTH0_REDIRECT_URI as string | undefined) ||
      (typeof window !== 'undefined' ? window.location.origin : '')
  };
}

async function init() {
  const { domain, clientId, audience, redirectUri } = getConfig();
  if (!domain || !clientId) {
    set({
      isLoading: false,
      isAuthenticated: false,
      user: null,
      token: null,
      error: 'Auth0 config missing'
    });
    return;
  }

  auth0Client = await createAuth0Client({
    domain,
    clientId,
    authorizationParams: {
      redirect_uri: redirectUri,
      audience
    }
  });

  if (typeof window !== 'undefined') {
    const search = window.location.search;
    if (search.includes('code=') && search.includes('state=')) {
      await auth0Client.handleRedirectCallback();
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }

  const isAuthenticated = await auth0Client.isAuthenticated();
  let user: User | null = null;
  let token: string | null = null;

  if (isAuthenticated) {
    user = await auth0Client.getUser();
    token = await auth0Client.getTokenSilently();
  }

  set({
    isLoading: false,
    isAuthenticated,
    user,
    token,
    error: null
  });
}

async function loginWithGoogle() {
  const { audience } = getConfig();
  await auth0Client?.loginWithRedirect({
    authorizationParams: {
      connection: 'google-oauth2',
      audience
    }
  });
}

function logout() {
  const { redirectUri } = getConfig();
  auth0Client?.logout({
    logoutParams: {
      returnTo: redirectUri
    }
  });
}

async function refreshToken() {
  if (!auth0Client) return null;
  const token = await auth0Client.getTokenSilently();
  update((state) => ({ ...state, token }));
  return token;
}

export const auth = {
  subscribe,
  init,
  loginWithGoogle,
  logout,
  refreshToken
};
