import numpy as np
import tensorflow as tf
from collections import deque

# config
SEQ_LEN = 10 
FEATURES = 2
MODEL_PATH = "train.keras" # Name deiner Datei

# load model and create buffer for incoming data
model = tf.keras.models.load_model(MODEL_PATH)
buffer = deque(maxlen=SEQ_LEN)

# values for controlling fan and heater

def predict_next_value(temperature, humidity):

    # put data into the buffer
    buffer.append([temperature / 100, temperature / 100])
    
    if len(buffer) < SEQ_LEN:
        return None
    
    # transform the buffer into the right shape for prediction (1, SEQ_LEN, FEATURES)
    input_data = np.array(buffer).reshape(1, SEQ_LEN, FEATURES)
    
    # get the prediction from the model
    prediction = model.predict(input_data, verbose=0)

    predicted_temp = float(prediction[0][0])
    
    # return dictionary with the results
    return {
        "predicted_temp": round(predicted_temp, 3) * 100,
        "predicted_hum": humidity,
    }