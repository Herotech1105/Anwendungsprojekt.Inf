from picozero import pico_led
from time import sleep, time
import network
import urequests as requests

"""WLAN Parameter für den Aufbau einer Verbindung"""
SSID = "Production"
PASSWORD = "Production-01"

"""REST API für Friedrichshafen"""
API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=47.65&longitude=9.48&current_weather=true"
)

def connect_wifi():
    """Verbindung zum WLAN"""
    wlan = network.WLAN(network.STA_IF) # Client-Modus, verbindet sich mit einem Router
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Verbinde mit WLAN...")
    while not wlan.isconnected():
        sleep(1)
        print("...")

    print("Verbunden! IP:", wlan.ifconfig()[0])
    return wlan


def fetch_outside_temperature():
    """Daten aus Friedrichshafen"""
    try:
        print("Hole Außentemperatur von Open-Meteo...")
        r = requests.get(API_URL)
        data = r.json()
        r.close()
        temp = data["current_weather"]["temperature"]
        print("Außentemperatur Friedrichshafen:", temp, "°C")
        return temp
    except Exception as e:
        print("Fehler bei API:", e)
        return None


def get_blink_interval(temp):
    """Pico LED Blinkintervall"""
    if temp is None:
        return 1.0
    if temp < 10:
        return 2.0
    elif temp <= 25:
        return 1.0
    else:
        return 0.3


wlan = connect_wifi() # Wlan verbinden

outside_temp = fetch_outside_temperature()
blink_interval = get_blink_interval(outside_temp)
next_api_call = time() + 600  # alle 10 Minuten

while True:
    """Haupt-Loop"""
    pico_led.on()
    sleep(blink_interval / 2)
    pico_led.off()
    sleep(blink_interval / 2)

    if time() >= next_api_call:
        outside_temp = fetch_outside_temperature()
        blink_interval = get_blink_interval(outside_temp)
        next_api_call = time() + 600

# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3
# Zugriff: 18.04.2026
# Pico W firmware

# https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008312-DS-1-pico-w-datasheet.pdf?disposition=inline
# Zugriff: 18.04.2026
# Pico W datasheet

# https://docs.micropython.org/en/latest/rp2/quickref.html
# Zugriff: 24.04.2026
# RP2 code reference