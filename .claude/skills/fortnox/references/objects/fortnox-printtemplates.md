# Fortnox Object: PrintTemplates

API group `fortnox` · spec tag `fortnox_PrintTemplates`

## Purpose

Get print templates

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/printtemplates` | Retrieve a list of print templates |

## Calling it

Records are wrapped under `PrintTemplates`, so pagination works normally:

```python
for record in client.paginate("printtemplates", "PrintTemplates"):
    ...
```

## Key fields

`Name`, `Template`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `type` | string | Filters the list of print templates by type |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read PrintTemplates for investigation, reporting and export.

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
