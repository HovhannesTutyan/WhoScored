from typing import Any

from rest_framework import status
from rest_framework.response import Response


def build_payload(*, success: bool, data: Any, meta: dict[str, Any] | None = None, errors: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "success": success,
        "data": data,
        "meta": meta or {},
        "errors": errors or [],
    }


def success_response(data: Any, meta: dict[str, Any] | None = None, status_code: int = status.HTTP_200_OK) -> Response:
    return Response(build_payload(success=True, data=data, meta=meta), status=status_code)


def error_response(errors: list[dict[str, Any]], status_code: int = status.HTTP_400_BAD_REQUEST, meta: dict[str, Any] | None = None) -> Response:
    return Response(build_payload(success=False, data=None, meta=meta, errors=errors), status=status_code)
