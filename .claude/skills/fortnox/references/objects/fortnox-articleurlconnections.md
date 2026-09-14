# Fortnox Object: ArticleUrlConnections

API group `fortnox` · spec tag `fortnox_ArticleUrlConnections`

## Purpose

The article url connections register can return a list of records or a single record. By specifying an id in the URL, a single record will be returned. Not specifying an id will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/articleurlconnections` | Retrieve a list of article url connections |

## Calling it

Records are wrapped under `ArticleUrlConnections`, so pagination works normally:

```python
for record in client.paginate("articleurlconnections", "ArticleUrlConnections"):
    ...
```

## Key fields

`ArticleNumber`, `Id`, `URLConnection`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `articlenumber` | integer | identifies the article |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read ArticleUrlConnections for investigation, reporting and export.

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
