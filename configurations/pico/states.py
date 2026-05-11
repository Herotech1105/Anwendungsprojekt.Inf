from picozero import pico_led
from machine import Pin
import dht

sensor = dht.DHT22(Pin(2, Pin.IN, Pin.PULL_UP))
radiator = Pin(12, Pin.OUT)   # Heizung
fan = Pin(13, Pin.OUT)        # Lüfter / Kühlung

pico_led.on()

TEMP_TOO_LOW  = 0
TEMP_OK       = 1
TEMP_TOO_HIGH = 2

HUM_TOO_LOW   = 3
HUM_OK        = 4
HUM_TOO_HIGH  = 5

current_state = None

TEMP_MIN = 19.5
TEMP_MAX = 20.5
HUM_MIN  = 42.0
HUM_MAX  = 53.0


def determine_temp_state(temp):
    """Ermittelt Temperaturzustand"""
    if temp < TEMP_MIN:
        return TEMP_TOO_LOW
    elif temp > TEMP_MAX:
        return TEMP_TOO_HIGH
    else:
        return TEMP_OK


def determine_hum_state(hum):
    """Ermittelt Feuchtezustand"""
    if hum < HUM_MIN:
        return HUM_TOO_LOW
    elif hum > HUM_MAX:
        return HUM_TOO_HIGH
    else:
        return HUM_OK


def apply_state(temp_state, hum_state):
    """Regelt zuerst Temperatur, dann Feuchtigkeit"""

    global current_state

    if temp_state == TEMP_TOO_HIGH:
        radiator.off()
        fan.on()
        print("STATE: Temp HIGH → Kühlen")
        current_state = "COOLING"
        return

    if temp_state == TEMP_TOO_LOW:
        radiator.on()
        fan.off()
        print("STATE: Temp LOW → Heizen")
        current_state = "HEATING"
        return

    if hum_state == HUM_TOO_HIGH:
        radiator.on()
        fan.off()
        print("STATE: Hum HIGH → Trocknen (Heizen)")
        current_state = "DRYING"
        return

    if hum_state == HUM_TOO_LOW:
        radiator.off()
        fan.on()
        print("STATE: Hum LOW → Befeuchten (Kühlen)")
        current_state = "HUMIDIFYING"
        return

    radiator.off()
    fan.off()
    print("STATE: Alles OK → Alles AUS")
    current_state = "IDLE"
