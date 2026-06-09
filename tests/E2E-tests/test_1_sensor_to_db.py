"""
Test 1: Sensordaten kommen in der Datenbank an (Happy Path)
============================================================
MQTT Publish -> Broker -> controller.py -> nginx -> server.js -> MariaDB

Publishes a sensor message with a unique temperature value via MQTT,
waits for the data to flow through the entire pipeline, then queries
the dashboard range API to verify the value arrived in the database.

Uses /api/sensordata/range instead of /api/sensordata because the
real Pico may be sending live data, making our test value no longer
the "latest" entry by the time we query.
"""

import json
import ssl
import time
from datetime import datetime, timezone, timedelta

import paho.mqtt.client as mqtt
import requests

from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD,
    MQTT_SENSOR_TOPIC, MQTT_TLS_INSECURE, CA_CERT_FILE,
    BACKEND_BASE_URL, KC_TOKEN_URL, KC_DASHBOARD_CLIENT_ID,
    KC_NORMAL_USER, KC_NORMAL_PASSWORD,
    HTTP_TIMEOUT, PIPELINE_WAIT,
    TEST_TEMPERATURE, TEST_HUMIDITY, SSL_VERIFY,
)
from helpers import print_header, record, exit_with_result, PASS, FAIL


def _get_dashboard_token() -> str | None:
    """Get a Bearer token for iotuser01 via password grant."""
    try:
        resp = requests.post(
            KC_TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": KC_DASHBOARD_CLIENT_ID,
                "username": KC_NORMAL_USER,
                "password": KC_NORMAL_PASSWORD,
            },
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        return None
    except requests.RequestException:
        return None


def run():
    print_header("TEST 1: Sensor Data -> Database (Happy Path)")

    # -- Step 1: Get a dashboard token to query DB later --
    token = _get_dashboard_token()
    if token is None:
        record(FAIL, "Get dashboard token for DB query",
               "Could not get token. Is Keycloak running?")
        exit_with_result()
    record(PASS, f"Dashboard token obtained (user: {KC_NORMAL_USER})")

    # -- Step 2: Record time window and publish MQTT message --
    time_before = datetime.now(timezone.utc) - timedelta(seconds=5)

    print(f"\n  Publishing MQTT message: temp={TEST_TEMPERATURE}, hum={TEST_HUMIDITY}")
    print(f"  Topic: {MQTT_SENSOR_TOPIC} @ {MQTT_HOST}:{MQTT_PORT}\n")

    payload = json.dumps({
        "temperature": TEST_TEMPERATURE,
        "humidity": TEST_HUMIDITY,
    })

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
        record(PASS, "MQTT message published")
    except Exception as exc:
        record(FAIL, "MQTT message published", str(exc))
        exit_with_result()

    # -- Step 3: Wait for pipeline --
    print(f"\n  Waiting {PIPELINE_WAIT}s for data to flow through the pipeline...\n")
    time.sleep(PIPELINE_WAIT)

    # -- Step 4: Query range API to find our value --
    time_after = datetime.now(timezone.utc) + timedelta(seconds=5)
    range_url = f"{BACKEND_BASE_URL}/api/sensordata/range"

    try:
        resp = requests.get(
            range_url,
            params={
                "from": time_before.isoformat(),
                "to": time_after.isoformat(),
            },
            headers={"Authorization": f"Bearer {token}"},
            timeout=HTTP_TIMEOUT,
            verify=SSL_VERIFY,
        )

        if resp.status_code != 200:
            record(FAIL, "Backend returned sensor data range",
                   f"Status {resp.status_code}: {resp.text[:150]}")
            exit_with_result()

        record(PASS, "Backend returned sensor data range",
               f"Status {resp.status_code}")
    except requests.RequestException as exc:
        record(FAIL, "Backend returned sensor data range", str(exc))
        exit_with_result()

    # -- Step 5: Search for our specific temperature in the results --
    data = resp.json()
    temperatures = data.get("temperatures", [])

    found = any(abs(float(t) - TEST_TEMPERATURE) < 0.1 for t in temperatures)

    if found:
        record(PASS, "Test temperature found in DB",
               f"Found {TEST_TEMPERATURE} among {len(temperatures)} entries in time window")
    else:
        record(FAIL, "Test temperature found in DB",
               f"Expected {TEST_TEMPERATURE} not found. "
               f"Got {len(temperatures)} entries: {temperatures[:10]}...")

    exit_with_result()


if __name__ == "__main__":
    run()
