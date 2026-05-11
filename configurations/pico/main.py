from time import sleep, time
import ujson
import wifi
import states
import mqtt

wlan = wifi.connect_wifi()

mqtt.client.connect()

while True:
    """Haupt-Loop"""
    try:
        states.sensor.measure()
        temp = round(states.sensor.temperature(), 1)
        hum = round(states.sensor.humidity(), 1)

        payload = ujson.dumps({
          "temperature": temp,
          "humidity": hum
        })
        
        mqtt.client.publish("sensor/data", payload)

        temp_state = states.determine_temp_state(temp)
        hum_state  = states.determine_hum_state(hum)

        states.apply_state(temp_state, hum_state)
    except OSError as e:
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