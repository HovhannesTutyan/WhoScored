from apps.common.exceptions import ApiError


def validate_line_value(line: float) -> float:
    if line <= 0:
        raise ApiError("line must be a valid number greater than 0.", code="VALIDATION_ERROR")
    return line
