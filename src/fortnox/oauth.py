"""OAuth2 authorization-code flow against Fortnox.

Flow, per the Fortnox developer documentation:

1. Send the user to :func:`build_authorization_url`. They approve the
   integration inside Fortnox.
2. Fortnox redirects back to your ``redirect_uri`` with ``code`` and ``state``.
   The code is valid for 10 minutes and can only be used once.
3. Exchange it with :func:`exchange_code` for an access token (1 hour) and a
   refresh token (45 days, single-use).
4. Call :func:`refresh_token` before the access token expires. Persist the new
   refresh token from the response - the old one is dead the moment it is used.
"""

from __future__ import annotations

import base64
import secrets
from typing import Any
from urllib.parse import urlencode

import httpx

from .config import FortnoxConfig
from .errors import FortnoxConfigError, RefreshTokenExpiredError, TokenError
from .tokens import Token

# Fortnox rejects a refresh token with these OAuth2 error codes when it has been
# used, revoked or has expired. None of them are retryable.
_UNRECOVERABLE_ERRORS = {"invalid_grant", "invalid_request", "unauthorized_client"}


def build_authorization_url(
    config: FortnoxConfig,
    *,
    state: str | None = None,
    scopes: list[str] | None = None,
    account_type: str | None = "service",
) -> tuple[str, str]:
    """Build the URL the user visits to authorize the integration.

    Args:
        config: Client configuration; ``redirect_uri`` must be set and must
            match the value registered in the Fortnox developer portal exactly.
        state: CSRF token. Generated with :func:`secrets.token_urlsafe` if
            omitted. Store it and compare it against the value Fortnox sends back.
        scopes: Scopes to request. Defaults to ``config.scopes``.
        account_type: ``"service"`` creates a service account, which is what you
            want for unattended integrations. Pass ``None`` to omit it.

    Returns:
        A ``(url, state)`` pair.
    """
    if not config.redirect_uri:
        raise FortnoxConfigError("redirect_uri must be set to build an authorization URL")

    requested = scopes if scopes is not None else config.scopes
    if not requested:
        raise FortnoxConfigError("at least one scope must be requested")

    state = state or secrets.token_urlsafe(32)
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": " ".join(requested),
        "state": state,
        "access_type": "offline",  # required to receive a refresh token
        "response_type": "code",
    }
    if account_type:
        params["account_type"] = account_type

    return f"{config.authorize_url}?{urlencode(params)}", state


def _basic_auth_header(config: FortnoxConfig) -> str:
    raw = f"{config.client_id}:{config.client_secret}".encode()
    return "Basic " + base64.b64encode(raw).decode("ascii")


def _post_token(
    config: FortnoxConfig,
    data: dict[str, str],
    *,
    client: httpx.Client | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    headers = {
        "Authorization": _basic_auth_header(config),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    if client is not None:
        response = client.post(config.token_url, data=data, headers=headers)
    else:
        with httpx.Client(timeout=config.timeout) as own_client:
            response = own_client.post(config.token_url, data=data, headers=headers)

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    if response.is_success:
        return payload

    error = str(payload.get("error", "")) or f"http_{response.status_code}"
    description = payload.get("error_description") or response.text.strip()
    message = f"Fortnox token request failed: {error}"
    if description:
        message = f"{message} - {description}"

    if error in _UNRECOVERABLE_ERRORS or response.status_code in (400, 401):
        raise RefreshTokenExpiredError(f"{message}. The integration must be authorized again.")
    raise TokenError(message)


def exchange_code(config: FortnoxConfig, code: str, *, client: httpx.Client | None = None) -> Token:
    """Exchange an authorization code for a token pair.

    The code expires 10 minutes after it is issued and works exactly once.
    """
    if not config.redirect_uri:
        raise FortnoxConfigError("redirect_uri is required to exchange an authorization code")

    payload = _post_token(
        config,
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.redirect_uri,
        },
        client=client,
    )
    return Token.from_response(payload)


def fetch_service_account_token(
    config: FortnoxConfig,
    tenant_id: str | None = None,
    *,
    scopes: list[str] | None = None,
    client: httpx.Client | None = None,
) -> Token:
    """Mint an access token with the client-credentials grant.

    This is the better path for unattended integrations. Instead of guarding a
    single-use refresh token for 45 days, a fresh access token can be minted at
    any time from the client id, client secret and tenant id - there is no
    refresh token to rotate, lose, or race on.

    It requires the customer to have activated with ``account_type=service``,
    which :func:`build_authorization_url` requests by default. The consent from
    that activation is what this grant draws on.

    Args:
        tenant_id: The customer's tenant, sent in the ``TenantId`` header.
            Defaults to ``config.tenant_id``. It is the same value as
            ``DatabaseNumber`` from ``/3/companyinformation``, and is also a
            claim on any access token you already hold.
        scopes: Scopes to request. If omitted, Fortnox uses the scopes from the
            customer's consent.
    """
    tenant_id = tenant_id or config.tenant_id
    if not tenant_id:
        raise FortnoxConfigError(
            "tenant_id is required for the client-credentials grant "
            "(set FORTNOX_TENANT_ID, or read DatabaseNumber from /3/companyinformation)"
        )

    data = {"grant_type": "client_credentials"}
    requested = scopes if scopes is not None else None
    if requested:
        data["scope"] = " ".join(requested)

    payload = _post_token(config, data, client=client, extra_headers={"TenantId": str(tenant_id)})
    # This grant returns no refresh token - that is the whole point of it.
    return Token.from_response(payload, require_refresh_token=False)


def refresh_token(
    config: FortnoxConfig, token: Token, *, client: httpx.Client | None = None
) -> Token:
    """Trade a refresh token for a fresh token pair.

    The returned token carries a *new* refresh token; the one passed in is now
    invalid. Persist the result before doing anything else, or the integration
    will be locked out and need re-authorization.
    """
    payload = _post_token(
        config,
        {"grant_type": "refresh_token", "refresh_token": token.refresh_token},
        client=client,
    )
    new_token = Token.from_response(payload)
    # Fortnox always rotates the refresh token, but fall back to the previous
    # scopes if the response omits them so we do not lose that metadata.
    if not new_token.scopes and token.scopes:
        new_token = new_token.replace(scopes=token.scopes)
    return new_token
