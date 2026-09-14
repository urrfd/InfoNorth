# Fortnox Object: StartCompanyOrderBankProcess

API group `Company-Order-Bank-Process-API` · spec tag `Company-Order-Bank-Process-API_StartCompanyOrderBankProcess`

## Purpose

Returns a list of orders depending on the statuses provided.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/bank-process-start-orders/v1` | Returns start company orders |
| GET | `/api/bank-process-start-orders/v1/{order_id}` | Returns a start company order |
| PATCH | `/api/bank-process-start-orders/v1/{order_id}` | Modify an order |
| GET | `/api/bank-process-start-orders/v1/{order_id}/documents` | Returns available document types for an order |
| POST | `/api/bank-process-start-orders/v1/{order_id}/documents` | Create document for the order |
| GET | `/api/bank-process-start-orders/v1/{order_id}/documents/{document_type}/content` | Returns content of order document |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/bank-process-start-orders/v1")
```

## Key fields

`authorized_signatories`, `board_members`, `company_information`, `contact_person`, `created_at`, `id`, `share_capital_received_date`, `share_holders`, `share_info`, `status`, `updated_at`

## Writable fields

`share_capital_received_date`, `status`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `founder_civic_number` | string | Filter orders by founder civic number. |
| `status` | array | Filter orders by one or multiple statuses. |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `limit`, `offset`.

## Safe use cases

- Read StartCompanyOrderBankProcess for investigation, reporting and export.

## Dangerous / live actions

- `PATCH, POST` change live accounting data in the customer's company.
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
