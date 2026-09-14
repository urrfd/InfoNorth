# Fortnox Object: CostCenters

API group `fortnox` · spec tag `fortnox_CostCenters`

## Purpose

The cost centers register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/costcenters` | Retrieve a list of cost centers |
| POST | `/3/costcenters` | Create a cost center |
| GET | `/3/costcenters/{Code}` | Retrieve a single cost center |
| PUT | `/3/costcenters/{Code}` | Update a cost center |
| DELETE | `/3/costcenters/{Code}` | Remove a cost center |

## Calling it

Records are wrapped under `CostCenters`, so pagination works normally:

```python
for record in client.paginate("costcenters", "CostCenters"):
    ...
```

## Key fields

`Active`, `Code`, `Description`, `Note`

## Writable fields

`Active`, `Code`, `Description`, `Note`

Required: `Code`, `Description`

## Safe use cases

- Read CostCenters for investigation, reporting and export.

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
