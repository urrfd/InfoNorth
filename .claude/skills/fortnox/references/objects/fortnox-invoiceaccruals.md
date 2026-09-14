# Fortnox Object: InvoiceAccruals

API group `fortnox` · spec tag `fortnox_InvoiceAccruals`

## Purpose

The invoice accruals register can return a list of records or a single record. By specifying a InvoiceNumber in the URL, a single record will be returned. Not specifying a InvoiceNumber will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/invoiceaccruals` | Retrieve a list of invoice accruals |
| POST | `/3/invoiceaccruals` | Create an invoice accrual |
| GET | `/3/invoiceaccruals/{InvoiceNumber}` | Retrieve a single invoice accrual |
| PUT | `/3/invoiceaccruals/{InvoiceNumber}` | Update an invoice accrual |
| DELETE | `/3/invoiceaccruals/{InvoiceNumber}` | Remove an invoice accrual |

## Calling it

Records are wrapped under `InvoiceAccruals`, so pagination works normally:

```python
for record in client.paginate("invoiceaccruals", "InvoiceAccruals"):
    ...
```

## Key fields

`AccrualAccount`, `Description`, `EndDate`, `InvoiceAccrualRows`, `InvoiceNumber`, `Period`, `RevenueAccount`, `StartDate`, `Times`, `Total`, `VATIncluded`

## Writable fields

`AccrualAccount`, `Description`, `EndDate`, `InvoiceAccrualRows`, `InvoiceNumber`, `Period`, `RevenueAccount`, `StartDate`, `Times`, `Total`, `VATIncluded`

Required: `AccrualAccount`, `Description`, `EndDate`, `InvoiceAccrualRows`, `InvoiceNumber`, `RevenueAccount`, `StartDate`, `Total`

## Safe use cases

- Read InvoiceAccruals for investigation, reporting and export.

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
