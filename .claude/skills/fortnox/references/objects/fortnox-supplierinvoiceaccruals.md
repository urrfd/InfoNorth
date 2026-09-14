# Fortnox Object: SupplierInvoiceAccruals

API group `fortnox` · spec tag `fortnox_SupplierInvoiceAccruals`

## Purpose

The supplier invoice accruals register can return a list of records or a single record. By specifying a SupplierInvoiceNumber in the URL, a single record will be returned. Not specifying a SupplierInvoiceNumber will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/supplierinvoiceaccruals` | Retrieve a list of supplier invoice accruals |
| POST | `/3/supplierinvoiceaccruals` | Create a supplier invoice accrual |
| GET | `/3/supplierinvoiceaccruals/{SupplierInvoiceNumber}` | Retrieve a single supplier invoice accrual |
| PUT | `/3/supplierinvoiceaccruals/{SupplierInvoiceNumber}` | Update a supplier invoice accrual |
| DELETE | `/3/supplierinvoiceaccruals/{SupplierInvoiceNumber}` | Remove a supplier invoice accrual |

## Calling it

Records are wrapped under `SupplierInvoiceAccruals`, so pagination works normally:

```python
for record in client.paginate("supplierinvoiceaccruals", "SupplierInvoiceAccruals"):
    ...
```

## Key fields

`AccrualAccount`, `CostAccount`, `Description`, `EndDate`, `Period`, `StartDate`, `SupplierInvoiceAccrualRows`, `SupplierInvoiceNumber`, `Times`, `Total`, `VATIncluded`

## Writable fields

`AccrualAccount`, `CostAccount`, `Description`, `EndDate`, `Period`, `StartDate`, `SupplierInvoiceAccrualRows`, `SupplierInvoiceNumber`, `Times`, `Total`, `VATIncluded`

Required: `AccrualAccount`, `CostAccount`, `EndDate`, `Period`, `StartDate`, `SupplierInvoiceAccrualRows`, `SupplierInvoiceNumber`, `Times`, `Total`

## Safe use cases

- Read SupplierInvoiceAccruals for investigation, reporting and export.

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
