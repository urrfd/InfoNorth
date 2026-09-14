# Fortnox Object: ArticleFileConnections

API group `fortnox` · spec tag `fortnox_ArticleFileConnections`

## Purpose

The article file connections register can return a list of records or a single record. By specifying a FileId in the URL, a single record will be returned. Not specifying a FileId will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/articlefileconnections` | Retrieve a list of article file connections |
| POST | `/3/articlefileconnections` | Create an article file connection |
| GET | `/3/articlefileconnections/{FileId}` | Retrieve a single article file connection |
| DELETE | `/3/articlefileconnections/{FileId}` | Remove an article file connection |

## Calling it

Records are wrapped under `ArticleFileConnections`, so pagination works normally:

```python
for record in client.paginate("articlefileconnections", "ArticleFileConnections"):
    ...
```

## Key fields

`ArticleNumber`, `FileId`

## Writable fields

`ArticleNumber`, `FileId`

Required: `ArticleNumber`, `FileId`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `articlenumber` | string | Articlenumber of file connections to list |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read ArticleFileConnections for investigation, reporting and export.

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
