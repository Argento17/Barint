"""Google Search Console — organic search performance (Search Analytics API).

For: Marketing Agent. The one source that answers "what is Bari actually ranking for in
Israeli Google, and on which queries are we close to page one?" — clicks, impressions,
CTR, and average position, broken down by query, page, or country. This is the spine of
the SEO pillar: it turns content-pillar planning from intuition into a keyword-gap list.

Position in the stack: Plausible (analytics.py) measures on-site behaviour *after* arrival;
Search Console measures the *acquisition* side — what Google shows and what gets clicked,
including queries that never convert to a visit. Complementary, not overlapping.

POST note: Search Analytics is a POST query (a read — it mutates nothing). The shared
`http` module is GET-only by design, so this client carries a tiny stdlib POST helper
scoped to this one read-query use; it still performs no write to any Google resource.

AUTH: OAuth2 — Search Console has no static API key. Two paths, in priority order:
1. GSC_ACCESS_TOKEN env var (a raw ~1h token) — for one-off manual runs.
2. SERVICE ACCOUNT (the standing path, wired 2026-07-04 TASK-505): auto-mints fresh
   `webmasters.readonly` tokens from the same GA4 reader key
   (ga4-mcp-reader@toms-budget; key at GSC_SA_KEY_FILE, default the ga4-mcp key path).
   Requires the service account added as a user on the Search Console property
   (done 2026-07-04) and the `google-auth` package (present). Tokens are cached and
   auto-refreshed in-process.
GSC_SITE_URL defaults to "sc-domain:bari.digital" (owner-confirmed Domain property,
2026-07-04); override via env for any other property.

Docs: https://developers.google.com/webmaster-tools/v1/searchanalytics/query
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from .http_client import USER_AGENT, HttpError

CLIENT_VERSION = "1.1"
API = "https://searchconsole.googleapis.com/webmasters/v3"

_DEFAULT_SA_KEY = r"C:\Users\HP\.config\ga4-mcp\ga4-mcp-reader-key.json"
_GSC_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
_sa_credentials = None  # cached google.oauth2 credentials, refreshed on expiry


def _sa_key_file() -> str:
    return os.environ.get("GSC_SA_KEY_FILE", _DEFAULT_SA_KEY)


def _sa_token() -> str:
    """Mint (and cache) an access token from the service-account key. Returns '' if
    the key file or google-auth is unavailable — callers fall back to env token."""
    global _sa_credentials
    try:
        if _sa_credentials is None:
            if not os.path.isfile(_sa_key_file()):
                return ""
            from google.oauth2 import service_account  # deferred import
            _sa_credentials = service_account.Credentials.from_service_account_file(
                _sa_key_file(), scopes=[_GSC_SCOPE])
        if not _sa_credentials.valid:
            from google.auth.transport.requests import Request  # deferred import
            _sa_credentials.refresh(Request())
        return _sa_credentials.token or ""
    except Exception:
        return ""


def _token() -> str:
    return os.environ.get("GSC_ACCESS_TOKEN", "") or _sa_token()


def _site() -> str:
    return os.environ.get("GSC_SITE_URL", "sc-domain:bari.digital")


def is_configured() -> bool:
    return bool(_token() and _site())


def _post_json(url: str, body: dict, timeout: int = 25) -> dict:
    """Minimal stdlib POST for the read-only Search Analytics query. Mirrors http.get's
    error contract (raises HttpError, carries status)."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {_token()}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:  # type: ignore[attr-defined]
        raise HttpError(f"HTTP {e.code} for {url}", status=e.code)
    except urllib.error.URLError as e:   # type: ignore[attr-defined]
        raise HttpError(f"network error for {url}: {e.reason}")


@dataclass
class SearchRow:
    keys: list[str]                 # the dimension values (e.g. [query] or [query, page])
    clicks: int = 0
    impressions: int = 0
    ctr: float = 0.0                # 0..1
    position: float = 0.0           # average rank (lower is better)

    @property
    def query(self) -> str:
        return self.keys[0] if self.keys else ""

    @property
    def near_page_one(self) -> bool:
        """Position 11-20 with real impressions = a content-optimisation opportunity."""
        return 10 < self.position <= 20 and self.impressions >= 50


def query(dimensions: tuple[str, ...] = ("query",), days: int = 28, row_limit: int = 25,
          search_type: str = "web") -> list[SearchRow]:
    """Run a Search Analytics query over the last `days`. dimensions: any of
    ('query','page','country','device','date'). Returns rows ordered by clicks desc."""
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days)
    site_enc = urllib.parse.quote(_site(), safe="")
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": list(dimensions),
        "rowLimit": row_limit,
        "type": search_type,
    }
    data = _post_json(f"{API}/sites/{site_enc}/searchAnalytics/query", body)
    out: list[SearchRow] = []
    for r in data.get("rows", []):
        out.append(SearchRow(
            keys=r.get("keys", []),
            clicks=int(r.get("clicks", 0)),
            impressions=int(r.get("impressions", 0)),
            ctr=float(r.get("ctr", 0.0)),
            position=round(float(r.get("position", 0.0)), 1),
        ))
    return out


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"Search Console configured: {is_configured()} "
          f"(needs GSC_ACCESS_TOKEN + GSC_SITE_URL)")
    if not is_configured():
        print("NEEDS-ENV-VERIFY: OAuth token (webmasters.readonly) + property URL, then re-run.")
        raise SystemExit(0)
    try:
        rows = query(("query",), days=28, row_limit=10)
        print(f"top queries (28d): {len(rows)} rows")
        for r in rows[:8]:
            flag = " <- near page 1" if r.near_page_one else ""
            print(f"  pos={r.position:>4} clicks={r.clicks:>4} impr={r.impressions:>6} "
                  f"{r.query}{flag}")
    except HttpError as e:
        print(f"call failed (HTTP {e.status}): token may be expired or property unverified. {e}")
