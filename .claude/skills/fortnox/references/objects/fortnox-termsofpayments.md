# Fortnox Object: TermsOfPayments

API group `fortnox` · spec tag `fortnox_TermsOfPayments`

## Purpose

Get terms of payments

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/termsofpayments` | Retrieve a list of all terms of payments |
| POST | `/3/termsofpayments` | Create a term of payment |
| GET | `/3/termsofpayments/{Code}` | Retrieve a single terms of payment |
| PUT | `/3/termsofpayments/{Code}` | Update a term of payment |
| DELETE | `/3/termsofpayments/{Code}` | Remove a term of payment |

## Calling it

Records are wrapped under `TermsOfPayments`, so pagination works normally:

```python
for record in client.paginate("termsofpayments", "TermsOfPayments"):
    ...
```

## Key fields

`Code`, `Description`

## Writable fields

`Code`, `Description`

Required: `Code`, `Description`

## Safe use cases

- Read TermsOfPayments for investigation, reporting and export.

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
