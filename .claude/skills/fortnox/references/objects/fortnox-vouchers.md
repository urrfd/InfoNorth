# Fortnox Object: Vouchers

API group `fortnox` · spec tag `fortnox_Vouchers`

## Purpose

Note that vouchers have two keys, one for voucher series and one for voucher number. The financial year is also specified for each voucher, this is due to the same voucher series and number is used each year.
 To get a unique voucher you need the voucher series, the voucher number and the financial year. These properties will always be returned where ever vouchers is used.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/vouchers` | Retrieve all vouchers |
| POST | `/3/vouchers` | Create a voucher |
| GET | `/3/vouchers/sublist` | Retrieve all vouchers for the current financial year |
| GET | `/3/vouchers/sublist/{VoucherSeries}` | Retrieve a list of vouchers for a specific series |
| GET | `/3/vouchers/{VoucherSeries}/{VoucherNumber}` | Retrieve a specific voucher |

## Calling it

Records are wrapped under `Vouchers`, so pagination works normally:

```python
for record in client.paginate("vouchers", "Vouchers"):
    ...
```

## Key fields

`ApprovalState`, `Comments`, `CostCenter`, `Description`, `Project`, `ReferenceNumber`, `ReferenceType`, `TransactionDate`, `VoucherNumber`, `VoucherRows`, `VoucherSeries`, `Year`

## Writable fields

`ApprovalState`, `Comments`, `CostCenter`, `Description`, `Project`, `ReferenceNumber`, `ReferenceType`, `TransactionDate`, `VoucherNumber`, `VoucherRows`, `VoucherSeries`, `Year`

Required: `Description`, `TransactionDate`, `VoucherSeries`, `Year`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `costcenter` | string | filter on cost center |
| `fromdate` | string | filter on from date |
| `todate` | string | filter on to date |
| `voucherseries` | string | filter on voucher series |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `financialyear`, `lastmodified`.

## Safe use cases

- Read Vouchers for investigation, reporting and export.

## Dangerous / live actions

- `POST` change live accounting data in the customer's company.
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
