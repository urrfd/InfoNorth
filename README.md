# InfoNorth

A wiki for BeOnenorth.

## `fortnox` — Fortnox OAuth2 + REST API client

A Python client for the [Fortnox API](https://www.fortnox.se/developer). It handles the
parts of the integration that are easy to get wrong and expensive to get wrong:
token refresh, single-use refresh-token rotation, rate limiting and retries.

### Two ways to authenticate

**Client credentials (recommended for InfoNorth).** If the customer activates with
`account_type=service`, you can mint an access token any time from client id + client
secret + tenant id. There is no refresh token to rotate, lose, or race on. Set
`FORTNOX_TENANT_ID` and the client uses this automatically.

**Authorization code + refresh token.** The general-purpose flow, for user accounts.
Supported in full, including the awkward parts below.

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

Either way, Fortnox rate-limits to **25 requests per 5 seconds** per access token
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

### Test against a sandbox first

The developer portal lets you create up to **30 test environments** — each a full Fortnox
company tied to your developer account, using the same email as the user who created it.
Do the first end-to-end run against one of those, not a live customer.

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
permissions. It is gitignored, but **keep it outside the repo in production**: it holds a
live refresh token, which is a standing key to that customer's accounting data for up to
45 days. Treat it with the same care as the client secret, and back it up knowing what it
is.

### Switch to client credentials (no more refresh tokens)

Once you have any token for the tenant, read its id and pin it:

```bash
fortnox-auth tenant           # reads the tenantId claim out of the access token
export FORTNOX_TENANT_ID=...
fortnox-auth service-token    # mints a token — no refresh token involved
```

The tenant id is also `DatabaseNumber` from `/3/companyinformation` (needs the
`companyinformation` scope), and Fortnox can push it to you via the *Consent created* /
*Consent revoked* webhooks configured in the developer portal.

With `FORTNOX_TENANT_ID` set, `FortnoxClient` mints tokens on demand and ignores any
stored refresh token entirely. The two flows can coexist for the same integration if you
need user-account tokens as well.

### Use

```python
from fortnox import FortnoxClient, FortnoxConfig

config = FortnoxConfig.from_env()

with FortnoxClient(config) as client:
    company = client.get("companyinformation")

    # Paged endpoints are iterators; paging is handled for you.
    for customer in client.paginate("customers", "Customers"):
        print(customer["CustomerNumber"], customer["Name"])

    # Filters pass straight through. Note Fortnox allows only ONE resource-specific
    # filter at a time, though you may combine it with a global one like lastmodified.
    unpaid = client.paginate("invoices", "Invoices", params={"filter": "unpaid"}, limit=500)

    client.post("customers", json={"Customer": {"Name": "Acme AB"}})
```

Token handling is automatic — there is no `login()` to call. The client obtains a token
when the current one is within 120 seconds of expiry, and once more if Fortnox
unexpectedly returns 401.

`limit` accepts 1–500 (Fortnox's documented range, default 100) and is validated before
the request goes out. Raising it is the cheapest way to cut rate-limit pressure on bulk
reads. `sortby` and `sortorder` pass through in `params`.

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

### Serving several customers

**One token store per tenant — never share a file.** The refresh token is single-use, so
two tenants behind one store race each other, and one customer reconnecting would
overwrite another's state. `for_tenant` derives an isolated path and selects the
client-credentials grant:

```python
base = FortnoxConfig.from_env()

for tenant_id in ("123456", "789012"):
    with FortnoxClient(base.for_tenant(tenant_id)) as client:
        ...  # token store: fortnox_token.123456.json, fortnox_token.789012.json
```

Rate limits are per access token, not per IP, so **every tenant gets its own 300/minute**.
Serving 40 customers does not divide one allowance between them — which is why the limiter
lives on the client instance rather than being global.

### Keeping the refresh chain alive

The 45 days is an **idle ceiling, not a budget**: every refresh resets it. An hourly job
never comes close. A month-end job can — seven quiet weeks and it is dead on the next run,
recoverable only by the customer reconnecting.

If that is your shape, refresh on a schedule independent of the real work:

```cron
# Weekly, well inside the 45-day window. Exits non-zero if the chain has broken.
0 3 * * 1  cd /srv/infonorth && .venv/bin/fortnox-auth keepalive
```

`keepalive` only refreshes when the stored token is older than `--max-age-days` (default 7),
so it is cheap to run often and safe to run twice. `fortnox-auth status` warns once the
window drops under 10 days. In service-account mode it is a no-op — there is no chain to
keep alive, which is the other reason to prefer that grant.

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

### Known gaps

- **File endpoints** (`archive`, `inbox`) need `multipart/form-data`; this client only
  sends JSON bodies.
- **Scopes are read+write** — there is no read-only variant — and cannot be added silently
  to an existing connection. Widening them means every customer re-activates, so request
  what you need up front.
- **Legacy auth** (static `Access-Token` + `Client-Secret` headers) is retired and not
  supported; for code that never refreshed anything, moving to OAuth2 is a rewrite rather
  than a config change.
- No live call has been made from this repo yet; the suite runs entirely against mocks.

### Develop

```bash
.venv/bin/python -m pytest              # 121 tests, no network required
.venv/bin/python -m pytest --cov=fortnox
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format .
```

Tests mock the HTTP layer with `respx`, so the suite runs offline and never touches a real
Fortnox tenant.
