"""Per-tenant isolation and refresh-token idle-window handling.

Both come straight from Fortnox's own guidance: a token store must never be
shared between tenants, and the 45-day refresh window is an idle ceiling that
only resets when you actually refresh.
"""

from __future__ import annotations

import time

import pytest

from fortnox.config import FortnoxConfig
from fortnox.errors import FortnoxConfigError
from fortnox.tokens import REFRESH_TOKEN_TTL_SECONDS, Token

# -- per-tenant config ---------------------------------------------------


def test_for_tenant_derives_a_distinct_token_path(config):
    config.token_path = "/var/lib/infonorth/fortnox_token.json"

    a = config.for_tenant("123456")
    b = config.for_tenant("789012")

    assert a.token_path == "/var/lib/infonorth/fortnox_token.123456.json"
    assert b.token_path == "/var/lib/infonorth/fortnox_token.789012.json"
    assert a.token_path != b.token_path


def test_for_tenant_sets_the_tenant_id(config):
    assert config.for_tenant("123456").tenant_id == "123456"


def test_for_tenant_leaves_the_original_untouched(config):
    original_path = config.token_path
    config.for_tenant("123456")
    assert config.token_path == original_path
    assert config.tenant_id is None


def test_for_tenant_carries_over_credentials_and_scopes(config):
    scoped = config.for_tenant("123456")
    assert scoped.client_id == config.client_id
    assert scoped.client_secret == config.client_secret
    assert scoped.scopes == config.scopes


def test_for_tenant_accepts_an_explicit_path(config):
    scoped = config.for_tenant("123456", token_path="/secrets/acme.json")
    assert scoped.token_path == "/secrets/acme.json"


def test_for_tenant_sanitises_path_separators(config):
    """A tenant id must never be able to steer the write outside its directory."""
    config.token_path = "/var/lib/tokens/fortnox_token.json"

    scoped = config.for_tenant("../../etc/passwd")

    assert scoped.token_path.startswith("/var/lib/tokens/")
    assert ".." not in scoped.token_path
    assert scoped.token_path.count("/") == config.token_path.count("/")


def test_for_tenant_rejects_an_empty_tenant_id(config):
    with pytest.raises(FortnoxConfigError, match="tenant_id"):
        config.for_tenant("")


def test_for_tenant_is_usable_without_a_directory(config):
    config.token_path = "fortnox_token.json"
    assert config.for_tenant("42").token_path == "fortnox_token.42.json"


# -- the 45-day idle window ----------------------------------------------


def test_days_remaining_is_full_window_for_a_new_token():
    now = time.time()
    token = Token(access_token="a", refresh_token="r", expires_at=now + 3600, obtained_at=now)
    assert token.refresh_token_days_remaining(now=now) == pytest.approx(45.0)


def test_days_remaining_shrinks_as_the_token_idles():
    now = time.time()
    token = Token(access_token="a", refresh_token="r", expires_at=0.0, obtained_at=now - 40 * 86400)
    assert token.refresh_token_days_remaining(now=now) == pytest.approx(5.0)


def test_days_remaining_goes_negative_once_the_window_has_passed():
    now = time.time()
    token = Token(
        access_token="a",
        refresh_token="r",
        expires_at=0.0,
        obtained_at=now - REFRESH_TOKEN_TTL_SECONDS - 86400,
    )
    assert token.refresh_token_days_remaining(now=now) < 0


def test_refresh_token_age_counts_up_from_issue():
    now = time.time()
    token = Token(access_token="a", refresh_token="r", obtained_at=now - 3 * 86400)
    assert token.refresh_token_age(now=now) == pytest.approx(3 * 86400)


def test_refresh_token_age_is_never_negative():
    """Clock skew must not make a fresh token look like it came from the future."""
    now = time.time()
    token = Token(access_token="a", refresh_token="r", obtained_at=now + 60)
    assert token.refresh_token_age(now=now) == 0.0


def test_a_config_default_is_a_real_config():
    """for_tenant must work on the plain from-env shape, not just the fixture."""
    base = FortnoxConfig(client_id="a", client_secret="b")
    assert base.for_tenant("7").token_path == "fortnox_token.7.json"
