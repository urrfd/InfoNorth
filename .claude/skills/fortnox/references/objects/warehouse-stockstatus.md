# Fortnox Object: StockStatus

API group `warehouse` · spec tag `warehouse_StockStatus`

## Purpose

<p>
 Get stock balance for each stockpoint.
 <p>
 Returns a list of <code>itemId</code>, <code>stockPointCode</code>,
 <code>availableStock</code>, <code>inStock</code>.
 <p>
 (The difference between <code>availableStock</code> and <code>inStock</code>
 is the reserved amount.)

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/status-v1/stockbalance` | Get stock balance |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/status-v1/stockbalance")
```

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `itemIds` | array | Optional filter on itemIds (comma-separated) |
| `stockPointCodes` | array | Optional filter on stock point codes (comma-separated). |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read StockStatus for investigation, reporting and export.

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
