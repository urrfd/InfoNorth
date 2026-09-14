# Fortnox Object: Orders

API group `fortnox` · spec tag `fortnox_Orders`

## Purpose

Get orders

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/orders` | Retrieve a list of orders |
| POST | `/3/orders` | Create a new order |
| GET | `/3/orders/{DocumentNumber}` | Retrieve a single order |
| PUT | `/3/orders/{DocumentNumber}` | Update an order |
| PUT | `/3/orders/{DocumentNumber}/cancel` | Cancels given order |
| PUT | `/3/orders/{DocumentNumber}/createinvoice` | Create invoice out of given order |
| GET | `/3/orders/{DocumentNumber}/email` | Send given order as email |
| PUT | `/3/orders/{DocumentNumber}/externalprint` | Set given order as sent |
| GET | `/3/orders/{DocumentNumber}/preview` | Preview given offer |
| GET | `/3/orders/{DocumentNumber}/print` | Print given order |

## Calling it

Records are wrapped under `Orders`, so pagination works normally:

```python
for record in client.paginate("orders", "Orders"):
    ...
```

## Key fields

`Address1`, `Address2`, `AdministrationFee`, `AdministrationFeeVAT`, `BasisTaxReduction`, `Cancelled`, `City`, `Comments`, `ContributionPercent`, `ContributionValue`, `CopyRemarks`, `CostCenter`, `Country`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `CustomerName`, `CustomerNumber`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryDate`, `DeliveryName`, `DeliveryState`, `DeliveryZipCode`, `DocumentNumber`, `EmailInformation`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `Freight`, `FreightVAT`, `Gross`, `HouseWork`, `InvoiceReference`, `Labels`, `Language`, `Net`, `NotCompleted`, `OfferReference`, `OrderDate`, `OrderRows`, `OrderType`, `OrganisationNumber`, `OurReference`, `OutboundDate`, `Phone1`, `Phone2`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `RoundOff`, `Sent`, `StockPointCode`, `StockPointId`, `TaxReduction`, `TaxReductionType`, `TermsOfDelivery`, `TermsOfPayment`, `TimeBasisReference`, `Total`, `TotalToPay`, `TotalVAT`, `VATIncluded`, `WarehouseReady`, `WayOfDelivery`, `YourOrderNumber`, `YourReference`, `ZipCode`

## Writable fields

`Address1`, `Address2`, `AdministrationFee`, `City`, `Comments`, `CopyRemarks`, `CostCenter`, `Country`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `CustomerName`, `CustomerNumber`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryDate`, `DeliveryName`, `DeliveryState`, `DeliveryZipCode`, `DocumentNumber`, `EmailInformation`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `Freight`, `Labels`, `Language`, `NotCompleted`, `OrderDate`, `OrderRows`, `OrganisationNumber`, `OurReference`, `OutboundDate`, `Phone1`, `Phone2`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `StockPointCode`, `StockPointId`, `TaxReductionType`, `TermsOfDelivery`, `TermsOfPayment`, `VATIncluded`, `WayOfDelivery`, `YourOrderNumber`, `YourReference`, `ZipCode`

Required: `CustomerNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `costcenter` | string | filter by cost center |
| `customername` | string | filter by customer name |
| `customernumber` | string | filter by customer number |
| `documentnumber` | string | filter by document number |
| `externalinvoicereference1` | string | filter by external invoice reference 1 |
| `externalinvoicereference2` | string | filter by external invoice reference 2 |
| `filter` | `cancelled`, `expired`, `invoicecreated`, `invoicenotcreated` | possibility to filter orders |
| `fromdate` | string | filter by from date |
| `label` | string | filter by label |
| `notcompleted` | boolean | filter by not completed |
| `ordertype` | string | filter by order type |
| `ourreference` | string | filter by ourreference |
| `project` | string | filter by project |
| `sent` | boolean | filter by sent |
| `todate` | string | filter by to date |
| `yourreference` | string | filter by your reference |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read Orders for investigation, reporting and export.

## Dangerous / live actions

- `POST, PUT` change live accounting data in the customer's company.
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
