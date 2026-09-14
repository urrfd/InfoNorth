from __future__ import annotations

import time

import httpx
import pytest
import respx

from fortnox.cli import _extract_code, main
from fortnox.config import TOKEN_URL
from fortnox.tokens import FileTokenStore

TOKEN_RESPONSE = {
    "access_token": "a",
    "refresh_token": "r",
    "expires_in": 3600,
    "scope": "customer",
}


@pytest.fixture(autouse=True)
def env(monkeypatch, tmp_path):
    monkeypatch.setenv("FORTNOX_CLIENT_ID", "cid")
    monkeypatch.setenv("FORTNOX_CLIENT_SECRET", "secret")
    monkeypatch.setenv("FORTNOX_REDIRECT_URI", "https://example.test/cb")
    monkeypatch.setenv("FORTNOX_SCOPES", "customer")
    monkeypatch.setenv("FORTNOX_TOKEN_PATH", str(tmp_path / "token.json"))
    return tmp_path


def test_extract_code_accepts_a_bare_code():
    assert _extract_code("abc123") == "abc123"


def test_extract_code_accepts_a_redirect_url():
    url = "https://example.test/cb?code=abc123&state=xyz"
    assert _extract_code(url) == "abc123"


def test_extract_code_rejects_a_url_without_a_code():
    with pytest.raises(SystemExit):
        _extract_code("https://example.test/cb?error=access_denied")


def test_url_command_prints_the_authorization_url(capsys):
    assert main(["url"]) == 0
    assert "apps.fortnox.se/oauth-v1/auth" in capsys.readouterr().out


@respx.mock
def test_exchange_command_persists_the_token(env, capsys):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=TOKEN_RESPONSE))

    assert main(["exchange", "https://example.test/cb?code=the-code"]) == 0

    token = FileTokenStore(env / "token.json").load()
    assert token is not None
    assert token.refresh_token == "r"


def test_status_command_reports_a_missing_token(capsys):
    assert main(["status"]) == 1
    assert "No token stored" in capsys.readouterr().out


@respx.mock
def test_status_command_reports_a_stored_token(env, capsys):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=TOKEN_RESPONSE))
    main(["exchange", "the-code"])
    capsys.readouterr()

    assert main(["status"]) == 0
    out = capsys.readouterr().out
    assert "access token expires" in out
    assert "customer" in out


@respx.mock
def test_unrecoverable_token_error_exits_nonzero(env, capsys):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(400, json={"error": "invalid_grant"}))
    assert main(["exchange", "stale-code"]) == 1
    assert "error:" in capsys.readouterr().err


def test_tenant_command_reports_a_missing_token(capsys):
    assert main(["tenant"]) == 1
    assert "No token stored" in capsys.readouterr().err


@respx.mock
def test_tenant_command_prints_the_claim(env, make_jwt, capsys):
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": make_jwt({"tenantId": 424242}),
                "refresh_token": "r",
                "expires_in": 3600,
            },
        )
    )
    main(["exchange", "the-code"])
    capsys.readouterr()

    assert main(["tenant"]) == 0
    assert capsys.readouterr().out.strip() == "424242"


@respx.mock
def test_service_token_command_mints_without_a_refresh_token(env, monkeypatch, capsys):
    monkeypatch.setenv("FORTNOX_TENANT_ID", "424242")
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "svc", "expires_in": 3600})
    )

    assert main(["service-token"]) == 0

    assert route.calls.last.request.headers["TenantId"] == "424242"
    token = FileTokenStore(env / "token.json").load()
    assert token.access_token == "svc"
    assert token.refresh_token == ""


@respx.mock
def test_status_command_reports_service_account_mode(env, monkeypatch, capsys):
    monkeypatch.setenv("FORTNOX_TENANT_ID", "424242")
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "svc", "expires_in": 3600})
    )
    main(["service-token"])
    capsys.readouterr()

    assert main(["status"]) == 0
    out = capsys.readouterr().out
    assert "client-credentials" in out
    assert "none (client-credentials tokens do not have one)" in out


# -- keepalive -----------------------------------------------------------


def _seed_token(env, obtained_at):
    """Write a token file directly, with a chosen issue time."""
    from fortnox.tokens import Token

    store = FileTokenStore(env / "token.json")
    store.save(
        Token(
            access_token="a",
            refresh_token="r",
            expires_at=obtained_at + 3600,
            obtained_at=obtained_at,
            scopes=("customer",),
        )
    )


def test_keepalive_reports_a_missing_token(capsys):
    assert main(["keepalive"]) == 1
    assert "No token stored" in capsys.readouterr().err


@respx.mock
def test_keepalive_does_nothing_for_a_recent_token(env, capsys):
    _seed_token(env, time.time() - 2 * 86400)
    route = respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=TOKEN_RESPONSE))

    assert main(["keepalive"]) == 0

    assert not route.called
    assert "nothing to do" in capsys.readouterr().out


@respx.mock
def test_keepalive_refreshes_an_idle_token(env, capsys):
    _seed_token(env, time.time() - 30 * 86400)
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(
            200, json={"access_token": "new-a", "refresh_token": "new-r", "expires_in": 3600}
        )
    )

    assert main(["keepalive"]) == 0

    assert route.called
    # The rotated refresh token must be persisted, resetting the 45-day window.
    token = FileTokenStore(env / "token.json").load()
    assert token.refresh_token == "new-r"
    assert token.refresh_token_days_remaining() > 44
    assert "window reset" in capsys.readouterr().out


@respx.mock
def test_keepalive_threshold_is_configurable(env, capsys):
    _seed_token(env, time.time() - 3 * 86400)
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(
            200, json={"access_token": "new-a", "refresh_token": "new-r", "expires_in": 3600}
        )
    )

    assert main(["keepalive", "--max-age-days", "1"]) == 0
    assert route.called


@respx.mock
def test_keepalive_surfaces_an_expired_chain_as_a_failure(env, capsys):
    """A dead refresh chain needs a human, so it must not exit 0 from cron."""
    _seed_token(env, time.time() - 50 * 86400)
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(400, json={"error": "invalid_grant"}))

    assert main(["keepalive"]) == 1
    assert "error:" in capsys.readouterr().err


def test_keepalive_is_a_noop_in_service_account_mode(env, monkeypatch, capsys):
    monkeypatch.setenv("FORTNOX_TENANT_ID", "424242")
    assert main(["keepalive"]) == 0
    assert "nothing to do" in capsys.readouterr().out


@respx.mock
def test_status_warns_when_the_idle_window_is_nearly_gone(env, capsys):
    _seed_token(env, time.time() - 40 * 86400)

    assert main(["status"]) == 0

    captured = capsys.readouterr()
    assert "idle window left" in captured.out
    assert "WARNING" in captured.err
    assert "keepalive" in captured.err


@respx.mock
def test_status_does_not_warn_for_a_fresh_token(env, capsys):
    _seed_token(env, time.time())

    assert main(["status"]) == 0
    assert "WARNING" not in capsys.readouterr().err
