from fastapi import Header, HTTPException, status
from typing import Optional

from app.core.config import get_settings


def api_key_auth(x_api_key: Optional[str] = Header(default=None)) -> None:
    """
    Simple API key authentication dependency.

    This is intentionally minimal and can later be replaced
    with OAuth2, JWT, or HMAC verification without changing handlers.
    """
    settings = get_settings()

    # For now, allow unauthenticated access in development
    if settings.environment == "development":
        return

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    # Placeholder: replace with real key validation
    if x_api_key != "expected-api-key":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
