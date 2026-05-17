"""MQTT-Client-Aufbau und Callbacks."""

import ssl
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from lstm_handler import predict_next_value, forecast_future

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_TOPIC, MQTT_CA_FILE, MQTT_CLIENT_ID,
    MQTT_TLS_INSECURE, TEMP_HIGH, TEMP_LOW, log,
)
from validation import parse_and_validate
from http_client import forward_to_backend


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
    # MQTT-Payload enthält keinen Timestamp -> beim Empfang setzen (UTC ISO)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    forward_to_backend(temperature, humidity, timestamp)

    # -------------- LSTM-Vorhersage und Steuerungsentscheidungen -------------------

    # Buffer mit aktuellem Messwert füllen
    predict_next_value(temperature, humidity)

    # 30-Minuten-Forecast erstellen (Folie 5-35 / 5-41)
    forecast = forecast_future(minutes=30, alpha=0.2)

    if forecast is not None:
        # Proaktive Steuerung: prüfen ob Temperatur im Forecast-Zeitraum
        # den Bereich [TEMP_LOW, TEMP_HIGH] verlässt
        max_temp = max(forecast)
        min_temp = min(forecast)

        if max_temp > TEMP_HIGH:
            action = "fan_on"
        elif min_temp < TEMP_LOW:
            action = "heater_on"
        else:
            action = "both_off"

        # Auf Broker publishen (Folie 5-39: Pico erwartet String-Action)
        client.publish("actuator/control", payload=action, qos=1)
        log.info(
            "Forecast 30min: min=%.2f C, max=%.2f C -> Aktion: %s",
            min_temp, max_temp, action,
        )



# --- Client-Setup ---------------------------------------------------------

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
