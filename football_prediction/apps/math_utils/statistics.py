from __future__ import annotations

from typing import Iterable


def coalesce_number(value: float | int | None, default: float = 0.0) -> float:
    if value is None:
        return default
    return float(value)


def safe_divide(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator) / float(denominator)


def safe_subtract(left: float | int | None, right: float | int | None) -> float | None:
    if left is None or right is None:
        return None
    return float(left) - float(right)


def average(values: Iterable[float | int | None]) -> float | None:
    numeric_values = [float(value) for value in values if value is not None]
    if not numeric_values:
        return None
    return sum(numeric_values) / len(numeric_values)


def weighted_average(pairs: dict[str, tuple[float | None, float]]) -> float | None:
    available = {key: value for key, value in pairs.items() if value[0] is not None and value[1] > 0}
    if not available:
        return None
    total_weight = sum(weight for _, weight in available.values())
    return sum(float(score) * weight for score, weight in available.values()) / total_weight


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))
