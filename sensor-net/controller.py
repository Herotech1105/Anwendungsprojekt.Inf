"""
controller.py

Reads sensor data from the MQTT broker (over TLS) and forwards it to
the backend webserver via HTTP POST.
"""

from __future__ import annotations

import json
import logging
import os
import signal
import ssl
import sys
import time
import traceback
from datetime import datetime, timezone
from typing import Optional, Tuple

import paho.mqtt.client as mqtt
import requests


# --- Konfiguration --------------------------------------------------------

# MQTT (Subscribe-Seite)
MQTT_HOST = os.getenv("MQTT_HOST", "mqtt.local")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "testuser")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensor/data")
MQTT_CA_FILE = os.getenv("MQTT_CA_FILE")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "controller")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))
# Wenn das Server-Zertifikat keinen passenden SAN/CN fuer den Docker-DNS-Namen
# besitzt, kann die Hostname-Pruefung temporaer abgeschaltet werden.
MQTT_TLS_INSECURE = os.getenv("MQTT_TLS_INSECURE", "true").lower() == "true"

# HTTP (Publish-Seite -> Webserver / Reverse Proxy)
BACKEND_URL = os.getenv(
    "BACKEND_URL", "https://www.lab.local/api/internal/sensordata"
)
API_KEY = os.getenv("API_KEY", "")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "5"))

# Plausibilitaetsbereiche (decken sich mit validateSensorPayload in server.js)
TEMP_MIN = float(os.getenv("TEMP_MIN", "0"))
TEMP_MAX = float(os.getenv("TEMP_MAX", "60"))
HUM_MIN = float(os.getenv("HUM_MIN", "10"))
HUM_MAX = float(os.getenv("HUM_MAX", "70"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


# --- Logging --------------------------------------------------------------

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("controller")


# --- Validierung ----------------------------------------------------------

def parse_and_validate(raw: bytes) -> Optional[Tuple[float, float]]:
    """Dekodiert MQTT-Payload und gibt (temperature, humidity) zurueck.

    None bei ungueltigen oder unplausiblen Daten.
    """
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        log.warning("Verwerfe nicht-JSON-Nachricht: %s", exc)
        return None

    if not isinstance(data, dict):
        log.warning("Verwerfe Payload (kein Objekt): %r", data)
        return None

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (KeyError, TypeError, ValueError):
        log.warning("temperature/humidity fehlt oder ungueltig: %r", data)
        return None

    if not (TEMP_MIN <= temperature <= TEMP_MAX):
        log.warning(
            "Temperatur %.1f ausserhalb [%.1f, %.1f]",
            temperature, TEMP_MIN, TEMP_MAX,
        )
        return None

    if not (HUM_MIN <= humidity <= HUM_MAX):
        log.warning(
            "Luftfeuchtigkeit %.1f ausserhalb [%.1f, %.1f]",
            humidity, HUM_MIN, HUM_MAX,
        )
        return None

    return temperature, humidity


# --- HTTP-Forwarding ------------------------------------------------------

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
            verify=False, # Until nginx Certificate can be verified
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


# --- MQTT-Callbacks (paho-mqtt v2 API) -----------------------------------

def on_connect(client, userdata, flags, reason_code, properties=None):
    # In paho 2.x ist reason_code ein ReasonCode-Objekt; '== 0' funktioniert.
    if reason_code == 0:
        log.info("Verbunden mit MQTT-Broker %s:%d", MQTT_HOST, MQTT_PORT)
        client.subscribe(MQTT_TOPIC, qos=1)
        log.info("Topic abonniert: %r (qos=1)", MQTT_TOPIC)
    else:
        log.error("MQTT-Connect fehlgeschlagen: %s", reason_code)


def on_disconnect(client, userdata, flags, reason_code, properties=None):
    log.warning(
        "MQTT-Verbindung getrennt (rc=%s). Auto-Reconnect...", reason_code
    )


def on_message(client, userdata, msg):
    log.debug("Empfangen auf %s: %s", msg.topic, msg.payload)
    parsed = parse_and_validate(msg.payload)
    if parsed is None:
        return
    temperature, humidity = parsed
    # MQTT-Payload enthaelt keinen Timestamp -> beim Empfang setzen (UTC ISO)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    forward_to_backend(temperature, humidity, timestamp)


# --- Setup & Main ---------------------------------------------------------

def build_client() -> mqtt.Client:
    client = mqtt.Client(
        client_id=MQTT_CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )

    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    # TLS-Kontext: Server-Zertifikat gegen die Projekt-CA verifizieren
    ssl_ctx = ssl.create_default_context(cafile=MQTT_CA_FILE)
    if MQTT_TLS_INSECURE:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        log.warning(
            "TLS-Verifizierung DEAKTIVIERT (MQTT_TLS_INSECURE=true) - "
            "nur fuer Tests verwenden!"
        )
    client.tls_set_context(ssl_ctx)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Eingebauter Reconnect-Backoff (genutzt von loop_forever)
    client.reconnect_delay_set(min_delay=1, max_delay=60)
    return client


def main() -> None:
    if not API_KEY:
        log.error(
            "API_KEY env-Variable ist leer - Backend wird POSTs ablehnen"
        )
    if not MQTT_PASSWORD:
        log.warning("MQTT_PASSWORD env-Variable ist leer")
    if not os.path.isfile(MQTT_CA_FILE):
        log.error("CA-Datei nicht gefunden: %s", MQTT_CA_FILE)

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
