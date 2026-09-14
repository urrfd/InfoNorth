# Fortnox Object: Integration Sales

API group `integration-developer` · spec tag `integration-developer_Integration Sales`

## Purpose

<p>
 Prerequisites
 The partner has an active developer account and a published integration that is purchased through Fortnox.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/integration-developer/sales-v1/{integrationId}` | Resolves sales information of an integration |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("https://api.fortnox.se/api/integration-developer/sales-v1/{integrationId}")
```

## Safe use cases

- Read Integration Sales for investigation, reporting and export.

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
