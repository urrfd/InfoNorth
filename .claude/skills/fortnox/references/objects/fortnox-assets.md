# Fortnox Object: Assets

API group `fortnox` · spec tag `fortnox_Assets`

## Purpose

Get assets

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/assets` | Retrieve a list of assets |
| POST | `/3/assets` | Create an Asset |
| PUT | `/3/assets/changeob/{Id}` | Change manual OB value of an Asset |
| POST | `/3/assets/depreciate` | Perform a Depreciation of an Asset |
| GET | `/3/assets/depreciations/{ToDate}` | Assets depreciation list |
| PUT | `/3/assets/scrap/{Id}` | Scrap an Asset |
| PUT | `/3/assets/sell/{Id}` | Sell an Asset |
| PUT | `/3/assets/writedown/{Id}` | Write down an Asset |
| PUT | `/3/assets/writeup/{Id}` | Write up an Asset |
| GET | `/3/assets/{Id}` | Retrieve a single asset |
| PUT | `/3/assets/{Id}` | Update an Asset |
| DELETE | `/3/assets/{Id}` | Delete or Void an Asset |

## Calling it

Records are wrapped under `Assets`, so pagination works normally:

```python
for record in client.paginate("assets", "Assets"):
    ...
```

## Key fields

`AcquisitionDate`, `AcquisitionStart`, `AcquisitionValue`, `Brand`, `CostCenter`, `Department`, `DepreciateToResidualValue`, `DepreciatedTo`, `DepreciationFinal`, `DepreciationMethod`, `Description`, `Group`, `History`, `Id`, `InsuredNumber`, `InsuredWith`, `ManualOb`, `Notes`, `Number`, `Placement`, `Project`, `Reference`, `Room`, `Status`, `StatusId`, `Type`, `TypeId`

## Writable fields

`AcquisitionDate`, `AcquisitionStart`, `AcquisitionValue`, `Brand`, `CostCenter`, `Department`, `DepreciateToResidualValue`, `DepreciationFinal`, `DepreciationMethod`, `Description`, `Group`, `InsuredNumber`, `InsuredWith`, `Notes`, `Number`, `Placement`, `Project`, `Reference`, `Room`, `TypeId`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `description` | string | Asset description |
| `number` | string | Asset number |
| `type` | string | Asset type |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`.

## Safe use cases

- Read Assets for investigation, reporting and export.

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
