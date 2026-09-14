from __future__ import annotations

import base64
from urllib.parse import parse_qs, urlparse

import httpx
import pytest
import respx

from fortnox.config import TOKEN_URL
from fortnox.errors import FortnoxConfigError, RefreshTokenExpiredError, TokenError
from fortnox.oauth import build_authorization_url, exchange_code, refresh_token
from fortnox.tokens import Token

TOKEN_RESPONSE = {
    "access_token": "new-access",
    "refresh_token": "new-refresh",
    "expires_in": 3600,
    "scope": "companyinformation customer",
    "token_type": "Bearer",
}


def test_authorization_url_has_every_required_parameter(config):
    url, state = build_authorization_url(config)
    query = parse_qs(urlparse(url).query)

    assert urlparse(url).netloc == "apps.fortnox.se"
    assert query["client_id"] == ["test-client-id"]
    assert query["redirect_uri"] == ["https://example.test/callback"]
    assert query["scope"] == ["companyinformation customer"]
    assert query["response_type"] == ["code"]
    assert query["access_type"] == ["offline"]
    assert query["account_type"] == ["service"]
    assert query["state"] == [state]


def test_authorization_url_generates_unpredictable_state(config):
    _, first = build_authorization_url(config)
    _, second = build_authorization_url(config)
    assert first != second
    assert len(first) >= 32


def test_authorization_url_accepts_explicit_state_and_scopes(config):
    url, state = build_authorization_url(config, state="fixed", scopes=["invoice"])
    query = parse_qs(urlparse(url).query)
    assert state == "fixed"
    assert query["scope"] == ["invoice"]


def test_authorization_url_can_omit_account_type(config):
    url, _ = build_authorization_url(config, account_type=None)
    assert "account_type" not in parse_qs(urlparse(url).query)


def test_authorization_url_requires_redirect_uri(config):
    config.redirect_uri = ""
    with pytest.raises(FortnoxConfigError, match="redirect_uri"):
        build_authorization_url(config)


def test_authorization_url_requires_a_scope(config):
    config.scopes = []
    with pytest.raises(FortnoxConfigError, match="scope"):
        build_authorization_url(config)


@respx.mock
def test_exchange_code_sends_basic_auth_and_form_body(config):
    route = respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=TOKEN_RESPONSE))

    token = exchange_code(config, "the-code")

    request = route.calls.last.request
    expected = base64.b64encode(b"test-client-id:test-client-secret").decode()
    assert request.headers["Authorization"] == f"Basic {expected}"
    assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"

    body = parse_qs(request.content.decode())
    assert body["grant_type"] == ["authorization_code"]
    assert body["code"] == ["the-code"]
    assert body["redirect_uri"] == ["https://example.test/callback"]

    assert token.access_token == "new-access"
    assert token.refresh_token == "new-refresh"
    assert token.scopes == ("companyinformation", "customer")


@respx.mock
def test_refresh_token_rotates_the_refresh_token(config):
    route = respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=TOKEN_RESPONSE))
    old = Token(
        access_token="old-access", refresh_token="old-refresh", expires_at=0.0, obtained_at=0.0
    )

    new = refresh_token(config, old)

    body = parse_qs(route.calls.last.request.content.decode())
    assert body["grant_type"] == ["refresh_token"]
    assert body["refresh_token"] == ["old-refresh"]
    assert new.refresh_token == "new-refresh"
    assert new.refresh_token != old.refresh_token


@respx.mock
def test_refresh_keeps_previous_scopes_when_response_omits_them(config):
    payload = dict(TOKEN_RESPONSE)
    payload.pop("scope")
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=payload))
    old = Token(
        access_token="a",
        refresh_token="r",
        expires_at=0.0,
        scopes=("invoice", "order"),
        obtained_at=0.0,
    )

    assert refresh_token(config, old).scopes == ("invoice", "order")


@respx.mock
def test_used_refresh_token_raises_unrecoverable_error(config):
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(
            400,
            json={"error": "invalid_grant", "error_description": "Refresh token has expired"},
        )
    )
    old = Token(access_token="a", refresh_token="r", expires_at=0.0)

    with pytest.raises(RefreshTokenExpiredError, match="authorized again"):
        refresh_token(config, old)


@respx.mock
def test_server_side_token_failure_is_retryable_token_error(config):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(503, json={"error": "server_error"}))
    old = Token(access_token="a", refresh_token="r", expires_at=0.0)

    with pytest.raises(TokenError) as exc_info:
        refresh_token(config, old)
    assert not isinstance(exc_info.value, RefreshTokenExpiredError)
