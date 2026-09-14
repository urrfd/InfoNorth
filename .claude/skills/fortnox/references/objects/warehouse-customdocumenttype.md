# Fortnox Object: CustomDocumentType

API group `warehouse` · spec tag `warehouse_CustomDocumentType`

## Purpose

List custom document types

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/documentdeliveries/custom/documenttypes-v1` | List custom document types |
| POST | `/api/warehouse/documentdeliveries/custom/documenttypes-v1` | Create custom document type |
| GET | `/api/warehouse/documentdeliveries/custom/documenttypes-v1/{type}` | Get custom document type |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/documentdeliveries/custom/documenttypes-v1")
```

## Writable fields

`category`, `referenceType`

Required: `category`, `referenceType`

## Safe use cases

- Read CustomDocumentType for investigation, reporting and export.

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
