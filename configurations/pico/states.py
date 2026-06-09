import control


"""State Variables"""
#0----States-----
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
#1----States-----


#0----Apply State-----
def apply_state(temp_state, hum_state):
    """Regulates temperature first, then humidity"""

    global current_state

    if temp_state == TEMP_TOO_HIGH:
        control.radiator.off()
        control.fan.on()
        control.peltier.on()
        print("STATE: Temp HIGH → Kühlen")
        current_state = "COOLING"
        return

    if temp_state == TEMP_TOO_LOW:
        control.radiator.on()
        control.fan.off()
        control.peltier.off()
        print("STATE: Temp LOW → Heizen")
        current_state = "HEATING"
        return

    if hum_state == HUM_TOO_HIGH:
        control.radiator.on()
        control.fan.off()
        control.peltier.off()
        print("STATE: Hum HIGH → Trocknen (Heizen)")
        current_state = "DRYING"
        return

    if hum_state == HUM_TOO_LOW:
        control.radiator.off()
        control.fan.on()
        control.peltier.off()
        print("STATE: Hum LOW → Befeuchten (Kühlen)")
        current_state = "HUMIDIFYING"
        return

    control.radiator.off()
    control.fan.off()
    control.peltier.off()
    print("STATE: Alles OK → Alles AUS")
    current_state = "OK"
#1----Apply State-----
