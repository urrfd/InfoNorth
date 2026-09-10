from __future__ import annotations

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
