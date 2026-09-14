# Fortnox Object: StockTaking

API group `warehouse` · spec tag `warehouse_StockTaking`

## Purpose

<p>
 Sortable fields:
 <code>id</code>,
 <code>name</code>,
 <code>date</code>,
 <code>responsible</code>,
 <code>state</code>
 </p>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/stocktaking-v1` | List stock takings |
| POST | `/api/warehouse/stocktaking-v1` | Create stock taking |
| GET | `/api/warehouse/stocktaking-v1/{id}` | Get Stock Taking document |
| PUT | `/api/warehouse/stocktaking-v1/{id}` | Update a stock taking |
| DELETE | `/api/warehouse/stocktaking-v1/{id}` | Delete Stock Taking document |
| POST | `/api/warehouse/stocktaking-v1/{id}/addrows` | Add rows by filter |
| GET | `/api/warehouse/stocktaking-v1/{id}/candidates` | Get candidate rows |
| PUT | `/api/warehouse/stocktaking-v1/{id}/release` | Release Stock Taking document |
| GET | `/api/warehouse/stocktaking-v1/{id}/rows` | Get Stock Taking Rows |
| POST | `/api/warehouse/stocktaking-v1/{id}/rows` | Add rows |
| DELETE | `/api/warehouse/stocktaking-v1/{id}/rows` | Delete rows by filter |
| DELETE | `/api/warehouse/stocktaking-v1/{id}/rows/{rowId}` | Delete row |
| PUT | `/api/warehouse/stocktaking-v1/{id}/void` | Void Stock Taking document |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/stocktaking-v1")
```

## Key fields

`countedBy`, `currentRowNo`, `hasPostReleaseStockChanges`, `id`, `itemId`, `stockLocationId`, `stockPointId`, `stockTakenQuantity`, `stockTakingId`, `stockTakingRowId`, `totalQuantityInStock`

## Writable fields

`countedBy`, `currentRowNo`, `hasPostReleaseStockChanges`, `id`, `itemId`, `stockLocationId`, `stockPointId`, `stockTakenQuantity`, `stockTakingId`, `stockTakingRowId`, `totalQuantityInStock`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `excludeZeroBalanceItems` | boolean |  |
| `includeNonInboundItems` | boolean | Include items that do not exist on inbound deliveries. |
| `itemDescriptionSearch` | string |  |
| `itemId` | string | Include only stock takings with the given item. |
| `itemIdSearch` | string |  |
| `itemIds` | array |  |
| `secondaryorder` | string | Secondary sorting order |
| `secondarysortby` | string | Secondary sorting column |
| `startingItemId` | string | the itemId that should be on top of the rows list (used to jump to specific row), can be empty |
| `startingRowNo` | integer | the row number to start the search from, used with startingItemId to jump to specific rows, can be empty |
| `state` | `all`, `planning`, `started`, `completed`, `voided` | Include only stock takings with the given state. |
| `stateFilter` | `all`, `notStockTaken`, `stockTakenNoDeviation`, `stockTakenWithDeviation` |  |
| `stockLocationIds` | array |  |
| `stockPointIds` | array |  |
| `supplierNumbers` | array |  |
| `transactionDate` | string |  |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read StockTaking for investigation, reporting and export.

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
