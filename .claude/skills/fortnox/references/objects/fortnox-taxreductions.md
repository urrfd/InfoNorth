# Fortnox Object: TaxReductions

API group `fortnox` · spec tag `fortnox_TaxReductions`

## Purpose

Get tax reductions

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/taxreductions` | Retrieve a list of tax reductions |
| POST | `/3/taxreductions` | Create a Tax Reduction |
| GET | `/3/taxreductions/{Id}` | Retrieve a single tax reduction |
| PUT | `/3/taxreductions/{Id}` | Update a tax reduction |
| DELETE | `/3/taxreductions/{Id}` | Remove a tax reduction |

## Calling it

Records are wrapped under `TaxReductions`, so pagination works normally:

```python
for record in client.paginate("taxreductions", "TaxReductions"):
    ...
```

## Key fields

`ApprovedAmount`, `AskedAmount`, `BilledAmount`, `CustomerName`, `Id`, `PropertyDesignation`, `ReferenceDocumentType`, `ReferenceNumber`, `RequestSent`, `ResidenceAssociationOrganisationNumber`, `SocialSecurityNumber`, `TaxReductionAmounts`, `TypeOfReduction`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`, `WorkType`

## Writable fields

`ApprovedAmount`, `AskedAmount`, `BilledAmount`, `CustomerName`, `Id`, `PropertyDesignation`, `ReferenceDocumentType`, `ReferenceNumber`, `RequestSent`, `ResidenceAssociationOrganisationNumber`, `SocialSecurityNumber`, `TaxReductionAmounts`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`

Required: `AskedAmount`, `CustomerName`, `ReferenceDocumentType`, `ReferenceNumber`, `SocialSecurityNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `filter` | `invoices`, `orders`, `offers` | possibility to filter tax reductions |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read TaxReductions for investigation, reporting and export.

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
