# Fortnox Object: AssetTypes

API group `fortnox` · spec tag `fortnox_AssetTypes`

## Purpose

Get assets

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/assets/types` | Retrieve a list of asset types |
| POST | `/3/assets/types` | Create an asset type |
| GET | `/3/assets/types/{id}` | Retrieve an asset type |
| PUT | `/3/assets/types/{id}` | Update an asset type |
| DELETE | `/3/assets/types/{id}` | Delete an asset type |

## Calling it

Records are wrapped under `Types`, so pagination works normally:

```python
for record in client.paginate("assets/types", "Types"):
    ...
```

## Key fields

`AccountAsset`, `AccountAssetId`, `AccountDepreciation`, `AccountDepreciationId`, `AccountOffsetSale`, `AccountOffsetSaleId`, `AccountRevaluation`, `AccountRevaluationId`, `AccountSaleLoss`, `AccountSaleLossId`, `AccountSaleWin`, `AccountSaleWinId`, `AccountValueLoss`, `AccountValueLossId`, `AccountWriteDown`, `AccountWriteDownAck`, `AccountWriteDownAckId`, `AccountWriteDownId`, `Description`, `Id`, `InUse`, `Notes`, `Number`, `Type`

## Writable fields

`AccountAssetId`, `AccountDepreciationId`, `AccountOffsetSaleId`, `AccountRevaluationId`, `AccountSaleLossId`, `AccountSaleWinId`, `AccountValueLossId`, `AccountWriteDownAckId`, `AccountWriteDownId`, `Description`, `Notes`, `Number`, `Type`

Required: none declared in the spec

## Safe use cases

- Read AssetTypes for investigation, reporting and export.

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
