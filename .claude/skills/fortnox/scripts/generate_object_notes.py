#!/usr/bin/env python3
"""Generate one object note per Fortnox API resource from the OpenAPI spec.

The notes are derived, never hand-written, so they can be regenerated whenever
Fortnox publishes a new spec and they cannot drift from it by neglect. What the
spec cannot tell us - whether a call has actually been made, and what came back -
is left as an explicit gap for a human to fill after testing, rather than guessed.

Usage:
    python generate_object_notes.py [--spec PATH] [--out DIR] [--check]

``--check`` regenerates into a temporary directory and exits non-zero if the
committed notes differ, so CI can catch notes edited by hand instead of
regenerated.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_SPEC = HERE.parent / "references" / "openapi.json"
DEFAULT_OUT = HERE.parent / "references" / "objects"

HTTP_METHODS = ("get", "post", "put", "patch", "delete")
WRITE_METHODS = ("post", "put", "patch", "delete")

# Query parameters Fortnox applies across resources rather than per resource.
GLOBAL_PARAMS = {"limit", "offset", "page", "sortby", "sortorder", "lastmodified", "financialyear"}


def slugify(tag: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", tag.lower()).strip("-")


def title_of(tag: str) -> str:
    """`fortnox_Articles` -> `Articles`; keeps the group for disambiguation."""
    return tag.split("_", 1)[1] if "_" in tag else tag


def group_of(tag: str) -> str:
    return tag.split("_", 1)[0] if "_" in tag else "(ungrouped)"


def deref(spec: dict, node: Any, seen: frozenset[str] = frozenset()) -> Any:
    """Resolve a local $ref, guarding against the spec's recursive schemas."""
    if not isinstance(node, dict):
        return node
    ref = node.get("$ref")
    if not ref:
        return node
    if ref in seen:
        return {}
    name = ref.rsplit("/", 1)[-1]
    return deref(spec, spec.get("components", {}).get("schemas", {}).get(name, {}), seen | {ref})


def unwrap(spec: dict, schema: Any) -> tuple[str | None, dict]:
    """Return (collection_key, item_schema) for a Fortnox `*_Wrap` response.

    Fortnox wraps every payload in a named key - ``{"Articles": [...]}`` for
    lists, ``{"Article": {...}}`` for single resources. That key is exactly what
    ``FortnoxClient.paginate`` needs, so it is worth surfacing explicitly.
    """
    schema = deref(spec, schema)
    props = schema.get("properties") or {}
    for key, value in props.items():
        if key == "MetaInformation":
            continue
        value = deref(spec, value)
        if value.get("type") == "array":
            return key, deref(spec, value.get("items", {}))
        if value.get("type") == "object" or value.get("properties"):
            return key, value
    return None, schema


def field_names(schema: dict) -> list[str]:
    return sorted(k for k in (schema.get("properties") or {}) if not k.startswith("@"))


def response_schema(spec: dict, op: dict) -> Any:
    for code in ("200", "201"):
        content = (op.get("responses", {}).get(code) or {}).get("content") or {}
        for media in content.values():
            if media.get("schema"):
                return media["schema"]
    return None


def request_schema(spec: dict, op: dict) -> Any:
    content = (op.get("requestBody") or {}).get("content") or {}
    for media in content.values():
        if media.get("schema"):
            return media["schema"]
    return None


def collect(spec: dict) -> dict[str, dict]:
    """Group operations by tag - one tag is one resource, one note."""
    by_tag: dict[str, dict] = defaultdict(lambda: {"ops": [], "paths": set()})
    for path, item in spec.get("paths", {}).items():
        shared = item.get("parameters", [])
        for method in HTTP_METHODS:
            op = item.get(method)
            if not op:
                continue
            for tag in op.get("tags") or ["(untagged)"]:
                entry = by_tag[tag]
                entry["ops"].append(
                    {
                        "method": method,
                        "path": path,
                        "op": op,
                        "params": shared + op.get("parameters", []),
                    }
                )
                entry["paths"].add(path)
    return by_tag


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


def escape(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def render(spec: dict, tag: str, entry: dict) -> str:
    name = title_of(tag)
    ops = sorted(entry["ops"], key=lambda o: (o["path"], HTTP_METHODS.index(o["method"])))
    methods = sorted({o["method"].upper() for o in ops})
    writes = sorted({o["method"].upper() for o in ops if o["method"] in WRITE_METHODS})

    lines = [
        f"# Fortnox Object: {name}",
        "",
        f"API group `{group_of(tag)}` · spec tag `{tag}`",
        "",
        "## Purpose",
        "",
    ]

    # Prefer a list-endpoint description; it usually describes the resource itself.
    blurb = ""
    for o in ops:
        if o["method"] == "get":
            blurb = (o["op"].get("description") or o["op"].get("summary") or "").strip()
            if blurb:
                break
    lines.append(blurb or f"Operations on `{name}`.")
    lines += ["", "## Endpoints", ""]
    lines += md_table(
        ["Method", "Path", "Summary"],
        [
            [o["method"].upper(), f"`{o['path']}`", escape(o["op"].get("summary") or "")]
            for o in ops
        ],
    )

    # How to actually call this resource. Fortnox is really two APIs: the classic
    # `/3/` one with wrapped responses that FortnoxClient is built around, and
    # newer `/api/*` services with their own conventions. Getting this wrong is a
    # silent 404 or a TypeError, so the note states it explicitly.
    list_op = next((o for o in ops if o["method"] == "get" and "{" not in o["path"]), None)
    coll_key: str | None = None
    list_item: dict = {}
    single_item: dict = {}
    bare_array = False

    for o in ops:
        schema = response_schema(spec, o["op"])
        if not schema:
            continue
        if o["method"] != "get":
            continue
        resolved = deref(spec, schema) if "$ref" in schema else schema
        if resolved.get("type") == "array":
            if o is list_op:
                bare_array = True
                list_item = deref(spec, resolved.get("items", {}))
            continue
        key, item = unwrap(spec, schema)
        if o is list_op and key:
            coll_key, list_item = key, item
        elif key and not single_item:
            single_item = item

    lines += ["", "## Calling it", ""]
    if list_op:
        path = list_op["path"]
        if path.startswith("/3/"):
            rel = path[len("/3/") :]
            if coll_key:
                lines += [
                    f"Records are wrapped under `{coll_key}`, so pagination works normally:",
                    "",
                    "```python",
                    f'for record in client.paginate("{rel}", "{coll_key}"):',
                    "    ...",
                    "```",
                ]
            else:
                lines += [
                    "```python",
                    f'result = client.get("{rel}")',
                    "```",
                ]
        else:
            lines += [
                "This resource lives outside the classic `/3/` API, which the client's base",
                "URL points at. Pass the absolute URL:",
                "",
                "```python",
                f'result = client.get("https://api.fortnox.se{path}")',
                "```",
            ]
        if bare_array:
            lines += [
                "",
                "**The list response is a bare JSON array, not a wrapped object.**",
                "`client.paginate()` assumes the `/3/` wrapping and will not work here -",
                "iterate the returned list directly and handle paging from the parameters below.",
            ]
    else:
        paths = sorted(entry["paths"])
        lines += [
            "No collection endpoint: every operation addresses a single record.",
            "",
            "```python",
            f'result = client.get("{paths[0].lstrip("/").replace("3/", "", 1)}")'
            if paths[0].startswith("/3/")
            else f'result = client.get("https://api.fortnox.se{paths[0]}")',
            "```",
        ]

    fields = field_names(list_item) or field_names(single_item)
    if fields:
        lines += ["", "## Key fields", "", ", ".join(f"`{f}`" for f in fields)]

    # Writable fields, from the request payload schema.
    payload_fields: list[str] = []
    required: list[str] = []
    for o in ops:
        if o["method"] not in ("post", "put", "patch"):
            continue
        schema = request_schema(spec, o["op"])
        if not schema:
            continue
        _, item = unwrap(spec, schema)
        payload_fields = field_names(item)
        required = sorted(item.get("required") or [])
        if payload_fields:
            break
    if payload_fields:
        lines += ["", "## Writable fields", "", ", ".join(f"`{f}`" for f in payload_fields)]
        req = ", ".join(f"`{r}`" for r in required) or "none declared in the spec"
        lines += ["", f"Required: {req}"]

    # Query parameters, split global vs resource-specific, because Fortnox only
    # allows one resource-specific filter at a time.
    seen: dict[str, dict] = {}
    for o in ops:
        if o["method"] != "get":
            continue
        for p in o["params"]:
            p = deref(spec, p) if "$ref" in p else p
            if p.get("in") == "query" and p.get("name") not in seen:
                seen[p["name"]] = p
    specific = [p for n, p in sorted(seen.items()) if n.lower() not in GLOBAL_PARAMS]
    globals_present = sorted(n for n in seen if n.lower() in GLOBAL_PARAMS)

    if specific:
        rows = []
        for p in specific:
            sch = p.get("schema") or {}
            values = ", ".join(f"`{v}`" for v in (sch.get("enum") or [])) or sch.get("type", "")
            rows.append([f"`{p['name']}`", escape(values), escape(p.get("description") or "")])
        lines += ["", "## Resource filters", ""]
        lines += md_table(["Parameter", "Values", "Notes"], rows)
        lines += [
            "",
            "Only **one** resource-specific filter may be used per request, though it can be",
            "combined with a global parameter such as `lastmodified`.",
        ]
    if globals_present:
        names = ", ".join(f"`{g}`" for g in globals_present)
        lines += ["", f"Global parameters accepted: {names}."]

    # Safety, following the SAP B1 service-layer note convention.
    lines += ["", "## Safe use cases", ""]
    if "GET" in methods:
        lines.append(f"- Read {name} for investigation, reporting and export.")
    else:
        lines.append(f"- No read-only operation is exposed for {name}.")

    lines += ["", "## Dangerous / live actions", ""]
    if writes:
        lines += [
            f"- `{', '.join(writes)}` change live accounting data in the customer's company.",
            "- These post to real books. Keep them behind the read-only default, a dry run,",
            "  and explicit approval.",
        ]
    else:
        lines.append("- None: this resource is read-only.")

    lines += [
        "",
        "## Dry-run requirements",
        "",
        "- Verify with a read-only `GET` first.",
        "- Write out the exact request body and target, and have it reviewed, before any write.",
        "- Run it against a sandbox company before a live tenant.",
        "",
        "## Approval requirements",
        "",
        "- Explicit user approval for every write. Approval for one write is not approval",
        "  for the next.",
        "",
        "## Tested read-only requests",
        "",
        "- None yet. Add the exact calls you have run once verified against a real tenant.",
        "",
        "## Example response fields",
        "",
        "- Fill in after reviewing a successful response. The fields above come from the",
        "  spec, which describes what may be returned, not what a given company does return.",
        "",
        "## Date tested",
        "",
        "- Not yet verified against a live or sandbox tenant.",
        "",
        "## Notes",
        "",
        "- Generated from the Fortnox OpenAPI specification; do not edit by hand.",
        f"  Regenerate with `python {Path(__file__).name}`.",
        "",
    ]
    return "\n".join(lines)


def render_index(spec: dict, by_tag: dict[str, dict]) -> str:
    groups: dict[str, list[str]] = defaultdict(list)
    for tag in by_tag:
        groups[group_of(tag)].append(tag)

    total_ops = sum(len(e["ops"]) for e in by_tag.values())
    lines = [
        "# Fortnox object notes",
        "",
        f"One note per API resource: **{len(by_tag)} resources**, {total_ops} operations, ",
        f"{len(spec.get('paths', {}))} paths. Generated from the OpenAPI specification in ",
        "`../openapi.json` — see `../../scripts/generate_object_notes.py`.",
        "",
        "Each note carries the resource's endpoints, the collection key needed by",
        "`FortnoxClient.paginate`, its fields, its filters, and the safety rules that apply",
        "to its write operations. Read the note for a resource before calling it.",
        "",
        "**The field and filter lists are derived from the spec, not from observed traffic.**",
        "They describe what Fortnox documents, which is not always what a given company",
        "returns. Each note has a `Date tested` line recording whether anyone has checked.",
        "",
    ]
    for group in sorted(groups):
        tags = sorted(groups[group], key=title_of)
        lines += [f"## {group}", ""]
        for tag in tags:
            methods = sorted({o["method"].upper() for o in by_tag[tag]["ops"]})
            writes = [m for m in methods if m != "GET"]
            mark = " ⚠️ writes" if writes else ""
            lines.append(f"- [{title_of(tag)}]({slugify(tag)}.md) — {', '.join(methods)}{mark}")
        lines.append("")
    return "\n".join(lines)


def generate(spec_path: Path, out_dir: Path) -> int:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    by_tag = collect(spec)

    out_dir.mkdir(parents=True, exist_ok=True)
    for existing in out_dir.glob("*.md"):
        existing.unlink()

    for tag, entry in by_tag.items():
        (out_dir / f"{slugify(tag)}.md").write_text(render(spec, tag, entry), encoding="utf-8")
    (out_dir / "README.md").write_text(render_index(spec, by_tag), encoding="utf-8")
    return len(by_tag)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="fail if committed notes are stale")
    args = ap.parse_args()

    if not args.spec.exists():
        print(f"error: spec not found at {args.spec}", file=sys.stderr)
        return 2

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp) / "objects"
            generate(args.spec, tmp_dir)
            a = sorted(p.name for p in tmp_dir.glob("*.md"))
            b = sorted(p.name for p in args.out.glob("*.md"))
            if a != b:
                print("error: object notes are stale (file list differs)", file=sys.stderr)
                return 1
            for name in a:
                if (tmp_dir / name).read_text() != (args.out / name).read_text():
                    print(f"error: {name} is stale; regenerate it", file=sys.stderr)
                    return 1
        print(f"object notes are up to date ({len(a)} files)")
        return 0

    count = generate(args.spec, args.out)
    print(f"wrote {count} object notes + index to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
