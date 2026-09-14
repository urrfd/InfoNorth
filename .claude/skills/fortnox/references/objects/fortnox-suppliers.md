# Fortnox Object: Suppliers

API group `fortnox` · spec tag `fortnox_Suppliers`

## Purpose

The supplier register can return a list of records or a single record. By specifying a SupplierNumber in the URL, a single record will be returned. Not specifying a SupplierNumber will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/suppliers` | Retrieve a list of suppliers |
| POST | `/3/suppliers` | Create a supplier |
| GET | `/3/suppliers/{SupplierNumber}` | Retrieve a single supplier |
| PUT | `/3/suppliers/{SupplierNumber}` | Update a supplier |

## Calling it

Records are wrapped under `Suppliers`, so pagination works normally:

```python
for record in client.paginate("suppliers", "Suppliers"):
    ...
```

## Key fields

`Active`, `Address1`, `Address2`, `BG`, `BIC`, `Bank`, `BankAccountNumber`, `BranchCode`, `City`, `ClearingNumber`, `Comments`, `CostCenter`, `Country`, `CountryCode`, `Currency`, `DisablePaymentFile`, `Email`, `Fax`, `IBAN`, `Name`, `OrganisationNumber`, `OurCustomerNumber`, `OurReference`, `PG`, `Phone`, `Phone1`, `Phone2`, `PreDefinedAccount`, `Project`, `SupplierNumber`, `TermsOfPayment`, `VATNumber`, `VATType`, `VisitingAddress`, `VisitingCity`, `VisitingCountry`, `VisitingCountryCode`, `VisitingZipCode`, `WWW`, `WorkPlace`, `YourReference`, `ZipCode`

## Writable fields

`Active`, `Address1`, `Address2`, `BG`, `BIC`, `Bank`, `BankAccountNumber`, `BranchCode`, `City`, `ClearingNumber`, `Comments`, `CostCenter`, `Country`, `CountryCode`, `Currency`, `DisablePaymentFile`, `Email`, `Fax`, `IBAN`, `Name`, `OrganisationNumber`, `OurCustomerNumber`, `OurReference`, `PG`, `Phone1`, `Phone2`, `PreDefinedAccount`, `Project`, `SupplierNumber`, `TermsOfPayment`, `VATNumber`, `VATType`, `VisitingAddress`, `VisitingCity`, `VisitingCountry`, `VisitingCountryCode`, `VisitingZipCode`, `WWW`, `WorkPlace`, `YourReference`, `ZipCode`

Required: `Name`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `city` | string | filter on city |
| `email` | string | filter on email |
| `name` | string | filter on name |
| `organisationnumber` | string | filter on organisation number |
| `phone` | string | filter on phone |
| `suppliernumber` | string | filter on supplier number |
| `zipcode` | string | filter on zip code |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`.

## Safe use cases

- Read Suppliers for investigation, reporting and export.

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
