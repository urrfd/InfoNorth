# Fortnox Object: ScheduleTimes

API group `fortnox` · spec tag `fortnox_ScheduleTimes`

## Purpose

Retrieve a schedule time

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/scheduletimes/{EmployeeId}/{Date}` | Retrieve a specific schedule time |
| PUT | `/3/scheduletimes/{EmployeeId}/{Date}` | Update a schedule time |
| PUT | `/3/scheduletimes/{EmployeeId}/{Date}/resetday` | Reset schedule time |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("scheduletimes/{EmployeeId}/{Date}")
```

## Key fields

`Date`, `EmployeeId`, `Hours`, `IWH1`, `IWH2`, `IWH3`, `IWH4`, `IWH5`, `ScheduleId`

## Writable fields

`Date`, `EmployeeId`, `Hours`, `IWH1`, `IWH2`, `IWH3`, `IWH4`, `IWH5`, `ScheduleId`

Required: none declared in the spec

## Safe use cases

- Read ScheduleTimes for investigation, reporting and export.

## Dangerous / live actions

- `PUT` change live accounting data in the customer's company.
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
