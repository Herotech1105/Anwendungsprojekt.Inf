import ssl
from umqtt.robust import MQTTClient
import iot_config as iot
import states


#0----Subscribe Message-----
last_message = {"topic": None, "payload": None}

def on_message(topic, msg):
    """Returns the subscribe data"""
    last_message["topic"] = topic
    last_message["payload"] = msg
    print(topic, msg)

def process_last():
    """Only processes the latest message, returns True if there was a message"""
    msg = last_message["payload"]
    if msg is None:
        return False
    
    last_message["payload"] = None

    if msg == b"COOL":
        states.apply_state(states.TEMP_TOO_HIGH, states.HUM_OK)
    elif msg == b"HEAT":
        states.apply_state(states.TEMP_TOO_LOW, states.HUM_OK)
    elif msg == b"DRY":
        states.apply_state(states.TEMP_OK, states.HUM_TOO_HIGH)
    elif msg == b"HUM":
        states.apply_state(states.TEMP_OK, states.HUM_TOO_LOW)
    elif msg == b"OK":
        states.apply_state(states.TEMP_OK, states.HUM_OK)
    else:
        print("Invalid message:", msg)
    
    return True
#1----Subscribe Message-----


"""Creates a MQTT-Client and configures CA and TLS"""
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
