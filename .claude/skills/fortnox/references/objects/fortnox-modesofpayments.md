# Fortnox Object: ModesOfPayments

API group `fortnox` · spec tag `fortnox_ModesOfPayments`

## Purpose

The modes of payments register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/modesofpayments` | Retrieve a list of modes of payments |
| POST | `/3/modesofpayments` | Create a mode of payment |
| GET | `/3/modesofpayments/{Code}` | Retrieve a single mode of payment |
| PUT | `/3/modesofpayments/{Code}` | Update a mode of payment |
| DELETE | `/3/modesofpayments/{Code}` | Remove a mode of payment |

## Calling it

Records are wrapped under `ModesOfPayments`, so pagination works normally:

```python
for record in client.paginate("modesofpayments", "ModesOfPayments"):
    ...
```

## Key fields

`AccountNumber`, `Code`, `Description`

## Writable fields

`AccountNumber`, `Code`, `Description`

Required: `AccountNumber`

## Safe use cases

- Read ModesOfPayments for investigation, reporting and export.

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
