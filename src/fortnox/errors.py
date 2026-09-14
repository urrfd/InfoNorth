"""Exception hierarchy for the Fortnox client."""

from __future__ import annotations

from typing import Any


class FortnoxError(Exception):
    """Base class for every error raised by this package."""


class FortnoxConfigError(FortnoxError):
    """Raised when required configuration is missing or malformed."""


class TokenError(FortnoxError):
    """Base class for token lifecycle problems."""


class NoTokenError(TokenError):
    """Raised when no token has been stored yet - the app was never authorized."""


class RefreshTokenExpiredError(TokenError):
    """Raised when the refresh token is rejected by Fortnox.

    Fortnox refresh tokens are single-use and valid for 45 days. Once one is
    rejected the only recovery is to send the user through the authorization
    flow again; no amount of retrying will help.
    """


class FortnoxAPIError(FortnoxError):
    """An error response from the Fortnox REST API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        code: int | None = None,
        payload: Any = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.payload = payload
        self.request_id = request_id

    def __str__(self) -> str:
        parts = [f"HTTP {self.status_code}"]
        if self.code is not None:
            parts.append(f"Fortnox code {self.code}")
        if self.request_id:
            parts.append(f"request {self.request_id}")
        return f"{self.message} ({', '.join(parts)})"


class AuthenticationError(FortnoxAPIError):
    """401 - the access token is missing, expired or invalid."""


class AuthorizationError(FortnoxAPIError):
    """403 - the token is valid but lacks the scope for this endpoint."""


class NotFoundError(FortnoxAPIError):
    """404 - the requested resource does not exist."""


class RateLimitError(FortnoxAPIError):
    """429 - the rate limit was exceeded and retries were exhausted."""

    def __init__(self, message: str, *, retry_after: float | None = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(FortnoxAPIError):
    """5xx - Fortnox failed to process the request."""
