# Fortnox Object: ManualDocument

API group `warehouse` · spec tag `warehouse_ManualDocument`

## Purpose

List manual documents

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/deliveries-v1` | List manual documents |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/deliveries-v1")
```

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `itemId` | string | Include only documents containing the given item. |
| `state` | `all`, `unreleased`, `released`, `voided` | Include only documents with given state. |
| `type` | `all`, `inbound`, `outbound`, `stocktransfer` | Include only documents with given type. |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read ManualDocument for investigation, reporting and export.

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
