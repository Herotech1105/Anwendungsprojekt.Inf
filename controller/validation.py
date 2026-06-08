"""Validation of MQTT sensor payloads."""

from __future__ import annotations

import json
from typing import Optional, Tuple

from config import (
    TEMP_MIN, TEMP_MAX, HUM_MIN, HUM_MAX, log,
)


def parse_and_validate(raw: bytes) -> Optional[Tuple[float, float]]:
    """Decode MQTT payload and return (temperature, humidity).

    Returns None for invalid or implausible data.
    """
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        log.warning("Discarding non-JSON message: %s", exc)
        return None

    if not isinstance(data, dict):
        log.warning("Discarding payload (not an object): %r", data)
        return None

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (KeyError, TypeError, ValueError):
        log.warning("temperature/humidity missing or invalid: %r", data)
        return None

    if not (TEMP_MIN <= temperature <= TEMP_MAX):
        log.warning(
            "Temperature %.1f outside range [%.1f, %.1f]",
            temperature, TEMP_MIN, TEMP_MAX,
        )
        return None

    if not (HUM_MIN <= humidity <= HUM_MAX):
        log.warning(
            "Humidity %.1f outside range [%.1f, %.1f]",
            humidity, HUM_MIN, HUM_MAX,
        )
        return None

    return temperature, humidity
