# Fortnox Object: Prices

API group `fortnox` · spec tag `fortnox_Prices`

## Purpose

Retrieve a price

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/prices` | Retrieve a list of prices |
| POST | `/3/prices` | Create a price |
| GET | `/3/prices/sublist/{PriceList}/{ArticleNumber}` | Retrieve a list of articles with all their prices in the specified price list |
| GET | `/3/prices/{PriceList}/{ArticleNumber}` | Retrieve the first price for the specified article |
| PUT | `/3/prices/{PriceList}/{ArticleNumber}` | Update the first price in the specified article |
| GET | `/3/prices/{PriceList}/{ArticleNumber}/{FromQuantity}` | Retrieve a price for a specified article |
| PUT | `/3/prices/{PriceList}/{ArticleNumber}/{FromQuantity}` | Update a price |
| DELETE | `/3/prices/{PriceList}/{ArticleNumber}/{FromQuantity}` | Delete a single price |

## Calling it

Records are wrapped under `Price`, so pagination works normally:

```python
for record in client.paginate("prices", "Price"):
    ...
```

## Key fields

`ArticleNumber`, `Date`, `FromQuantity`, `Percent`, `Price`, `PriceList`

## Writable fields

`ArticleNumber`, `Date`, `FromQuantity`, `Percent`, `Price`, `PriceList`

Required: `ArticleNumber`, `PriceList`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `fromquantity` | number | Lists prices by from quantity |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read Prices for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, POST, PUT` change live accounting data in the customer's company.
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
