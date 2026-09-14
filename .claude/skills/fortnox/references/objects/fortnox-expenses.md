# Fortnox Object: Expenses

API group `fortnox` · spec tag `fortnox_Expenses`

## Purpose

Retrieve expense codes.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/expenses` | Retrieve expenses |
| POST | `/3/expenses` | Create an expense |
| GET | `/3/expenses/{ExpenseCode}` | Retrieve an expense |

## Calling it

Records are wrapped under `Expenses`, so pagination works normally:

```python
for record in client.paginate("expenses", "Expenses"):
    ...
```

## Key fields

`Account`, `Code`, `Text`

## Writable fields

`Account`, `Code`, `Text`

Required: `Account`, `Code`, `Text`

## Safe use cases

- Read Expenses for investigation, reporting and export.

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
