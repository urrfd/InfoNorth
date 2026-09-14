# Fortnox Object: Invoices

API group `fortnox` · spec tag `fortnox_Invoices`

## Purpose

Get invoices

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/invoices` | Retrieve a list of invoices |
| POST | `/3/invoices` | Create an invoice |
| GET | `/3/invoices/{DocumentNumber}` | Retrieve a single invoice |
| PUT | `/3/invoices/{DocumentNumber}` | Update an invoice |
| PUT | `/3/invoices/{DocumentNumber}/bookkeep` | Bookkeep an invoice |
| PUT | `/3/invoices/{DocumentNumber}/cancel` | Cancel an invoice |
| PUT | `/3/invoices/{DocumentNumber}/credit` | Credit an invoice |
| GET | `/3/invoices/{DocumentNumber}/einvoice` | Send an invoice as e-invoice |
| GET | `/3/invoices/{DocumentNumber}/email` | Send an invoice as email |
| GET | `/3/invoices/{DocumentNumber}/eprint` | Send an invoice as e-print |
| PUT | `/3/invoices/{DocumentNumber}/externalprint` | Set an invoice as sent |
| GET | `/3/invoices/{DocumentNumber}/preview` | Preview an invoice |
| GET | `/3/invoices/{DocumentNumber}/print` | Print an invoice |
| GET | `/3/invoices/{DocumentNumber}/printreminder` | Print an invoice as reminder |
| PUT | `/3/invoices/{DocumentNumber}/warehouseready` | Set an invoice as done |

## Calling it

Records are wrapped under `Invoices`, so pagination works normally:

```python
for record in client.paginate("invoices", "Invoices"):
    ...
```

## Key fields

`AccountingMethod`, `Address1`, `Address2`, `AdministrationFee`, `AdministrationFeeVAT`, `Balance`, `BasisTaxReduction`, `Booked`, `Cancelled`, `City`, `Comments`, `ContractReference`, `ContributionPercent`, `ContributionValue`, `CostCenter`, `Country`, `Credit`, `CreditInvoiceReference`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `CustomerName`, `CustomerNumber`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryDate`, `DeliveryName`, `DeliveryZipCode`, `DocumentNumber`, `DueDate`, `EDIInformation`, `EUQuarterlyReport`, `EmailInformation`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `FinalPayDate`, `Freight`, `FreightVAT`, `Gross`, `HouseWork`, `InvoiceDate`, `InvoicePeriodEnd`, `InvoicePeriodStart`, `InvoiceReference`, `InvoiceRows`, `InvoiceType`, `Labels`, `Language`, `LastRemindDate`, `Net`, `NotCompleted`, `NoxFinans`, `OCR`, `OfferReference`, `OrderReference`, `OrganisationNumber`, `OurReference`, `OutboundDate`, `PaymentWay`, `Phone1`, `Phone2`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `Reminders`, `RoundOff`, `Sent`, `TaxReduction`, `TaxReductionType`, `TermsOfDelivery`, `TermsOfPayment`, `TimeBasisReference`, `Total`, `TotalToPay`, `TotalVAT`, `VATIncluded`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `WarehouseReady`, `WayOfDelivery`, `YourOrderNumber`, `YourReference`, `ZipCode`

## Writable fields

`Address1`, `Address2`, `AdministrationFee`, `City`, `Comments`, `CostCenter`, `Country`, `CreditInvoiceReference`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `CustomerName`, `CustomerNumber`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryDate`, `DeliveryName`, `DeliveryZipCode`, `DocumentNumber`, `DueDate`, `EDIInformation`, `EUQuarterlyReport`, `EmailInformation`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `Freight`, `InvoiceDate`, `InvoiceRows`, `InvoiceType`, `Labels`, `Language`, `NotCompleted`, `OCR`, `OurReference`, `OutboundDate`, `PaymentWay`, `Phone1`, `Phone2`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `TaxReductionType`, `TermsOfDelivery`, `TermsOfPayment`, `VATIncluded`, `WayOfDelivery`, `YourOrderNumber`, `YourReference`, `ZipCode`

Required: `CustomerNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `accountnumberfrom` | string | Accountnumberfrom of invoices to list |
| `accountnumberto` | string | Accountnumberto of invoices to list |
| `articledescription` | string | Articledescription of invoices to list |
| `articlenumber` | string | Articlenumber of invoices to list |
| `costcenter` | string | Costcenter of invoices to list |
| `credit` | string | Credit of invoices to list |
| `currency` | string | Currency of invoices to list |
| `customername` | string | Customername of invoices to list |
| `customernumber` | string | Customernumber of invoices to list |
| `documentnumber` | string | Documentnumber of invoices to list |
| `externalinvoicereference1` | string | Externalinvoicereference1 of invoices to list |
| `externalinvoicereference2` | string | Externalinvoicereference2 of invoices to list |
| `filter` | `cancelled`, `fullypaid`, `unpaid`, `unpaidoverdue`, `unbooked` | possibility to filter invoices |
| `fromdate` | string | Fromdate of invoices to list |
| `fromfinalpaydate` | string | Fromfinalpaydate of invoices to list |
| `invoicetype` | string | Invoicetype of invoices to list |
| `label` | string | Label of invoices to list |
| `notcompleted` | string | Notcompleted of invoices to list |
| `ocr` | string | Ocr of invoices to list |
| `ourreference` | string | Ourreference of invoices to list |
| `project` | string | Project of invoices to list |
| `sent` | string | Sent of invoices to list |
| `todate` | string | Todate of invoices to list |
| `tofinalpaydate` | string | Tofinalpaydate of invoices to list |
| `yourordernumber` | string | Yourordernumber of invoices to list |
| `yourreference` | string | Yourreference of invoices to list |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read Invoices for investigation, reporting and export.

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
