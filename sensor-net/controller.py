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
    MQTT_KEEPALIVE, API_KEY, BACKEND_URL, HTTP_TIMEOUT, log,
)
from mqtt_handler import build_client
from lstm_handler import buffer


# ---------------------------------------------------------------------------
# Warmstart: Buffer mit letzten Temperaturwerten aus der Datenbank füllen,
# damit nach einem Neustart sofort Forecasts möglich sind
# ---------------------------------------------------------------------------

def warmstart() -> None:
    """Laedt die aktuellsten Temperaturwerte vom Backend in den Buffer."""
    url = BACKEND_URL.rsplit("/", 1)[0] + "/sensordata/latest"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    try:
        resp = requests.get(
            url, headers=headers, timeout=HTTP_TIMEOUT, verify=False,
        )
    except requests.RequestException as exc:
        log.warning("Warmstart fehlgeschlagen (Netzwerk): %s", exc)
        return

    if resp.status_code != 200:
        log.warning(
            "Warmstart: Backend antwortete mit Status %s", resp.status_code,
        )
        return

    try:
        data = resp.json()
        # Backend liefert Liste von {temperature, humidity, ...}
        records = data if isinstance(data, list) else data.get("data", [])
        for record in records:
            temp = float(record["temperature"])
            hum = float(record["humidity"])
            buffer.append([temp, hum])
        log.info(
            "Warmstart: %d Werte aus Backend in Buffer geladen", len(records),
        )
    except (KeyError, TypeError, ValueError) as exc:
        log.warning("Warmstart: Antwort konnte nicht verarbeitet werden: %s", exc)


def main() -> None:
    if not API_KEY:
        log.error(
            "API_KEY env-Variable ist leer - Backend wird POSTs ablehnen"
        )
    if not MQTT_PASSWORD:
        log.warning("MQTT_PASSWORD env-Variable ist leer")
    if not os.path.isfile(os.getenv("MQTT_CA_FILE", "")):
        log.error("CA-Datei nicht gefunden: %s", os.getenv("MQTT_CA_FILE"))

    # Warmstart: letzte Messwerte aus DB in den LSTM-Buffer laden
    warmstart()

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
