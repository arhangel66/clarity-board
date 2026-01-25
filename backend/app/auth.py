"""Auth helpers for verifying Auth0 JWTs."""

from __future__ import annotations

import json
import os
import time
import urllib.request

from jose import jwt


class AuthError(Exception):
    """Raised when authentication fails."""


_ALGORITHMS = ["RS256"]
_JWKS_CACHE: dict[str, object] = {"fetched_at": 0.0, "keys": []}
_JWKS_TTL_SECONDS = 60 * 60


def _get_settings() -> tuple[str, str, str]:
    domain = os.getenv("AUTH0_DOMAIN", "").strip()
    audience = os.getenv("AUTH0_AUDIENCE", "").strip()
    issuer = os.getenv("AUTH0_ISSUER", "").strip()
    if not domain or not audience:
        raise AuthError("Auth configuration missing")
    if not issuer:
        issuer = f"https://{domain}/"
    return domain, audience, issuer


def _fetch_jwks(domain: str) -> list[dict]:
    url = f"https://{domain}/.well-known/jwks.json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("keys", [])


def _get_jwks(domain: str) -> list[dict]:
    now = time.time()
    fetched_at = float(_JWKS_CACHE.get("fetched_at", 0.0))
    if _JWKS_CACHE.get("keys") and now - fetched_at < _JWKS_TTL_SECONDS:
        return _JWKS_CACHE["keys"]  # type: ignore[return-value]
    keys = _fetch_jwks(domain)
    _JWKS_CACHE["keys"] = keys
    _JWKS_CACHE["fetched_at"] = now
    return keys


def verify_token(token: str) -> dict:
    if not token:
        raise AuthError("Missing token")
    token = token.replace("Bearer ", "").strip()

    # DEV bypass: accept "dev-token" when DEV_AUTH_BYPASS=true
    if os.getenv("DEV_AUTH_BYPASS", "").lower() == "true" and token == "dev-token":
        return {"sub": "dev-user"}

    domain, audience, issuer = _get_settings()
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        raise AuthError("Invalid token header")

    jwks = _get_jwks(domain)
    key = next((k for k in jwks if k.get("kid") == kid), None)
    if not key:
        raise AuthError("Signing key not found")

    try:
        return jwt.decode(token, key, algorithms=_ALGORITHMS, audience=audience, issuer=issuer)
    except Exception as exc:  # pragma: no cover - best effort error reporting
        raise AuthError("Token verification failed") from exc


def get_user_id(token: str) -> str:
    payload = verify_token(token)
    sub = payload.get("sub")
    if not sub:
        raise AuthError("Token missing subject")
    return str(sub)
