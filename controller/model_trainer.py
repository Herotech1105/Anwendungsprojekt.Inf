import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 1. Load your CSV data
# Assuming the file is named 'weather_data.csv'
df = pd.read_csv('Messdaten2.csv')

# Extract only the target features (ignoring the timestamp string)
data = df[['temperature', 'humidity']].values

# 2. Define manual scaler parameters to match inference setup
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.data_min_ = np.array([0.0, 0.0])
scaler.data_max_ = np.array([100.0, 100.0])
scaler.data_range_ = scaler.data_max_ - scaler.data_min_
scaler.scale_ = 1.0 / scaler.data_range_
scaler.min_ = -scaler.data_min_ * scaler.scale_

# Scale the dataset
scaled_data = scaler.transform(data)

# 3. Create sliding windows
SEQ_LEN = 10

X, y = [], []
for i in range(len(scaled_data) - SEQ_LEN):
    X.append(scaled_data[i:(i + SEQ_LEN), :])  # Input: Past 10 timesteps
    y.append(scaled_data[i + SEQ_LEN, :])      # Target: Next 1 timestep [Temp, Hum]

X = np.array(X)
y = np.array(y)

# 4. Build and train the LSTM
model = Sequential([
    # Input shape: (10 timesteps, 2 features)
    LSTM(64, activation='tanh', input_shape=(SEQ_LEN, 2), return_sequences=False),
    Dense(32, activation='relu'),
    Dense(2)  # Outputs 2 features: [predicted_temp, predicted_hum]
])

model.compile(optimizer='adam', loss='mse')

# Train model
model.fit(X, y, epochs=15, batch_size=32, verbose=1)

# Save the model exactly where your inference script looks for it
model.save("train.keras")
print("Model saved successfully as train.keras!")