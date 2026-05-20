from time import sleep, time
import network
import iot_config as iot
import control

panel = control.lcd

"""WLAN Parameter für den Aufbau einer Verbindung"""
SSID 	 = iot.WIFI_SSID
PASSWORD = iot.WIFI_PASSWORD

def connect_wifi():
    """Verbindung zum WLAN"""
    wlan = network.WLAN(network.STA_IF) # Client-Modus, verbindet sich mit einem Router
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Verbinde mit WLAN...")
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("Verbinde WLAN")
    while not wlan.isconnected():
        sleep(1)
        print("...")
        print(wlan.status())
        panel.clear()
        panel.move_to(0, 0)
        panel.putstr("Versuch WLAN zu")
        panel.move_to(0, 1)
        panel.putstr("verbinden...")

    print("Verbunden! IP: ", wlan.ifconfig()[0])
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("Verbunden IP:")
    panel.move_to(0, 1)
    panel.putstr(str(wlan.ifconfig()[0]))
    return wlan
