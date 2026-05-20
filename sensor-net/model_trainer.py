import argparse
import csv
import os

import numpy as np
from tensorflow.keras.callbacks import EarlyStopping

from lstm_handler import SEQ_LEN, build_model

DEFAULT_WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "weights", "lstm_weights.weights.h5")


def load_csv_data(csv_file, temp_col=0, humidity_col=1, skip_header=False):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV-Datei nicht gefunden: {csv_file}")
    rows = []
    with open(csv_file, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)
        for line_no, row in enumerate(reader, start=2 if skip_header else 1):
            if len(row) <= max(temp_col, humidity_col):
                if len(row) == 0 or all(not cell.strip() for cell in row):
                    continue
                raise ValueError(f"Zeile {line_no} hat zu wenige Spalten: {len(row)}")
            try:
                temp = float(row[temp_col])
                humidity = float(row[humidity_col])
            except ValueError:
                continue
            rows.append((temp, humidity))
    if not rows:
        raise ValueError("Keine verwertbaren Messdaten in der CSV-Datei gefunden.")
    return np.array(rows, dtype=np.float32)


def build_sequences(data):
    if len(data) <= SEQ_LEN:
        raise ValueError(f"Mindestens {SEQ_LEN + 1} Zeilen erforderlich, aber nur {len(data)} gefunden.")
    X = [data[i : i + SEQ_LEN] for i in range(len(data) - SEQ_LEN)]
    y = [data[i + SEQ_LEN, 0] for i in range(len(data) - SEQ_LEN)]
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32).reshape(-1, 1)


def train_model(csv_file, weights_file, temp_col, humidity_col, skip_header, epochs, batch_size, validation_split):
    data = load_csv_data(csv_file, temp_col=temp_col, humidity_col=humidity_col, skip_header=skip_header)
    X, y = build_sequences(data)

    split = int(len(X) * (1 - validation_split))
    if split < 1:
        raise ValueError("Zu wenig Daten für die gewählte Validierungsgröße.")

    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]

    model = build_model()

    print(f"Trainingsdaten: {X_train.shape}, Validierungsdaten: {X_val.shape}")

    callbacks = [EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)]

    history = model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=2,
    )

    model.save_weights(weights_file)
    print(f"Gewichte gespeichert in: {weights_file}")
    return history


def parse_args():
    parser = argparse.ArgumentParser(description="Trainiere das LSTM-Modell auf CSV-Daten.")
    parser.add_argument("csv_file", help="Pfad zur Eingabe-CSV.")
    parser.add_argument("--weights-file", default=DEFAULT_WEIGHTS_PATH, help="Gewichtsdatei.")
    parser.add_argument("--temp-col", type=int, default=0, help="Temperatur-Spalte.")
    parser.add_argument("--humidity-col", type=int, default=1, help="Feuchte-Spalte.")
    parser.add_argument("--skip-header", action="store_true", help="Header überspringen.")
    parser.add_argument("--epochs", type=int, default=50, help="Epochen.")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch-Größe.")
    parser.add_argument("--validation-split", type=float, default=0.2, help="Validierungsanteil.")
    return parser.parse_args()


if __name__ == "__main__":
    # Hauptskript: Argumente parsen und Training starten.
    args = parse_args()
    os.makedirs(os.path.dirname(args.weights_file), exist_ok=True)
    train_model(
        args.csv_file,
        args.weights_file,
        temp_col=args.temp_col,
        humidity_col=args.humidity_col,
        skip_header=args.skip_header,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=args.validation_split,
    )
