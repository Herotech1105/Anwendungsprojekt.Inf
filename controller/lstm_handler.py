import numpy as np
import tensorflow as tf
from collections import deque
from sklearn.preprocessing import MinMaxScaler

# config
SEQ_LEN = 10 
FEATURES = 2
MODEL_PATH = "train.keras"

# load model and create buffer for incoming data
model = tf.keras.models.load_model(MODEL_PATH)
buffer = deque(maxlen=SEQ_LEN)

# Recreate the scaler used in training
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.data_min_ = np.array([0.0, 0.0])
scaler.data_max_ = np.array([100.0, 100.0])
scaler.data_range_ = scaler.data_max_ - scaler.data_min_
scaler.scale_ = 1.0 / scaler.data_range_
scaler.min_ = -scaler.data_min_ * scaler.scale_


def predict_next_value(temperature, humidity):
    buffer.append([temperature, humidity])

    # Check if we have enough steps to make a prediction
    if len(buffer) < SEQ_LEN:
        return None

    # Convert buffer to numpy array -> Shape: (SEQ_LEN, 2)
    recent_data = np.array(buffer)

    # Fix 2: Scale the data using the training scaler
    scaled_input = scaler.transform(recent_data)  # Shape: (SEQ_LEN, 2)

    # Fix 3: Reshape for Keras expectations -> Shape: (1, SEQ_LEN, 2)
    scaled_input = np.expand_dims(scaled_input, axis=0)

    # Get the RAW scaled prediction from the model
    prediction = model.predict(scaled_input, verbose=0)
    raw_predicted_temp = float(prediction[0][0])

    # Fix 4: Inverse transform to bring back to actual degrees Celsius
    # Create a dummy row matching the feature shape (2 features) to decode
    dummy_array = np.zeros((1, 2))
    dummy_array[0, 0] = raw_predicted_temp  # Put temperature prediction in col 0

    unscaled_result = scaler.inverse_transform(dummy_array)
    actual_temp_prediction = unscaled_result[0, 0]

    # Return dictionary with the results
    return {
        "predicted_temp": round(actual_temp_prediction, 2),
        "predicted_hum": humidity,  # Keeping your default return choice
    }