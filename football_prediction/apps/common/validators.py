from typing import Any

from apps.common.exceptions import ApiError


def ensure_numeric(value: Any, *, field_name: str) -> float:
    if value is None:
        raise ApiError(f"{field_name} is required.", code="VALIDATION_ERROR")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ApiError(f"{field_name} must be a valid number.", code="VALIDATION_ERROR") from exc


def ensure_non_negative(value: Any, *, field_name: str) -> float:
    numeric_value = ensure_numeric(value, field_name=field_name)
    if numeric_value < 0:
        raise ApiError(f"{field_name} must be greater than or equal to 0.", code="VALIDATION_ERROR")
    return numeric_value


def ensure_positive(value: Any, *, field_name: str) -> float:
    numeric_value = ensure_numeric(value, field_name=field_name)
    if numeric_value <= 0:
        raise ApiError(f"{field_name} must be greater than 0.", code="VALIDATION_ERROR")
    return numeric_value


def ensure_range(value: int, *, field_name: str, minimum: int, maximum: int) -> int:
    if value < minimum or value > maximum:
        raise ApiError(
            f"{field_name} must be between {minimum} and {maximum}.",
            code="VALIDATION_ERROR",
        )
    return value
