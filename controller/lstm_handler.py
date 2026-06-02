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
TEMP_HIGH = 28.0 
TEMP_LOW = 18.0 

def predict_next_value(temperature, humidity):

    # put data into the buffer
    buffer.append([temperature, humidity])
    
    if len(buffer) < SEQ_LEN:
        return None
    
    # transform the buffer into the right shape for prediction (1, SEQ_LEN, FEATURES)
    input_data = np.array(buffer).reshape(1, SEQ_LEN, FEATURES)
    
    # get the prediction from the model
    prediction = model.predict(input_data, verbose=0)

    predicted_temp = float(prediction[0][0])
    
    # set fan and heater states based on the predicted temperature
    fan_on = predicted_temp > TEMP_HIGH
    heater_on = predicted_temp < TEMP_LOW
    both_off = not fan_on and not heater_on
    
    # return dictionary with the results
    return {
        "predicted_temp": round(predicted_temp, 2),
        "fan_on": fan_on,
        "heater_on": heater_on,
        "both_off": both_off
    }