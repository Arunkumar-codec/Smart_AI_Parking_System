from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from backend.app.core.logging import logger


class SPMSError(Exception):
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(SPMSError):
    def __init__(self, message="Requested resource was not found.", details=None):
        super().__init__(message, "RESOURCE_NOT_FOUND", 404, details)


class ValidationError(SPMSError):
    def __init__(self, message="Invalid request payload.", details=None):
        super().__init__(message, "VALIDATION_ERROR", 422, details)


class ConflictError(SPMSError):
    def __init__(self, message="Resource state conflict encountered.", details=None):
        super().__init__(message, "RESOURCE_CONFLICT", 409, details)


class AuthorizationError(SPMSError):
    def __init__(self, message="Access denied or insufficient permissions.", details=None):
        super().__init__(message, "UNAUTHORIZED_ACCESS", 403, details)


class BusinessRuleError(SPMSError):
    def __init__(self, message="Business rule constraint violated.", details=None):
        super().__init__(message, "BUSINESS_RULE_VIOLATION", 400, details)


class DatabaseError(SPMSError):
    def __init__(self, message="Database operation failed.", details=None):
        super().__init__(message, "DATABASE_ERROR", 500, details)


class ExternalServiceError(SPMSError):
    def __init__(self, message="External integration failed.", details=None):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", 502, details)


async def spms_exception_handler(request: Request, exc: SPMSError) -> JSONResponse:
    logger.warning(
        "Domain exception: [%s] %s",
        exc.code,
        exc.message,
        extra={"correlation_id": getattr(request.state, "correlation_id", "N/A")},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        }},
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": {
            "code": "VALIDATION_ERROR",
            "message": "Request payload validation failed.",
            "details": {"validation_errors": exc.errors()},
        }},
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    logger.exception(
        "Unhandled SQLAlchemy error",
        extra={"correlation_id": getattr(request.state, "correlation_id", "N/A")},
    )
    return JSONResponse(
        status_code=500,
        content={"error": {
            "code": "DATABASE_ERROR",
            "message": "An internal database error occurred.",
            "details": {},
        }},
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(
        "Unhandled internal server error",
        extra={"correlation_id": getattr(request.state, "correlation_id", "N/A")},
    )
    return JSONResponse(
        status_code=500,
        content={"error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred.",
            "details": {},
        }},
    )
