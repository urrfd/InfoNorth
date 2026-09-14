from __future__ import annotations

import base64
import json

import pytest

from fortnox.config import FortnoxConfig


@pytest.fixture
def config(tmp_path) -> FortnoxConfig:
    return FortnoxConfig(
        client_id="test-client-id",
        client_secret="test-client-secret",
        redirect_uri="https://example.test/callback",
        scopes=["companyinformation", "customer"],
        token_path=str(tmp_path / "token.json"),
        max_retries=2,
    )


@pytest.fixture
def make_jwt():
    """Build a JWT-shaped access token. The signature is never verified.

    Lives here rather than in a test module so no test has to import another
    one - that only works when the repo root happens to be on sys.path, which
    is true for `python -m pytest` but not for a bare `pytest` as CI runs it.
    """

    def _make(claims: dict) -> str:
        def b64(data: bytes) -> str:
            return base64.urlsafe_b64encode(data).decode().rstrip("=")

        header = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
        payload = b64(json.dumps(claims).encode())
        return f"{header}.{payload}.not-a-real-signature"

    return _make
