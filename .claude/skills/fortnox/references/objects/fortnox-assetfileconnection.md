# Fortnox Object: AssetFileConnection

API group `fortnox` · spec tag `fortnox_AssetFileConnection`

## Purpose

The asset register can return a list of assets or a single asset. By specifying a FileId in the URL, a single asset will be returned. Not specifying a FileId will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/assetfileconnections` | Retrieve a list of asset file connections |
| POST | `/3/assetfileconnections` | Create an asset file connection |
| DELETE | `/3/assetfileconnections/{FileId}` | Remove an asset file connection |

## Calling it

Records are wrapped under `AssetFileConnections`, so pagination works normally:

```python
for record in client.paginate("assetfileconnections", "AssetFileConnections"):
    ...
```

## Key fields

`AssetId`, `FileId`, `Name`

## Writable fields

`AssetId`, `FileId`, `Name`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `assetid` | string | Assetid of asset file connections to list |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read AssetFileConnection for investigation, reporting and export.

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
