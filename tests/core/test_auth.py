import pytest
from fastapi import HTTPException
from app.core.auth import validate_api_key, API_KEY, API_KEY_NAME

def test_validate_api_key_success():
    key = API_KEY
    result = validate_api_key(api_key=key)
    assert result == API_KEY

def test_validate_api_key_missing():
    with pytest.raises(HTTPException) as exc_info:
        validate_api_key(api_key=None)
    assert exc_info.value.status_code == 401
    assert "Invalid API Key" in exc_info.value.detail

def test_validate_api_key_invalid():
    with pytest.raises(HTTPException) as exc_info:
        validate_api_key(api_key="wrong-key")
    assert exc_info.value.status_code == 401
    assert "Invalid API Key" in exc_info.value.detail
