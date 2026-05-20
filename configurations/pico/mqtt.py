import ssl
from umqtt.robust import MQTTClient
import iot_config as iot
import states

#0----Subscribe Message-----
def on_message(topic, msg):
    """Gibt die Daten des Subscribe aus"""
    print(topic, msg)
    if msg == b"COOL":
        states.apply_state(states.TEMP_TOO_HIGH, states.HUM_OK)
    elif msg == b"HEAT":
        states.apply_state(states.TEMP_TOO_LOW, states.HUM_OK)
    elif msg == b"DRY":
        states.apply_state(states.TEMP_OK, states.HUM_TOO_HIGH)
    elif msg == b"HUM":
        states.apply_state(states.TEMP_OK, states.HUM_TOO_LOW)
    else:
        print("Invalid message")
#1----Subscribe Message-----

"""Erstellt einen MQTTClient und konfiguriert CA und TLS"""
print("mqtt.py - Start")

with open(iot.CA_CERT, "rb") as f:
    ca_data = f.read()
print("mqtt.py - CA geladen")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cadata=ca_data)
print("mqtt.py - Context erstellt")

client = MQTTClient(
    client_id   = iot.MQTT_CLIENT,
    server      = iot.MQTT_BROKER,
    port        = iot.MQTT_PORT,
    user        = iot.MQTT_USER,
    password    = iot.MQTT_PASS,
    ssl         = context,
    ssl_params  = {}
)
print("mqtt.py - Client erstellt")
