# Fortnox Object: InvoiceRequests

API group `Recurring-API` · spec tag `Recurring-API_InvoiceRequests`

## Purpose

Returns invoice requests (the administrative records for invoice generation) for the supplied recurring IDs, optionally narrowed by status.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/recurring-billing/recurrings-invoice-requests-v1` | List all invoice requests |
| POST | `/api/recurring-billing/recurrings-invoice-requests-v1` | Create invoice requests for multiple recurrings |
| GET | `/api/recurring-billing/recurrings-invoice-requests-v1/{invoice-request-id}` | Get an invoice request by ID |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/recurring-billing/recurrings-invoice-requests-v1")
```

**The list response is a bare JSON array, not a wrapped object.**
`client.paginate()` assumes the `/3/` wrapping and will not work here -
iterate the returned list directly and handle paging from the parameters below.

## Key fields

`created_at`, `id`, `items`, `modified_at`, `processed_at`, `processing_mode`, `status`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `recurring-ids` | array | Recurring IDs to return invoice requests for. At least one and at most 100 IDs, comma-separated. |
| `status` | array | Filter by invoice request status. Multiple values must be comma-separated (e.g. `status=PENDING,FAILED`). |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read InvoiceRequests for investigation, reporting and export.

## Dangerous / live actions

- `POST` change live accounting data in the customer's company.
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
