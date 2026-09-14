# Fortnox Object: PurchaseOrder

API group `warehouse` · spec tag `warehouse_PurchaseOrder`

## Purpose

<p>
 List purchase orders matching the given parameters.
 </p>
 <p>
 Sortable fields:
 <code>id</code>,
 <code>supplier_number</code>,
 <code>order_date</code>,
 <code>internal_reference</code>,
 <code>response_state</code>,
 <code>delivery_date</code>
 </p>

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/warehouse/purchaseorders-v1` | List Purchase Orders |
| POST | `/api/warehouse/purchaseorders-v1` | Create Purchase Order |
| GET | `/api/warehouse/purchaseorders-v1/csv` | Get CSV list of Purchase Orders |
| PUT | `/api/warehouse/purchaseorders-v1/response` | Update response states |
| POST | `/api/warehouse/purchaseorders-v1/sendpurchaseorders` | Sends multiple purchase orders via email |
| GET | `/api/warehouse/purchaseorders-v1/{id}` | Get Purchase Order |
| PUT | `/api/warehouse/purchaseorders-v1/{id}` | Update Purchase Order |
| PUT | `/api/warehouse/purchaseorders-v1/{id}/complete` | Manually complete Purchase Order |
| PUT | `/api/warehouse/purchaseorders-v1/{id}/dropshipcomplete` | Manually complete dropship order |
| GET | `/api/warehouse/purchaseorders-v1/{id}/matches` | List matched documents |
| GET | `/api/warehouse/purchaseorders-v1/{id}/notes` | Get notes |
| PATCH | `/api/warehouse/purchaseorders-v1/{id}/partial` | Partial update Purchase Order |
| PUT | `/api/warehouse/purchaseorders-v1/{id}/response` | Update response state |
| POST | `/api/warehouse/purchaseorders-v1/{id}/send` | Send purchase order via email |
| PUT | `/api/warehouse/purchaseorders-v1/{id}/void` | Void Purchase Order |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/warehouse/purchaseorders-v1")
```

## Key fields

`id`, `type`

## Writable fields

`id`, `type`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `ignoreIncomingGoodsId` | integer | used for calculating the remaining ordered quantity. null will take the received quantity from all incoming goods |
| `internalReference` | string | Include only documents where `internalReference' contains the given text (case-insensitive). |
| `itemId` | string | Include only documents with the given `itemId`. |
| `note` | string | Include only documents where `note`-field contains the given text (case-insensitive). |
| `purchaseType` | `WAREHOUSE`, `DROPSHIP` | Include only documents with the given `purchaseType` |
| `q` | string | Include only documents where `id` or `internalReference`-field contains the given text (case-insensitive). |
| `showPurchaseTypeColumn` | boolean | True to include the purchase type column, default is false. |
| `state` | `NOT_SENT`, `SENT`, `SENT_NOT_REJECTED`, `DELAYED`, `RECEIVED`, `VOIDED`, `CURRENT`, `ALL` | Include only documents with the given `purchaseOrderState`. |
| `supplierNumber` | string | Include only documents with the given `supplierNumber`. |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read PurchaseOrder for investigation, reporting and export.

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
