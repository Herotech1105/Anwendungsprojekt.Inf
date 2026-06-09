"""
Test 5: Aktor-Steuerung bei hoher Temperatur
==============================================
MQTT "sensor/data" (zu warm) -> controller.py -> LSTM -> MQTT "actuator/control" = "COOL"

Publishes multiple high-temperature sensor messages to fill the LSTM
buffer, then listens on actuator/control for a "COOL" command.
"""

import json
import ssl
import time

import paho.mqtt.client as mqtt

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_SENSOR_TOPIC, MQTT_ACTUATOR_TOPIC,
    MQTT_TLS_INSECURE, CA_CERT_FILE,
    PIPELINE_WAIT, LSTM_BUFFER_FILL_COUNT, HIGH_TEMPERATURE,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL


def run():
    print_header("TEST 5: Actuator Control (High Temperature -> COOL)")

    received_commands = []
    connected = False

    def on_connect(client, userdata, flags, rc, properties=None):
        nonlocal connected
        if rc == 0:
            connected = True
            client.subscribe(MQTT_ACTUATOR_TOPIC, qos=1)

    def on_message(client, userdata, msg):
        cmd = msg.payload.decode()
        received_commands.append(cmd)

    # -- Step 1: Connect and subscribe to actuator/control --
    client = mqtt.Client(
        client_id="e2e-test-5",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    ssl_ctx = ssl.create_default_context(cafile=CA_CERT_FILE)
    if MQTT_TLS_INSECURE:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
    client.tls_set_context(ssl_ctx)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
        client.loop_start()

        for _ in range(50):
            if connected:
                break
            time.sleep(0.1)

        if not connected:
            record(FAIL, "Connected to MQTT broker", "Timeout after 5s")
            exit_with_result()

        record(PASS, f"Subscribed to '{MQTT_ACTUATOR_TOPIC}'")
    except Exception as exc:
        record(FAIL, "Connected to MQTT broker", str(exc))
        exit_with_result()

    # -- Step 2: Publish high-temperature messages to fill LSTM buffer --
    print(f"  Publishing {LSTM_BUFFER_FILL_COUNT} messages with temp={HIGH_TEMPERATURE}...\n")

    try:
        for i in range(LSTM_BUFFER_FILL_COUNT):
            payload = json.dumps({
                "temperature": HIGH_TEMPERATURE,
                "humidity": 45.0,
            })
            result = client.publish(MQTT_SENSOR_TOPIC, payload=payload, qos=1)
            result.wait_for_publish(timeout=5)
            # Delay between messages so the controller processes each one
            # and the LSTM buffer fills up properly
            time.sleep(1.0)

        record(PASS, f"{LSTM_BUFFER_FILL_COUNT} sensor messages published")
    except Exception as exc:
        record(FAIL, "Sensor messages published", str(exc))
        client.loop_stop()
        client.disconnect()
        exit_with_result()

    # -- Step 3: Wait for controller to process and respond --
    print(f"  Waiting {PIPELINE_WAIT}s for actuator response...\n")
    time.sleep(PIPELINE_WAIT)

    client.loop_stop()
    client.disconnect()

    # -- Step 4: Check if COOL was received --
    if not received_commands:
        record(FAIL, "Received actuator command",
               "No messages on actuator/control within timeout. "
               "Check: 1) Is the controller container running? "
               "2) Does mosquitto ACL allow test client to subscribe to actuator/control? "
               "3) Check controller logs: docker logs controller")
    elif "COOL" in received_commands:
        record(PASS, "Received 'COOL' on actuator/control",
               f"All commands received: {received_commands}")
    else:
        record(FAIL, "Received 'COOL' on actuator/control",
               f"Commands received: {received_commands} (expected COOL)")

    exit_with_result()


if __name__ == "__main__":
    run()
