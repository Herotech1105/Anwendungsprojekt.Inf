"""HTTP-Weiterleitung der Sensordaten an das Backend."""

import requests

from config import BACKEND_URL, API_KEY, HTTP_TIMEOUT, CA_CERT_PATH, log, TRAININGURL
from keycloak_auth import auth_header


def _build_headers() -> dict:
    """Erstellt die HTTP-Header mit API-Key und Bearer-Token."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    headers.update(auth_header())
    return headers


def forward_to_backend(
    temperature: float, humidity: float, timestamp: str
) -> None:
    """POSTet die Sensordaten an den Webserver. Wirft keine Exception."""
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
            timeout=HTTP_TIMEOUT
        )
    except requests.RequestException as exc:
        log.error("HTTP-POST an Backend fehlgeschlagen: %s", exc)
        return

    if 200 <= resp.status_code < 300:
        log.info(
            "An Backend weitergeleitet: %s (status %s)",
            payload, resp.status_code,
        )
    else:
        log.warning(
            "Backend hat Payload abgelehnt: status=%s body=%s",
            resp.status_code, resp.text[:200],
        )

