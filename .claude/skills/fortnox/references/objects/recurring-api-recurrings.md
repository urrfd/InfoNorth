# Fortnox Object: Recurrings

API group `Recurring-API` · spec tag `Recurring-API_Recurrings`

## Purpose

Returns a paginated list of recurring contracts for the authenticated tenant. The result can be narrowed with the `customer-numbers`, `statuses`, `invoice-handlings` and `error-status` filters, ordered with `sortby` and `order`, and paged with `offset` and `limit` (1-100, default 100). Pagination metadata is returned in the `X-PAGINATION` and `X-LAST-RECORD` response headers.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/recurring-billing/recurrings-v1` | List all recurring contracts |
| POST | `/api/recurring-billing/recurrings-v1` | Create a new Recurring |
| GET | `/api/recurring-billing/recurrings-v1/{recurring-id}` | Get a recurring by ID |
| PUT | `/api/recurring-billing/recurrings-v1/{recurring-id}` | Update a Recurring by ID |
| PATCH | `/api/recurring-billing/recurrings-v1/{recurring-id}` | Update only specified fields of a Recurring by ID |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/recurring-billing/recurrings-v1")
```

**The list response is a bare JSON array, not a wrapped object.**
`client.paginate()` assumes the `/3/` wrapping and will not work here -
iterate the returned list directly and handle paging from the parameters below.

## Writable fields

`address`, `city`, `country_code`, `name`, `number`, `phone`, `zip`

Required: `number`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `customer-numbers` | array | Filter by customer numbers. Multiple values must be comma-separated (e.g. `customer-numbers=1,2,3`). |
| `error-status` |  | Filter recurrings by error status |
| `invoice-handlings` | array | Filter by invoice handling types. Multiple values must be comma-separated (e.g. `invoice-handlings=MANUAL,AUTOMATIC`). |
| `order` |  | Sort order direction |
| `statuses` | array | Filter by recurring statuses. Multiple values must be comma-separated (e.g. `statuses=ACTIVE,DRAFT`). |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `limit`, `offset`, `sortby`.

## Safe use cases

- Read Recurrings for investigation, reporting and export.

## Dangerous / live actions

- `PATCH, POST, PUT` change live accounting data in the customer's company.
- These post to real books. Keep them behind the read-only default, a dry run,
  and explicit approval.

## Dry-run requirements

- Verify with a read-only `GET` first.
- Write out the exact request body and target, and have it reviewed, before any write.
- Run it against a sandbox company before a live tenant.

## Approval requirements

- Explicit user approval for every write. Approval for one write is not approval
  for the next.

## Tested read-only requests

- None yet. Add the exact calls you have run once verified against a real tenant.

## Example response fields

- Fill in after reviewing a successful response. The fields above come from the
  spec, which describes what may be returned, not what a given company does return.

## Date tested

- Not yet verified against a live or sandbox tenant.

## Notes

- Generated from the Fortnox OpenAPI specification; do not edit by hand.
  Regenerate with `python generate_object_notes.py`.
