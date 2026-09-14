# Fortnox Object: VacationDebtBasis

API group `fortnox` · spec tag `fortnox_VacationDebtBasis`

## Purpose

Retrieve a vacation debt basis

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/vacationdebtbasis/{Year}/{Month}` | Retrieve a specific vacation debt basis for a posted voucher |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("vacationdebtbasis/{Year}/{Month}")
```

## Key fields

`Employees`, `LastDay`, `Month`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `Year`

## Safe use cases

- Read VacationDebtBasis for investigation, reporting and export.

## Dangerous / live actions

- None: this resource is read-only.

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
