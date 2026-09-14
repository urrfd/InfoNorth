# Fortnox Object: SupplierInvoiceFileConnections

API group `fortnox` · spec tag `fortnox_SupplierInvoiceFileConnections`

## Purpose

The supplier invoice file connections register can return a list of records or a single record. By specifying a FileId in the URL, a single record will be returned. Not specifying a FileId will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/supplierinvoicefileconnections` | Retrieve a list of supplier invoice file connections |
| POST | `/3/supplierinvoicefileconnections` | Create an supplier invoice file connection |
| GET | `/3/supplierinvoicefileconnections/{FileId}` | Retrieve a single supplier invoice file connection |
| DELETE | `/3/supplierinvoicefileconnections/{FileId}` | Remove an supplier invoice file connection |

## Calling it

Records are wrapped under `SupplierInvoiceFileConnections`, so pagination works normally:

```python
for record in client.paginate("supplierinvoicefileconnections", "SupplierInvoiceFileConnections"):
    ...
```

## Key fields

`FileId`, `Name`, `SupplierInvoiceNumber`, `SupplierName`

## Writable fields

`FileId`, `Name`, `SupplierInvoiceNumber`, `SupplierName`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `supplierinvoicenumber` | integer | Filter file connections by supplier invoice number |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read SupplierInvoiceFileConnections for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, POST` change live accounting data in the customer's company.
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
