# Fortnox Object: ContractTemplates

API group `fortnox` · spec tag `fortnox_ContractTemplates`

## Purpose

The contract template resource can return a list of records or a single record. By specifying a TemplateNumber in the URL, a single record will be returned. Not specifying a TemplateNumber will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/contracttemplates` | Retrieve a list of contract templates |
| POST | `/3/contracttemplates` | Create a contract template |
| GET | `/3/contracttemplates/{TemplateNumber}` | Retrieve a single contract template |
| PUT | `/3/contracttemplates/{TemplateNumber}` | Update a contract template |

## Calling it

Records are wrapped under `ContractTemplates`, so pagination works normally:

```python
for record in client.paginate("contracttemplates", "ContractTemplates"):
    ...
```

## Key fields

`AdministrationFee`, `Continuous`, `ContractLength`, `ContractTemplate`, `ContractTemplateName`, `Freight`, `InvoiceInterval`, `InvoiceRows`, `OurReference`, `PrintTemplate`, `Remarks`, `TemplateName`, `TemplateNumber`, `TermsOfDelivery`, `TermsOfPayment`, `WayOfDelivery`

## Writable fields

`AdministrationFee`, `Continuous`, `ContractLength`, `Freight`, `InvoiceInterval`, `InvoiceRows`, `OurReference`, `PrintTemplate`, `Remarks`, `TemplateName`, `TemplateNumber`, `TermsOfDelivery`, `TermsOfPayment`, `WayOfDelivery`

Required: `TemplateName`

## Safe use cases

- Read ContractTemplates for investigation, reporting and export.

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
