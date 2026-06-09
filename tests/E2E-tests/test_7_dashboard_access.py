"""
Test 7: Dashboard-Zugriff auf Sensordaten (Rollenbasiert)
==========================================================
User -> Keycloak (Login + Token) -> nginx -> server.js (Rolle pruefen) -> MariaDB

Tests access to the dashboard API endpoint with three different users:
  7a - Admin user       (admin-user + dashboard-user)  -> 200 OK
  7b - Normal user      (dashboard-user)               -> 200 OK
  7c - User without role (no dashboard-user)            -> 403 Forbidden

PREREQUISITE: 'directAccessGrantsEnabled' must be set to true on the
              'dashboard-client' in iot-realm.json for these tests to work.
              A user without roles (KC_NOROLE_USER) must exist in Keycloak.
"""

import requests

from config import (
    KC_TOKEN_URL, KC_DASHBOARD_CLIENT_ID,
    KC_ADMIN_USER, KC_ADMIN_PASSWORD,
    KC_NORMAL_USER, KC_NORMAL_PASSWORD,
    KC_NOROLE_USER, KC_NOROLE_PASSWORD,
    DASHBOARD_SENSORDATA_URL, ADMIN_EXPORT_URL,
    CA_CERT_FILE, HTTP_TIMEOUT, SSL_VERIFY,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL, SKIP


def _get_user_token(username: str, password: str) -> str | None:
    """Get a token for a user via Resource Owner Password Grant."""
    try:
        resp = requests.post(
            KC_TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": KC_DASHBOARD_CLIENT_ID,
                "username": username,
                "password": password,
            },
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        return None
    except requests.RequestException:
        return None


def run():
    print_header("TEST 7: Dashboard Access (Role-Based)")

    # ===== 7a: Admin user =====
    print("  --- 7a: Admin user ---\n")

    admin_token = _get_user_token(KC_ADMIN_USER, KC_ADMIN_PASSWORD)
    if admin_token is None:
        record(FAIL, f"Login as '{KC_ADMIN_USER}'",
               "Could not get token. Is directAccessGrantsEnabled=true?")
    else:
        record(PASS, f"Login as '{KC_ADMIN_USER}'")

        # Admin accesses dashboard sensordata
        try:
            resp = requests.get(
                DASHBOARD_SENSORDATA_URL,
                headers={"Authorization": f"Bearer {admin_token}"},
                timeout=HTTP_TIMEOUT,
                verify=SSL_VERIFY,
            )
            if resp.status_code == 200:
                record(PASS, "Admin GET /api/sensordata -> 200 OK")
            else:
                record(FAIL, "Admin GET /api/sensordata -> 200 OK",
                       f"Got {resp.status_code}: {resp.text[:150]}")
        except requests.RequestException as exc:
            record(FAIL, "Admin GET /api/sensordata", str(exc))

        # Admin accesses export endpoint (requires admin-user role)
        try:
            resp = requests.get(
                ADMIN_EXPORT_URL,
                headers={"Authorization": f"Bearer {admin_token}"},
                timeout=HTTP_TIMEOUT,
                verify=SSL_VERIFY,
            )
            if resp.status_code == 200:
                record(PASS, "Admin GET /api/admin/export -> 200 OK",
                       f"Content-Type: {resp.headers.get('Content-Type', '?')}")
            else:
                record(FAIL, "Admin GET /api/admin/export -> 200 OK",
                       f"Got {resp.status_code}: {resp.text[:150]}")
        except requests.RequestException as exc:
            record(FAIL, "Admin GET /api/admin/export", str(exc))

    # ===== 7b: Normal user =====
    print("\n  --- 7b: Normal user ---\n")

    user_token = _get_user_token(KC_NORMAL_USER, KC_NORMAL_PASSWORD)
    if user_token is None:
        record(FAIL, f"Login as '{KC_NORMAL_USER}'",
               "Could not get token. Is directAccessGrantsEnabled=true?")
    else:
        record(PASS, f"Login as '{KC_NORMAL_USER}'")

        # Normal user accesses dashboard sensordata
        try:
            resp = requests.get(
                DASHBOARD_SENSORDATA_URL,
                headers={"Authorization": f"Bearer {user_token}"},
                timeout=HTTP_TIMEOUT,
                verify=SSL_VERIFY,
            )
            if resp.status_code == 200:
                record(PASS, "User GET /api/sensordata -> 200 OK")
            else:
                record(FAIL, "User GET /api/sensordata -> 200 OK",
                       f"Got {resp.status_code}: {resp.text[:150]}")
        except requests.RequestException as exc:
            record(FAIL, "User GET /api/sensordata", str(exc))

        # Normal user should NOT access admin export (no admin-user role)
        try:
            resp = requests.get(
                ADMIN_EXPORT_URL,
                headers={"Authorization": f"Bearer {user_token}"},
                timeout=HTTP_TIMEOUT,
                verify=SSL_VERIFY,
            )
            if resp.status_code == 403:
                record(PASS, "User GET /api/admin/export -> 403 Forbidden")
            else:
                record(FAIL, "User GET /api/admin/export -> 403 Forbidden",
                       f"Expected 403, got {resp.status_code}")
        except requests.RequestException as exc:
            record(FAIL, "User GET /api/admin/export", str(exc))

    # ===== 7c: User without role =====
    print("\n  --- 7c: User without 'dashboard-user' role ---\n")

    norole_token = _get_user_token(KC_NOROLE_USER, KC_NOROLE_PASSWORD)
    if norole_token is None:
        record(SKIP, f"Login as '{KC_NOROLE_USER}'",
               f"User '{KC_NOROLE_USER}' does not exist or password wrong. "
               "Create this user in Keycloak WITHOUT any roles.")
    else:
        record(PASS, f"Login as '{KC_NOROLE_USER}' (no roles)")

        # User without role should be rejected
        try:
            resp = requests.get(
                DASHBOARD_SENSORDATA_URL,
                headers={"Authorization": f"Bearer {norole_token}"},
                timeout=HTTP_TIMEOUT,
                verify=SSL_VERIFY,
            )
            if resp.status_code == 403:
                record(PASS, "No-role user GET /api/sensordata -> 403 Forbidden",
                       "AuthN passed but AuthZ denied (correct behavior)")
            else:
                record(FAIL, "No-role user GET /api/sensordata -> 403 Forbidden",
                       f"Expected 403, got {resp.status_code}")
        except requests.RequestException as exc:
            record(FAIL, "No-role user GET /api/sensordata", str(exc))

    exit_with_result()


if __name__ == "__main__":
    run()
