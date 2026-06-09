"""
Test 2: Keycloak Token-Flow
============================
controller.py -> Keycloak (Token holen) -> nginx -> server.js (Token validieren)

Gets a token via Client Credentials Flow, verifies the JWT contains
the required role, and confirms the backend accepts it.
"""

import base64
import json
import time

import requests

from config import (
    KC_TOKEN_URL, KC_CONTROLLER_CLIENT_ID, KC_CONTROLLER_CLIENT_SECRET,
    KC_REQUIRED_ROLE, CA_CERT_FILE, HTTP_TIMEOUT,
    DASHBOARD_SENSORDATA_URL, KC_DASHBOARD_CLIENT_ID,
    KC_NORMAL_USER, KC_NORMAL_PASSWORD, SSL_VERIFY,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL


def run():
    print_header("TEST 2: Keycloak Token Flow (Client Credentials)")

    token = None

    # -- Step 1: Request token from Keycloak --
    try:
        resp = requests.post(
            KC_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": KC_CONTROLLER_CLIENT_ID,
                "client_secret": KC_CONTROLLER_CLIENT_SECRET,
            },
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )

        if resp.status_code == 200:
            body = resp.json()
            token = body["access_token"]
            record(PASS, "Token retrieved from Keycloak",
                   f"expires_in={body.get('expires_in')}s")
        else:
            record(FAIL, "Token retrieved from Keycloak",
                   f"Status {resp.status_code}: {resp.text[:150]}")
            exit_with_result()
    except requests.RequestException as exc:
        record(FAIL, "Token retrieved from Keycloak", str(exc))
        exit_with_result()

    # -- Step 2: Verify JWT structure (3 parts) --
    parts = token.split(".")
    if len(parts) == 3:
        record(PASS, "Token is valid JWT format (header.payload.signature)")
    else:
        record(FAIL, "Token is valid JWT format", f"Got {len(parts)} parts")
        exit_with_result()

    # -- Step 3: Decode payload and check role --
    try:
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))

        roles = payload.get("realm_access", {}).get("roles", [])
        if KC_REQUIRED_ROLE in roles:
            record(PASS, f"Role '{KC_REQUIRED_ROLE}' present in token",
                   f"All roles: {roles}")
        else:
            record(FAIL, f"Role '{KC_REQUIRED_ROLE}' present in token",
                   f"Available roles: {roles}")
    except Exception as exc:
        record(FAIL, "JWT payload decoded", str(exc))
        exit_with_result()

    # -- Step 4: Check token is not expired --
    exp = payload.get("exp", 0)
    now = time.time()
    if exp > now:
        record(PASS, "Token not expired", f"{int(exp - now)}s remaining")
    else:
        record(FAIL, "Token not expired", f"Expired {int(now - exp)}s ago")

    # -- Step 5: Backend validates a Bearer token (via dashboard endpoint) --
    # Get a dashboard-user token to test actual JWT validation in server.js
    try:
        user_resp = requests.post(
            KC_TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": KC_DASHBOARD_CLIENT_ID,
                "username": KC_NORMAL_USER,
                "password": KC_NORMAL_PASSWORD,
            },
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if user_resp.status_code != 200:
            record(FAIL, "Get dashboard-user token for validation test",
                   f"Status {user_resp.status_code}")
            exit_with_result()

        user_token = user_resp.json()["access_token"]

        resp = requests.get(
            DASHBOARD_SENSORDATA_URL,
            headers={"Authorization": f"Bearer {user_token}"},
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code == 200:
            record(PASS, "Backend validates Bearer token on /api/sensordata",
                   f"Status {resp.status_code}")
        else:
            record(FAIL, "Backend validates Bearer token on /api/sensordata",
                   f"Status {resp.status_code}: {resp.text[:150]}")
    except requests.RequestException as exc:
        record(FAIL, "Backend validates Bearer token", str(exc))

    exit_with_result()


if __name__ == "__main__":
    run()
