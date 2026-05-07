import ssl
from umqtt.robust import MQTTClient

with open("/certs/ca.der", "rb") as f:
    ca_data = f.read()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cadata=ca_data)

client = MQTTClient(
    client_id="pico",
    server="192.168.4.18",
    port=8883,
    user="iotuser",
    password="kleber",
    ssl=context,
    ssl_params={}
)