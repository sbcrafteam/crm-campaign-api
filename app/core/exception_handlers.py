from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.models.error import ErrorResponse
import logging

logger = logging.getLogger("uvicorn.error")

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unexpected exceptions.

    Args:
        request (Request): The incoming request object.
        exc (Exception): The exception that was raised.

    Returns:
        JSONResponse: A 500 Internal Server Error response.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code=500,
            message="Internal Server Error",
            detail=str(exc)
        ).model_dump()
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler for FastAPI HTTPExceptions.

    Args:
        request (Request): The request that caused the exception.
        exc (HTTPException): The HTTPException instance.

    Returns:
        JSONResponse: A structured error response with HTTPException details.
    """
    logger.error(f"HTTPException raised: {exc}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=exc.status_code,
            message="HTTP Error",
            detail=exc.detail if isinstance(exc.detail, str) else str(exc.detail)
        ).model_dump()
    )
