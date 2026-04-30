from time import sleep, time
import network

"""WLAN Parameter für den Aufbau einer Verbindung"""
SSID = "Production" # Production
PASSWORD = "Production-01" # Production-01

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