from __future__ import annotations

from math import sqrt
from typing import Sequence


def _clean_values(values: Sequence[float | int | None]) -> list[float]:
    return [float(value) for value in values if value is not None]


def min_max_normalize(value: float | int | None, values: Sequence[float | int | None], *, reverse: bool = False) -> float | None:
    numeric_values = _clean_values(values)
    if value is None or not numeric_values:
        return None
    minimum = min(numeric_values)
    maximum = max(numeric_values)
    if minimum == maximum:
        score = 0.5
    else:
        score = (float(value) - minimum) / (maximum - minimum)
    return 1.0 - score if reverse else score


def reverse_normalize(value: float | int | None, values: Sequence[float | int | None]) -> float | None:
    return min_max_normalize(value, values, reverse=True)


def z_score_normalize(value: float | int | None, values: Sequence[float | int | None]) -> float | None:
    numeric_values = _clean_values(values)
    if value is None or len(numeric_values) < 2:
        return None
    mean = sum(numeric_values) / len(numeric_values)
    variance = sum((item - mean) ** 2 for item in numeric_values) / len(numeric_values)
    std_dev = sqrt(variance)
    if std_dev == 0:
        return 0.0
    return (float(value) - mean) / std_dev


def percentile_rank(value: float | int | None, values: Sequence[float | int | None], *, reverse: bool = False) -> float | None:
    numeric_values = sorted(_clean_values(values))
    if value is None or not numeric_values:
        return None
    count_less_or_equal = sum(1 for item in numeric_values if item <= float(value))
    percentile = count_less_or_equal / len(numeric_values)
    return 1.0 - percentile if reverse else percentile
