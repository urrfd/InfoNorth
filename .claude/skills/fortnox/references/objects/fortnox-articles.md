# Fortnox Object: Articles

API group `fortnox` · spec tag `fortnox_Articles`

## Purpose

Retrieves a list of articles. The articles are returned sorted by article number with the lowest number appearing first.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/articles` | Retrieve a list of articles |
| POST | `/3/articles` | Create an article |
| GET | `/3/articles/{ArticleNumber}` | Retrieve an article |
| PUT | `/3/articles/{ArticleNumber}` | Update an article |
| DELETE | `/3/articles/{ArticleNumber}` | Delete an article |

## Calling it

Records are wrapped under `Articles`, so pagination works normally:

```python
for record in client.paginate("articles", "Articles"):
    ...
```

## Key fields

`Active`, `ArticleNumber`, `Bulky`, `CommodityCode`, `ConstructionAccount`, `CostCalculationMethod`, `DefaultStockLocation`, `DefaultStockPoint`, `Depth`, `Description`, `DirectCost`, `DisposableQuantity`, `EAN`, `EUAccount`, `EUVATAccount`, `Expired`, `ExportAccount`, `FreightCost`, `Height`, `Housework`, `HouseworkType`, `Manufacturer`, `ManufacturerArticleNumber`, `Note`, `OtherCost`, `PurchaseAccount`, `PurchasePrice`, `QuantityInStock`, `ReservedQuantity`, `SalesAccount`, `SalesPrice`, `StockAccount`, `StockChangeAccount`, `StockGoods`, `StockPlace`, `StockValue`, `StockWarning`, `SupplierName`, `SupplierNumber`, `Type`, `Unit`, `VAT`, `WebshopArticle`, `Weight`, `Width`

## Writable fields

`Active`, `ArticleNumber`, `Bulky`, `ConstructionAccount`, `CostCalculationMethod`, `DefaultStockLocation`, `DefaultStockPoint`, `Depth`, `Description`, `DirectCost`, `DisposableQuantity`, `EAN`, `EUAccount`, `EUVATAccount`, `Expired`, `ExportAccount`, `FreightCost`, `Height`, `Housework`, `HouseworkType`, `Manufacturer`, `ManufacturerArticleNumber`, `Note`, `OtherCost`, `PurchaseAccount`, `PurchasePrice`, `QuantityInStock`, `ReservedQuantity`, `SalesAccount`, `SalesPrice`, `StockAccount`, `StockChangeAccount`, `StockGoods`, `StockPlace`, `StockValue`, `StockWarning`, `SupplierName`, `SupplierNumber`, `Type`, `Unit`, `VAT`, `WebshopArticle`, `Weight`, `Width`

Required: `Description`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `articlenumber` | string | filter by article number |
| `description` | string | filter by description |
| `ean` | string | filter by ean |
| `filter` | `active`, `inactive` | possibility to filter supplier invoices |
| `manufacturer` | string | filter by manufacturer |
| `manufacturerarticlenumber` | string | filter by manufacturerarticlenumber |
| `suppliernumber` | string | filter by supplier number |
| `webshop` | string | filter by web shop |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read Articles for investigation, reporting and export.

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
