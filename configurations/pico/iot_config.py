# --- WLAN Konfiguration ---
WIFI_SSID 		= "Production"
WIFI_PASSWORD 	= "Production-01"

# --- MQTT Broker Konfiguration ---
# Client
MQTT_CLIENT = "pico"

# IP-Adresse
MQTT_BROKER = "192.168.4.18"

# TLS-Port
MQTT_PORT 	= 8883              

# Topic 
MQTT_SENSOR_TOPIC = b"sensor/data"
MQTT_ACTOR_TOPIC  = b"actuator/control"

# --- MQTT User ---
MQTT_USER = "iotuser"
MQTT_PASS = "kleber"

# --- Zertifikate ---
CA_CERT   = "/certs/ca.der"