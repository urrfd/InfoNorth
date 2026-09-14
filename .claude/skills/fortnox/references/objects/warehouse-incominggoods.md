# Fortnox Object: IncomingGoods

API group `warehouse` · spec tag `warehouse_IncomingGoods`

## Purpose

<p>
     List incoming goods documents matching the given parameters.
 </p>
 <p>
     Sortable fields:
     <code>id</code>,
     <code>has_delivery_note</code>,
     <code>delivery_note_id</code>,
     <code>supplier_number</code>,
     <code>date</code>
 </p>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/incominggoods-v1` | List Incoming Goods Documents |
| POST | `/api/warehouse/incominggoods-v1` | Create Incoming Goods document |
| GET | `/api/warehouse/incominggoods-v1/{id}` | Get Incoming Goods document |
| PUT | `/api/warehouse/incominggoods-v1/{id}` | Update Incoming Goods document |
| PATCH | `/api/warehouse/incominggoods-v1/{id}` | Partial update Incoming Goods document |
| PUT | `/api/warehouse/incominggoods-v1/{id}/completed` | Complete Incoming Goods document |
| PUT | `/api/warehouse/incominggoods-v1/{id}/release` | Release Incoming Goods document |
| PUT | `/api/warehouse/incominggoods-v1/{id}/void` | Void Incoming Goods document |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/incominggoods-v1")
```

**The list response is a bare JSON array, not a wrapped object.**
`client.paginate()` assumes the `/3/` wrapping and will not work here -
iterate the returned list directly and handle paging from the parameters below.

## Key fields

`completed`, `date`, `deliveryNoteId`, `hasDeliveryNote`, `id`, `note`, `released`, `stockPointId`, `supplierName`, `supplierNumber`, `unmatchedValue`, `voided`

## Writable fields

`backOrderQuantity`, `batch`, `costCenterCode`, `directCost`, `id`, `invoicedQuantity`, `isStockItem`, `itemDescription`, `itemId`, `itemUnit`, `orderedQuantity`, `projectId`, `purchaseOrderId`, `purchaseOrderRowId`, `receivedQuantity`, `remainingOrderedQuantity`, `rowOrder`, `stockLocationCode`, `stockLocationId`, `stockLocationName`, `stockPointCode`, `stockPointId`, `stockPointName`, `takenQuantity`

Required: `backOrderQuantity`, `invoicedQuantity`, `itemId`, `orderedQuantity`, `receivedQuantity`, `takenQuantity`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `completed` | boolean | `true` to include only completed documents.  `false` to include only non-completed documents. |
| `deliveryNote` | string | Include only documents where `deliveryNote`-field contains the given text (case-insensitive). |
| `ignoreSupplierInvoiceId` | integer | This Supplier Invoice id will be excluded when calculating the takenQuantity. |
| `itemId` | string | Include only documents with the given `itemId`. |
| `note` | string | Include only documents where `note`-field contains the given text (case-insensitive). |
| `q` | string | Include only documents where `id` or `deliveryNote`-field contains the given text (case-insensitive). |
| `released` | boolean | `true` to include only released documents.  `false` to include only non-released documents. |
| `supplierNumber` | string | Include only documents with the given `supplierNumber`. |
| `voided` | boolean | `true` to include only voided documents.  `false` to include only non-voided documents. |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read IncomingGoods for investigation, reporting and export.

## Dangerous / live actions

- `PATCH, POST, PUT` change live accounting data in the customer's company.
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
