"""HTTP-Weiterleitung der Sensordaten an das Backend."""

import requests
from tensorflow.python.saved_model.tag_constants import TRAINING

from config import BACKEND_URL, API_KEY, HTTP_TIMEOUT, log, TRAININGURL


def forward_to_backend(
    temperature: float, humidity: float, timestamp: str
) -> None:
    """POSTet die Sensordaten an den Webserver. Wirft keine Exception."""
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp,
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    try:
        resp = requests.post(
            BACKEND_URL,
            json=payload,
            headers=headers,
            timeout=HTTP_TIMEOUT,
            verify=False,  # Until nginx Certificate can be verified
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


def forward_training_data_to_backend(
    temperature: float, humidity: float, timestamp: str, heater: bool, fan: bool
) -> None:
    """POSTet die Sensordaten an den Webserver. Wirft keine Exception."""
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp,
        "heater": heater,
        "fan": fan,
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    try:
        resp = requests.post(
            TRAININGURL,
            json=payload,
            headers=headers,
            timeout=HTTP_TIMEOUT,
            verify=False,  # Until nginx Certificate can be verified
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
