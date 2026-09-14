# Fortnox Object: CustomOutboundDocument

API group `warehouse` · spec tag `warehouse_CustomOutboundDocument`

## Purpose

Get custom outbound document

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{id}` | Get custom outbound document |
| PUT | `/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{id}` | Save a custom outbound document |
| PUT | `/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{id}/release` | Release custom outbound document |
| PUT | `/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{id}/void` | Void custom outbound document |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("https://api.fortnox.se/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{id}")
```

## Key fields

`averageCostInSEK`, `itemId`, `stockPointId`

## Writable fields

`averageCostInSEK`, `itemId`, `stockPointId`

Required: none declared in the spec

## Safe use cases

- Read CustomOutboundDocument for investigation, reporting and export.

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
