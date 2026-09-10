from __future__ import annotations

import json
import os
import stat
import threading
import time

import pytest

from fortnox.errors import TokenError
from fortnox.tokens import FileTokenStore, MemoryTokenStore, Token


def make_token(**overrides) -> Token:
    base = {
        "access_token": "access-1",
        "refresh_token": "refresh-1",
        "expires_at": time.time() + 3600,
        "scopes": ("customer",),
        "obtained_at": time.time(),
    }
    base.update(overrides)
    return Token(**base)


def test_from_response_parses_scopes_and_expiry():
    token = Token.from_response(
        {
            "access_token": "a",
            "refresh_token": "r",
            "expires_in": 3600,
            "scope": "customer invoice",
            "token_type": "Bearer",
        },
        now=1000.0,
    )
    assert token.expires_at == 4600.0
    assert token.scopes == ("customer", "invoice")
    assert token.obtained_at == 1000.0


def test_from_response_requires_both_tokens():
    with pytest.raises(TokenError, match="refresh_token"):
        Token.from_response({"access_token": "a", "expires_in": 3600})


def test_from_response_rejects_non_numeric_expires_in():
    with pytest.raises(TokenError, match="expires_in"):
        Token.from_response({"access_token": "a", "refresh_token": "r", "expires_in": "soon"})


def test_is_expired_respects_leeway():
    token = make_token(expires_at=1000.0)
    assert not token.is_expired(now=800.0)
    assert token.is_expired(leeway=300.0, now=800.0)
    assert token.is_expired(now=1000.0)


def test_repr_hides_secrets():
    text = repr(make_token())
    assert "access-1" not in text
    assert "refresh-1" not in text


def test_file_store_round_trip(tmp_path):
    store = FileTokenStore(tmp_path / "token.json")
    assert store.load() is None

    token = make_token()
    store.save(token)
    assert store.load() == token


def test_file_store_is_owner_only(tmp_path):
    path = tmp_path / "token.json"
    FileTokenStore(path).save(make_token())
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == 0o600


def test_file_store_creates_parent_directories(tmp_path):
    store = FileTokenStore(tmp_path / "nested" / "deeper" / "token.json")
    store.save(make_token())
    assert store.load() is not None


def test_file_store_rejects_corrupt_json(tmp_path):
    path = tmp_path / "token.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(TokenError, match="not valid JSON"):
        FileTokenStore(path).load()


def test_file_store_rejects_incomplete_token(tmp_path):
    path = tmp_path / "token.json"
    path.write_text(json.dumps({"access_token": "a"}), encoding="utf-8")
    with pytest.raises(TokenError, match="malformed"):
        FileTokenStore(path).load()


def test_file_store_treats_empty_file_as_no_token(tmp_path):
    path = tmp_path / "token.json"
    path.write_text("", encoding="utf-8")
    assert FileTokenStore(path).load() is None


def test_transaction_serializes_threads(tmp_path):
    store = FileTokenStore(tmp_path / "token.json")
    store.save(make_token())
    order: list[str] = []
    inside = threading.Event()

    def first():
        with store.transaction():
            order.append("first-in")
            inside.set()
            time.sleep(0.15)
            order.append("first-out")

    def second():
        inside.wait(timeout=2)
        with store.transaction():
            order.append("second-in")

    threads = [threading.Thread(target=first), threading.Thread(target=second)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)

    assert order == ["first-in", "first-out", "second-in"]


def test_memory_store_round_trip():
    store = MemoryTokenStore()
    assert store.load() is None
    token = make_token()
    store.save(token)
    with store.transaction():
        assert store.load() == token
