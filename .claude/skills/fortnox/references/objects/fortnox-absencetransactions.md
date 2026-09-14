# Fortnox Object: AbsenceTransactions

API group `fortnox` · spec tag `fortnox_AbsenceTransactions`

## Purpose

Supports query-string parameters <strong>employeeid</strong> and <strong>date</strong> for filtering the result.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/absencetransactions` | Lists all absence transactions |
| POST | `/3/absencetransactions` | Create a new absence transaction |
| GET | `/3/absencetransactions/{id}` | Retrieve a specific absence transaction |
| PUT | `/3/absencetransactions/{id}` | Update a single absence transaction |
| DELETE | `/3/absencetransactions/{id}` | Delete an absence transaction |
| GET | `/3/absencetransactions/{id}/{Date}/{Code}` | Retrieve absence transactions |

## Calling it

Records are wrapped under `AbsenceTransactions`, so pagination works normally:

```python
for record in client.paginate("absencetransactions", "AbsenceTransactions"):
    ...
```

## Key fields

`CauseCode`, `CostCenter`, `Date`, `EmployeeId`, `Extent`, `HolidayEntitling`, `Hours`, `Project`, `id`

## Writable fields

`CauseCode`, `CostCenter`, `Date`, `EmployeeId`, `Extent`, `HolidayEntitling`, `Hours`, `Project`

Required: `CauseCode`, `Date`, `EmployeeId`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `date` | string | filter by date |
| `employeeid` | string | filter by employee id |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read AbsenceTransactions for investigation, reporting and export.

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
