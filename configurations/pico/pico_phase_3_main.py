from picozero import pico_led
from machine import Pin
from time import sleep, time
import dht
import network
import urequests as requests

"""WLAN Parameter für den Aufbau einer Verbindung"""
SSID = "Production" # Production
PASSWORD = "Production-01" # Production-01

"""Backend-Proxy"""
BACKEND_PROXY_URL = "http://192.168.50.20:5000/weather"

"""Inputs / Outputs für Sensoren / Aktoren"""
sensor = dht.DHT22(Pin(2, Pin.IN, Pin.PULL_UP))
radiator = Pin(12, Pin.OUT)
fan = Pin(13, Pin.OUT)

"""Pico LED zeigt an, ob der Pico W läuft"""
pico_led.on()

"""Zustände für Temperatur- und Luftfeuchtigkeit"""
STATE_HIGH_TEMP_LOW_HUM = 0
STATE_LOW_TEMP_LOW_HUM  = 1
STATE_HIGH_TEMP_HIGH_HUM = 2
STATE_LOW_TEMP_HIGH_HUM  = 3

current_state = None

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

def apply_state(state):
    """Anwendung State-Machine"""
    global current_state

    if state == STATE_HIGH_TEMP_LOW_HUM:
        radiator.off()
        fan.on()
        print("STATE: Temp HIGH, Hum LOW")

    elif state == STATE_LOW_TEMP_LOW_HUM:
        radiator.on()
        fan.on()
        print("STATE: Temp LOW, Hum LOW")

    elif state == STATE_HIGH_TEMP_HIGH_HUM:
        radiator.off()
        fan.off()
        print("STATE: Temp HIGH, Hum HIGH")

    elif state == STATE_LOW_TEMP_HIGH_HUM:
        radiator.on()
        fan.off()
        print("STATE: Temp LOW, Hum HIGH")

    current_state = state


def determine_state(temp, hum):
    """State-Machine"""
    if temp > 20.5 and hum < 52.0:
        return STATE_HIGH_TEMP_LOW_HUM

    if temp < 19.5 and hum < 52.0:
        return STATE_LOW_TEMP_LOW_HUM

    if temp > 20.5 and hum > 58.0:
        return STATE_HIGH_TEMP_HIGH_HUM

    if temp < 19.5 and hum > 58.0:
        return STATE_LOW_TEMP_HIGH_HUM

    return current_state

# wlan = connect_wifi() # Wlan verbinden

while True:
    """Haupt-Loop"""
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print("Temperature: {:.1f}°C   Humidity: {:.1f}%".format(temp, hum))

        new_state = determine_state(temp, hum)

        if new_state != current_state:
            apply_state(new_state)

    except OSError:
        print("Failed to read sensor:", e)

    sleep(60)


# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3
# Zugriff: 18.04.2026
# Pico W firmware

# https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008312-DS-1-pico-w-datasheet.pdf?disposition=inline
# Zugriff: 18.04.2026
# Pico W datasheet

# https://docs.micropython.org/en/latest/rp2/quickref.html
# Zugriff: 24.04.2026
# RP2 code reference