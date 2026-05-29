"""
controller.py

Liest Sensordaten vom MQTT-Broker (ueber TLS) und leitet sie
per HTTP POST an den Backend-Webserver weiter.
Enthaelt Forecast-Logik (30 Min) via LSTM-Modell und
publiziert Steuerungsnachrichten auf 'actuator/control'.
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
            "API_KEY env-Variable ist leer - Backend wird POSTs ablehnen"
        )
    if not MQTT_PASSWORD:
        log.warning("MQTT_PASSWORD env-Variable ist leer")
    if not os.path.isfile(os.getenv("MQTT_CA_FILE", "")):
        log.error("CA-Datei nicht gefunden: %s", os.getenv("MQTT_CA_FILE"))

    # Keycloak AuthN/AuthZ: Token holen und Rolle pruefen
    try:
        verify_role()
    except Exception as exc:
        log.error("Keycloak-Authentifizierung fehlgeschlagen: %s", exc)
        sys.exit(1)


    client = build_client()

    # Sauberes Beenden bei SIGTERM (z.B. 'docker stop')
    def _shutdown(signum, _frame):
        log.info("Signal %s erhalten, trenne Verbindung...", signum)
        try:
            client.disconnect()
        finally:
            sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    log.info(
        "Starte Controller -> MQTT %s:%d als '%s', Backend %s",
        MQTT_HOST, MQTT_PORT, MQTT_USER, BACKEND_URL,
    )

    # loop_forever() handhabt Reconnects intern; aeusserer Loop faengt
    # Faelle ab, in denen schon der erste Connect scheitert (z.B. Broker
    # nicht erreichbar, Zertifikatsfehler).
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
