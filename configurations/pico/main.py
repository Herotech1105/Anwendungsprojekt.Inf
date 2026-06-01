from time import sleep, time
from utime import ticks_ms, ticks_diff, sleep_ms
import ujson
import iot_config as iot
import wifi
import states
import control
import mqtt


panel = control.lcd
mqtt.client.set_callback(mqtt.on_message)


#0----Interrupt-----
press_time = 0
last_reset = 0

def button_pressed(pin):
    """Reset Button um den Pico neu zu starten"""
    global press_time, last_reset
    now   = ticks_ms()
    value = control.button.value()
    
    if value == 0:
        press_time = now
    else:
        if ticks_diff(now, last_reset) < 500:
            return
        if ticks_diff(now, press_time) >= 3000:
            last_reset = now
            sleep_ms(50)
            control.reset()

control.button.irq(
    trigger = control.Pin.IRQ_FALLING | control.Pin.IRQ_RISING,
    handler = button_pressed
)
#1----Interrupt-----


"""Verbindung zum WLAN"""
#0----WLAN-Connection-----
try:
    wlan = wifi.connect_wifi()
except OSError as e:
    print("Failed connect wlan: ", e)
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("WLAN Error")
    panel.move_to(0, 1)
    panel.putstr("Reconnecting...")
#1----WLAN-Connection-----


sleep(3)


"""Verbindung zum MQTT-Broker"""
#0----MQTT-Connection-----
mqtt_connected = False
print("Vor MQTT connect")
try:
    mqtt.client.connect()
    print("Nach MQTT connect")
    mqtt.client.subscribe(iot.MQTT_ACTOR_TOPIC)
    print("subscribed")
    mqtt_connected = True
    print("MQTT verbunden!")
except OSError as e:
    print("Failed connect mqtt: ", e)
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("MQTT Error")
    panel.move_to(0, 1)
    panel.putstr("Reconnecting...")
except Exception as e:
    print("MQTT Exception:", e)
    panel.clear()
    panel.move_to(0, 0)
    panel.putstr("MQTT Error")
    panel.move_to(0, 1)
    panel.putstr(str(e)[:16])
#1----MQTT-Connection-----


while True:
    """Haupt-Loop"""
    try:
        #0----Sensor-Measuring-----
        control.sensor.measure()
        temp = round(control.sensor.temperature(), 1)
        hum  = round(control.sensor.humidity(), 1)
        #1----Sensor-Measuring-----


        #0----MQTT-Message-----
        payload = ujson.dumps({
          "temperature": temp,
          "humidity"   : hum
        })

        if mqtt_connected:
            mqtt.client.publish(iot.MQTT_SENSOR_TOPIC, payload)
            print("Published")

        wait_start = ticks_ms()
        while ticks_diff(ticks_ms(), wait_start) < 10000:
            if mqtt_connected:
                mqtt.client.check_msg()
                if mqtt.process_last():
                    
                    
                    #0----Value-Display-----
                    panel.clear()
                    panel.move_to(0, 0)
                    panel.putstr("{:.1f}C".format(temp))
                    panel.putstr(" ")
                    panel.putstr("{:.1f}%".format(hum))
                    panel.move_to(0, 1)
                    panel.putstr(str(states.current_state))
                    #1----Value-Display-----
            
            
            sleep_ms(1000)
        #1----MQTT-Message-----


        #states.lcd.clear()
        #states.scroll_text("Das ist ein sehr langer Text um den Scroll Text zu testen", zeile=0)


    #0----Sensor-Error-----
    except OSError as e:
        print("Failed to read sensor: ", e)
        panel.clear()
        panel.move_to(0, 0)
        panel.putstr("Sensor Error")
        panel.move_to(0, 1)
        panel.putstr("Can't read")
    #1----Sensor-Error-----



# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3
# Zugriff: 18.04.2026
# Pico W firmware

# https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008312-DS-1-pico-w-datasheet.pdf?disposition=inline
# Zugriff: 18.04.2026
# Pico W datasheet

# https://docs.micropython.org/en/latest/rp2/quickref.html
# Zugriff: 24.04.2026
# RP2 code reference

# https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/example_sub.py
# Zugriff: 18.05.2026
# umqtt reference