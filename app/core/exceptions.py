from typing import Any, Dict, Optional

class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.details = details
        self.headers = headers
        super().__init__(self.message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None) -> None:
        super().__init__(status_code=404, message=message, details=details)

class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details: Optional[Any] = None) -> None:
        super().__init__(status_code=400, message=message, details=details)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Could not validate credentials", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=401,
            message=message,
            details=details,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(AppException):
    def __init__(self, message: str = "Not enough permissions", details: Optional[Any] = None) -> None:
        super().__init__(status_code=403, message=message, details=details)

class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists", details: Optional[Any] = None) -> None:
        super().__init__(status_code=409, message=message, details=details)

class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", details: Optional[Any] = None) -> None:
        super().__init__(status_code=422, message=message, details=details)
