"""HTTP forwarding of sensor data to the backend."""

import requests

from config import BACKEND_URL, API_KEY, HTTP_TIMEOUT, CA_CERT_FILE, log
from keycloak_auth import auth_header


def _build_headers() -> dict:
    """Build HTTP headers with API key and Bearer token."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    headers.update(auth_header())
    return headers


def forward_to_backend(
    temperature: float, humidity: float, timestamp: str
) -> None:
    """POST sensor data to the web server. Does not raise exceptions."""
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp,
    }
    try:
        resp = requests.post(
            BACKEND_URL,
            json=payload,
            headers=_build_headers(),
            timeout=HTTP_TIMEOUT,
            verify=CA_CERT_FILE,
        )
    except requests.RequestException as exc:
        log.error("HTTP POST to backend failed: %s", exc)
        return

    if 200 <= resp.status_code < 300:
        log.info(
            "Forwarded to backend: %s (status %s)",
            payload, resp.status_code,
        )
    else:
        log.warning(
            "Backend rejected payload: status=%s body=%s",
            resp.status_code, resp.text[:200],
        )

