# InfoNorth

A wiki for BeOnenorth.

## `fortnox` — Fortnox OAuth2 + REST API client

A Python client for the [Fortnox API](https://www.fortnox.se/developer). It handles the
parts of the integration that are easy to get wrong and expensive to get wrong:
token refresh, single-use refresh-token rotation, rate limiting and retries.

### Why this exists

Fortnox's OAuth2 has two sharp edges:

| Thing | Lifetime | Catch |
|---|---|---|
| Authorization code | 10 minutes | Single use |
| Access token | 1 hour | — |
| Refresh token | 45 days | **Single use — rotated on every refresh** |

The refresh token rotating on every use is the one that bites. If two workers refresh at
the same time, or a process dies after refreshing but before persisting, the integration
is locked out and a human has to click through the authorization flow again. This client
serializes the whole read-check-refresh-write cycle under a lock and writes the token file
atomically, so neither can happen.

On top of that, Fortnox rate-limits to **25 requests per 5 seconds** per access token
(300/minute per client-id and tenant), and bursting past it keeps the limiter engaged
until the average drops back down. The client paces requests locally rather than absorbing
the 429s.

### Install

```bash
uv venv && uv pip install -e ".[dev]"
```

### Configure

Copy `.env.example` to `.env` and fill in the Client-ID and Client-Secret from your
integration in the [Fortnox developer portal](https://developer.fortnox.se).

```bash
export FORTNOX_CLIENT_ID=...
export FORTNOX_CLIENT_SECRET=...
export FORTNOX_REDIRECT_URI=http://localhost:8000/fortnox/callback
export FORTNOX_SCOPES="companyinformation customer invoice"
```

`FORTNOX_REDIRECT_URI` must match the value registered on the integration character for
character, or the token exchange fails.

### Authorize (once per Fortnox tenant)

```bash
# 1. Print the URL and open it in a browser. Approve the integration in Fortnox.
fortnox-auth url

# 2. Fortnox redirects to your redirect_uri with ?code=...
#    Paste either the code or the whole URL — the code is valid for 10 minutes.
fortnox-auth exchange 'http://localhost:8000/fortnox/callback?code=...&state=...'

# 3. Check what you got.
fortnox-auth status

# 4. Make a call.
fortnox-auth get companyinformation
```

The token pair lands in `FORTNOX_TOKEN_PATH` (default `fortnox_token.json`) with `0600`
permissions. It is gitignored — **do not commit it**.

### Use

```python
from fortnox import FortnoxClient, FortnoxConfig

config = FortnoxConfig.from_env()

with FortnoxClient(config) as client:
    company = client.get("companyinformation")

    # Paged endpoints are iterators; paging is handled for you.
    for customer in client.paginate("customers", "Customers"):
        print(customer["CustomerNumber"], customer["Name"])

    # Filters pass straight through.
    unpaid = client.paginate("invoices", "Invoices", params={"filter": "unpaid"})

    client.post("customers", json={"Customer": {"Name": "Acme AB"}})
```

Refreshing happens automatically — there is no `login()` to call. The client refreshes when
the access token is within 120 seconds of expiry, and once more if Fortnox unexpectedly
returns 401.

### Errors

Everything derives from `FortnoxError`:

```
FortnoxError
├── FortnoxConfigError          missing or malformed configuration
├── TokenError
│   ├── NoTokenError            never authorized — run `fortnox-auth url`
│   └── RefreshTokenExpiredError  refresh token used/revoked/expired — re-authorize
└── FortnoxAPIError             any error response (.status_code, .code, .payload)
    ├── AuthenticationError     401
    ├── AuthorizationError      403 — token lacks the scope
    ├── NotFoundError           404
    ├── RateLimitError          429 after retries (.retry_after)
    └── ServerError             5xx after retries
```

`RefreshTokenExpiredError` is the one to alert on: it is unrecoverable without a human
re-authorizing, and retrying will not help.

### Retries

429 and 5xx are retried up to `max_retries` (default 4), honouring `Retry-After` when
Fortnox sends it and otherwise backing off exponentially with full jitter. 4xx responses
are not retried — apart from 401, which triggers exactly one forced refresh.

### Running several workers

`FileTokenStore` locks across processes via a sidecar `.lock` file, so multiple workers on
one machine sharing a token file are safe. Across machines, implement the `TokenStore`
protocol against your database or secret manager — `load`, `save` and a `transaction`
context manager that takes an exclusive lock:

```python
class DatabaseTokenStore:
    def load(self) -> Token | None: ...
    def save(self, token: Token) -> None: ...

    @contextmanager
    def transaction(self):
        with db.advisory_lock("fortnox-token"):
            yield


client = FortnoxClient(config, token_store=DatabaseTokenStore())
```

The rate limiter is per-process, so size each worker's `rate_limit_requests` to its share
of the tenant's 25-per-5-seconds budget.

### Develop

```bash
.venv/bin/python -m pytest              # 67 tests, no network required
.venv/bin/python -m pytest --cov=fortnox
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format .
```

Tests mock the HTTP layer with `respx`, so the suite runs offline and never touches a real
Fortnox tenant.
