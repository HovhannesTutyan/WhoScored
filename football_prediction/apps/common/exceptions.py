from typing import Any

from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler

from apps.common.responses import error_response


class ApiError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "API_ERROR"

    def __init__(self, message: str, *, code: str | None = None, status_code: int | None = None, meta: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.code = code or self.default_code
        if status_code is not None:
            self.status_code = status_code
        self.meta = meta or {}


class NotEnoughDataError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "NOT_ENOUGH_DATA"


class ModelUnavailableError(ApiError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_code = "MODEL_UNAVAILABLE"


def _flatten_validation_errors(detail: Any, prefix: str = "") -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if isinstance(detail, dict):
        for field_name, field_value in detail.items():
            next_prefix = f"{prefix}.{field_name}" if prefix else str(field_name)
            errors.extend(_flatten_validation_errors(field_value, next_prefix))
        return errors

    if isinstance(detail, list):
        for item in detail:
            errors.extend(_flatten_validation_errors(item, prefix))
        return errors

    code = "VALIDATION_ERROR"
    message = f"{prefix}: {detail}" if prefix else str(detail)
    errors.append({"code": code, "message": message})
    return errors


def custom_exception_handler(exc: Exception, context: dict[str, Any]):
    if isinstance(exc, ApiError):
        return error_response(
            [{"code": exc.code, "message": exc.message}],
            status_code=exc.status_code,
            meta=exc.meta,
        )

    response = drf_exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data
    if isinstance(detail, dict) and "detail" in detail:
        errors = [{"code": "API_ERROR", "message": str(detail["detail"])}]
    else:
        errors = _flatten_validation_errors(detail)

    response.data = {
        "success": False,
        "data": None,
        "meta": {},
        "errors": errors,
    }
    return response
