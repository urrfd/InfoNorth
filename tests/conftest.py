from __future__ import annotations

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
