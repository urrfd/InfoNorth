"""Fortnox OAuth2 authentication and REST API client.

Quick start:
    >>> from fortnox import FortnoxClient, FortnoxConfig
    >>> config = FortnoxConfig.from_env()
    >>> with FortnoxClient(config) as client:
    ...     print(client.get("companyinformation"))
"""

from .client import FortnoxClient
from .config import FortnoxConfig
from .errors import (
    AuthenticationError,
    AuthorizationError,
    FortnoxAPIError,
    FortnoxConfigError,
    FortnoxError,
    NotFoundError,
    NoTokenError,
    RateLimitError,
    RefreshTokenExpiredError,
    ServerError,
    TokenError,
)
from .oauth import (
    build_authorization_url,
    exchange_code,
    fetch_service_account_token,
    refresh_token,
)
from .tokens import (
    FileTokenStore,
    MemoryTokenStore,
    Token,
    TokenStore,
    decode_jwt_claims,
)

__version__ = "0.1.0"

__all__ = [
    "AuthenticationError",
    "AuthorizationError",
    "FileTokenStore",
    "FortnoxAPIError",
    "FortnoxClient",
    "FortnoxConfig",
    "FortnoxConfigError",
    "FortnoxError",
    "MemoryTokenStore",
    "NoTokenError",
    "NotFoundError",
    "RateLimitError",
    "RefreshTokenExpiredError",
    "ServerError",
    "Token",
    "TokenError",
    "TokenStore",
    "build_authorization_url",
    "decode_jwt_claims",
    "exchange_code",
    "fetch_service_account_token",
    "refresh_token",
]
