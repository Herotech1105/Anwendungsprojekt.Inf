"""MQTT client setup and callbacks."""
import json
import ssl
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from lstm_handler import predict_next_value

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_TOPIC, CA_CERT_FILE, MQTT_CLIENT_ID,
    MQTT_TLS_INSECURE, log, HUM_HIGH, HUM_LOW, TEMP_HIGH, TEMP_LOW,
)
from validation import parse_and_validate
from https_client import forward_to_backend


# --- MQTT callbacks (paho-mqtt v2 API) ------------------------------------

def on_connect(client, userdata, flags, reason_code, properties=None):
    # In paho 2.x reason_code is a ReasonCode object; '== 0' still works.
    if reason_code == 0:
        log.info("Connected to MQTT broker %s:%d", MQTT_HOST, MQTT_PORT)
        client.subscribe(MQTT_TOPIC, qos=1)
        log.info("Subscribed to topic: %r (qos=1)", MQTT_TOPIC)
    else:
        log.error("MQTT connect failed: %s", reason_code)


def on_disconnect(client, userdata, flags, reason_code, properties=None):
    log.warning(
        "MQTT connection lost (rc=%s). Auto-reconnecting...", reason_code
    )


def on_message(client, userdata, msg):
    log.debug("Received on %s: %s", msg.topic, msg.payload)
    parsed = parse_and_validate(msg.payload)
    if parsed is None:
        return
    temperature, humidity = parsed
    # MQTT payload contains no timestamp -> set on receipt (UTC ISO)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    forward_to_backend(temperature, humidity, timestamp)

    # -------------- LSTM prediction and control decisions ---------------------

    # Get prediction
    try:
        prediction = predict_next_value(temperature, humidity)
        if prediction is None:
            return
        predicted_temp = prediction["predicted_temp"]
        predicted_hum = prediction["predicted_hum"]
        topic = "actuator/control"

        temp_state = _determine_temp_state(predicted_temp)
        hum_state = _determine_hum_state(predicted_hum)
        action = _resolve_action(temp_state, hum_state)

        # Publish message
        result = client.publish(topic, payload=action, qos=1)

        # Log after publishing
        if result.rc == 0:
            log.info(
                f"Published {action} on {topic}\nTemp: {predicted_temp}\nHumidity: {predicted_hum}"
            )
        else:
            log.error("Failed to publish to MQTT broker. Return code: %s", result.rc)
    except Exception as e:
        log.error("Failed to publish to MQTT broker:", e)


def _determine_temp_state(avg_temp):
    """Determine temperature state based on forecast average."""
    if avg_temp > TEMP_HIGH:
        return "TOO_HIGH"
    elif avg_temp < TEMP_LOW:
        return "TOO_LOW"
    return "OK"


def _determine_hum_state(humidity):
    """Determine humidity state based on current measurement."""
    if humidity > HUM_HIGH:
        return "TOO_HIGH"
    elif humidity < HUM_LOW:
        return "TOO_LOW"
    return "OK"


def _resolve_action(temp_state, hum_state):
    """Priority logic: temperature takes precedence over humidity.
    Messages matching Pico mqtt.py on_message:
    COOL, HEAT, DRY, HUM
    """
    # 1. Check temperature (highest priority)
    if temp_state == "TOO_HIGH":
        return "COOL"
    if temp_state == "TOO_LOW":
        return "HEAT"
    # 2. Check humidity
    if hum_state == "TOO_HIGH":
        return "DRY"
    if hum_state == "TOO_LOW":
        return "HUM"
    # 3. Everything within range
    return "OK"


# --- Client setup ---------------------------------------------------------

def build_client() -> mqtt.Client:
    client = mqtt.Client(
        client_id=MQTT_CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )

    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    # TLS context: verify server certificate against the project CA
    ssl_ctx = ssl.create_default_context(cafile=CA_CERT_FILE)
    if MQTT_TLS_INSECURE:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        log.warning(
            "TLS verification DISABLED (MQTT_TLS_INSECURE=true) - "
            "use for testing only!"
        )
    client.tls_set_context(ssl_ctx)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Built-in reconnect backoff (used by loop_forever)
    client.reconnect_delay_set(min_delay=1, max_delay=60)
    return client
