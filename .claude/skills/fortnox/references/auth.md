# Fortnox authentication reference

Endpoints, request shapes and failure modes. Read this when changing `oauth.py`,
`tokens.py`, or the token-handling parts of `client.py`.

## Contents

- [Endpoints](#endpoints)
- [Token lifetimes](#token-lifetimes)
- [Authorization code flow](#authorization-code-flow)
- [Refresh](#refresh)
- [Client credentials](#client-credentials)
- [Finding a tenant id](#finding-a-tenant-id)
- [What failures mean](#what-failures-mean)

## Endpoints

| Purpose | URL |
|---|---|
| Authorize (browser) | `https://apps.fortnox.se/oauth-v1/auth` |
| Token (all grants) | `https://apps.fortnox.se/oauth-v1/token` |
| API base | `https://api.fortnox.se/3` |

Client credentials go in an `Authorization: Basic base64(client_id:client_secret)` header
on token requests, with `Content-Type: application/x-www-form-urlencoded`. API calls use
`Authorization: Bearer <access token>` with `Accept: application/json`.

## Token lifetimes

| Token | Lifetime | Catch |
|---|---|---|
| Authorization code | 10 minutes | Single use |
| Access token | 1 hour | A JWT; carries a `tenantId` claim |
| Refresh token | 45 idle days | **Single use — rotates on every refresh** |

The access token expiring hourly does *not* mean re-authorizing hourly — that is what the
refresh token is for. A human is only involved again if the refresh chain breaks.

## Authorization code flow

Send the user to the authorize URL:

```
GET https://apps.fortnox.se/oauth-v1/auth
  ?client_id=...
  &redirect_uri=...        # must match the portal registration character for character
  &scope=companyinformation customer
  &state=...               # CSRF token; compare it when Fortnox redirects back
  &access_type=offline     # required, or you get no refresh token
  &response_type=code
  &account_type=service    # creates a service account — the prerequisite for client
                           # credentials, and removes the dependency on one named person
```

Fortnox redirects to `redirect_uri` with `code` and `state`. Exchange within 10 minutes:

```
POST /oauth-v1/token
grant_type=authorization_code&code=<code>&redirect_uri=<the identical redirect_uri>
```

A token response with no `refresh_token` means `access_type=offline` was missing. The
client raises rather than accepting it, because the failure would otherwise surface an
hour later as an unexplained disconnection.

## Refresh

```
POST /oauth-v1/token
grant_type=refresh_token&refresh_token=<current>
```

```json
{
  "access_token": "…", "refresh_token": "…",
  "scope": "companyinformation", "expires_in": 3600, "token_type": "bearer"
}
```

The returned `refresh_token` is a **different value**. Persist it before anything uses the
new access token — if the process dies in between, that tenant is disconnected for good.
Store an absolute `expires_at`, never the `expires_in` countdown: a restart would reset a
clock that was already 50 minutes old.

Refresh early. The client uses a 120-second skew to absorb clock drift and slow requests;
refreshing at the exact expiry produces intermittent 401s that are miserable to reproduce.

## Client credentials

Needs the customer to have activated with `account_type=service`.

```
POST /oauth-v1/token
Authorization: Basic base64(client_id:client_secret)
TenantId: 123456          # numeric, in the header — not the body
grant_type=client_credentials&scope=companyinformation   # scope optional
```

Returns an access token and **no refresh token**, which is the point. Mint one whenever
you need it. Requires `companyinformation` among the consented scopes.

## Finding a tenant id

In order of convenience:

1. Decode the `tenantId` claim from any access token — `fortnox-auth tenant`. Signature
   verification is skipped deliberately: Fortnox doesn't publish the key, and the value is
   routing metadata, never an access decision.
2. `DatabaseNumber` from `/3/companyinformation` or `/3/settings/company`.
3. The *Consent created* / *Consent revoked* webhooks configured in the developer portal,
   which carry it on activation and deactivation.

## What failures mean

| Response | Meaning | Do |
|---|---|---|
| `invalid_grant` on refresh | Token already used, expired, or access revoked | **Stop.** Only the customer can reconnect. Never retry |
| 401 on an API call | Token invalid or revoked early | One forced refresh, then give up |
| 403 | Valid token, missing scope | Scope list is wrong — needs re-consent, not a retry |
| 429 | Rate limited | Honour `Retry-After`, back off |
| 5xx | Fortnox-side | Retry with jittered backoff |

`invalid_grant` is the one failure where a retry loop both fails *and* hides the cause.
It must become a visible "this customer must reconnect" item.
