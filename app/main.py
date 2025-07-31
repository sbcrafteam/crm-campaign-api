from fastapi import FastAPI, Depends
from app.routers import campaigns, segments
from app.core.auth import validate_api_key
from app.core.exception_handlers import (
    generic_exception_handler,
    http_exception_handler,
)
from app.models.error import ErrorResponse
from fastapi.exceptions import HTTPException

app = FastAPI(title="CRM Campaign API")

# Include routers with API key validation dependency
app.include_router(campaigns.router, dependencies=[Depends(validate_api_key)])
app.include_router(segments.router, dependencies=[Depends(validate_api_key)])

# Register exception handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
