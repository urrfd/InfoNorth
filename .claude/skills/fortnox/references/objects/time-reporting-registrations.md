# Fortnox Object: Registrations

API group `time-reporting` · spec tag `time-reporting_Registrations`

## Purpose

<p>
 <b>Response property descriptions:</b><br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>id</i></b> - The unique id of the registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>userId</i></b> - The user ID who owns the registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>userName</i></b> - The name of the user who owns the registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>workedDate</i></b> - The date for which the registration is created.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>workedHours</i></b> - The time spent, or the time of absence.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>startTime</i></b> - The start of clock time.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>stopTime</i></b> - The end of clock time.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>invoiceText</i></b> - The text to be included in the invoice/order basis which would be used to create an invoice/order.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>note</i></b> - The note on the registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>chargeHours</i></b> - The time to be invoiced, or 0 for the absence, or locked for non-invoiceable.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>childId</i></b> - The child ID related to the absence registration of parental leave (FPE), which comes from Payroll application.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>nonInvoiceable</i></b> - If the registration would be ignored for charging or not.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>invoiceBasisId</i></b> - The ID of invoice/order basis which is used for creating an invoice/order.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>documentId</i></b> - The document ID which includes the registration and is created in Invoicing application.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>documentType</i></b> - The document type which could be "invoice" or "order".<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>unitCost</i></b> - The unit cost from the registration owner who takes the work.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>unitPrice</i></b> - The unit price for the service on the registration, which comes in priority from "invoice/order basis", "price group" or "service".
 <p>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/time/registrations-v2` | Get time/absence registrations that match filter |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/time/registrations-v2")
```

**The list response is a bare JSON array, not a wrapped object.**
`client.paginate()` assumes the `/3/` wrapping and will not work here -
iterate the returned list directly and handle paging from the parameters below.

## Key fields

`chargeHours`, `childId`, `costCenter`, `createdBy`, `createdTime`, `customer`, `documentId`, `documentType`, `id`, `invoiceBasisId`, `invoiceText`, `nonInvoiceable`, `note`, `project`, `registrationCode`, `service`, `startTime`, `stopTime`, `unitCost`, `unitPrice`, `updatedBy`, `userId`, `userName`, `workedDate`, `workedHours`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `costCenterIds` | array | An array of cost center IDs.  Example: cc1,cc2,cc3 |
| `customerIds` | array | An array of customer IDs which are being used in database and in one-to-one relation with customer numbers.  Example: 100,101,102 |
| `fromDate` | string | The start date of the search span, the max of which should be 1 year to the end date ("toDate").  Example: 2022-11-01 |
| `inInvoiceBasis` | boolean | If the time/absence registration is locked on an invoice basis, or not. |
| `includeNonInvoiceableChargeHours` | boolean | If the price of the non-invoiceable time/absence registration is included, or not. |
| `includeRegistrationsWithoutProject` | boolean | If the time/absence registration without project is included, or not. |
| `internalTime` | boolean | If the time/absence registration is internal, which is registered on an internal customer, or not. |
| `invoiced` | boolean | If a document is created with the time/absence registration, or not. |
| `nonInvoiceable` | boolean | If the time/absence registration has been moved to non-invoiceable, or not. |
| `projectIds` | array | An array of project IDs.  Example: p1,p2,p3 |
| `regCodes` | array | An array of registration codes.  Example: TID,SEM,FPE |
| `serviceIds` | array | An array of service IDs.  Example: s1,s2,s3 |
| `toDate` | string | The end date of the search span, the max of which should be 1 year back to the start date ("fromDate").  Example: 2022-11-30 |
| `userIds` | array | An array of user IDs that time/absence registrations belong to.  Example: 1,2,3 |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read Registrations for investigation, reporting and export.

## Dangerous / live actions

- None: this resource is read-only.

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
