"""
E2E Test Configuration
======================
All values can be overridden via environment variables.
Adjust these to match your deployment before running the tests.

Prerequisites:
  - All Docker containers must be running (docker-compose up)
  - For Test 7 (dashboard access), 'directAccessGrantsEnabled' must be
    set to true on the 'dashboard-client' in iot-realm.json, because
    the tests use the Resource Owner Password Grant to get user tokens
    without a browser.
  - For Test 7c, a user WITHOUT the 'dashboard-user' role must exist
    in Keycloak (configured below as KC_NOROLE_USER).
"""

import os

# ---------------------------------------------------------------------------
# Backend (nginx reverse proxy)
# ---------------------------------------------------------------------------
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "https://local.kleber.data")
API_KEY = os.getenv("API_KEY", "api_key")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10"))

# Derived endpoints
SENSORDATA_URL = f"{BACKEND_BASE_URL}/api/internal/sensordata"
SENSORDATA_LATEST_URL = f"{BACKEND_BASE_URL}/api/internal/sensordata/latest"
DASHBOARD_SENSORDATA_URL = f"{BACKEND_BASE_URL}/api/sensordata"
ADMIN_EXPORT_URL = f"{BACKEND_BASE_URL}/api/admin/export"
STATUS_URL = f"{BACKEND_BASE_URL}/api/status"

# ---------------------------------------------------------------------------
# TLS / CA Certificate
# ---------------------------------------------------------------------------
CA_CERT_FILE = os.getenv("CA_CERT_PATH", "../../CA/ca.crt")

# ---------------------------------------------------------------------------
# Keycloak
# ---------------------------------------------------------------------------
KC_BASE_URL = os.getenv("KC_BASE_URL", "https://www.lab.local/auth")
KC_TOKEN_URL = os.getenv(
    "KC_TOKEN_URL",
    f"{KC_BASE_URL}/realms/iot/protocol/openid-connect/token",
)

# Controller client (Client Credentials Flow)
KC_CONTROLLER_CLIENT_ID = os.getenv("KC_CONTROLLER_CLIENT_ID", "controller-client")
KC_CONTROLLER_CLIENT_SECRET = os.getenv("KC_CONTROLLER_CLIENT_SECRET", "change-me-please")
KC_REQUIRED_ROLE = os.getenv("KC_REQUIRED_ROLE", "controller-ingest")

# Dashboard client (Resource Owner Password Grant for tests)
KC_DASHBOARD_CLIENT_ID = os.getenv("KC_DASHBOARD_CLIENT_ID", "dashboard-client")

# Test users
KC_ADMIN_USER = os.getenv("KC_ADMIN_USER", "admin")
KC_ADMIN_PASSWORD = os.getenv("KC_ADMIN_PASSWORD", "admin")

KC_NORMAL_USER = os.getenv("KC_NORMAL_USER", "iotuser01")
KC_NORMAL_PASSWORD = os.getenv("KC_NORMAL_PASSWORD", "password")

KC_NOROLE_USER = os.getenv("KC_NOROLE_USER", "testuser_norole")
KC_NOROLE_PASSWORD = os.getenv("KC_NOROLE_PASSWORD", "password")

# ---------------------------------------------------------------------------
# MQTT Broker
# ---------------------------------------------------------------------------
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "testuser")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "test")
MQTT_SENSOR_TOPIC = os.getenv("MQTT_SENSOR_TOPIC", "sensor/data")
MQTT_ACTUATOR_TOPIC = os.getenv("MQTT_ACTUATOR_TOPIC", "actuator/control")
MQTT_TLS_INSECURE = os.getenv("MQTT_TLS_INSECURE", "true").lower() == "true"

# ---------------------------------------------------------------------------
# Test tuning
# ---------------------------------------------------------------------------
# How long to wait (seconds) for data to flow through the pipeline
PIPELINE_WAIT = float(os.getenv("PIPELINE_WAIT", "5"))
# How many MQTT messages to send to fill the LSTM buffer (needs 10)
LSTM_BUFFER_FILL_COUNT = int(os.getenv("LSTM_BUFFER_FILL_COUNT", "12"))
# Unique temperature used in Test 1 to identify our data in the DB
TEST_TEMPERATURE = float(os.getenv("TEST_TEMPERATURE", "17.77"))
TEST_HUMIDITY = float(os.getenv("TEST_HUMIDITY", "44.33"))
# High temperature for actuator test (must be above TEMP_HIGH threshold)
HIGH_TEMPERATURE = float(os.getenv("HIGH_TEMPERATURE", "35.0"))
