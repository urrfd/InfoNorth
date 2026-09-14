# Fortnox Object: Articles

API group `time-reporting` · spec tag `time-reporting_Articles`

## Purpose

<p>
 <b>Response property descriptions:</b><br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>id</i></b> - The unique id of a basic common combination of article registrations. (The basic common combination means "user/purchase date/customer/project/cost center", which leads to a dialog with several article registrations.)<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>purchaseDate</i></b> - The date on which the article is purchased or registered for charging.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>ownerId</i></b> - The user ID who creates the basic common combination.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>ownerName</i></b> - The name of the user who creates the basic common combination.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>version</i></b> - The version of the basic common combination (article dialog) being updated, which is used for handling the concurrency issue.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b><i>registrationType</i></b> - It is always "ARTICLE" for article list endpoint.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;    <b>Sub-Class - ArticleRegistration:</b><br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>id</i></b> - The unique id of an article registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>registrationId</i></b> - The id of the basic common combination.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>orderIndex</i></b> - the order index for the article registration in regard of the common combination.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>ownerId</i></b> - The user ID who owns the article registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>ownerName</i></b> - The name of the user who owns the article registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>totalQuantity</i></b> - The quantity of the article.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>unitPrice</i></b> - The unit price connected to the article registration, which might be locked on an invoice/order basis or for non-invoiceable.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>unitCost</i></b> - The unit cost connected to the article registration, which might be locked on an invoice/order basis.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>invoiceBasisId</i></b> - The ID of invoice/order basis which is used for creating an invoice/order.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>nonInvoiceable</i></b> - If the article registration would be ignored for charging or not.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>note</i></b> - The note on the article registration.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>documentId</i></b> - The document ID which includes the article registration and is created in Invoicing application.<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        <b><i>documentType</i></b> - The document type which could be "invoice" or "order".
 </p>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/time/articles-v1` | Get full article registrations that match filter |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/time/articles-v1")
```

**The list response is a bare JSON array, not a wrapped object.**
`client.paginate()` assumes the `/3/` wrapping and will not work here -
iterate the returned list directly and handle paging from the parameters below.

## Key fields

`articleRegistrations`, `costCenter`, `createdTime`, `customer`, `id`, `ownerId`, `ownerName`, `project`, `purchaseDate`, `registeredArticle`, `registrationType`, `version`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `costCenterIds` | array | An array of cost center IDs.  Example: cc1,cc2,cc3 |
| `customerIds` | array | An array of customer IDs which are being used in database and in one-to-one relation with customer numbers.  Example: 100,101,102 |
| `fromDate` | string | The start date of the search span, the max of which should be 1 year to the end date ("toDate").  Example: 2022-11-01 |
| `inInvoiceBasis` | boolean | If the article registration is locked on an invoice basis, or not. |
| `includeNonInvoiceablePrice` | boolean | If the price of the non-invoiceable article registration is included, or not. |
| `includeRegistrationsWithoutProject` | boolean | If the article registration without project is included, or not. |
| `internalArticles` | boolean | If the article registration is internal, which is registered on an internal customer, or not. |
| `invoiced` | boolean | If a document is created with the article registration, or not. |
| `itemIds` | array | An array of article IDs.  Example: s1,s2,s3 |
| `nonInvoiceable` | boolean | If the article registration has been moved to non-invoiceable, or not. |
| `ownerIds` | array | An array of user ids who own the article registrations.  Example: 1,2,3 |
| `projectIds` | array | An array of project IDs.  Example: p1,p2,p3 |
| `toDate` | string | The end date of the search span, the max of which should be 1 year back to the start date ("fromDate").  Example: 2022-11-30 |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read Articles for investigation, reporting and export.

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
