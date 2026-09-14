# Fortnox Object: SupplierInvoicePayments

API group `fortnox` · spec tag `fortnox_SupplierInvoicePayments`

## Purpose

Get supplier invoice payments

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/supplierinvoicepayments` | Retrieve a list of supplier invoice payments |
| POST | `/3/supplierinvoicepayments` | Create a supplier invoice payment |
| GET | `/3/supplierinvoicepayments/{Number}` | Retrieve a single supplier invoice payment |
| PUT | `/3/supplierinvoicepayments/{Number}` | Update a supplier invoice payment |
| DELETE | `/3/supplierinvoicepayments/{Number}` | Remove a supplier invoice payment |
| PUT | `/3/supplierinvoicepayments/{Number}/bookkeep` | Bookkeep a supplier invoice payment |

## Calling it

Records are wrapped under `SupplierInvoicePayments`, so pagination works normally:

```python
for record in client.paginate("supplierinvoicepayments", "SupplierInvoicePayments"):
    ...
```

## Key fields

`Amount`, `AmountCurrency`, `Booked`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `Information`, `InvoiceDueDate`, `InvoiceNumber`, `InvoiceOCR`, `InvoiceSupplierName`, `InvoiceSupplierNumber`, `InvoiceTotal`, `ModeOfPayment`, `Number`, `PaymentDate`, `Source`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `WriteOffExist`, `WriteOffs`

## Writable fields

`Amount`, `AmountCurrency`, `Booked`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `Information`, `InvoiceDueDate`, `InvoiceNumber`, `InvoiceOCR`, `InvoiceSupplierName`, `InvoiceSupplierNumber`, `InvoiceTotal`, `ModeOfPayment`, `Number`, `PaymentDate`, `Source`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `WriteOffs`

Required: `InvoiceNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `invoicenumber` | integer | Filter payments by invoice number |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`.

## Safe use cases

- Read SupplierInvoicePayments for investigation, reporting and export.

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
