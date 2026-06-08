"""Keycloak Client Credentials Flow: fetch, cache, and verify tokens."""

import base64
import json
import time

import requests

from config import (
    KC_TOKEN_URL, KC_CLIENT_ID, KC_CLIENT_SECRET,
    KC_REQUIRED_ROLE, HTTP_TIMEOUT, log, CA_CERT_FILE
)

_cached_token: str | None = None
_token_expires_at: float = 0.0


def _decode_jwt_payload(token: str) -> dict:
    """Base64-decode the JWT payload (without signature verification)."""
    payload_b64 = token.split(".")[1]
    # JWT uses Base64URL encoding — add padding
    padded = payload_b64 + "=" * (-len(payload_b64) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))


def request_token() -> str:
    """Fetch a new access token via Client Credentials Grant."""
    data = {
        "grant_type": "client_credentials",
        "client_id": KC_CLIENT_ID,
        "client_secret": KC_CLIENT_SECRET,
    }
    resp = requests.post(
        KC_TOKEN_URL,
        data=data,
        timeout=HTTP_TIMEOUT,
        verify=CA_CERT_FILE,
    )
    resp.raise_for_status()
    body = resp.json()

    global _cached_token, _token_expires_at
    _cached_token = body["access_token"]
    # 30 s buffer so the token does not expire during a request
    _token_expires_at = time.time() + body.get("expires_in", 300) - 30

    log.info("Keycloak access token obtained (expires_in=%ss)", body.get("expires_in"))
    return _cached_token


def get_token() -> str:
    """Return a valid access token (cached or freshly fetched)."""
    if _cached_token and time.time() < _token_expires_at:
        return _cached_token
    return request_token()


def verify_role() -> None:
    """Verify that the current token contains the required role.

    Raises RuntimeError if the role is missing.
    """
    token = get_token()
    payload = _decode_jwt_payload(token)
    roles = payload.get("realm_access", {}).get("roles", [])
    if KC_REQUIRED_ROLE not in roles:
        raise RuntimeError(
            f"Keycloak token does not contain role '{KC_REQUIRED_ROLE}'. "
            f"Available roles: {roles}"
        )
    log.info("Role '%s' verified in token", KC_REQUIRED_ROLE)


def auth_header() -> dict:
    """Return the Authorization header for HTTP requests."""
    return {"Authorization": f"Bearer {get_token()}"}
