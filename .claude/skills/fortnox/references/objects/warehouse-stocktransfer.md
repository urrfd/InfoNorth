# Fortnox Object: StockTransfer

API group `warehouse` · spec tag `warehouse_StockTransfer`

## Purpose

Get stock transfer document

## Endpoints

| Method | Path | Summary |
|---|---|---|
| POST | `/api/warehouse/stocktransfer-v1` | Create a stock transfer document |
| GET | `/api/warehouse/stocktransfer-v1/{id}` | Get stock transfer document |
| PUT | `/api/warehouse/stocktransfer-v1/{id}` | Update a stock transfer document |
| PUT | `/api/warehouse/stocktransfer-v1/{id}/release` | Release a stock transfer document |
| PUT | `/api/warehouse/stocktransfer-v1/{id}/void` | Void a stock transfer document |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("https://api.fortnox.se/api/warehouse/stocktransfer-v1")
```

## Key fields

`fromStockLocationCode`, `fromStockLocationId`, `fromStockLocationName`, `fromStockPointCode`, `fromStockPointId`, `fromStockPointName`, `itemDescription`, `itemId`, `itemUnit`, `quantity`, `requestedQuantity`, `rowNum`, `toStockLocationCode`, `toStockLocationId`, `toStockLocationName`, `toStockPointCode`, `toStockPointId`, `toStockPointName`

## Writable fields

`fromStockLocationCode`, `fromStockLocationId`, `fromStockLocationName`, `fromStockPointCode`, `fromStockPointId`, `fromStockPointName`, `itemDescription`, `itemId`, `itemUnit`, `quantity`, `requestedQuantity`, `rowNum`, `toStockLocationCode`, `toStockLocationId`, `toStockLocationName`, `toStockPointCode`, `toStockPointId`, `toStockPointName`

Required: `fromStockPointId`, `itemId`, `requestedQuantity`, `toStockPointId`

## Safe use cases

- Read StockTransfer for investigation, reporting and export.

## Dangerous / live actions

- `POST, PUT` change live accounting data in the customer's company.
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
