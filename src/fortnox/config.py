"""Configuration for the Fortnox client, loadable from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path

from .errors import FortnoxConfigError

# Fortnox OAuth2 and API endpoints.
AUTHORIZE_URL = "https://apps.fortnox.se/oauth-v1/auth"
TOKEN_URL = "https://apps.fortnox.se/oauth-v1/token"
API_BASE_URL = "https://api.fortnox.se/3"

# Fortnox enforces a sliding window of 25 requests per 5 seconds per
# access token (300/minute per client-id and tenant).
RATE_LIMIT_REQUESTS = 25
RATE_LIMIT_WINDOW_SECONDS = 5.0

# Fortnox caps list endpoints at 500 records per page and defaults to 100.
MAX_PAGE_LIMIT = 500
DEFAULT_PAGE_LIMIT = 100

# Access tokens live for one hour. Refresh this many seconds before expiry so a
# request is never sent with a token that expires mid-flight.
DEFAULT_REFRESH_LEEWAY_SECONDS = 120


def _env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name, default)
    if value is not None:
        value = value.strip()
    return value or default


@dataclass(slots=True)
class FortnoxConfig:
    """Everything the client needs to talk to Fortnox.

    Attributes:
        client_id: The Client-ID from your Fortnox developer portal integration.
        client_secret: The Client-Secret from the same integration.
        redirect_uri: Must match the redirect URI registered in the portal exactly.
        scopes: Scopes to request during authorization, e.g. ``["customer", "invoice"]``.
        token_path: Where the token file is persisted.
        tenant_id: The customer's Fortnox tenant (their ``DatabaseNumber``). Setting
            it switches the client to the client-credentials grant, which mints
            access tokens on demand and needs no refresh token at all. Only works
            for customers who activated with ``account_type=service``.
    """

    client_id: str
    client_secret: str
    redirect_uri: str = ""
    scopes: list[str] = field(default_factory=list)
    token_path: str = "fortnox_token.json"
    tenant_id: str | None = None

    authorize_url: str = AUTHORIZE_URL
    token_url: str = TOKEN_URL
    api_base_url: str = API_BASE_URL

    timeout: float = 30.0
    max_retries: int = 4
    refresh_leeway_seconds: int = DEFAULT_REFRESH_LEEWAY_SECONDS
    rate_limit_requests: int = RATE_LIMIT_REQUESTS
    rate_limit_window: float = RATE_LIMIT_WINDOW_SECONDS

    def __post_init__(self) -> None:
        if not self.client_id:
            raise FortnoxConfigError("client_id is required")
        if not self.client_secret:
            raise FortnoxConfigError("client_secret is required")
        self.api_base_url = self.api_base_url.rstrip("/")

    def for_tenant(self, tenant_id: str, *, token_path: str | None = None) -> FortnoxConfig:
        """Return a copy of this config scoped to one customer's tenant.

        A token store must never be shared between tenants: the refresh token is
        single-use, so two tenants behind one file race each other, and one
        customer reconnecting would overwrite another's state. This derives a
        distinct path per tenant - ``fortnox_token.json`` becomes
        ``fortnox_token.123456.json`` - and sets ``tenant_id`` so the
        client-credentials grant is used where it is available.

        Example:
            >>> base = FortnoxConfig.from_env()
            >>> for tenant in ("123456", "789012"):
            ...     client = FortnoxClient(base.for_tenant(tenant))
        """
        if not tenant_id:
            raise FortnoxConfigError("tenant_id must not be empty")

        if token_path is None:
            path = Path(self.token_path)
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(tenant_id))
            token_path = str(path.with_name(f"{path.stem}.{safe}{path.suffix}"))

        return replace(self, tenant_id=str(tenant_id), token_path=token_path)

    @classmethod
    def from_env(cls, **overrides: object) -> FortnoxConfig:
        """Build a config from ``FORTNOX_*`` environment variables.

        Reads FORTNOX_CLIENT_ID, FORTNOX_CLIENT_SECRET, FORTNOX_REDIRECT_URI,
        FORTNOX_SCOPES (space or comma separated), FORTNOX_TOKEN_PATH and
        FORTNOX_TENANT_ID. Any keyword argument overrides the corresponding
        environment value.
        """
        client_id = _env("FORTNOX_CLIENT_ID")
        client_secret = _env("FORTNOX_CLIENT_SECRET")
        if not client_id:
            raise FortnoxConfigError("FORTNOX_CLIENT_ID is not set")
        if not client_secret:
            raise FortnoxConfigError("FORTNOX_CLIENT_SECRET is not set")

        raw_scopes = _env("FORTNOX_SCOPES", "") or ""
        scopes = [s for s in raw_scopes.replace(",", " ").split() if s]

        values: dict[str, object] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": _env("FORTNOX_REDIRECT_URI", "") or "",
            "scopes": scopes,
            "token_path": _env("FORTNOX_TOKEN_PATH", "fortnox_token.json"),
            "tenant_id": _env("FORTNOX_TENANT_ID"),
        }
        values.update(overrides)
        return cls(**values)  # type: ignore[arg-type]
