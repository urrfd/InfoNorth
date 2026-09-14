# Fortnox Object: Accounts

API group `fortnox` · spec tag `fortnox_Accounts`

## Purpose

The accounts are returned sorted by account number with the lowest number appearing first.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/accounts` | List all accounts |
| POST | `/3/accounts` | Create an account |
| GET | `/3/accounts/{Number}` | Retrieve an account |
| PUT | `/3/accounts/{Number}` | Update an account |
| DELETE | `/3/accounts/{Number}` | Deletes an account |

## Calling it

Records are wrapped under `Accounts`, so pagination works normally:

```python
for record in client.paginate("accounts", "Accounts"):
    ...
```

## Key fields

`Active`, `BalanceBroughtForward`, `BalanceCarriedForward`, `CostCenter`, `CostCenterSettings`, `Description`, `Number`, `OpeningQuantities`, `Project`, `ProjectSettings`, `QuantitySettings`, `QuantityUnit`, `SRU`, `TransactionInformation`, `TransactionInformationSettings`, `VATCode`, `Year`

## Writable fields

`Active`, `BalanceBroughtForward`, `CostCenter`, `CostCenterSettings`, `Description`, `Number`, `OpeningQuantities`, `Project`, `ProjectSettings`, `SRU`, `TransactionInformation`, `TransactionInformationSettings`, `VATCode`

Required: `Description`, `Number`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `sru` | integer | Sru of accounts to list |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

Global parameters accepted: `lastmodified`, `sortby`.

## Safe use cases

- Read Accounts for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, POST, PUT` change live accounting data in the customer's company.
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
