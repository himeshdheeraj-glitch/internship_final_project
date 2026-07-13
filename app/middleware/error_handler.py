from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppException
from app.core.logging import logger
from app.core.responses import APIResponse

def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(f"AppException: status_code={exc.status_code} message={exc.message} details={exc.details}")
        response_model = APIResponse(
            success=False,
            message=exc.message,
            data=exc.details
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response_model.model_dump(),
            headers=exc.headers
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(f"ValidationError: {exc.errors()}")
        response_model = APIResponse(
            success=False,
            message="Validation error",
            data=exc.errors()
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response_model.model_dump()
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.error(f"Database Error: {str(exc)}", exc_info=True)
        response_model = APIResponse(
            success=False,
            message="Database operational error occurred",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response_model.model_dump()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled Error: {str(exc)}", exc_info=True)
        response_model = APIResponse(
            success=False,
            message="Internal server error",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response_model.model_dump()
        )
