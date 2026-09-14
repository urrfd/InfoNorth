# InfoNorth

A wiki for BeOnenorth, plus `src/fortnox/` — a client for the
[Fortnox API](https://www.fortnox.se/developer) (Swedish accounting/ERP SaaS).

## Commands

```bash
uv venv && uv pip install -e ".[dev]"   # set up

.venv/bin/pytest                         # test
.venv/bin/pytest --cov=fortnox --cov-report=term-missing
.venv/bin/ruff check .                   # lint
.venv/bin/ruff format .                  # format
```

**Run tests as `pytest`, not `python -m pytest`.** The two are not equivalent:
`python -m pytest` puts the working directory on `sys.path`, which hides import bugs
that CI then catches. A test needing a helper from another test module is a smell —
put it in `tests/conftest.py` as a fixture instead.

## Layout

| Path | What |
|---|---|
| `src/fortnox/` | The API client. See `.claude/skills/fortnox/` before changing it. |
| `tests/` | Offline suite — the HTTP layer is mocked with `respx`, no live calls. |
| `.github/workflows/ci.yml` | Lint, format and tests on Python 3.11–3.13. |

## Conventions

**Tests never touch the network.** Every HTTP interaction is mocked with `respx`. This
keeps the suite fast and means it can't fail because someone's sandbox expired or burn a
real refresh token. Keep it that way — if you need a new response shape, mock it.

**Inject clocks rather than sleeping.** `SlidingWindowRateLimiter` takes `monotonic` and
`sleep` callables so its tests run instantly and deterministically. Do the same for
anything else time-dependent; a suite with real sleeps in it stops being run.

**Secrets never reach a log or a traceback.** `Token.__repr__` masks both tokens
deliberately. Don't add logging that prints a token response body, and don't commit a
token file — `fortnox_token*.json` is gitignored for that reason.

**Name tests as sentences.** `test_expiring_token_is_refreshed_before_use` states a claim
about behaviour; `test_refresh_2` doesn't. When one fails, the name should tell you what
broke without opening the file.

## Git

Work on a branch and open a PR — `main` stays green. CI must pass before merging; if it
fails, fix the cause rather than re-running. Don't commit directly to `main`.
