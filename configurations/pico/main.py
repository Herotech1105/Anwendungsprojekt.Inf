from time import sleep, time
# import urequests as requests
import wifi
import states

"""Backend-Proxy"""
BACKEND_PROXY_URL = "http://192.168.50.20:5000/weather"

# wlan = wifi.connect_wifi() # Wlan verbinden

while True:
    """Haupt-Loop"""
    try:
        states.sensor.measure()
        temp = states.sensor.temperature()
        hum = states.sensor.humidity()

        print("Temperature: {:.1f}°C   Humidity: {:.1f}%".format(temp, hum))

        new_state = states.determine_state(temp, hum)

        if new_state != states.current_state:
            states.apply_state(new_state)

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