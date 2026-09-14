# Fortnox Object: Offers

API group `fortnox` · spec tag `fortnox_Offers`

## Purpose

Get offers

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/offers` | Retrieve a list of offers |
| POST | `/3/offers` | Create an offer |
| GET | `/3/offers/{DocumentNumber}` | Retrieve a single offer |
| PUT | `/3/offers/{DocumentNumber}` | Update an offer |
| PUT | `/3/offers/{DocumentNumber}/cancel` | Cancels given offer |
| PUT | `/3/offers/{DocumentNumber}/createinvoice` | Create invoice out of given offer |
| PUT | `/3/offers/{DocumentNumber}/createorder` | Create order out of given offer |
| GET | `/3/offers/{DocumentNumber}/email` | Send given offer as email |
| PUT | `/3/offers/{DocumentNumber}/externalprint` | Set given offer as sent |
| GET | `/3/offers/{DocumentNumber}/preview` | Preview given offer |
| GET | `/3/offers/{DocumentNumber}/print` | Print given offer |

## Calling it

Records are wrapped under `Offers`, so pagination works normally:

```python
for record in client.paginate("offers", "Offers"):
    ...
```

## Key fields

`Address1`, `Address2`, `AdministrationFee`, `AdministrationFeeVAT`, `BasisTaxReduction`, `Cancelled`, `City`, `Comments`, `ContributionPercent`, `ContributionValue`, `CopyRemarks`, `CostCenter`, `Country`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `CustomerName`, `CustomerNumber`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryDate`, `DeliveryName`, `DeliveryZipCode`, `DocumentNumber`, `EmailInformation`, `ExpireDate`, `Freight`, `FreightVAT`, `Gross`, `HouseWork`, `InvoiceReference`, `Labels`, `Language`, `Net`, `NotCompleted`, `OfferDate`, `OfferRows`, `OrderReference`, `OrganisationNumber`, `OurReference`, `Phone1`, `Phone2`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `RoundOff`, `Sent`, `TaxReduction`, `TaxReductionType`, `TermsOfDelivery`, `TermsOfPayment`, `Total`, `TotalToPay`, `TotalVAT`, `VATIncluded`, `WayOfDelivery`, `YourReference`, `YourReferenceNumber`, `ZipCode`

## Writable fields

`Address1`, `Address2`, `AdministrationFee`, `City`, `Comments`, `CopyRemarks`, `CostCenter`, `Country`, `Currency`, `CurrencyRate`, `CurrencyUnit`, `CustomerName`, `CustomerNumber`, `DeliveryAddress1`, `DeliveryAddress2`, `DeliveryCity`, `DeliveryCountry`, `DeliveryDate`, `DeliveryName`, `DeliveryZipCode`, `DocumentNumber`, `EmailInformation`, `ExpireDate`, `Freight`, `Labels`, `Language`, `NotCompleted`, `OfferDate`, `OfferRows`, `OrganisationNumber`, `OurReference`, `Phone1`, `Phone2`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `TaxReductionType`, `TermsOfDelivery`, `TermsOfPayment`, `VATIncluded`, `WayOfDelivery`, `YourReference`, `YourReferenceNumber`, `ZipCode`

Required: `CustomerNumber`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `costcenter` | string | filter by cost center |
| `customername` | string | filter by customer name |
| `customernumber` | string | filter by customer number |
| `documentnumber` | string | filter by document number |
| `filter` | `cancelled`, `expired`, `completed`, `notcompleted`, `ordercreated`, `ordernotcreated` | possibility to filter offers |
| `fromdate` | string | filter by from date |
| `label` | string | filter by label |
| `notcompleted` | boolean | filter by not completed |
| `ourreference` | string | filter by our reference |
| `project` | string | filter by project |
| `sent` | boolean | filter by sent |
| `todate` | string | filter by to date |
| `yourreference` | string | filter by your reference |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read Offers for investigation, reporting and export.

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
