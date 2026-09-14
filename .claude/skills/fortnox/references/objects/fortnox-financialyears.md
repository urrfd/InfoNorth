# Fortnox Object: FinancialYears

API group `fortnox` · spec tag `fortnox_FinancialYears`

## Purpose

Add the query param to filter on specific date.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/financialyears` | Retrieve a list of financial years |
| POST | `/3/financialyears` | Create a financial year |
| GET | `/3/financialyears/{Id}` | Retrieve financial year by id |

## Calling it

Records are wrapped under `FinancialYears`, so pagination works normally:

```python
for record in client.paginate("financialyears", "FinancialYears"):
    ...
```

## Key fields

`AccountChartType`, `AccountingMethod`, `FromDate`, `Id`, `ToDate`

## Writable fields

`AccountChartType`, `AccountingMethod`, `FromDate`, `Id`, `ToDate`

Required: `FromDate`, `ToDate`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `Date` | string | date to filter on, for example 2020-06-30 |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read FinancialYears for investigation, reporting and export.

## Dangerous / live actions

- `POST` change live accounting data in the customer's company.
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
