"""Plausible Analytics — privacy-friendly site traffic + behaviour (Stats API).

For: Marketing + Product Agents. Turns "is anyone using the comparison pages, and which
categories pull traffic?" from a guess into a number. Plausible's Stats API gives
aggregate visitors/pageviews, time-series, and breakdowns by page / source / country —
enough for Marketing to see which categories earn search interest and for Product to see
which shelves get used (a real input to rollout sequencing).

Why Plausible (not GA4): a single clean Bearer key, no OAuth dance, GET-only JSON — it
fits this layer's read-only stdlib contract exactly. GA4 would need the OAuth + protobuf
Data API; if the project adopts GA4 later it gets its own client.

AUTH (both required): PLAUSIBLE_API_KEY (Bearer token from plausible.io > Settings > API
Keys) and PLAUSIBLE_SITE_ID (the domain as registered, e.g. "bari.co.il"). Self-hosted
instances: set PLAUSIBLE_BASE_URL. Status is NEEDS-ENV-VERIFY until a key + connected
site exist — the endpoints are documented and stable; live verification waits on the
account.

Docs: https://plausible.io/docs/stats-api
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .http import HttpError, get_json

CLIENT_VERSION = "1.0"


def _base() -> str:
    return os.environ.get("PLAUSIBLE_BASE_URL", "https://plausible.io").rstrip("/")


def _site() -> str:
    return os.environ.get("PLAUSIBLE_SITE_ID", "")


def _auth() -> dict[str, str]:
    key = os.environ.get("PLAUSIBLE_API_KEY", "")
    return {"Authorization": f"Bearer {key}"} if key else {}


def is_configured() -> bool:
    return bool(os.environ.get("PLAUSIBLE_API_KEY") and os.environ.get("PLAUSIBLE_SITE_ID"))


@dataclass
class Aggregate:
    period: str
    visitors: int | None = None
    pageviews: int | None = None
    bounce_rate: float | None = None
    visit_duration: float | None = None      # seconds


@dataclass
class BreakdownRow:
    label: str                                # page path / source / country, per property
    visitors: int | None = None
    pageviews: int | None = None


def aggregate(period: str = "30d",
              metrics: tuple[str, ...] = ("visitors", "pageviews", "bounce_rate", "visit_duration")
              ) -> Aggregate:
    """Top-line metrics for the site over a period ('7d','30d','month','6mo','12mo')."""
    data = get_json(
        f"{_base()}/api/v1/stats/aggregate",
        params={"site_id": _site(), "period": period, "metrics": ",".join(metrics)},
        headers=_auth(),
    )
    res = data.get("results", {})
    def _v(k):
        return res.get(k, {}).get("value") if isinstance(res.get(k), dict) else res.get(k)
    return Aggregate(
        period=period,
        visitors=_v("visitors"),
        pageviews=_v("pageviews"),
        bounce_rate=_v("bounce_rate"),
        visit_duration=_v("visit_duration"),
    )


def breakdown(property_: str = "event:page", period: str = "30d", limit: int = 20,
              metrics: tuple[str, ...] = ("visitors", "pageviews")) -> list[BreakdownRow]:
    """Break a metric down by a property — e.g. 'event:page' (which comparison pages get
    used), 'visit:source', 'visit:country'. The Product/Marketing workhorse query."""
    data = get_json(
        f"{_base()}/api/v1/stats/breakdown",
        params={"site_id": _site(), "period": period, "property": property_,
                "metrics": ",".join(metrics), "limit": limit},
        headers=_auth(),
    )
    out: list[BreakdownRow] = []
    for r in data.get("results", []):
        label = r.get(property_.split(":")[-1]) or r.get("page") or r.get("name") or ""
        out.append(BreakdownRow(label=label, visitors=r.get("visitors"),
                                pageviews=r.get("pageviews")))
    return out


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"Plausible configured: {is_configured()} "
          f"(needs PLAUSIBLE_API_KEY + PLAUSIBLE_SITE_ID)")
    if not is_configured():
        print("NEEDS-ENV-VERIFY: set the two env vars + connect a site, then re-run.")
        raise SystemExit(0)
    try:
        agg = aggregate("30d")
        print(f"30d: visitors={agg.visitors} pageviews={agg.pageviews} "
              f"bounce={agg.bounce_rate}% dur={agg.visit_duration}s")
        print("Top pages:")
        for row in breakdown("event:page", "30d", limit=5):
            print(f"  {row.visitors:>6} visitors  {row.label}")
    except HttpError as e:
        print(f"call failed (HTTP {e.status}): check key/site_id. {e}")
