from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.core.exceptions.base import DefaultHTTPException

# Safely attempt to import advanced_alchemy exceptions if database layer exists
try:
    from advanced_alchemy.exceptions import (
        IntegrityError,
        DuplicateKeyError,
        NotFoundError,
    )
    from src.core.exceptions.service import (
        IntegrityErrorException,
        DuplicateKeyException,
        NotFoundException,
    )

    HAS_ALCHEMY = True
except ImportError:
    HAS_ALCHEMY = False


def default_http_exception_handler(
    request: Request, exc: DefaultHTTPException
) -> JSONResponse:
    """
    Format standard DefaultHTTPException subclass errors into consistent API JSON.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": {
                "code": exc.error,
                "details": {
                    "field": exc.field,
                    "message": exc.message,
                },
            },
        },
    )


async def database_exception_handler(request: Request, exc: Exception) -> None:
    """
    Map advanced_alchemy exceptions to DefaultHTTPExceptions.
    """
    if HAS_ALCHEMY:
        if exc.__class__.__name__ == "IntegrityError":
            raise IntegrityErrorException()
        if exc.__class__.__name__ == "DuplicateKeyError":
            raise DuplicateKeyException()
        if exc.__class__.__name__ == "NotFoundError":
            raise NotFoundException()


def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Format validation errors into consistent location, field, and message lists.
    """
    errors = []
    for err in exc.errors():
        location = ".".join(str(loc) for loc in err.get("loc", []))
        field = err.get("loc", [None])[-1]
        errors.append(
            {
                "location": location,
                "field": field,
                "message": err.get("msg", "Invalid input"),
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error": {
                "code": "VALIDATION_ERROR",
                "details": errors,
            },
        },
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Register exception handlers on the FastAPI application instance.
    """
    if HAS_ALCHEMY:
        app.add_exception_handler(IntegrityError, database_exception_handler)
        app.add_exception_handler(DuplicateKeyError, database_exception_handler)
        app.add_exception_handler(NotFoundError, database_exception_handler)

    app.add_exception_handler(DefaultHTTPException, default_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
