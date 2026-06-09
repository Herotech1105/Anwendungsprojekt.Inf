from time import sleep, time
import network
import iot_config as iot
import control

#========== Anhang ==========
panel = control.lcd
#========== Anhang Ende ==========

"""WLAN Parameters for connecting to the WiFi"""
SSID 	 = iot.WIFI_SSID
PASSWORD = iot.WIFI_PASSWORD


def connect_wifi():
    """Connects to the WiFi and returns the WLAN object"""
    wlan = network.WLAN(network.STA_IF) # Client-Mode, connects to a Router
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Verbinde mit WLAN...")
    
    #========== Anhang ==========
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("Verbinde WLAN")
    #========== Anhang Ende ==========

    while not wlan.isconnected():
        sleep(1)
        print("...")
        print(wlan.status())

        #========== Anhang ==========
        panel.clear()
        panel.move_to(0, 0)
        panel.putstr("Versuch WLAN zu")
        panel.move_to(0, 1)
        panel.putstr("verbinden...")
        #========== Anhang Ende ==========

    print("Verbunden! IP: ", wlan.ifconfig()[0])

    #========== Anhang ==========
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("Verbunden IP:")
    panel.move_to(0, 1)
    panel.putstr(str(wlan.ifconfig()[0]))
    #========== Anhang Ende ==========

    return wlan
