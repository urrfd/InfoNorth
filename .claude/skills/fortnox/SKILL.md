---
name: fortnox
description: >-
  Working with the Fortnox API (Swedish accounting/ERP SaaS) in this repo — OAuth2 tokens,
  refresh rotation, scopes, rate limits, and the `src/fortnox/` client. Use this whenever
  the task touches Fortnox, `src/fortnox/`, `fortnox-auth`, or anything accounting-adjacent
  in this codebase: invoices, customers, articles, vouchers, suppliers, orders, offers,
  bookkeeping, or a `FORTNOX_*` environment variable. Also use it when debugging auth
  failures, 401s, 429s, expired or rejected tokens, or "the integration stopped working",
  even if Fortnox is never named — in this repo those are almost always Fortnox token
  problems, and the failure modes here are unforgiving and easy to get wrong by guessing.
---

# Fortnox integration

Fortnox is a Swedish accounting and ERP platform. Its API is unforgiving in two specific
ways, and most mistakes here are *unrecoverable without a human* — so the cost of guessing
is high and the rules below are worth following even where they look fussy.

## Use the client; don't hand-roll requests

`src/fortnox/` already handles auth, refresh, rate limiting, retries and pagination. A
raw `httpx`/`requests` call to `api.fortnox.se` bypasses all of it and will eventually
produce a 429 storm or a dead integration.

```python
from fortnox import FortnoxClient, FortnoxConfig

with FortnoxClient(FortnoxConfig.from_env()) as client:
    company = client.get("companyinformation")
    for customer in client.paginate("customers", "Customers", limit=500):
        ...
```

There is no `login()`. Tokens are obtained and refreshed automatically.

## The one thing that will bite you: refresh tokens rotate

Every refresh returns a **new** refresh token and **immediately invalidates the old one**.
There is no way to re-use one and no way to ask Fortnox for the current one. That makes
two ordinary-looking bugs fatal:

- **Two workers refreshing at once.** One wins; the other gets `invalid_grant` and may
  overwrite good state with nothing.
- **Crashing between refreshing and persisting.** Fortnox has moved on, you hold a token
  it already invalidated.

Either way the customer is disconnected until *they* re-authorize. No retry helps.

The client handles this by running the whole read → check → refresh → write cycle inside
`token_store.transaction()` and re-reading after taking the lock, because whoever you
queued behind has probably already done the work. **If you touch token handling, preserve
that shape.** `FileTokenStore` also writes atomically (temp file + `os.replace`), so a
crash mid-write can't leave a half-written file.

`RefreshTokenExpiredError` means a human must reconnect. Never retry it, never swallow
it — surface it as a reconnect task.

## Prefer client credentials — it deletes the problem above

If the customer activated with `account_type=service`, an access token can be minted any
time from client id + secret + tenant id. No refresh token, nothing to rotate or race.

```bash
fortnox-auth tenant              # read tenantId from the current token
export FORTNOX_TENANT_ID=...     # client now uses client-credentials automatically
```

For an unattended integration this is the better path. Reach for the refresh-token flow
only when you genuinely need a user-account token. Both can coexist for one integration.

## Writes post to real books — default to read-only

A `GET` is harmless. A `POST` to `invoices` raises a real invoice, and a `POST` to
`vouchers` posts to the ledger of a real company's accounts. Accounting records are not
freely reversible: a booked voucher is corrected by another voucher, and the mistake stays
in the audit trail. Treat every non-GET as an action with consequences outside the code.

Before any `POST`, `PUT`, `PATCH` or `DELETE`:

1. **Read first.** Fetch the record and confirm you are acting on what you think you are.
2. **Dry run.** State the exact method, URL and body, and what it will change. Have a
   human read it.
3. **Get explicit approval.** Approval for one write is not approval for the next.
4. **Sandbox before live.** Prove it on a test company first.

Each object note under `references/objects/` records which methods a resource exposes and
flags the destructive ones. Read the note before calling a resource you have not used.

## Two APIs under one host

Fortnox is really two API families, and they behave differently:

- **`/3/…`** — the classic API, ~164 paths. Responses wrap records in a named key
  (`{"Customers": [...]}`), `MetaInformation` drives paging, and `FortnoxClient` is built
  around exactly this. Call it with a relative path: `client.get("customers")`.
- **`/api/…`** — newer services (warehouse, recurring billing, time reporting,
  fileattachments and others), ~85 paths. Different conventions; some list endpoints
  return a **bare JSON array** with no wrapper, so `client.paginate()` does not apply.
  The client's base URL points at `/3`, so pass the absolute URL:
  `client.get("https://api.fortnox.se/api/warehouse/...")`.

Assuming the `/3/` shape on an `/api/` resource fails confusingly — a 404 from the wrong
base, or a `TypeError` from indexing a list as a dict. The object note for each resource
shows the correct call.

## Rules that are easy to get wrong

**Scopes are frozen at activation.** A connection keeps the scopes your integration had
when that customer activated. Adding one later does not widen existing connections —
every affected customer must reactivate. There is no read-only variant; scopes grant read
*and* write. Decide the scope list before you have customers.

**One token store per tenant, never shared.** A shared file is a race, and one customer
reconnecting would clobber another's state. Use `config.for_tenant(tenant_id)`, which
derives an isolated path and sanitizes the id into a single path segment.

**The 45-day refresh window is an idle ceiling, not a budget.** Every refresh resets it.
An hourly job never approaches it; a month-end job can sit through seven quiet weeks and
find itself dead. For infrequent integrations run `fortnox-auth keepalive` on a schedule
independent of the real work.

**Rate limits are per access token, not per IP** — 25 requests / 5s sliding window,
300/minute. Each tenant gets its own allowance, so serving 40 customers doesn't divide one
budget. The limiter therefore lives on the client instance, not globally. Raising `limit`
on list endpoints (max 500) is the cheapest way to cut pressure.

**Never log a token response body.** It contains both tokens. Log the status, scope and
new expiry — nothing else. `Token.__repr__` masks secrets; don't undo that.

## Testing

The suite is offline: `respx` mocks the HTTP layer, so it never touches a real tenant or
burns a refresh token. Keep it that way.

Run `pytest`, not `python -m pytest` — the latter puts the CWD on `sys.path` and hides
import bugs CI will catch. Shared test helpers belong in `tests/conftest.py` as fixtures,
never imported across test modules.

When testing anything time-dependent, inject the clock rather than sleeping.

## Going deeper

- **`references/objects/`** — one note per API resource (87 of them), generated from
  Fortnox's OpenAPI spec: endpoints, the collection key `paginate` needs, fields, writable
  fields and required ones, resource filters, and the safety rules for its writes. Start
  at `references/objects/README.md` and read the note for the resource you are touching.
  Regenerate with `scripts/generate_object_notes.py` when Fortnox publishes a new spec;
  the notes are derived, so never edit one by hand.
- `references/auth.md` — the flows end to end: endpoints, exact request shapes, token
  lifetimes, how to obtain a tenant id, what each failure means.
- `references/api.md` — conventions for calling the API: pagination, filters, sorting,
  the error envelope, rate limits, and known gaps in this client.

The object notes describe what Fortnox *documents*. Every one carries a `Date tested`
line, and today they all say the same thing: not yet verified against a real tenant. When
you confirm a call, record it in that note — a spec is a claim, a tested call is evidence.

## Verifying against a real tenant

The suite proves the logic, not the integration. The developer portal allows up to 30
sandbox companies — use one, never a live customer, because testing refresh *spends*
the refresh token and a persistence bug will disconnect whatever you point it at.

```bash
fortnox-auth url                          # approve in a browser
fortnox-auth exchange '<redirect URL>'
fortnox-auth get companyinformation       # first real call
fortnox-auth refresh && fortnox-auth status   # rotation actually persisted?
```
