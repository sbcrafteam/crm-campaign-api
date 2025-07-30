import pytest
from fastapi import HTTPException
from fastapi.requests import Request
from app.core.exception_handlers import generic_exception_handler, http_exception_handler
from app.models.error import ErrorResponse

class DummyRequest:
    pass

@pytest.mark.asyncio
async def test_generic_exception_handler():
    exc = Exception("Unexpected error")
    response = await generic_exception_handler(DummyRequest(), exc)

    assert response.status_code == 500
    content = response.body.decode()
    assert "Internal Server Error" in content
    assert "Unexpected error" in content

@pytest.mark.asyncio
async def test_http_exception_handler():
    exc = HTTPException(status_code=404, detail="Not Found")
    response = await http_exception_handler(DummyRequest(), exc)

    assert response.status_code == 404
    content = response.body.decode()
    assert "HTTP Error" in content
    assert "Not Found" in content
