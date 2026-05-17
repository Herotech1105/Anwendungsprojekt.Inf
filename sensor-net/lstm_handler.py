from collections import deque

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam

SEQ_LEN = 10
FEATURES = 2

input_shape = (SEQ_LEN, FEATURES)

# initialize LSTM model
def build_model():
    model = Sequential([
        Input(shape=input_shape),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(64),
        Dropout(0.2),
        Dense(1),
    ])
    # regulate learning rate
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="mse",
    )
    return model


model = build_model()

# save last values in buffer
buffer = deque(maxlen=SEQ_LEN)

def predict_next_value(temperature, humidity):

    current_features = [temperature, humidity]
    buffer.append(current_features)

    # only predict when enough data in the buffer
    if len(buffer) < SEQ_LEN:
        return None

    # rehshape buffer to (1, SEQ_LEN, FEATURES) for LSTM input
    input_data = np.array(buffer).reshape(1, SEQ_LEN, FEATURES)

    # predict next value
    prediction = model.predict(input_data, verbose=0)

    return float(prediction[0][0])


def forecast_future(minutes=30, alpha=0.2):
    """Rekursive Vorhersage für die nächsten Minuten."""

    if len(buffer) < SEQ_LEN:
        return None

    future_predictions = []
    seq = np.array(buffer, dtype=np.float32)
    seq = np.expand_dims(seq, axis=0)          # (1, SEQ_LEN, FEATURES)

    last_humidity = float(seq[0, -1, 1])       # Humidity konstant halten

    for _ in range(minutes):
        pred = model.predict(seq, verbose=0)
        # Vorhersagewert glätten
        next_temp = (1 - alpha) * float(pred[0, 0]) \
                    + alpha * float(seq[0, -1, 0])
        future_predictions.append(next_temp)

        # Alte Sequenz ab Index 1 mit neuem Wert entlang Zeitachse verbinden
        next_step = np.array([[[next_temp, last_humidity]]], dtype=np.float32)
        seq = np.concatenate([seq[:, 1:, :], next_step], axis=1)

    return future_predictions
