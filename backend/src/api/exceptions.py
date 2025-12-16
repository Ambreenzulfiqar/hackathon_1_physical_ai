from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[dict] = None

# Custom exceptions for the application
class TextbookException(HTTPException):
    def __init__(self, detail: str, code: str = "GENERAL_ERROR", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(
            status_code=status_code,
            detail=detail
        )
        self.code = code

class ResourceNotFoundError(TextbookException):
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            detail=f"{resource_type} with ID {resource_id} not found",
            code="RESOURCE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ValidationError(TextbookException):
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class RateLimitExceededError(TextbookException):
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            detail=detail,
            code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

class InternalError(TextbookException):
    def __init__(self, detail: str = "An internal error occurred"):
        super().__init__(
            detail=detail,
            code="INTERNAL_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class UnauthorizedError(TextbookException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(
            detail=detail,
            code="UNAUTHORIZED",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

# Exception handlers for FastAPI
async def http_exception_handler(request, exc):
    return {
        "error": str(exc.detail) if hasattr(exc, 'detail') else "An error occurred",
        "code": getattr(exc, 'code', 'HTTP_ERROR'),
        "status_code": exc.status_code
    }

async def validation_exception_handler(request, exc):
    return {
        "error": "Validation error",
        "code": "VALIDATION_ERROR",
        "details": exc.errors() if hasattr(exc, 'errors') else None
    }

async def general_exception_handler(request, exc):
    return {
        "error": "An internal server error occurred",
        "code": "INTERNAL_ERROR",
        "details": str(exc) if str(exc) else None
    }