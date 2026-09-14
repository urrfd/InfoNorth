# Fortnox Object: Contracts

API group `fortnox` · spec tag `fortnox_Contracts`

## Purpose

Get contracts

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/contracts` | Retrieve a list of contracts |
| POST | `/3/contracts` | Create a contract |
| GET | `/3/contracts/{DocumentNumber}` | Retrieve a single contract |
| PUT | `/3/contracts/{DocumentNumber}` | Update a contract |
| PUT | `/3/contracts/{DocumentNumber}/createinvoice` | Create invoice from contract |
| PUT | `/3/contracts/{DocumentNumber}/finish` | Set a contract as finished |
| PUT | `/3/contracts/{DocumentNumber}/increaseinvoicecount` | Increases the invoice count without creating an invoice |

## Calling it

Records are wrapped under `Contracts`, so pagination works normally:

```python
for record in client.paginate("contracts", "Contracts"):
    ...
```

## Key fields

`Active`, `AdministrationFee`, `BasisTaxReduction`, `Comments`, `Continuous`, `ContractDate`, `ContractLength`, `ContributionPercent`, `ContributionValue`, `CostCenter`, `Currency`, `CustomerName`, `CustomerNumber`, `DocumentNumber`, `EmailInformation`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `Freight`, `Gross`, `HouseWork`, `InvoiceDiscount`, `InvoiceInterval`, `InvoiceRows`, `Invoiceinterval`, `InvoicesRemaining`, `Language`, `LastInvoiceDate`, `Net`, `OurReference`, `PeriodEnd`, `PeriodStart`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `RoundOff`, `Status`, `TaxReduction`, `TaxReductionType`, `TemplateName`, `TemplateNumber`, `TermsOfDelivery`, `TermsOfPayment`, `Total`, `TotalToPay`, `TotalVAT`, `VATIncluded`, `WayOfDelivery`, `YourOrderNumber`, `YourReference`

## Writable fields

`Active`, `AdministrationFee`, `Comments`, `Continuous`, `ContractDate`, `ContractLength`, `CostCenter`, `Currency`, `CustomerNumber`, `DocumentNumber`, `EmailInformation`, `ExternalInvoiceReference1`, `ExternalInvoiceReference2`, `Freight`, `HouseWork`, `InvoiceDiscount`, `InvoiceInterval`, `InvoiceRows`, `Language`, `OurReference`, `PeriodEnd`, `PeriodStart`, `PriceList`, `PrintTemplate`, `Project`, `Remarks`, `TaxReductionType`, `TemplateNumber`, `TermsOfDelivery`, `TermsOfPayment`, `VATIncluded`, `WayOfDelivery`, `YourOrderNumber`, `YourReference`

Required: `CustomerNumber`, `InvoiceRows`, `PeriodEnd`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `customernumber` | string | Filter contracts by customer number |
| `documentnumber` | integer | Filter contracts by document number |
| `filter` | `active`, `inactive`, `finished` | Filter contracts by status |
| `invoicesremaining` | integer | Filter contracts by number of remaining invoices |
| `periodend` | string | Filter contracts by end of contract period |
| `periodstart` | string | Filter contracts by start of contract period |
| `templatenumber` | integer | Filter contracts by template number |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`.

## Safe use cases

- Read Contracts for investigation, reporting and export.

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
