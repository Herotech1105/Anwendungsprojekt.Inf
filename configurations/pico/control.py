from picozero import pico_led
from machine import Pin, I2C, reset
from pico_i2c_lcd import I2cLcd
from time import sleep
import dht


"""Initialization Input/Output"""
#0----Initialization-----
sensor 	 = dht.DHT22(Pin(2, Pin.IN, Pin.PULL_UP))
radiator = Pin(12, Pin.OUT)
fan 	 = Pin(13, Pin.OUT)

#========== Anhang ==========
peltier = Pin(11, Pin.OUT)
button 	 = Pin(14, Pin.IN, Pin.PULL_UP) # Reset Button
i2c 	 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd 	 = I2cLcd(i2c, 0x27, 2, 16)
#========== Anhang Ende ==========

#1----Initialization-----

pico_led.on()

#========== Anhang ==========
def scroll_text(text, zeile=0):
    """Scrollt den Text auf dem LCD-Display von Rechts nach Links"""
    padded = " " * 16 + text + " " * 16
    prev   = ""
    for i in range(len(padded) - 15):
        current = padded[i:i+16]
        for j in range(16):
            if j >= len(prev) or current[j] != prev[j]:
                lcd.move_to(j, zeile)
                lcd.putstr(current[j])
        prev = current
        sleep(0.2)
#========== Anhang Ende ==========