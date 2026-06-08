"""
controller.py

Reads sensor data from the MQTT broker (via TLS) and forwards it
to the backend web server via HTTP POST.
Contains forecast logic (30 min) via LSTM model and
publishes control messages on 'actuator/control'.
"""

import os
import signal
import ssl
import sys
import time
import traceback

import requests

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_KEEPALIVE, API_KEY, BACKEND_URL, log,
)
from keycloak_auth import verify_role
from mqtt_handler import build_client



def main() -> None:
    if not API_KEY:
        log.error(
            "API_KEY env variable is empty - backend will reject POSTs"
        )
    if not MQTT_PASSWORD:
        log.warning("MQTT_PASSWORD env variable is empty")
    if not os.path.isfile(os.getenv("MQTT_CA_FILE", "")):
        log.error("CA file not found: %s", os.getenv("MQTT_CA_FILE"))

    # Keycloak AuthN/AuthZ: retrieve token and verify role
    try:
        verify_role()
    except Exception as exc:
        log.error("Keycloak authentication failed: %s", exc)
        sys.exit(1)


    client = build_client()

    # Graceful shutdown on SIGTERM (e.g. 'docker stop')
    def _shutdown(signum, _frame):
        log.info("Signal %s received, disconnecting...", signum)
        try:
            client.disconnect()
        finally:
            sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    log.info(
        "Starting controller -> MQTT %s:%d as '%s', backend %s",
        MQTT_HOST, MQTT_PORT, MQTT_USER, BACKEND_URL,
    )

    # loop_forever() handles reconnects internally; outer loop catches
    # cases where the initial connect fails (e.g. broker unreachable,
    # certificate error).
    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=MQTT_KEEPALIVE)
            client.loop_forever(retry_first_connection=True)
        except (OSError, ssl.SSLError) as exc:
            log.error("Detailed Connection Error:")
            traceback.print_exc()
            time.sleep(5)


if __name__ == "__main__":
    main()
