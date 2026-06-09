"""
Test 3: Backend lehnt Requests ohne Authentifizierung ab
=========================================================
Request (ohne Token/API-Key) -> nginx -> server.js -> 401 Rejected

Sends requests without proper authentication and verifies
the backend rejects them.
"""

from datetime import datetime, timezone

import requests

from config import (
    SENSORDATA_URL, DASHBOARD_SENSORDATA_URL,
    HTTP_TIMEOUT, SSL_VERIFY,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL


def run():
    print_header("TEST 3: Unauthenticated Requests Rejected")

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {"temperature": 20.0, "humidity": 50.0, "timestamp": ts}

    # -- 3a: POST sensordata without any headers --
    try:
        resp = requests.post(
            SENSORDATA_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code == 401:
            record(PASS, "POST /api/internal/sensordata without auth -> 401")
        else:
            record(FAIL, "POST /api/internal/sensordata without auth -> 401",
                   f"Expected 401, got {resp.status_code}")
    except requests.RequestException as exc:
        record(FAIL, "POST /api/internal/sensordata without auth", str(exc))

    # -- 3b: POST sensordata with wrong API key --
    try:
        resp = requests.post(
            SENSORDATA_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": "wrong-key-12345",
            },
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code == 401:
            record(PASS, "POST with wrong API key -> 401")
        else:
            record(FAIL, "POST with wrong API key -> 401",
                   f"Expected 401, got {resp.status_code}")
    except requests.RequestException as exc:
        record(FAIL, "POST with wrong API key", str(exc))

    # -- 3c: GET dashboard sensordata without Bearer token --
    try:
        resp = requests.get(
            DASHBOARD_SENSORDATA_URL,
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code == 401:
            record(PASS, "GET /api/sensordata without Bearer -> 401")
        else:
            record(FAIL, "GET /api/sensordata without Bearer -> 401",
                   f"Expected 401, got {resp.status_code}")
    except requests.RequestException as exc:
        record(FAIL, "GET /api/sensordata without Bearer", str(exc))

    # -- 3d: GET dashboard sensordata with invalid Bearer token --
    try:
        resp = requests.get(
            DASHBOARD_SENSORDATA_URL,
            headers={"Authorization": "Bearer this.is.not.a.valid.jwt"},
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code in (401, 403):
            record(PASS, f"GET with invalid Bearer token -> {resp.status_code}")
        else:
            record(FAIL, "GET with invalid Bearer token -> 401/403",
                   f"Expected 401/403, got {resp.status_code}")
    except requests.RequestException as exc:
        record(FAIL, "GET with invalid Bearer token", str(exc))

    exit_with_result()


if __name__ == "__main__":
    run()
