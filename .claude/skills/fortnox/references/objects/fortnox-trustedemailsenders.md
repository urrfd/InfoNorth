# Fortnox Object: TrustedEmailSenders

API group `fortnox` · spec tag `fortnox_TrustedEmailSenders`

## Purpose

Get email senders

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/emailsenders` | Retrieve a list of all trusted and rejected senders |
| POST | `/3/emailsenders/trusted` | Add a new email address as trusted |
| DELETE | `/3/emailsenders/trusted/{Id}` | Delete an email address from the trusted senders list |

## Calling it

Records are wrapped under `EmailSenders`, so pagination works normally:

```python
for record in client.paginate("emailsenders", "EmailSenders"):
    ...
```

## Key fields

`RejectedSenders`, `TrustedSenders`

## Writable fields

`Email`, `Id`

Required: `Email`

## Safe use cases

- Read TrustedEmailSenders for investigation, reporting and export.

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
