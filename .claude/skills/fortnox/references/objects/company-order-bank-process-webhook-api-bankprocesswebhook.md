# Fortnox Object: BankProcessWebhook

API group `Company-Order-Bank-Process-Webhook-API` · spec tag `Company-Order-Bank-Process-Webhook-API_BankProcessWebhook`

## Purpose

List previously created webhooks

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/bank-process-webhooks/v1` | List webhooks |
| POST | `/api/bank-process-webhooks/v1` | Creates a webhook |
| GET | `/api/bank-process-webhooks/v1/{webhook_id}` | Returns a webhook |
| PATCH | `/api/bank-process-webhooks/v1/{webhook_id}` | Updates a webhook |
| DELETE | `/api/bank-process-webhooks/v1/{webhook_id}` | Deletes a webhook |
| POST | `/api/bank-process-webhooks/v1/{webhook_id}/evaluate` | Evaluates a webhook |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/bank-process-webhooks/v1")
```

## Key fields

`id`, `url`

## Safe use cases

- Read BankProcessWebhook for investigation, reporting and export.

## Dangerous / live actions

- `DELETE, PATCH, POST` change live accounting data in the customer's company.
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
