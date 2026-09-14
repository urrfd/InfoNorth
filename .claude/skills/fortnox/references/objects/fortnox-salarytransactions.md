# Fortnox Object: SalaryTransactions

API group `fortnox` · spec tag `fortnox_SalaryTransactions`

## Purpose

Supports query-string parameters <b>employeeid</b> and <b>date</b> for filtering the result.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/salarytransactions` | List all salary transactions for all employees |
| POST | `/3/salarytransactions` | Create a new salary transaction for an employee |
| GET | `/3/salarytransactions/{SalaryRow}` | Retrieve a single salary transaction |
| PUT | `/3/salarytransactions/{SalaryRow}` | Update a salary transaction |
| DELETE | `/3/salarytransactions/{SalaryRow}` | Delete a single salary transaction |

## Calling it

Records are wrapped under `SalaryTransactions`, so pagination works normally:

```python
for record in client.paginate("salarytransactions", "SalaryTransactions"):
    ...
```

## Key fields

`Amount`, `CostCenter`, `Date`, `EmployeeId`, `Expense`, `Number`, `Project`, `SalaryCode`, `SalaryRow`, `TextRow`, `Total`, `VAT`

## Writable fields

`Amount`, `CostCenter`, `Date`, `EmployeeId`, `Expense`, `Number`, `Project`, `SalaryCode`, `SalaryRow`, `TextRow`, `Total`, `VAT`

Required: `Date`, `EmployeeId`, `SalaryCode`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `date` | string | filter on date |
| `employeeId` | string | filter on employeeId |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read SalaryTransactions for investigation, reporting and export.

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
