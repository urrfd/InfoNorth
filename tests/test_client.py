from __future__ import annotations

import threading
import time

import httpx
import pytest
import respx

import fortnox.client as fortnox_client
from fortnox.client import FortnoxClient
from fortnox.config import TOKEN_URL
from fortnox.errors import (
    AuthenticationError,
    AuthorizationError,
    FortnoxAPIError,
    NotFoundError,
    NoTokenError,
    RateLimitError,
    ServerError,
)
from fortnox.tokens import MemoryTokenStore, Token

API = "https://api.fortnox.se/3"

FRESH_TOKEN_RESPONSE = {
    "access_token": "refreshed-access",
    "refresh_token": "rotated-refresh",
    "expires_in": 3600,
    "scope": "customer",
}


def valid_token(**overrides) -> Token:
    base = {
        "access_token": "current-access",
        "refresh_token": "current-refresh",
        "expires_at": time.time() + 3600,
        "obtained_at": time.time(),
    }
    base.update(overrides)
    return Token(**base)


@pytest.fixture
def store() -> MemoryTokenStore:
    return MemoryTokenStore(valid_token())


@pytest.fixture
def client(config, store) -> FortnoxClient:
    with FortnoxClient(config, token_store=store) as instance:
        # Keep retry backoff out of the test suite's wall clock.
        instance._backoff = lambda attempt, response: 0.0  # type: ignore[method-assign]
        yield instance


# -- authentication ------------------------------------------------------


def test_missing_token_is_actionable(config):
    with FortnoxClient(config, token_store=MemoryTokenStore()) as client:
        with pytest.raises(NoTokenError, match="fortnox-auth"):
            client.get("companyinformation")


@respx.mock
def test_request_sends_bearer_token(client):
    route = respx.get(f"{API}/companyinformation").mock(
        return_value=httpx.Response(200, json={"CompanyInformation": {"Name": "BeOnenorth"}})
    )

    result = client.get("companyinformation")

    assert route.calls.last.request.headers["Authorization"] == "Bearer current-access"
    assert result["CompanyInformation"]["Name"] == "BeOnenorth"


@respx.mock
def test_expiring_token_is_refreshed_before_use(config, store):
    store.save(valid_token(expires_at=time.time() + 30))  # inside the 120s leeway
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=FRESH_TOKEN_RESPONSE))
    route = respx.get(f"{API}/customers").mock(return_value=httpx.Response(200, json={}))

    with FortnoxClient(config, token_store=store) as client:
        client.get("customers")

    assert route.calls.last.request.headers["Authorization"] == "Bearer refreshed-access"
    # The rotated refresh token must be persisted, or the next run is locked out.
    assert store.load().refresh_token == "rotated-refresh"


@respx.mock
def test_valid_token_is_not_refreshed(client):
    token_route = respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={}))
    respx.get(f"{API}/customers").mock(return_value=httpx.Response(200, json={}))

    client.get("customers")

    assert not token_route.called


@respx.mock
def test_unexpected_401_triggers_one_refresh_and_retry(config, store):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=FRESH_TOKEN_RESPONSE))
    route = respx.get(f"{API}/customers").mock(
        side_effect=[
            httpx.Response(401, json={"ErrorInformation": {"message": "invalid token"}}),
            httpx.Response(200, json={"Customers": []}),
        ]
    )

    with FortnoxClient(config, token_store=store) as client:
        assert client.get("customers") == {"Customers": []}

    assert route.call_count == 2
    assert route.calls[0].request.headers["Authorization"] == "Bearer current-access"
    assert route.calls[1].request.headers["Authorization"] == "Bearer refreshed-access"


@respx.mock
def test_persistent_401_eventually_raises(config, store):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=FRESH_TOKEN_RESPONSE))
    respx.get(f"{API}/customers").mock(return_value=httpx.Response(401, json={}))

    with FortnoxClient(config, token_store=store) as client:
        with pytest.raises(AuthenticationError):
            client.get("customers")


@respx.mock
def test_concurrent_requests_refresh_the_token_only_once(config):
    """The single-use refresh token must not be spent twice."""
    store = MemoryTokenStore(valid_token(expires_at=time.time() - 1))
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=FRESH_TOKEN_RESPONSE)
    )
    respx.get(f"{API}/customers").mock(return_value=httpx.Response(200, json={}))

    with FortnoxClient(config, token_store=store) as client:
        errors: list[BaseException] = []

        def worker():
            try:
                client.get("customers")
            except BaseException as exc:  # pragma: no cover - only on a real bug
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

    assert not errors
    assert token_route.call_count == 1


# -- retries and errors --------------------------------------------------


@respx.mock
def test_429_is_retried(client):
    route = respx.get(f"{API}/customers").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0"}),
            httpx.Response(200, json={"Customers": []}),
        ]
    )

    assert client.get("customers") == {"Customers": []}
    assert route.call_count == 2


@respx.mock
def test_retry_after_header_is_honoured(config, store, monkeypatch):
    respx.get(f"{API}/customers").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "7"}),
            httpx.Response(200, json={}),
        ]
    )
    slept: list[float] = []
    monkeypatch.setattr(fortnox_client.time, "sleep", slept.append)

    with FortnoxClient(config, token_store=store) as client:
        client.get("customers")

    assert slept == [7.0]


@respx.mock
def test_backoff_falls_back_to_jitter_when_retry_after_is_unparseable(config, store, monkeypatch):
    respx.get(f"{API}/customers").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}),
            httpx.Response(200, json={}),
        ]
    )
    slept: list[float] = []
    monkeypatch.setattr(fortnox_client.time, "sleep", slept.append)

    with FortnoxClient(config, token_store=store) as client:
        client.get("customers")

    # An HTTP-date is not parsed; the client backs off with jitter instead.
    assert len(slept) == 1
    assert 0.0 <= slept[0] <= 0.5


@respx.mock
def test_exhausted_retries_raise_rate_limit_error(client):
    respx.get(f"{API}/customers").mock(
        return_value=httpx.Response(429, headers={"Retry-After": "3"}, json={})
    )

    with pytest.raises(RateLimitError) as exc_info:
        client.get("customers")
    assert exc_info.value.retry_after == 3.0


@respx.mock
def test_5xx_is_retried_then_raises(client):
    route = respx.get(f"{API}/customers").mock(return_value=httpx.Response(503, json={}))

    with pytest.raises(ServerError):
        client.get("customers")
    assert route.call_count == client.config.max_retries + 1


@respx.mock
def test_4xx_is_not_retried(client):
    route = respx.get(f"{API}/customers/9").mock(return_value=httpx.Response(404, json={}))

    with pytest.raises(NotFoundError):
        client.get("customers/9")
    assert route.call_count == 1


@respx.mock
def test_403_maps_to_authorization_error(client):
    respx.get(f"{API}/invoices").mock(return_value=httpx.Response(403, json={}))
    with pytest.raises(AuthorizationError):
        client.get("invoices")


@respx.mock
def test_error_information_is_surfaced(client):
    respx.get(f"{API}/customers").mock(
        return_value=httpx.Response(
            400,
            json={
                "ErrorInformation": {"error": 1, "message": "Kunden finns inte", "code": 2000570}
            },
        )
    )

    with pytest.raises(FortnoxAPIError) as exc_info:
        client.get("customers")

    error = exc_info.value
    assert error.message == "Kunden finns inte"
    assert error.code == 2000570
    assert error.status_code == 400
    assert "2000570" in str(error)


@respx.mock
def test_lowercase_error_information_is_also_handled(client):
    respx.get(f"{API}/customers").mock(
        return_value=httpx.Response(400, json={"errorInformation": {"Message": "Bad", "Code": 42}})
    )

    with pytest.raises(FortnoxAPIError) as exc_info:
        client.get("customers")
    assert exc_info.value.message == "Bad"
    assert exc_info.value.code == 42


@respx.mock
def test_non_json_error_body_still_raises(client):
    respx.get(f"{API}/customers").mock(return_value=httpx.Response(400, text="plain failure"))

    with pytest.raises(FortnoxAPIError, match="plain failure"):
        client.get("customers")


# -- request shapes ------------------------------------------------------


@respx.mock
def test_post_sends_json_body(client):
    route = respx.post(f"{API}/customers").mock(
        return_value=httpx.Response(201, json={"Customer": {"CustomerNumber": "1"}})
    )

    client.post("customers", json={"Customer": {"Name": "Acme"}})

    request = route.calls.last.request
    assert request.headers["Content-Type"] == "application/json"
    assert b"Acme" in request.content


@respx.mock
def test_204_returns_none(client):
    respx.delete(f"{API}/customers/1").mock(return_value=httpx.Response(204))
    assert client.delete("customers/1") is None


@respx.mock
def test_absolute_url_is_used_verbatim(client):
    route = respx.get("https://api.fortnox.se/3/invoices?page=2").mock(
        return_value=httpx.Response(200, json={})
    )
    client.get("https://api.fortnox.se/3/invoices?page=2")
    assert route.called


# -- pagination ----------------------------------------------------------


@respx.mock
def test_paginate_walks_every_page(client):
    respx.get(f"{API}/customers").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "MetaInformation": {"@TotalPages": 3, "@CurrentPage": 1},
                    "Customers": [{"CustomerNumber": "1"}],
                },
            ),
            httpx.Response(
                200,
                json={
                    "MetaInformation": {"@TotalPages": 3, "@CurrentPage": 2},
                    "Customers": [{"CustomerNumber": "2"}],
                },
            ),
            httpx.Response(
                200,
                json={
                    "MetaInformation": {"@TotalPages": 3, "@CurrentPage": 3},
                    "Customers": [{"CustomerNumber": "3"}],
                },
            ),
        ]
    )

    numbers = [c["CustomerNumber"] for c in client.paginate("customers", "Customers")]
    assert numbers == ["1", "2", "3"]


@respx.mock
def test_paginate_passes_through_filters_and_limit(client):
    route = respx.get(f"{API}/customers").mock(
        return_value=httpx.Response(
            200, json={"MetaInformation": {"@TotalPages": 1}, "Customers": []}
        )
    )

    list(client.paginate("customers", "Customers", params={"filter": "active"}, limit=50))

    query = route.calls.last.request.url.params
    assert query["filter"] == "active"
    assert query["limit"] == "50"
    assert query["page"] == "1"


@respx.mock
def test_paginate_stops_on_short_page_without_meta(client):
    route = respx.get(f"{API}/customers").mock(
        return_value=httpx.Response(200, json={"Customers": [{"CustomerNumber": "1"}]})
    )

    assert len(list(client.paginate("customers", "Customers", limit=100))) == 1
    assert route.call_count == 1


@respx.mock
def test_paginate_handles_an_empty_collection(client):
    respx.get(f"{API}/customers").mock(
        return_value=httpx.Response(200, json={"MetaInformation": {"@TotalPages": 0}})
    )
    assert list(client.paginate("customers", "Customers")) == []
