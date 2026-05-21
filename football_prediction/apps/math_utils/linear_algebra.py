from __future__ import annotations

from math import sqrt
from typing import Iterable, Sequence


def feature_vector(source: dict[str, float | int | None], fields: Iterable[str]) -> list[float]:
    return [float(source.get(field) or 0.0) for field in fields]


def dot_product(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    return sum(left * right for left, right in zip(vector_a, vector_b, strict=False))


def cosine_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    numerator = dot_product(vector_a, vector_b)
    magnitude_a = sqrt(dot_product(vector_a, vector_a))
    magnitude_b = sqrt(dot_product(vector_b, vector_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return numerator / (magnitude_a * magnitude_b)


def euclidean_distance(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    return sqrt(sum((left - right) ** 2 for left, right in zip(vector_a, vector_b, strict=False)))


def manhattan_distance(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    return sum(abs(left - right) for left, right in zip(vector_a, vector_b, strict=False))
