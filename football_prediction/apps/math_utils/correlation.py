from __future__ import annotations

from typing import Sequence

from apps.math_utils.statistics import safe_divide


def pearson_correlation(values_x: Sequence[float], values_y: Sequence[float]) -> float | None:
    if len(values_x) != len(values_y) or len(values_x) < 3:
        return None
    mean_x = sum(values_x) / len(values_x)
    mean_y = sum(values_y) / len(values_y)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(values_x, values_y, strict=False))
    denominator_x = sum((x - mean_x) ** 2 for x in values_x) ** 0.5
    denominator_y = sum((y - mean_y) ** 2 for y in values_y) ** 0.5
    denominator = denominator_x * denominator_y
    return safe_divide(numerator, denominator)


def _rank(values: Sequence[float]) -> list[float]:
    ordered = sorted((value, index) for index, value in enumerate(values))
    ranks = [0.0] * len(values)
    position = 0
    while position < len(ordered):
        end = position
        while end + 1 < len(ordered) and ordered[end + 1][0] == ordered[position][0]:
            end += 1
        average_rank = (position + end + 2) / 2
        for _, index in ordered[position : end + 1]:
            ranks[index] = average_rank
        position = end + 1
    return ranks


def spearman_correlation(values_x: Sequence[float], values_y: Sequence[float]) -> float | None:
    if len(values_x) != len(values_y) or len(values_x) < 3:
        return None
    return pearson_correlation(_rank(values_x), _rank(values_y))


def feature_relationships(dataset: list[dict[str, float]], target_field: str) -> dict[str, dict[str, float | str | None]]:
    if len(dataset) < 3:
        return {
            "message": {
                "pearson": None,
                "spearman": None,
                "note": "Not enough data for reliable correlation.",
            }
        }

    target_values = [float(item[target_field]) for item in dataset if item.get(target_field) is not None]
    if len(target_values) < 3:
        return {
            "message": {
                "pearson": None,
                "spearman": None,
                "note": "Not enough data for reliable correlation.",
            }
        }

    keys = [key for key in dataset[0] if key != target_field]
    relationships: dict[str, dict[str, float | str | None]] = {}
    for key in keys:
        paired = [(float(item[key]), float(item[target_field])) for item in dataset if item.get(key) is not None and item.get(target_field) is not None]
        if len(paired) < 3:
            relationships[key] = {
                "pearson": None,
                "spearman": None,
                "note": "Not enough data for reliable correlation.",
            }
            continue
        values_x = [item[0] for item in paired]
        values_y = [item[1] for item in paired]
        relationships[key] = {
            "pearson": pearson_correlation(values_x, values_y),
            "spearman": spearman_correlation(values_x, values_y),
            "note": "ok",
        }
    return relationships
