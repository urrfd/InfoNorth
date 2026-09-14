# Fortnox Object: Archive

API group `fortnox` · spec tag `fortnox_Archive`

## Purpose

If no path is provided the root will be returned.
 Providing fileId will return given file from fileattachments.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/archive` | Retrieve folder or file |
| POST | `/3/archive` | Upload a file to a specific subdirectory |
| DELETE | `/3/archive` | Remove files |
| GET | `/3/archive/{id}` | Retrieve a single file |
| DELETE | `/3/archive/{id}` | Delete a single file |

## Calling it

Records are wrapped under `Folder`, so pagination works normally:

```python
for record in client.paginate("archive", "Folder"):
    ...
```

## Key fields

`Email`, `Files`, `Folders`, `Id`, `Name`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `fileid` | string | fileId from fileattachments |
| `path` | string | name of folder |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read Archive for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, POST` change live accounting data in the customer's company.
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
