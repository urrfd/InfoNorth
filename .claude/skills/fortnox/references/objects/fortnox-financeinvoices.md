# Fortnox Object: FinanceInvoices

API group `fortnox` · spec tag `fortnox_FinanceInvoices`

## Purpose

<p>
 Retrieves the status and balance of an invoice sent to Fortnox Finans.
 You need to supply the invoice number in Fortox to retrieve the invoice.
 <p>
 <b>Note that</b> invoices sent with the old &quot;Noxbox&quot; platform will not have the &quot;ServiceName&quot;
 property in the response. This new property is added to the response if the invoice is
 sent with the new finance service.
 <p>
 Response explanation for <b>Service</b> and <b>ServiceName</b>
 <p>
 <b>Service:</b>
 <ul>
     <li><b>LEDGERBASE</b>: if the invoice is sent by using the old &quot;Noxbox&quot; platform, or the new finance service with the subtypes &quot;Service Full&quot; or &quot;Service Light&quot;. These services are explained above in the &quot;Fortnox Finans services&quot; section</li>
     <li><b>REMINDER</b>: If the invoice is sent by the new finance service, with the service Reminder Service</li>
 </ul>
 <p>
 <b>ServiceName</b> (only provided for <u>new finance service</u> invoices):
 <ul>
     <li><b>SERVICE_FULL</b>: Ledgerbase service <u>with</u> automatic reminders is used</li>
     <li><b>SERVICE_LIGHT</b>: Ledgerbase service <u>without</u> automatic reminders is used.</li>
     <li><b>REMINDER_SERVICE</b>: Reminder service is used</li>
 </ul>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| POST | `/3/noxfinansinvoices` | Send an invoice with Fortnox Finans |
| GET | `/3/noxfinansinvoices/{InvoiceNumber}` | Retrieve a single invoice payment |
| PUT | `/3/noxfinansinvoices/{InvoiceNumber}/pause` | Action Pause |
| PUT | `/3/noxfinansinvoices/{InvoiceNumber}/report-payment` | Action Report Payment |
| PUT | `/3/noxfinansinvoices/{InvoiceNumber}/stop` | Action Stop |
| PUT | `/3/noxfinansinvoices/{InvoiceNumber}/take-fees` | Action Take Fees |
| PUT | `/3/noxfinansinvoices/{InvoiceNumber}/unpause` | Action Unpause |

## Calling it

No collection endpoint: every operation addresses a single record.

```python
result = client.get("noxfinansinvoices")
```

## Key fields

`BalanceIncludeFees`, `BalanceIncludeFeesCurrency`, `CurrentCapitalBalance`, `CurrentCapitalBalanceCurrency`, `InvoiceDocumentURL`, `InvoiceNumber`, `NextEvent`, `NextEventDate`, `OCRNumber`, `Service`, `ServiceName`, `Status`

## Writable fields

`BalanceIncludeFees`, `BalanceIncludeFeesCurrency`, `CurrentCapitalBalance`, `CurrentCapitalBalanceCurrency`, `InvoiceDocumentURL`, `InvoiceNumber`, `NextEvent`, `NextEventDate`, `OCRNumber`, `SendMethod`, `Service`, `ServiceName`, `Status`

Required: `InvoiceNumber`, `SendMethod`, `Service`

## Safe use cases

- Read FinanceInvoices for investigation, reporting and export.

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
