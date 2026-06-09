"""Configuration of all data variables"""
# --- WLAN Configuration ---
WIFI_SSID 		= "Production"
WIFI_PASSWORD 	= "Production-01"

# --- MQTT Broker Configuration ---
# IP-Address
MQTT_BROKER = "192.168.4.18"

# TLS-Port
MQTT_PORT 	= 8883              

# Topic 
MQTT_SENSOR_TOPIC = b"sensor/data"
MQTT_ACTOR_TOPIC  = b"actuator/control"

# --- MQTT User ---
# Client
MQTT_CLIENT = "pico"

MQTT_USER = "iotuser"
MQTT_PASS = "kleber"

# --- Certificates ---
CA_CERT   = "/certs/ca.der"