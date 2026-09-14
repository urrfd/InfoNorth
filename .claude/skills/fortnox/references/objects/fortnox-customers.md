# Fortnox Object: Customers

API group `fortnox` · spec tag `fortnox_Customers`

## Purpose

The customers are returned sorted by customer number with the lowest number appearing first.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/customers` | Retrieve a list of customers |
| POST | `/3/customers` | Create a customer |
| GET | `/3/customers/{CustomerNumber}` | Retrieve a customer |
| PUT | `/3/customers/{CustomerNumber}` | Update a customer |
| DELETE | `/3/customers/{CustomerNumber}` | Delete a customer |

## Calling it

Records are wrapped under `Customers`, so pagination works normally:

```python
for record in client.paginate("customers", "Customers"):
    ...
```

## Key fields

`Active`, `Address1`, `Address2`, `City`, `Comments`, `CostCenter`, `Country`, `CountryCode`, `Currency`, `CustomerNumber`, `DefaultDeliveryTypes`, `DefaultTemplates`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryCountryCode`, `DeliveryFax`, `DeliveryName`, `DeliveryPhone1`, `DeliveryPhone2`, `DeliveryZipCode`, `Email`, `EmailInvoice`, `EmailInvoiceBCC`, `EmailInvoiceCC`, `EmailOffer`, `EmailOfferBCC`, `EmailOfferCC`, `EmailOrder`, `EmailOrderBCC`, `EmailOrderCC`, `ExternalReference`, `Fax`, `GLN`, `GLNDelivery`, `InvoiceAdministrationFee`, `InvoiceDiscount`, `InvoiceFreight`, `InvoiceRemark`, `Name`, `OrganisationNumber`, `OurReference`, `Phone`, `Phone1`, `Phone2`, `PriceList`, `Project`, `SalesAccount`, `ShowPriceVATIncluded`, `TermsOfDelivery`, `TermsOfPayment`, `Type`, `VATNumber`, `VATType`, `VisitingAddress`, `VisitingCity`, `VisitingCountry`, `VisitingCountryCode`, `VisitingZipCode`, `WWW`, `WayOfDelivery`, `YourReference`, `ZipCode`

## Writable fields

`Active`, `Address1`, `Address2`, `City`, `Comments`, `CostCenter`, `Country`, `CountryCode`, `Currency`, `CustomerNumber`, `DefaultDeliveryTypes`, `DefaultTemplates`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryCountryCode`, `DeliveryFax`, `DeliveryName`, `DeliveryPhone1`, `DeliveryPhone2`, `DeliveryZipCode`, `Email`, `EmailInvoice`, `EmailInvoiceBCC`, `EmailInvoiceCC`, `EmailOffer`, `EmailOfferBCC`, `EmailOfferCC`, `EmailOrder`, `EmailOrderBCC`, `EmailOrderCC`, `ExternalReference`, `Fax`, `GLN`, `GLNDelivery`, `InvoiceAdministrationFee`, `InvoiceDiscount`, `InvoiceFreight`, `InvoiceRemark`, `Name`, `OrganisationNumber`, `OurReference`, `Phone1`, `Phone2`, `PriceList`, `Project`, `SalesAccount`, `ShowPriceVATIncluded`, `TermsOfDelivery`, `TermsOfPayment`, `Type`, `VATNumber`, `VATType`, `VisitingAddress`, `VisitingCity`, `VisitingCountry`, `VisitingCountryCode`, `VisitingZipCode`, `WWW`, `WayOfDelivery`, `YourReference`, `ZipCode`

Required: `Name`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `city` | string | filter by city |
| `customernumber` | string | filter by customer number |
| `email` | string | filter by email |
| `filter` | `active`, `inactive` | possibility to filter customers |
| `gln` | string | filter by gln |
| `glndelivery` | string | filter by gln delivery |
| `name` | string | filter by name |
| `organisationnumber` | string | filter by organisation number |
| `phone` | string | filter by phone |
| `zipcode` | string | filter by zip code |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read Customers for investigation, reporting and export.

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
