# Fortnox Object: Projects

API group `fortnox` · spec tag `fortnox_Projects`

## Purpose

The project register can return a list of records or a single record. By specifying a ProjectNumber in the URL, a single record will be returned. If no ProjectNumber is provided, a list of records will be returned.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/projects` | Retrieve a list of projects |
| POST | `/3/projects` | Create a project |
| GET | `/3/projects/{ProjectNumber}` | Retrieve a single project |
| PUT | `/3/projects/{ProjectNumber}` | Update a project |
| DELETE | `/3/projects/{ProjectNumber}` | Remove a project |

## Calling it

Records are wrapped under `Projects`, so pagination works normally:

```python
for record in client.paginate("projects", "Projects"):
    ...
```

## Key fields

`Comments`, `ContactPerson`, `Description`, `EndDate`, `ProjectLeader`, `ProjectNumber`, `StartDate`, `Status`

## Writable fields

`Comments`, `ContactPerson`, `Description`, `EndDate`, `ProjectLeader`, `ProjectNumber`, `StartDate`, `Status`

Required: `Description`

## Resource filters

| Parameter | Values | Notes |
|---|---|---|
| `description` | string | filter on description |
| `projectleader` | string | filter on project leader |

Only **one** resource-specific filter may be used per request, though it can be
combined with a global parameter such as `lastmodified`.

## Safe use cases

- Read Projects for investigation, reporting and export.

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
