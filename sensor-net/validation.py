"""Validierung der MQTT-Sensor-Payloads."""

from __future__ import annotations

import json
from typing import Optional, Tuple

from config import (
    TEMP_MIN, TEMP_MAX, HUM_MIN, HUM_MAX, log,
)


def parse_and_validate(raw: bytes) -> Optional[Tuple[float, float]]:
    """Dekodiert MQTT-Payload und gibt (temperature, humidity) zurueck.

    None bei ungueltigen oder unplausiblen Daten.
    """
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        log.warning("Verwerfe nicht-JSON-Nachricht: %s", exc)
        return None

    if not isinstance(data, dict):
        log.warning("Verwerfe Payload (kein Objekt): %r", data)
        return None

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (KeyError, TypeError, ValueError):
        log.warning("temperature/humidity fehlt oder ungueltig: %r", data)
        return None

    if not (TEMP_MIN <= temperature <= TEMP_MAX):
        log.warning(
            "Temperatur %.1f ausserhalb [%.1f, %.1f]",
            temperature, TEMP_MIN, TEMP_MAX,
        )
        return None

    if not (HUM_MIN <= humidity <= HUM_MAX):
        log.warning(
            "Luftfeuchtigkeit %.1f ausserhalb [%.1f, %.1f]",
            humidity, HUM_MIN, HUM_MAX,
        )
        return None

    return temperature, humidity
