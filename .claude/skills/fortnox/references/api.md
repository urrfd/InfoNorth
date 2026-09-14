# Fortnox API conventions

How to call the API once authenticated. Read this when adding endpoint support or
debugging a response shape.

## Contents

- [Request shape](#request-shape)
- [Pagination](#pagination)
- [Filtering and sorting](#filtering-and-sorting)
- [Errors](#errors)
- [Rate limits](#rate-limits)
- [Gaps in this client](#gaps-in-this-client)
- [Developer portal](#developer-portal)

## Request shape

Base is `https://api.fortnox.se/3`. Headers: `Authorization: Bearer …`,
`Accept: application/json`, and `Content-Type: application/json` on writes.

Resources nest under a singular capitalised key, both in responses and request bodies:

```json
{ "Customer": { "Name": "Acme AB", "CustomerNumber": "1" } }
```

List endpoints use the plural: `{"Customers": [...]}`.

## Pagination

```json
{
  "MetaInformation": { "@TotalResources": 412, "@TotalPages": 5, "@CurrentPage": 1 },
  "Customers": [ ... ]
}
```

`client.paginate(path, collection_key)` walks this and yields records. `limit` is 1–500
(default 100) and validated before the request. **Raise it for bulk reads** — it is the
cheapest way to cut rate-limit pressure, since 500-per-page costs a fifth of the requests.

`offset` is supported by the API as an alternative to `page`; this client uses `page`.

## Filtering and sorting

| Parameter | Notes |
|---|---|
| `filter` | Resource-specific, e.g. `unpaid` on invoices |
| `lastmodified` | Global — everything changed since a timestamp. Ideal for incremental sync |
| `financialyear` | Selects the financial year for financial resources |
| `sortby` / `sortorder` | Sorting; inconsistently supported across endpoints |

**Only one resource-specific filter at a time**, though you may combine it with a global
parameter like `lastmodified`. Pass them through `params`:

```python
client.paginate("invoices", "Invoices", params={"filter": "unpaid"}, limit=500)
```

## Errors

```json
{ "ErrorInformation": { "error": 1, "message": "Kan inte hitta kontot.", "code": 2000423 } }
```

Messages are often Swedish. The client parses this into a typed exception carrying
`.status_code`, `.code`, `.message` and `.payload`; key casing varies by endpoint, so
`_error_information` checks several variants.

Codes worth recognising:

| Code | Meaning |
|---|---|
| 2000423 | Account not found — often the customer hasn't set default accounts under Settings → Accounting |
| 2000570 | Referenced resource does not exist |
| 2000311 | Auth problem — missing or invalid token |

A "could not find account" error is usually customer configuration, not a bug in your
request. Check their account plan before chasing it in code.

## Rate limits

25 requests per 5-second sliding window; 300/minute. Enforced **per access token**, so
each tenant has its own allowance. Exceeding it returns 429 and keeps the limiter engaged
until the average falls back under — bursting is counterproductive, which is why the
client paces requests rather than absorbing 429s.

## Gaps in this client

- **File endpoints** (`archive`, `inbox`) need `multipart/form-data`; only JSON bodies are
  sent today. Adding them means a separate code path, not a tweak.
- **No typed endpoint wrappers** yet — calls are `client.get("customers")` with dicts.
- **Webhooks** (consent created/revoked) are configured in the portal; nothing here
  receives them.
- **Legacy auth** (static `Access-Token` + `Client-Secret` headers) is retired and
  unsupported.

## Developer portal

Reached from Fortnox: Menu → *Developer portal*. Registration needs a Swedish personal or
organisation number. The portal issues the client id and secret, holds the redirect URI
and scope list, and creates **up to 30 sandbox companies** — each a full Fortnox company
on your own email address, administered like any other.

Test against a sandbox, never a live customer. Publishing to real customers is reviewed:
Fortnox checks the software, landing page, contact details, pricing and user agreement,
and you accept their partner agreement.

## Source

Everything here was verified against `https://www.fortnox.se/developer`. When something
looks wrong, that is the authority — these notes are a convenience, not a substitute.
