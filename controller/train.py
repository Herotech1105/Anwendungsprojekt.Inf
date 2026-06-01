# train.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

# --- 1. Konfiguration ---
SEQ_LEN = 10     # Das LSTM schaut 10 Zeitschritte in die Vergangenheit
FEATURES = 2    # Nur noch Temperatur und Luftfeuchtigkeit

# --- 2. Beispieldaten laden/generieren ---
# (Ersetze diesen Block später durch das Laden deiner echten CSV-Datei)
np.random.seed(42)
num_samples = 1000


simulated_temp = np.sin(np.linspace(0, 50, num_samples)) * 10 + 20 + np.random.randn(num_samples)
simulated_hum = 60 - (simulated_temp * 0.5) + np.random.randn(num_samples)

raw_data = np.column_stack((simulated_temp, simulated_hum))


scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(raw_data)

# --- 4. Daten in Sequenzen schneiden (Sliding Window) ---
X, y = [], []

for i in range(len(scaled_data) - SEQ_LEN):
    # X enthält die letzten 10 Schritte (Temp & Hum)
    X.append(scaled_data[i : i + SEQ_LEN])
    # y enthält das Ziel: Die Temperatur am nächsten Schritt (Spalte 0)
    y.append(scaled_data[i + SEQ_LEN, :2])

X = np.array(X)
y = np.array(y)

# --- 5. Das Modell bauen (Deine Architektur angepasst auf 2 Features) ---
model = Sequential([
    Input(shape=(SEQ_LEN, FEATURES)),  # Shape ist jetzt (10, 2)
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    Dense(1),                          # Ein Ausgang: Die prognostizierte Temperatur
])

# Modell konfigurieren
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse"
)

# --- 6. Modell trainieren ---
print(f"Starte Training mit Shape X: {X.shape} und y: {y.shape}...")
model.fit(
    X, y,
    epochs=20,
    batch_size=32,
    validation_split=0.2,  # 20% der Daten dienen zur Überprüfung
    verbose=1
)

# --- 7. Das fertige Modell speichern ---
model.save("mein_eigenes_modell.keras")
print("\n--> Modell erfolgreich als 'mein_eigenes_modell.keras' gespeichert!")