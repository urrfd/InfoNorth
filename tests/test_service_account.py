"""Tests for the client-credentials grant and JWT claim decoding."""

from __future__ import annotations

import base64
import time
from urllib.parse import parse_qs

import httpx
import pytest
import respx

from fortnox.client import FortnoxClient
from fortnox.config import TOKEN_URL
from fortnox.errors import FortnoxConfigError, TokenError
from fortnox.oauth import fetch_service_account_token
from fortnox.tokens import MemoryTokenStore, Token, decode_jwt_claims

API = "https://api.fortnox.se/3"

SERVICE_TOKEN_RESPONSE = {
    "access_token": "service-access",
    "expires_in": 3600,
    "scope": "companyinformation customer",
    "token_type": "Bearer",
}


# -- JWT claim decoding --------------------------------------------------


def test_decode_jwt_claims_reads_the_payload(make_jwt):
    token = make_jwt({"tenantId": 123456, "sub": "user-1"})
    assert decode_jwt_claims(token) == {"tenantId": 123456, "sub": "user-1"}


def test_decode_jwt_claims_handles_missing_padding(make_jwt):
    # A payload whose base64 length is not a multiple of 4 must still decode.
    token = make_jwt({"tenantId": 1})
    assert "=" not in token
    assert decode_jwt_claims(token)["tenantId"] == 1


@pytest.mark.parametrize(
    "value",
    ["", "not-a-jwt", "only.two", "a.b.c.d", "a.!!!notbase64!!!.c"],
)
def test_decode_jwt_claims_returns_empty_for_non_jwt(value):
    assert decode_jwt_claims(value) == {}


def test_decode_jwt_claims_returns_empty_for_non_object_payload():
    payload = base64.urlsafe_b64encode(b"[1, 2, 3]").decode().rstrip("=")
    assert decode_jwt_claims(f"header.{payload}.sig") == {}


def test_token_exposes_tenant_id_from_claims(make_jwt):
    token = Token(access_token=make_jwt({"tenantId": 987654}), expires_at=0.0)
    assert token.tenant_id == "987654"


def test_token_tenant_id_accepts_snake_case_claim(make_jwt):
    token = Token(access_token=make_jwt({"tenant_id": "42"}), expires_at=0.0)
    assert token.tenant_id == "42"


def test_token_tenant_id_is_none_when_absent(make_jwt):
    assert Token(access_token=make_jwt({"sub": "x"}), expires_at=0.0).tenant_id is None
    assert Token(access_token="opaque", expires_at=0.0).tenant_id is None


# -- the grant itself ----------------------------------------------------


@respx.mock
def test_service_token_sends_tenant_id_header_and_grant(config):
    config.tenant_id = "123456"
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )

    token = fetch_service_account_token(config)

    request = route.calls.last.request
    assert request.headers["TenantId"] == "123456"
    assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
    expected = base64.b64encode(b"test-client-id:test-client-secret").decode()
    assert request.headers["Authorization"] == f"Basic {expected}"

    body = parse_qs(request.content.decode())
    assert body["grant_type"] == ["client_credentials"]
    # Scope is omitted so Fortnox falls back to the customer's consent.
    assert "scope" not in body

    assert token.access_token == "service-access"


@respx.mock
def test_service_token_has_no_refresh_token(config):
    config.tenant_id = "123456"
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE))

    assert fetch_service_account_token(config).refresh_token == ""


@respx.mock
def test_service_token_can_narrow_scopes(config):
    config.tenant_id = "123456"
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )

    fetch_service_account_token(config, scopes=["companyinformation"])

    body = parse_qs(route.calls.last.request.content.decode())
    assert body["scope"] == ["companyinformation"]


@respx.mock
def test_service_token_accepts_an_explicit_tenant_id(config):
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )

    fetch_service_account_token(config, "999")

    assert route.calls.last.request.headers["TenantId"] == "999"


def test_service_token_requires_a_tenant_id(config):
    with pytest.raises(FortnoxConfigError, match="tenant_id"):
        fetch_service_account_token(config)


def test_authorization_code_flow_still_demands_a_refresh_token():
    """A response without one means access_type=offline was missing."""
    with pytest.raises(TokenError, match="refresh_token"):
        Token.from_response({"access_token": "a", "expires_in": 3600})


# -- client integration --------------------------------------------------


@respx.mock
def test_client_uses_client_credentials_when_tenant_id_is_set(config):
    config.tenant_id = "123456"
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )
    api_route = respx.get(f"{API}/companyinformation").mock(
        return_value=httpx.Response(200, json={"CompanyInformation": {}})
    )

    store = MemoryTokenStore()  # no prior authorization needed
    with FortnoxClient(config, token_store=store) as client:
        assert client.uses_service_account
        client.get("companyinformation")

    assert token_route.called
    assert api_route.calls.last.request.headers["Authorization"] == "Bearer service-access"


@respx.mock
def test_service_account_token_is_cached_between_calls(config):
    config.tenant_id = "123456"
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )
    respx.get(f"{API}/customers").mock(return_value=httpx.Response(200, json={}))

    with FortnoxClient(config, token_store=MemoryTokenStore()) as client:
        client.get("customers")
        client.get("customers")
        client.get("customers")

    assert token_route.call_count == 1


@respx.mock
def test_expired_service_account_token_is_reminted(config):
    config.tenant_id = "123456"
    expired = Token(access_token="old", expires_at=time.time() - 1, obtained_at=time.time() - 3601)
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )
    api_route = respx.get(f"{API}/customers").mock(return_value=httpx.Response(200, json={}))

    with FortnoxClient(config, token_store=MemoryTokenStore(expired)) as client:
        client.get("customers")

    assert token_route.call_count == 1
    assert api_route.calls.last.request.headers["Authorization"] == "Bearer service-access"


@respx.mock
def test_service_account_mode_never_uses_the_refresh_grant(config):
    """A stored refresh token must be ignored once a tenant id is configured."""
    config.tenant_id = "123456"
    stale = Token(access_token="old", refresh_token="stale-refresh", expires_at=time.time() - 1)
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=SERVICE_TOKEN_RESPONSE)
    )
    respx.get(f"{API}/customers").mock(return_value=httpx.Response(200, json={}))

    with FortnoxClient(config, token_store=MemoryTokenStore(stale)) as client:
        client.get("customers")

    body = parse_qs(token_route.calls.last.request.content.decode())
    assert body["grant_type"] == ["client_credentials"]
    assert "refresh_token" not in body


def test_client_defaults_to_the_refresh_grant(config):
    with FortnoxClient(config, token_store=MemoryTokenStore()) as client:
        assert not client.uses_service_account
