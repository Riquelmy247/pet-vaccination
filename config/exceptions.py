from typing import Any

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """
    Global DRF exception handler that wraps default behavior
    and ensures consistent error responses.
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, Http404):
        return Response(
            {"detail": "Not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ValidationError):
        return Response(
            {"detail": exc.detail},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"detail": "Internal server error."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

