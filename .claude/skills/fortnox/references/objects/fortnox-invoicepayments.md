# Fortnox Object: InvoicePayments

API group `fortnox` · spec tag `fortnox_InvoicePayments`

## Purpose

Get invoice payments

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/invoicepayments` | Retrieve a list of invoice payments |
| POST | `/3/invoicepayments` | Create an invoice payment |
| GET | `/3/invoicepayments/{Number}` | Retrieve a single invoice payment |
| PUT | `/3/invoicepayments/{Number}` | Update an invoice payment |
| DELETE | `/3/invoicepayments/{Number}` | Remove an invoice payment |
| PUT | `/3/invoicepayments/{Number}/bookkeep` | Bookkeep an invoice payment |

## Calling it

Records are wrapped under `InvoicePayments`, so pagination works normally:

```python
for record in client.paginate("invoicepayments", "InvoicePayments"):
    ...
```

## Key fields

`Amount`, `AmountCurrency`, `Booked`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `InvoiceCustomerName`, `InvoiceCustomerNumber`, `InvoiceDueDate`, `InvoiceNumber`, `InvoiceOCR`, `InvoiceTotal`, `ModeOfPayment`, `ModeOfPaymentAccount`, `Number`, `PaymentDate`, `Source`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `WriteOffExist`, `WriteOffs`

## Writable fields

`Amount`, `AmountCurrency`, `Booked`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `InvoiceCustomerName`, `InvoiceCustomerNumber`, `InvoiceDueDate`, `InvoiceNumber`, `InvoiceOCR`, `InvoiceTotal`, `ModeOfPayment`, `ModeOfPaymentAccount`, `Number`, `PaymentDate`, `Source`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `WriteOffs`

Required: `InvoiceNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `invoicenumber` | integer | filter by invoice number |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read InvoicePayments for investigation, reporting and export.

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
