"""Konfiguration und Logging fuer den Sensor-Controller."""

import logging
import os

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
TRAININGURL = os.getenv(
    "TRAININGURL", "https://www.lab.local/api/internal/trainingdata"
)
API_KEY = os.getenv("API_KEY", "")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "5"))
NGINX_CERT_FILE = os.getenv("CA_CERT_PATH", "/ca.crt")

# Keycloak (Client Credentials Flow)
KC_TOKEN_URL = os.getenv(
    "KC_TOKEN_URL",
    "https://www.lab.local/auth/realms/iot/protocol/openid-connect/token",
)
KC_CLIENT_ID = os.getenv("KC_CLIENT_ID", "controller-client")
KC_CLIENT_SECRET = os.getenv("KC_CLIENT_SECRET", "change-me-please")
KC_REQUIRED_ROLE = os.getenv("KC_REQUIRED_ROLE", "controller-ingest")

# Plausibilitaetsbereiche (decken sich mit validateSensorPayload in server.js)
TEMP_MIN = float(os.getenv("TEMP_MIN", "0"))
TEMP_MAX = float(os.getenv("TEMP_MAX", "100"))
HUM_MIN = float(os.getenv("HUM_MIN", "0"))
HUM_MAX = float(os.getenv("HUM_MAX", "100"))

# Steuerungsschwellenwerte fuer Aktor-Kontrolle
TEMP_LOW = float(os.getenv("TEMP_LOW", "19"))
TEMP_HIGH = float(os.getenv("TEMP_HIGH", "21"))
HUM_LOW = float(os.getenv("HUM_LOW", "42"))
HUM_HIGH = float(os.getenv("HUM_HIGH", "53"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("controller")
