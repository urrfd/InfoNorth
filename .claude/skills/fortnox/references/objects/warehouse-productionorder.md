# Fortnox Object: ProductionOrder

API group `warehouse` · spec tag `warehouse_ProductionOrder`

## Purpose

List production orders

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/productionorders-v1` | List production orders |
| POST | `/api/warehouse/productionorders-v1` | Create a new production order |
| GET | `/api/warehouse/productionorders-v1/billofmaterials/{itemId}` | Get the package items (Bill Of Materials, BOMs) for a production article |
| PUT | `/api/warehouse/productionorders-v1/release/{id}` | Release a production order document |
| PUT | `/api/warehouse/productionorders-v1/void/{id}` | Void a production order |
| GET | `/api/warehouse/productionorders-v1/{id}` | Get Production Order document |
| PUT | `/api/warehouse/productionorders-v1/{id}` | Update a production order |
| PATCH | `/api/warehouse/productionorders-v1/{id}` | Update the note of a production order |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/productionorders-v1")
```

## Key fields

`itemDescription`, `itemId`, `itemUnit`, `quantityRequired`, `quantityReserved`, `totalQuantityRequired`

## Writable fields

`itemDescription`, `itemId`, `itemUnit`, `quantityRequired`, `quantityReserved`, `totalQuantityRequired`

Required: `itemId`, `quantityRequired`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `id` | integer | the id of the production order (optional) |
| `itemId` | string | Include only production orders with the given production item. |
| `quantity` | string | the quantity of the production order (assumed 1 if left empty) |
| `state` | `all`, `incomplete`, `delayed`, `completed`, `voided` | Include only production orders with the given state.               Allowed states: all, incomplete, delayed, completed, voided.               (Default is incomplete) |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read ProductionOrder for investigation, reporting and export.

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
