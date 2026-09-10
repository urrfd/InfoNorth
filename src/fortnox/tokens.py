"""Token model and persistence.

Fortnox refresh tokens are **single-use**: every refresh returns a new refresh
token and invalidates the old one. If two processes refresh concurrently, or if
a process crashes after refreshing but before persisting, the integration is
locked out and the user has to re-authorize.

Everything here is built around those two failure modes:

* :class:`FileTokenStore` writes atomically (temp file + ``os.replace``), so a
  crash mid-write can never leave a truncated token file.
* :meth:`TokenStore.transaction` takes an exclusive lock for the whole
  read-refresh-write cycle, so only one process refreshes at a time and the
  others re-read the token the winner just persisted.
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Protocol

from .errors import TokenError

# Refresh tokens are valid for 45 days of inactivity.
REFRESH_TOKEN_TTL_SECONDS = 45 * 24 * 60 * 60


@dataclass(frozen=True, slots=True)
class Token:
    """An OAuth2 token pair plus the metadata needed to manage its lifecycle."""

    access_token: str
    refresh_token: str
    expires_at: float
    scopes: tuple[str, ...] = ()
    token_type: str = "Bearer"
    obtained_at: float = 0.0

    @classmethod
    def from_response(cls, payload: dict[str, Any], *, now: float | None = None) -> Token:
        """Build a token from a Fortnox ``/oauth-v1/token`` response body."""
        now = time.time() if now is None else now
        try:
            access_token = payload["access_token"]
            refresh_token = payload["refresh_token"]
        except KeyError as exc:
            raise TokenError(f"token response missing {exc.args[0]!r}") from exc

        expires_in = payload.get("expires_in", 3600)
        try:
            expires_in = float(expires_in)
        except (TypeError, ValueError) as exc:
            raise TokenError(f"token response has non-numeric expires_in: {expires_in!r}") from exc

        raw_scope = payload.get("scope") or ""
        scopes = tuple(s for s in raw_scope.replace(",", " ").split() if s)

        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=now + expires_in,
            scopes=scopes,
            token_type=payload.get("token_type", "Bearer"),
            obtained_at=now,
        )

    def is_expired(self, *, leeway: float = 0.0, now: float | None = None) -> bool:
        """True if the access token is expired, or expires within ``leeway`` seconds."""
        now = time.time() if now is None else now
        return now + leeway >= self.expires_at

    @property
    def refresh_token_expires_at(self) -> float:
        """Best-effort estimate of when the refresh token stops working.

        Fortnox does not return this, so it is derived from when the token was
        obtained. Treat it as a warning signal, not a guarantee.
        """
        return self.obtained_at + REFRESH_TOKEN_TTL_SECONDS

    def to_dict(self) -> dict[str, Any]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "scopes": list(self.scopes),
            "token_type": self.token_type,
            "obtained_at": self.obtained_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Token:
        try:
            return cls(
                access_token=data["access_token"],
                refresh_token=data["refresh_token"],
                expires_at=float(data["expires_at"]),
                scopes=tuple(data.get("scopes", ())),
                token_type=data.get("token_type", "Bearer"),
                obtained_at=float(data.get("obtained_at", 0.0)),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise TokenError(f"stored token is malformed: {exc}") from exc

    def replace(self, **changes: Any) -> Token:
        return replace(self, **changes)

    def __repr__(self) -> str:  # never leak secrets into logs or tracebacks
        return (
            f"Token(access_token='***', refresh_token='***', "
            f"expires_at={self.expires_at!r}, scopes={self.scopes!r})"
        )


class TokenStore(Protocol):
    """Where tokens live between runs.

    Implement this to keep tokens in a database, a secret manager, or anywhere
    else. ``transaction`` must serialize across every process that shares the
    store, otherwise concurrent refreshes will invalidate each other.
    """

    def load(self) -> Token | None:
        """Return the stored token, or None if the app was never authorized."""

    def save(self, token: Token) -> None:
        """Persist the token, replacing any previous one."""

    def transaction(self) -> Any:
        """Context manager holding an exclusive lock over load/save."""


class MemoryTokenStore:
    """In-process token store. Useful for tests and short-lived scripts."""

    def __init__(self, token: Token | None = None) -> None:
        self._token = token
        self._lock = threading.RLock()

    def load(self) -> Token | None:
        return self._token

    def save(self, token: Token) -> None:
        self._token = token

    @contextmanager
    def transaction(self) -> Iterator[None]:
        with self._lock:
            yield


class FileTokenStore:
    """Token store backed by a JSON file with ``0600`` permissions.

    Locking uses a sidecar ``<path>.lock`` file: ``fcntl.flock`` on POSIX and
    ``msvcrt.locking`` on Windows, plus an in-process lock so threads in the
    same interpreter serialize too.
    """

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)
        self._lock_path = self.path.with_name(self.path.name + ".lock")
        self._thread_lock = threading.RLock()

    def load(self) -> Token | None:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        if not raw.strip():
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise TokenError(f"token file {self.path} is not valid JSON: {exc}") from exc
        return Token.from_dict(data)

    def save(self, token: Token) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(self.path.parent), prefix=self.path.name, suffix=".tmp"
        )
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(token.to_dict(), handle, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, self.path)
        except BaseException:
            os.unlink(tmp_name)
            raise

    @contextmanager
    def transaction(self) -> Iterator[None]:
        with self._thread_lock:
            self._lock_path.parent.mkdir(parents=True, exist_ok=True)
            handle = open(self._lock_path, "a+b")
            try:
                _lock_file(handle)
                try:
                    yield
                finally:
                    _unlock_file(handle)
            finally:
                handle.close()


try:  # POSIX
    import fcntl

    def _lock_file(handle: Any) -> None:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(handle: Any) -> None:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

except ImportError:  # Windows
    import msvcrt

    def _lock_file(handle: Any) -> None:
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)

    def _unlock_file(handle: Any) -> None:
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
