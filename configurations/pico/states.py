from picozero import pico_led
from machine import Pin
import dht

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