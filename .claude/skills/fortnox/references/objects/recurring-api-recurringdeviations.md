# Fortnox Object: RecurringDeviations

API group `Recurring-API` · spec tag `Recurring-API_RecurringDeviations`

## Purpose

Returns the deviations defined for a recurring. A deviation overrides the normal invoicing for one or more occurrences of the recurring — either changing the rows (`ROWS`) or skipping the invoice entirely (`SKIP`).

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/recurring-billing/recurrings-v1/{recurring-id}/deviations` | List all deviations for a recurring |
| GET | `/api/recurring-billing/recurrings-v1/{recurring-id}/deviations/{deviation-id}` | Get a deviation by ID |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("https://api.fortnox.se/api/recurring-billing/recurrings-v1/{recurring-id}/deviations")
```

## Safe use cases

- Read RecurringDeviations for investigation, reporting and export.

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
