# Fortnox Object: SupplierInvoices

API group `fortnox` · spec tag `fortnox_SupplierInvoices`

## Purpose

Get supplier invoices

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/supplierinvoices` | Retrieve a list of supplier invoices |
| POST | `/3/supplierinvoices` | Create a supplier invoice |
| GET | `/3/supplierinvoices/{GivenNumber}` | Retrieve a single supplier invoice |
| PUT | `/3/supplierinvoices/{GivenNumber}` | Update a supplier invoice |
| PUT | `/3/supplierinvoices/{GivenNumber}/approvalbookkeep` | Approval of bookkeep of given supplier invoice |
| PUT | `/3/supplierinvoices/{GivenNumber}/approvalpayment` | Approval of payment of given supplier invoice |
| PUT | `/3/supplierinvoices/{GivenNumber}/bookkeep` | Bookkeep given supplier invoice |
| PUT | `/3/supplierinvoices/{GivenNumber}/cancel` | Cancels given supplier invoice |
| PUT | `/3/supplierinvoices/{GivenNumber}/credit` | Credit given supplier invoice |

## Calling it

Records are wrapped under `SupplierInvoices`, so pagination works normally:

```python
for record in client.paginate("supplierinvoices", "SupplierInvoices"):
    ...
```

## Key fields

`AccountingMethod`, `AdministrationFee`, `AuthorizerName`, `Balance`, `Booked`, `Cancel`, `Cancelled`, `Comments`, `CostCenter`, `Credit`, `CreditReference`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `DisablePaymentFile`, `DueDate`, `ExternalInvoiceNumber`, `ExternalInvoiceSeries`, `FinalPayDate`, `Freight`, `GivenNumber`, `InvoiceDate`, `InvoiceNumber`, `OCR`, `OurReference`, `PaymentPending`, `Project`, `RoundOffValue`, `SalesType`, `SupplierInvoiceRows`, `SupplierName`, `SupplierNumber`, `Total`, `VAT`, `VATType`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `Vouchers`, `YourReference`

## Writable fields

`AdministrationFee`, `Comments`, `CostCenter`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `DisablePaymentFile`, `DueDate`, `ExternalInvoiceNumber`, `ExternalInvoiceSeries`, `Freight`, `GivenNumber`, `InvoiceDate`, `InvoiceNumber`, `OCR`, `OurReference`, `PaymentPending`, `Project`, `RoundOffValue`, `SalesType`, `SupplierInvoiceRows`, `SupplierNumber`, `Total`, `VAT`, `VATType`, `YourReference`

Required: `SupplierNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `costcenter` | string | Filter supplier invoices by cost center |
| `filter` | `cancelled`, `fullypaid`, `unpaid`, `unpaidoverdue`, `unbooked`, `pendingpayment`, `authorizepending` | Filter supplier invoices by status |
| `fromdate` | string | Filter supplier invoices by from date |
| `fromfinalpaydate` | string | Filter supplier invoices by final from pay date |
| `invoicenumber` | string | Filter supplier invoices by invoice number |
| `ocr` | string | Filter supplier invoices by ocr number |
| `ourreference` | string | Filter supplier invoices by our reference |
| `project` | string | Filter supplier invoices by project |
| `serialnumber` | string | Filter supplier invoices by serial number |
| `suppliername` | string | Filter supplier invoices by supplier name |
| `suppliernumber` | string | Filter supplier invoices by supplier number |
| `todate` | string | Filter supplier invoices by to date |
| `tofinalpaydate` | string | Filter supplier invoices by final to pay date |
| `yourreference` | string | Filter supplier invoices by your reference |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`.

## Safe use cases

- Read SupplierInvoices for investigation, reporting and export.

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
