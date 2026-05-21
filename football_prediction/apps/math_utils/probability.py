from __future__ import annotations

from typing import Mapping


def normalize_probability_map(values: Mapping[str, float]) -> dict[str, float]:
    total = sum(values.values())
    if total <= 0:
        return {key: 0.0 for key in values}
    return {key: value / total for key, value in values.items()}


def redistribute_weights(weights: Mapping[str, float], available_keys: list[str]) -> dict[str, float]:
    available = {key: weights[key] for key in available_keys if key in weights}
    total = sum(available.values())
    if total <= 0:
        return {key: 0.0 for key in available_keys}
    return {key: value / total for key, value in available.items()}
