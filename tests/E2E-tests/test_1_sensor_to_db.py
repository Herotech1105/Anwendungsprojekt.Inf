"""
Test 1: Sensordaten kommen in der Datenbank an (Happy Path)
============================================================
MQTT Publish -> Broker -> controller.py -> nginx -> server.js -> MariaDB

Publishes a sensor message with a unique temperature value via MQTT,
waits for the data to flow through the entire pipeline, then queries
the backend API to verify the value arrived in the database.
"""

import json
import ssl
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
import requests

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_SENSOR_TOPIC, MQTT_TLS_INSECURE, CA_CERT_FILE,
    SENSORDATA_LATEST_URL, API_KEY, HTTP_TIMEOUT, PIPELINE_WAIT,
    TEST_TEMPERATURE, TEST_HUMIDITY,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL


def run():
    print_header("TEST 1: Sensor Data -> Database (Happy Path)")

    # -- Step 1: Publish MQTT message (simulates the Pico) --
    print(f"  Publishing MQTT message: temp={TEST_TEMPERATURE}, hum={TEST_HUMIDITY}")
    print(f"  Topic: {MQTT_SENSOR_TOPIC} @ {MQTT_HOST}:{MQTT_PORT}\n")

    payload = json.dumps({
        "temperature": TEST_TEMPERATURE,
        "humidity": TEST_HUMIDITY,
    })

    published = False
    try:
        client = mqtt.Client(
            client_id="e2e-test-1",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        if MQTT_USER:
            client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        ssl_ctx = ssl.create_default_context(cafile=CA_CERT_FILE)
        if MQTT_TLS_INSECURE:
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
        client.tls_set_context(ssl_ctx)

        client.connect(MQTT_HOST, MQTT_PORT, keepalive=10)
        result = client.publish(MQTT_SENSOR_TOPIC, payload=payload, qos=1)
        result.wait_for_publish(timeout=5)
        client.disconnect()
        published = True
        record(PASS, "MQTT message published")
    except Exception as exc:
        record(FAIL, "MQTT message published", str(exc))
        exit_with_result()

    # -- Step 2: Wait for pipeline --
    print(f"\n  Waiting {PIPELINE_WAIT}s for data to flow through the pipeline...\n")
    time.sleep(PIPELINE_WAIT)

    # -- Step 3: Query latest entry from backend API --
    try:
        resp = requests.get(
            SENSORDATA_LATEST_URL,
            headers={"x-api-key": API_KEY},
            timeout=HTTP_TIMEOUT,
            verify=CA_CERT_FILE,
        )

        if resp.status_code != 200:
            record(FAIL, "Backend returned latest sensor data",
                   f"Status {resp.status_code}: {resp.text[:150]}")
            exit_with_result()

        record(PASS, "Backend returned latest sensor data",
               f"Status {resp.status_code}")
    except requests.RequestException as exc:
        record(FAIL, "Backend returned latest sensor data", str(exc))
        exit_with_result()

    # -- Step 4: Verify the data matches --
    data = resp.json()
    db_temp = float(data.get("temperature", 0))

    if abs(db_temp - TEST_TEMPERATURE) < 0.01:
        record(PASS, "Temperature in DB matches published value",
               f"Expected: {TEST_TEMPERATURE}, Got: {db_temp}")
    else:
        record(FAIL, "Temperature in DB matches published value",
               f"Expected: {TEST_TEMPERATURE}, Got: {db_temp}")

    exit_with_result()


if __name__ == "__main__":
    run()
