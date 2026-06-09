"""
Test 4: Ungueltige Sensordaten werden verworfen
=================================================
Ungueltige MQTT-Nachricht -> Broker -> controller.py (verwirft) -> NICHTS in DB

Publishes invalid MQTT messages and verifies they do NOT create
new entries in the database. The controller's validation.py should
silently drop them.
"""

import json
import ssl
import time

import paho.mqtt.client as mqtt
import requests

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_SENSOR_TOPIC, MQTT_TLS_INSECURE, CA_CERT_FILE,
    SENSORDATA_LATEST_URL, API_KEY, HTTP_TIMEOUT, PIPELINE_WAIT,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL


def _get_latest_entry():
    """Fetch the most recent DB entry via the backend API."""
    resp = requests.get(
        SENSORDATA_LATEST_URL,
        headers={"x-api-key": API_KEY},
        timeout=HTTP_TIMEOUT,
        verify=CA_CERT_FILE,
    )
    if resp.status_code == 200:
        return resp.json()
    return None


def _publish_mqtt(payload_str: str):
    """Publish a raw string to the sensor topic."""
    client = mqtt.Client(
        client_id="e2e-test-4",
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
    result = client.publish(MQTT_SENSOR_TOPIC, payload=payload_str, qos=1)
    result.wait_for_publish(timeout=5)
    client.disconnect()


def run():
    print_header("TEST 4: Invalid Sensor Data Rejected")

    # -- Step 1: Remember current latest entry --
    before = _get_latest_entry()
    if before is None:
        record(FAIL, "Fetch baseline DB entry", "Could not reach backend API")
        exit_with_result()

    before_id = before.get("id", before.get("timestamp", ""))
    record(PASS, "Baseline DB entry fetched",
           f"id/timestamp: {before_id}")

    # -- Step 2: Publish various invalid messages --
    invalid_payloads = [
        ("Temperature out of range (999)",
         json.dumps({"temperature": 999.0, "humidity": 45.0})),
        ("Humidity out of range (-50)",
         json.dumps({"temperature": 22.0, "humidity": -50.0})),
        ("Not valid JSON",
         "this is not json"),
        ("Missing humidity field",
         json.dumps({"temperature": 22.0})),
        ("Non-numeric values",
         json.dumps({"temperature": "warm", "humidity": "wet"})),
    ]

    for label, payload in invalid_payloads:
        try:
            _publish_mqtt(payload)
            print(f"  -> Published: {label}")
        except Exception as exc:
            record(FAIL, f"Publish '{label}'", str(exc))
            exit_with_result()

    # -- Step 3: Wait for pipeline --
    print(f"\n  Waiting {PIPELINE_WAIT}s...\n")
    time.sleep(PIPELINE_WAIT)

    # -- Step 4: Check that no new entry was created --
    after = _get_latest_entry()
    if after is None:
        record(FAIL, "Fetch DB entry after invalid messages",
               "Could not reach backend API")
        exit_with_result()

    after_id = after.get("id", after.get("timestamp", ""))

    if str(before_id) == str(after_id):
        record(PASS, "No new DB entry after invalid messages",
               f"Latest entry still: {after_id}")
    else:
        record(FAIL, "No new DB entry after invalid messages",
               f"Before: {before_id}, After: {after_id} (new entry was created!)")

    exit_with_result()


if __name__ == "__main__":
    run()
