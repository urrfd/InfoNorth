# Fortnox Object: VoucherFileConnections

API group `fortnox` · spec tag `fortnox_VoucherFileConnections`

## Purpose

The voucher file connections register can return a list of records or a single record. By specifying a FileId in the URL, a single record will be returned. Not specifying a FileId will return a list of records.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/voucherfileconnections` | Retrieve a list of voucher file connections |
| POST | `/3/voucherfileconnections` | Create a voucher file connection |
| GET | `/3/voucherfileconnections/{FileId}` | Retrieve a single voucher file connection |
| DELETE | `/3/voucherfileconnections/{FileId}` | Remove a voucher file connection |

## Calling it

Records are wrapped under `VoucherFileConnections`, so pagination works normally:

```python
for record in client.paginate("voucherfileconnections", "VoucherFileConnections"):
    ...
```

## Key fields

`FileId`, `Name`, `VoucherDescription`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`

## Writable fields

`FileId`, `VoucherDescription`, `VoucherNumber`, `VoucherSeries`, `VoucherYear`

Required: `FileId`, `VoucherNumber`, `VoucherSeries`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `voucherdescription` | string | Voucherdescription of voucher file connections to list |
| `vouchernumber` | integer | Vouchernumber of voucher file connections to list |
| `voucherseries` | string | Voucherseries of voucher file connections to list |
| `voucheryear` | integer | Voucheryear of voucher file connections to list |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read VoucherFileConnections for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, POST` change live accounting data in the customer's company.
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
