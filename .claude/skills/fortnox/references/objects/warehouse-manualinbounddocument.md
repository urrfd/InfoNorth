# Fortnox Object: ManualInboundDocument

API group `warehouse` · spec tag `warehouse_ManualInboundDocument`

## Purpose

Get manual inbound document

## Endpoints

| Method | Path | Summary |
|---|---|---|
| POST | `/api/warehouse/deliveries-v1/inbounddeliveries` | Create manual inbound document |
| GET | `/api/warehouse/deliveries-v1/inbounddeliveries/{id}` | Get manual inbound document |
| PUT | `/api/warehouse/deliveries-v1/inbounddeliveries/{id}` | Update manual inbound document |
| PATCH | `/api/warehouse/deliveries-v1/inbounddeliveries/{id}` | Update note on manual inbound document |
| PUT | `/api/warehouse/deliveries-v1/inbounddeliveries/{id}/release` | Release manual inbound document |
| PUT | `/api/warehouse/deliveries-v1/inbounddeliveries/{id}/void` | Void manual inbound document |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("https://api.fortnox.se/api/warehouse/deliveries-v1/inbounddeliveries")
```

## Key fields

`batch`, `costCenterCode`, `directCost`, `freightCost`, `itemDescription`, `itemId`, `itemUnit`, `otherCost`, `projectId`, `quantity`, `rowId`, `stockLocationCode`, `stockLocationId`, `stockLocationName`, `stockPointCode`, `stockPointId`, `stockPointName`

## Writable fields

`batch`, `costCenterCode`, `directCost`, `freightCost`, `itemDescription`, `itemId`, `itemUnit`, `otherCost`, `projectId`, `quantity`, `rowId`, `stockLocationCode`, `stockLocationId`, `stockLocationName`, `stockPointCode`, `stockPointId`, `stockPointName`

Required: `itemId`, `quantity`

## Safe use cases

- Read ManualInboundDocument for investigation, reporting and export.

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
