# Fortnox Object: Inbox

API group `fortnox` · spec tag `fortnox_Inbox`

## Purpose

Get folders

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/inbox` | Retrieve the root folder containing files and folders |
| POST | `/3/inbox` | Upload a file |
| GET | `/3/inbox/{Id}` | Retrieve a single file |
| DELETE | `/3/inbox/{Id}` | Remove a file or folder |

## Calling it

Records are wrapped under `Folder`, so pagination works normally:

```python
for record in client.paginate("inbox", "Folder"):
    ...
```

## Key fields

`Email`, `Files`, `Folders`, `Id`, `Name`

## Safe use cases

- Read Inbox for investigation, reporting and export.

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
