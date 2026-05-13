import ssl
from umqtt.robust import MQTTClient
import iot_config as iot

def on_message(topic, msg):
    print(topic, msg)

"""Creates an MQTTClient and sets up CA & TLS"""
#0----CA & TLS-----
with open(iot.CA_CERT, "rb") as f:
    ca_data = f.read()

context 			= ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cadata=ca_data)
#1----CA & TLS-----

client = MQTTClient(
    client_id 	= iot.MQTT_CLIENT,
    server 		= iot.MQTT_BROKER,
    port 		= iot.MQTT_PORT,
    user 		= iot.MQTT_USER,
    password 	= iot.MQTT_PASS,
    ssl 		= context,
    ssl_params 	= {}
)
