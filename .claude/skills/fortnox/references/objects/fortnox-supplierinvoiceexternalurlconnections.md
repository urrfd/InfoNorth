# Fortnox Object: SupplierInvoiceExternalUrlConnections

API group `fortnox` · spec tag `fortnox_SupplierInvoiceExternalUrlConnections`

## Purpose

Retrieve a supplier invoice externalurl connection

## Endpoints

| Method | Path | Summary |
|---|---|---|
| POST | `/3/supplierinvoiceexternalurlconnections` | Create a supplier invoice external URL connection |
| GET | `/3/supplierinvoiceexternalurlconnections/{Id}` | Retrieve a single supplier invoice external URL connection |
| PUT | `/3/supplierinvoiceexternalurlconnections/{Id}` | Update a supplier invoice external URL connection |
| DELETE | `/3/supplierinvoiceexternalurlconnections/{Id}` | Remove a supplier invoice external URL connection |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("supplierinvoiceexternalurlconnections")
```

## Key fields

`ExternalURLConnection`, `Id`, `SupplierInvoiceNumber`, `Url`

## Writable fields

`ExternalURLConnection`, `SupplierInvoiceNumber`

Required: none declared in the spec

## Safe use cases

- Read SupplierInvoiceExternalUrlConnections for investigation, reporting and export.

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
