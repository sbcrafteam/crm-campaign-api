from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

API_KEY = "super-secret-key"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def validate_api_key(api_key: str = Security(api_key_header)):
    """
    Validates the provided API key against the expected value.

    Args:
        api_key (str): Provided API key.

    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )

    return api_key
