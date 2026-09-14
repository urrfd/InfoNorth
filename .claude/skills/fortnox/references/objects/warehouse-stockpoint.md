# Fortnox Object: StockPoint

API group `warehouse` · spec tag `warehouse_StockPoint`

## Purpose

<p>
 List stock points, optionally include a query parameter `q` to filter on stock point code or name.
 <p>
 Use query param `state` to filter on ACTIVE, INACTIVE or ALL (default is to include only ACTIVE stock points).
 <p>
 Stock locations are NOT included in the response.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/stockpoints-v1` | List stock points |
| POST | `/api/warehouse/stockpoints-v1` | Create stock point |
| GET | `/api/warehouse/stockpoints-v1/multi` | Get stock points |
| GET | `/api/warehouse/stockpoints-v1/{id}` | Get stock point |
| POST | `/api/warehouse/stockpoints-v1/{id}` | Append stock locations |
| PUT | `/api/warehouse/stockpoints-v1/{id}` | Update stock point |
| DELETE | `/api/warehouse/stockpoints-v1/{id}` | Delete stock point |
| GET | `/api/warehouse/stockpoints-v1/{id}/stocklocations` | Get stock locations |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/stockpoints-v1")
```

## Key fields

`code`, `id`, `name`, `stockPointId`

## Writable fields

`code`, `id`, `name`, `stockPointId`

Required: `code`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `ids` | array | stock point ids (comma separated list of UUIDs) |
| `q` | string | filters on stock point code or name. |
| `state` | `ALL`, `ACTIVE`, `INACTIVE` | filter on stock point state |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read StockPoint for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, POST, PUT` change live accounting data in the customer's company.
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
