"""The Fortnox REST API client."""

from __future__ import annotations

import random
import time
from collections.abc import Iterator
from typing import Any

import httpx

from . import oauth
from .config import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, FortnoxConfig
from .errors import (
    AuthenticationError,
    AuthorizationError,
    FortnoxAPIError,
    NotFoundError,
    NoTokenError,
    RateLimitError,
    ServerError,
)
from .ratelimit import SlidingWindowRateLimiter
from .tokens import FileTokenStore, Token, TokenStore

_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class FortnoxClient:
    """Authenticated access to the Fortnox REST API (``https://api.fortnox.se/3``).

    Handles the parts that are easy to get wrong: refreshing the access token
    before it expires, persisting the rotated refresh token under a lock, pacing
    requests under the rate limit, and backing off on 429s and 5xxs.

    Example:
        >>> config = FortnoxConfig.from_env()
        >>> with FortnoxClient(config) as client:
        ...     company = client.get("companyinformation")
        ...     for customer in client.paginate("customers", "Customers"):
        ...         print(customer["CustomerNumber"])
    """

    def __init__(
        self,
        config: FortnoxConfig,
        *,
        token_store: TokenStore | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.config = config
        self.token_store: TokenStore = token_store or FileTokenStore(config.token_path)
        self._owns_http_client = http_client is None
        self._http = http_client or httpx.Client(timeout=config.timeout)
        self._limiter = SlidingWindowRateLimiter(
            config.rate_limit_requests, config.rate_limit_window
        )

    # -- lifecycle ---------------------------------------------------------

    def __enter__(self) -> FortnoxClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_http_client:
            self._http.close()

    # -- tokens ------------------------------------------------------------

    def current_token(self) -> Token:
        """Return the stored token without refreshing it."""
        token = self.token_store.load()
        if token is None:
            raise NoTokenError(
                "no Fortnox token stored - run the authorization flow first "
                "(see `fortnox-auth url` and `fortnox-auth exchange`)"
            )
        return token

    @property
    def uses_service_account(self) -> bool:
        """True when a tenant id is configured, selecting the client-credentials grant."""
        return bool(self.config.tenant_id)

    def _is_usable(self, token: Token | None, *, force_refresh: bool) -> bool:
        if token is None or force_refresh:
            return False
        return not token.is_expired(leeway=self.config.refresh_leeway_seconds)

    def _access_token(self, *, force_refresh: bool = False) -> str:
        """Return a usable access token, obtaining a new one if needed."""
        if self.uses_service_account:
            return self._service_account_token(force_refresh=force_refresh)
        return self._refreshed_token(force_refresh=force_refresh)

    def _service_account_token(self, *, force_refresh: bool) -> str:
        """Mint an access token with the client-credentials grant.

        There is no refresh token here, so a cache miss costs one extra token
        request and nothing else. The lock only keeps a burst of threads from
        minting redundantly.
        """
        cached = self.token_store.load()
        if self._is_usable(cached, force_refresh=force_refresh):
            return cached.access_token  # type: ignore[union-attr]

        with self.token_store.transaction():
            cached = self.token_store.load()
            if self._is_usable(cached, force_refresh=force_refresh):
                return cached.access_token  # type: ignore[union-attr]

            token = oauth.fetch_service_account_token(self.config, client=self._http)
            self.token_store.save(token)
            return token.access_token

    def _refreshed_token(self, *, force_refresh: bool) -> str:
        """Return a usable access token from the stored refresh token.

        The whole read-check-refresh-write cycle runs inside the store's
        transaction, so concurrent workers cannot burn each other's single-use
        refresh token. A worker that loses the race re-reads the token the
        winner just wrote instead of refreshing again.
        """
        token = self.current_token()
        if self._is_usable(token, force_refresh=force_refresh):
            return token.access_token

        with self.token_store.transaction():
            token = self.current_token()
            # Another process may have refreshed while we waited for the lock.
            if self._is_usable(token, force_refresh=force_refresh):
                return token.access_token

            new_token = oauth.refresh_token(self.config, token, client=self._http)
            self.token_store.save(new_token)
            return new_token.access_token

    # -- requests ----------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Send an authenticated request and return the decoded JSON body.

        Args:
            method: HTTP method, e.g. ``"GET"``.
            path: Path relative to the API base, e.g. ``"customers"`` or
                ``"invoices/123"``. Absolute URLs are used as-is, which makes it
                easy to follow ``@NextPage`` style links.
            params: Query string parameters.
            json: Request body, serialized as JSON.
            headers: Extra headers merged over the defaults.

        Raises:
            FortnoxAPIError: or one of its subclasses, for any error response.
        """
        url = path if path.startswith("http") else f"{self.config.api_base_url}/{path.lstrip('/')}"
        forced_refresh = False
        last_response: httpx.Response | None = None

        for attempt in range(self.config.max_retries + 1):
            token = self._access_token(force_refresh=forced_refresh)
            forced_refresh = False

            request_headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
            if json is not None:
                request_headers["Content-Type"] = "application/json"
            if headers:
                request_headers.update(headers)

            self._limiter.acquire()
            response = self._http.request(
                method.upper(), url, params=params, json=json, headers=request_headers
            )
            last_response = response

            if response.is_success:
                return _decode(response)

            # A 401 on a token we believed was valid means Fortnox invalidated
            # it early. Force one refresh and retry before giving up.
            if response.status_code == 401 and attempt < self.config.max_retries:
                forced_refresh = True
                continue

            if response.status_code in _RETRYABLE_STATUS and attempt < self.config.max_retries:
                time.sleep(self._backoff(attempt, response))
                continue

            break

        assert last_response is not None  # the loop always runs at least once
        raise _error_for(last_response)

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, json: Any = None, **kwargs: Any) -> Any:
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Any = None, **kwargs: Any) -> Any:
        return self.request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)

    def paginate(
        self,
        path: str,
        collection_key: str,
        *,
        params: dict[str, Any] | None = None,
        limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Iterator[dict[str, Any]]:
        """Yield every record of a paged list endpoint.

        Fortnox list responses wrap the records in a named key and report paging
        in ``MetaInformation``:

        .. code-block:: json

            {"MetaInformation": {"@TotalPages": 3, "@CurrentPage": 1},
             "Customers": [...]}

        Args:
            path: List endpoint, e.g. ``"customers"``.
            collection_key: The key holding the records, e.g. ``"Customers"``.
            params: Extra filters passed through on every page request.
            limit: Records per page, 1 to 500. Larger pages mean fewer requests
                against the rate limit, so raise it for bulk reads.

        Raises:
            ValueError: if ``limit`` is outside the range Fortnox accepts.
        """
        if not 1 <= limit <= MAX_PAGE_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_PAGE_LIMIT}, got {limit}")

        page = 1
        while True:
            page_params = dict(params or {})
            page_params.update({"page": page, "limit": limit})
            payload = self.get(path, params=page_params)

            records = payload.get(collection_key) or []
            yield from records

            meta = payload.get("MetaInformation") or {}
            total_pages = _as_int(meta.get("@TotalPages"))
            if total_pages is not None:
                if page >= total_pages:
                    return
            elif len(records) < limit:
                # No meta information to go on: a short page means the end.
                return
            page += 1

    # -- retry helpers -----------------------------------------------------

    def _backoff(self, attempt: int, response: httpx.Response) -> float:
        """Seconds to wait before retrying, honouring ``Retry-After``."""
        retry_after = _retry_after_seconds(response)
        if retry_after is not None:
            return retry_after
        # Exponential backoff with full jitter, so concurrent workers that hit
        # the limit together do not retry in lockstep.
        return random.uniform(0, min(2**attempt * 0.5, 30.0))


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _retry_after_seconds(response: httpx.Response) -> float | None:
    raw = response.headers.get("Retry-After")
    if not raw:
        return None
    try:
        return max(float(raw), 0.0)
    except ValueError:
        # Fortnox sends numeric seconds; an HTTP-date is valid per RFC 9110 but
        # is not worth parsing here - fall back to normal backoff.
        return None


def _decode(response: httpx.Response) -> Any:
    if response.status_code == 204 or not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _error_for(response: httpx.Response) -> FortnoxAPIError:
    """Translate an error response into the matching exception."""
    try:
        payload = response.json()
    except ValueError:
        payload = None

    message = _error_message(payload) or response.text.strip() or response.reason_phrase
    code = _error_code(payload)
    request_id = response.headers.get("X-Request-Id")

    kwargs: dict[str, Any] = {
        "status_code": response.status_code,
        "code": code,
        "payload": payload,
        "request_id": request_id,
    }

    status = response.status_code
    if status == 401:
        return AuthenticationError(message, **kwargs)
    if status == 403:
        return AuthorizationError(message, **kwargs)
    if status == 404:
        return NotFoundError(message, **kwargs)
    if status == 429:
        return RateLimitError(message, retry_after=_retry_after_seconds(response), **kwargs)
    if status >= 500:
        return ServerError(message, **kwargs)
    return FortnoxAPIError(message, **kwargs)


def _error_information(payload: Any) -> dict[str, Any] | None:
    """Pull out Fortnox's ``ErrorInformation`` block, whatever case it uses."""
    if not isinstance(payload, dict):
        return None
    for key in ("ErrorInformation", "errorInformation", "ErrorInformationList"):
        info = payload.get(key)
        if isinstance(info, list) and info:
            info = info[0]
        if isinstance(info, dict):
            return info
    return None


def _error_message(payload: Any) -> str | None:
    info = _error_information(payload)
    if info:
        for key in ("message", "Message", "error_description"):
            value = info.get(key)
            if value:
                return str(value)
    if isinstance(payload, dict):
        for key in ("message", "Message", "error_description", "error"):
            value = payload.get(key)
            if value:
                return str(value)
    return None


def _error_code(payload: Any) -> int | None:
    info = _error_information(payload)
    if info:
        for key in ("code", "Code"):
            parsed = _as_int(info.get(key))
            if parsed is not None:
                return parsed
    return None
