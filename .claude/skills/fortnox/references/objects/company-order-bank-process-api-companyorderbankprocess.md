# Fortnox Object: CompanyOrderBankProcess

API group `Company-Order-Bank-Process-API` · spec tag `Company-Order-Bank-Process-API_CompanyOrderBankProcess`

## Purpose

Returns a list of orders depending on the statuses provided.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/bank-process-orders/v1` | Returns orders |
| GET | `/api/bank-process-orders/v1/find-by-organization-number/{organization_number}` | Returns zero or multiple orders |
| GET | `/api/bank-process-orders/v1/{order_id}` | Returns an order |
| PATCH | `/api/bank-process-orders/v1/{order_id}` | Modify an order |
| GET | `/api/bank-process-orders/v1/{order_id}/documents` | Returns available document types for an order |
| POST | `/api/bank-process-orders/v1/{order_id}/documents` | Create or update a document for an order. |
| PUT | `/api/bank-process-orders/v1/{order_id}/documents` | Create or update a document for an order. |
| GET | `/api/bank-process-orders/v1/{order_id}/documents/{document_type}/content` | Returns content of order document |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/bank-process-orders/v1")
```

## Key fields

`accountant`, `bank_power_of_attorney`, `board_members`, `company_information`, `contact_person`, `created_at`, `foreign_business_countries`, `general_power_of_attorney`, `id`, `secondary_power_of_attorney`, `share_holders`, `status`, `subsidiaries`, `updated_at`, `utm_source`

## Writable fields

`status`

Required: `status`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `status` | array | Filter orders by one or more statuses. - ACCEPTED: Orders accepted by us and currently in active processing. - SENT_TO_BV: Orders that have been sent to and are being processed by Bolagsverket. - COMPLETED: Orders that are completed and finalized. - ABORTED: Orders that have been cancelled by us. - DENIED_BY_BANK: Orders that were denied by the bank. Note: UNKNOWN is not a valid filter value. It may appear as a status on returned orders if an internal status could not be mapped to a known bank-process status. |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `limit`, `offset`.

## Safe use cases

- Read CompanyOrderBankProcess for investigation, reporting and export.

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
