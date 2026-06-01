"""Keycloak Client-Credentials-Flow: Token holen, cachen, Rolle pruefen."""

import base64
import json
import time

import requests

from config import (
    KC_TOKEN_URL, KC_CLIENT_ID, KC_CLIENT_SECRET,
    KC_REQUIRED_ROLE, HTTP_TIMEOUT, log, KEYCLOAK_CERT
)

_cached_token: str | None = None
_token_expires_at: float = 0.0


def _decode_jwt_payload(token: str) -> dict:
    """Base64-Decode des JWT-Payloads (ohne Signaturpruefung)."""
    payload_b64 = token.split(".")[1]
    # JWT nutzt Base64URL — Padding ergaenzen
    padded = payload_b64 + "=" * (-len(payload_b64) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))


def request_token() -> str:
    """Holt ein neues Access-Token via Client Credentials Grant."""
    data = {
        "grant_type": "client_credentials",
        "client_id": KC_CLIENT_ID,
        "client_secret": KC_CLIENT_SECRET,
    }
    resp = requests.post(
        KC_TOKEN_URL,
        data=data,
        timeout=HTTP_TIMEOUT,
        verify=False,
    )
    resp.raise_for_status()
    body = resp.json()

    global _cached_token, _token_expires_at
    _cached_token = body["access_token"]
    # 30 s Puffer, damit das Token nicht waehrend eines Requests ablaeuft
    _token_expires_at = time.time() + body.get("expires_in", 300) - 30

    log.info("Keycloak Access-Token erhalten (expires_in=%ss)", body.get("expires_in"))
    return _cached_token


def get_token() -> str:
    """Gibt ein gueltiges Access-Token zurueck (cached oder neu geholt)."""
    if _cached_token and time.time() < _token_expires_at:
        return _cached_token
    return request_token()


def verify_role() -> None:
    """Prueft ob das aktuelle Token die benoetigte Rolle enthaelt.

    Raises RuntimeError wenn die Rolle fehlt.
    """
    token = get_token()
    payload = _decode_jwt_payload(token)
    roles = payload.get("realm_access", {}).get("roles", [])
    if KC_REQUIRED_ROLE not in roles:
        raise RuntimeError(
            f"Keycloak-Token enthaelt Rolle '{KC_REQUIRED_ROLE}' nicht. "
            f"Vorhandene Rollen: {roles}"
        )
    log.info("Rolle '%s' im Token verifiziert", KC_REQUIRED_ROLE)


def auth_header() -> dict:
    """Liefert den Authorization-Header fuer HTTP-Requests."""
    return {"Authorization": f"Bearer {get_token()}"}
