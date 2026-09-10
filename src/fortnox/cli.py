"""``fortnox-auth`` - a small CLI for running the authorization flow by hand.

fortnox-auth url                    # print the URL to open in a browser
fortnox-auth exchange <code>        # swap the returned code for a token
fortnox-auth status                 # show token expiry and scopes
fortnox-auth refresh                # force a refresh now
fortnox-auth get companyinformation # make an authenticated GET
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from urllib.parse import parse_qs, urlparse

from . import oauth
from .client import FortnoxClient
from .config import FortnoxConfig
from .errors import FortnoxError
from .tokens import FileTokenStore


def _fmt_time(timestamp: float) -> str:
    return dt.datetime.fromtimestamp(timestamp, dt.UTC).isoformat(timespec="seconds")


def _extract_code(value: str) -> str:
    """Accept either a bare code or the whole redirect URL Fortnox sent back."""
    if "://" not in value:
        return value
    query = parse_qs(urlparse(value).query)
    codes = query.get("code")
    if not codes:
        raise SystemExit(f"no ?code= parameter found in {value!r}")
    return codes[0]


def _cmd_url(config: FortnoxConfig, args: argparse.Namespace) -> int:
    url, state = oauth.build_authorization_url(config, scopes=args.scope or None)
    print(url)
    print(f"\nstate: {state}", file=sys.stderr)
    print(
        "Open the URL, approve the integration, then run:\n"
        "  fortnox-auth exchange '<the redirect URL or its code parameter>'",
        file=sys.stderr,
    )
    return 0


def _cmd_exchange(config: FortnoxConfig, args: argparse.Namespace) -> int:
    token = oauth.exchange_code(config, _extract_code(args.code))
    store = FileTokenStore(config.token_path)
    with store.transaction():
        store.save(token)
    print(f"Token saved to {config.token_path}")
    print(f"  access token expires: {_fmt_time(token.expires_at)}")
    print(f"  scopes: {' '.join(token.scopes) or '(none reported)'}")
    return 0


def _cmd_status(config: FortnoxConfig, args: argparse.Namespace) -> int:
    mode = "client-credentials (service account)" if config.tenant_id else "refresh token"
    store = FileTokenStore(config.token_path)
    token = store.load()
    if token is None:
        hint = "service-token" if config.tenant_id else "url"
        print(f"Auth mode: {mode}")
        print(f"No token stored at {config.token_path}. Run `fortnox-auth {hint}` first.")
        return 1

    print(f"Auth mode:  {mode}")
    print(f"Token file: {config.token_path}")
    print(f"  access token expires:  {_fmt_time(token.expires_at)}")
    print(f"  expired:               {token.is_expired()}")
    print(f"  obtained:              {_fmt_time(token.obtained_at)}")
    print(f"  tenant id:             {token.tenant_id or '(not present in token)'}")
    print(f"  scopes:                {' '.join(token.scopes) or '(none reported)'}")
    if token.refresh_token:
        print(f"  refresh token expires: ~{_fmt_time(token.refresh_token_expires_at)} (estimated)")
    else:
        print("  refresh token:         none (client-credentials tokens do not have one)")
    return 0


def _cmd_tenant(config: FortnoxConfig, args: argparse.Namespace) -> int:
    """Print the tenant id, so it can be pinned as FORTNOX_TENANT_ID."""
    token = FileTokenStore(config.token_path).load()
    if token is None:
        print(f"No token stored at {config.token_path}.", file=sys.stderr)
        return 1

    tenant_id = token.tenant_id
    if tenant_id:
        print(tenant_id)
        return 0

    print(
        "The stored token carries no tenantId claim. Read DatabaseNumber from\n"
        "  fortnox-auth get companyinformation\n"
        "(requires the companyinformation scope).",
        file=sys.stderr,
    )
    return 1


def _cmd_service_token(config: FortnoxConfig, args: argparse.Namespace) -> int:
    """Mint an access token with client-credentials - no refresh token involved."""
    token = oauth.fetch_service_account_token(config, args.tenant_id)
    store = FileTokenStore(config.token_path)
    with store.transaction():
        store.save(token)
    print(f"Minted a service-account token, saved to {config.token_path}")
    print(f"  expires: {_fmt_time(token.expires_at)}")
    print(f"  scopes:  {' '.join(token.scopes) or '(from consent)'}")
    return 0


def _cmd_refresh(config: FortnoxConfig, args: argparse.Namespace) -> int:
    store = FileTokenStore(config.token_path)
    with store.transaction():
        token = store.load()
        if token is None:
            print(f"No token stored at {config.token_path}.", file=sys.stderr)
            return 1
        new_token = oauth.refresh_token(config, token)
        store.save(new_token)
    print(f"Refreshed. New access token expires {_fmt_time(new_token.expires_at)}")
    return 0


def _cmd_get(config: FortnoxConfig, args: argparse.Namespace) -> int:
    with FortnoxClient(config) as client:
        print(json.dumps(client.get(args.path), indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fortnox-auth", description="Run the Fortnox authorization flow from the terminal."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    url_parser = subparsers.add_parser("url", help="print the authorization URL")
    url_parser.add_argument(
        "--scope", action="append", help="scope to request (repeatable); defaults to FORTNOX_SCOPES"
    )
    url_parser.set_defaults(func=_cmd_url)

    exchange_parser = subparsers.add_parser(
        "exchange", help="exchange an authorization code for a token"
    )
    exchange_parser.add_argument("code", help="the code, or the full redirect URL containing it")
    exchange_parser.set_defaults(func=_cmd_exchange)

    status_parser = subparsers.add_parser("status", help="show the stored token's state")
    status_parser.set_defaults(func=_cmd_status)

    refresh_parser = subparsers.add_parser("refresh", help="force a token refresh")
    refresh_parser.set_defaults(func=_cmd_refresh)

    tenant_parser = subparsers.add_parser(
        "tenant", help="print the tenant id from the stored token"
    )
    tenant_parser.set_defaults(func=_cmd_tenant)

    service_parser = subparsers.add_parser(
        "service-token", help="mint a token via the client-credentials grant"
    )
    service_parser.add_argument("--tenant-id", help="tenant id; defaults to FORTNOX_TENANT_ID")
    service_parser.set_defaults(func=_cmd_service_token)

    get_parser = subparsers.add_parser("get", help="make an authenticated GET request")
    get_parser.add_argument("path", help="API path, e.g. companyinformation")
    get_parser.set_defaults(func=_cmd_get)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = FortnoxConfig.from_env()
        return int(args.func(config, args))
    except FortnoxError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
