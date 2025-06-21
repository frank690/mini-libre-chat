"""
Exception Handling. This module defines custom exception handlers for the API.
"""

__all__ = ["validation_exception_handler"]

from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.requests import Request
from mini_libre_chat.utils import create_logger

logger = create_logger("exceptions")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return await request_validation_exception_handler(request, exc)
