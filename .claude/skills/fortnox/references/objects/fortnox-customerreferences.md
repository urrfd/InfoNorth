# Fortnox Object: CustomerReferences

API group `fortnox` · spec tag `fortnox_CustomerReferences`

## Purpose

</p>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/customerreferences` | Retrieve a list of customers reference rows |
| POST | `/3/customerreferences` | Create a customer reference row |
| GET | `/3/customerreferences/{CustomerReferenceRowId}` | Retrieve a customer reference row |
| PUT | `/3/customerreferences/{CustomerReferenceRowId}` | Update a customer reference row |
| DELETE | `/3/customerreferences/{CustomerReferenceRowId}` | Delete a customer reference row |

## Calling it

Records are wrapped under `CustomerReference`, so pagination works normally:

```python
for record in client.paginate("customerreferences", "CustomerReference"):
    ...
```

## Key fields

`CustomerReferenceRows`

## Writable fields

`CustomerNumber`, `Id`, `Reference`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `customer` | string | possibility to filter by customer number |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read CustomerReferences for investigation, reporting and export.

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
