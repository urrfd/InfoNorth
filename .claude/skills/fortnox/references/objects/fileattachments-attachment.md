# Fortnox Object: Attachment

API group `fileattachments` · spec tag `fileattachments_Attachment`

## Purpose

Get attached files on an entity

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/api/fileattachments/attachments-v1` | Get attached files on an entity |
| POST | `/api/fileattachments/attachments-v1` | Attach files to one or more entities |
| GET | `/api/fileattachments/attachments-v1/numberofattachments` | List number of attachments |
| POST | `/api/fileattachments/attachments-v1/validateincludedonsend` | Validates a list of attachments that will be included on send |
| PUT | `/api/fileattachments/attachments-v1/{attachmentId}` | Update attachment |
| DELETE | `/api/fileattachments/attachments-v1/{attachmentId}` | Detach file |

## Calling it

This resource lives outside the classic `/3/` API, which the client's base
URL points at. Pass the absolute URL:

```python
result = client.get("https://api.fortnox.se/api/fileattachments/attachments-v1")
```

## Writable fields

`entityId`, `entityType`, `fileId`, `id`, `includeOnSend`

Required: none declared in the spec

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `entityid` | array | ids of the entities whose attachments should be fetched |
| `entityids` | array | ids of the entities to look for number of attachments on |
| `entitytype` | `OF`, `O`, `F`, `C`, `LGR_IO`, `LGR_IG` | type of the entities whose attachments should be fetched |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read Attachment for investigation, reporting and export.

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
