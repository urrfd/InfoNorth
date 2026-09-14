# Fortnox Object: Labels

API group `fortnox` · spec tag `fortnox_Labels`

## Purpose

Get labels

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/labels` | Retrieve a list of labels |
| POST | `/3/labels` | Create a label |
| PUT | `/3/labels/{Id}` | Update a label |
| DELETE | `/3/labels/{Id}` | Delete a label |

## Calling it

Records are wrapped under `Labels`, so pagination works normally:

```python
for record in client.paginate("labels", "Labels"):
    ...
```

## Key fields

`Description`, `Id`

## Writable fields

`Description`, `Id`

Required: `Description`

## Safe use cases

- Read Labels for investigation, reporting and export.

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
