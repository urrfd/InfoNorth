from __future__ import annotations

import pytest

from fortnox.config import FortnoxConfig
from fortnox.errors import FortnoxConfigError


def test_from_env_reads_every_field(monkeypatch):
    monkeypatch.setenv("FORTNOX_CLIENT_ID", "cid")
    monkeypatch.setenv("FORTNOX_CLIENT_SECRET", "secret")
    monkeypatch.setenv("FORTNOX_REDIRECT_URI", "https://example.test/cb")
    monkeypatch.setenv("FORTNOX_SCOPES", "customer, invoice  article")
    monkeypatch.setenv("FORTNOX_TOKEN_PATH", "/tmp/t.json")

    config = FortnoxConfig.from_env()

    assert config.client_id == "cid"
    assert config.scopes == ["customer", "invoice", "article"]
    assert config.token_path == "/tmp/t.json"


def test_from_env_requires_credentials(monkeypatch):
    monkeypatch.delenv("FORTNOX_CLIENT_ID", raising=False)
    monkeypatch.setenv("FORTNOX_CLIENT_SECRET", "secret")
    with pytest.raises(FortnoxConfigError, match="FORTNOX_CLIENT_ID"):
        FortnoxConfig.from_env()


def test_from_env_treats_blank_as_missing(monkeypatch):
    monkeypatch.setenv("FORTNOX_CLIENT_ID", "   ")
    monkeypatch.setenv("FORTNOX_CLIENT_SECRET", "secret")
    with pytest.raises(FortnoxConfigError, match="FORTNOX_CLIENT_ID"):
        FortnoxConfig.from_env()


def test_overrides_win_over_environment(monkeypatch):
    monkeypatch.setenv("FORTNOX_CLIENT_ID", "cid")
    monkeypatch.setenv("FORTNOX_CLIENT_SECRET", "secret")
    monkeypatch.setenv("FORTNOX_TOKEN_PATH", "/tmp/env.json")

    config = FortnoxConfig.from_env(token_path="/tmp/override.json")
    assert config.token_path == "/tmp/override.json"


def test_base_url_trailing_slash_is_trimmed():
    config = FortnoxConfig(
        client_id="a", client_secret="b", api_base_url="https://api.fortnox.se/3/"
    )
    assert config.api_base_url == "https://api.fortnox.se/3"


def test_direct_construction_validates_credentials():
    with pytest.raises(FortnoxConfigError, match="client_secret"):
        FortnoxConfig(client_id="a", client_secret="")
