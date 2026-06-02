import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 1440 * 30  # 1440 minutes = 1 full day of data (sampled every minute)
np.random.seed(42)

# Initialize starting conditions
current_time = datetime.strptime("00:00:00:00", "%H:%M:%S:%f")
temp = 20.0  # Starting temperature in Celsius
humidity = 55.0  # Starting humidity percentage
heater_on = 0
cooler_on = 0

data_rows = []

for i in range(NUM_ROWS):
    # 1. Format timestamp string to match your exact format: "00:00:00:00"
    timestamp_str = current_time.strftime("%H:%M:%S:00")

    # 2. Add natural environmental drift (sinusoidal wave for day/night cycles)
    # Natural ambient temperature change per minute
    ambient_drift = 0.05 * np.sin(2 * np.pi * i / NUM_ROWS)
    # Ambient humidity inversely follows temperature slightly
    ambient_humidity_drift = -0.02 * np.sin(2 * np.pi * i / NUM_ROWS)

    # 3. Apply the physical effects of the Actuators if they are ON
    if heater_on == 1:
        temp += 0.25  # Heater warms up the room rapidly
        humidity -= 0.15  # Heater dries out the air
    elif cooler_on == 1:
        temp -= 0.30  # Cooler cools down the room rapidly
        humidity += 0.05  # Cooler relative humidity changes
    else:
        # No actuators active -> apply natural ambient drift + small random noise
        temp += ambient_drift + np.random.normal(0, 0.02)
        humidity += ambient_humidity_drift + np.random.normal(0, 0.05)

    # Keep values bounded to realistic constraints
    temp = max(5.0, min(temp, 40.0))
    humidity = max(10.0, min(humidity, 95.0))

    # 4. Simulated Thermostat Logic (Controls the actors for the NEXT timestep)
    # If temp drops below 17°C, turn on heater. Turn off when comfortable (above 21°C)
    if temp < 17.0:
        heater_on = 1
    elif temp > 21.0:
        heater_on = 0

    # If temp goes above 26°C, turn on cooler. Turn off when cooled down (below 22°C)
    if temp > 26.0:
        cooler_on = 1
    elif temp < 22.0:
        cooler_on = 0

    # Prevent both from being on at the same time
    if heater_on == 1:
        cooler_on = 0

    # 5. Save the snapshot of this exact moment
    data_rows.append({
        "timestamp": timestamp_str,
        "temperature": round(temp, 2),
        "humidity": round(humidity, 2),
        "heater_status": heater_on,
        "cooler_status": cooler_on
    })

    # Advance time by 1 minute
    current_time += timedelta(minutes=1)

# Convert to DataFrame and save to disk
df = pd.DataFrame(data_rows)
df.to_csv("weather_data.csv", index=False)

print("Successfully generated 'weather_data.csv' with 1440 rows!")
print("\nFirst 5 rows look like:")
print(df.head())