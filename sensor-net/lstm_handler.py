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
    
    prediction = model.predict(input_data, verbose=0)
    
    return float(prediction[0][0])