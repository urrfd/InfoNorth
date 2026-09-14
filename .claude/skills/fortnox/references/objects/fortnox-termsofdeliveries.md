# Fortnox Object: TermsOfDeliveries

API group `fortnox` · spec tag `fortnox_TermsOfDeliveries`

## Purpose

The terms of deliveries register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/termsofdeliveries` | Retrieve a list of terms of deliveries |
| POST | `/3/termsofdeliveries` | Create a terms of delivery |
| GET | `/3/termsofdeliveries/{Code}` | Retrieve a single terms of delivery |
| PUT | `/3/termsofdeliveries/{Code}` | Update a terms of delivery |

## Calling it

Records are wrapped under `TermsOfDeliveries`, so pagination works normally:

```python
for record in client.paginate("termsofdeliveries", "TermsOfDeliveries"):
    ...
```

## Key fields

`Code`, `Description`, `DescriptionEnglish`

## Writable fields

`Code`, `Description`, `DescriptionEnglish`

Required: `Code`, `Description`

## Safe use cases

- Read TermsOfDeliveries for investigation, reporting and export.

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
