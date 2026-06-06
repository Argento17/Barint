"""Google PageSpeed Insights — mobile performance + Core Web Vitals.

For: Frontend Agent. The phase metric is "first-time mobile user understands the shelf
in 15-20 seconds" — load performance is half of that and is currently unmeasured. This
gives Lighthouse performance + field CWV for any live comparison-page URL, so Frontend
can ship against a number instead of a vibe.

AUTH: works without a key but is aggressively rate-limited (the build sandbox hit 429).
Set PAGESPEED_API_KEY (free from Google Cloud, "PageSpeed Insights API") for reliable
use. Endpoint is confirmed live; a clean run needs the key.

Docs: https://developers.google.com/speed/docs/insights/v5/get-started
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from .http import get_json

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


@dataclass
class PageSpeedResult:
    url: str
    strategy: str
    performance: float | None          # 0-100 Lighthouse performance score
    lcp_s: float | None = None         # Largest Contentful Paint (s)
    cls: float | None = None           # Cumulative Layout Shift
    tbt_ms: float | None = None        # Total Blocking Time (ms)
    fcp_s: float | None = None         # First Contentful Paint (s)
    speed_index_s: float | None = None

    @property
    def passes_mobile_budget(self) -> bool:
        """Heuristic budget for a comprehension-critical mobile page."""
        return (
            (self.performance or 0) >= 80
            and (self.lcp_s is None or self.lcp_s <= 2.5)
            and (self.cls is None or self.cls <= 0.1)
        )


def _num(audits: dict, key: str) -> float | None:
    a = audits.get(key, {})
    v = a.get("numericValue")
    return float(v) if v is not None else None


def analyze(url: str, strategy: str = "mobile") -> PageSpeedResult:
    """Run PageSpeed Insights for a URL. strategy = 'mobile' | 'desktop'."""
    params = {"url": url, "strategy": strategy, "category": "performance"}
    key = os.environ.get("PAGESPEED_API_KEY")
    if key:
        params["key"] = key
    data = get_json(API, params=params, timeout=60, retries=3, backoff=3)
    lh = data.get("lighthouseResult", {})
    audits = lh.get("audits", {})
    perf = lh.get("categories", {}).get("performance", {}).get("score")
    fcp = _num(audits, "first-contentful-paint")
    lcp = _num(audits, "largest-contentful-paint")
    tbt = _num(audits, "total-blocking-time")
    si = _num(audits, "speed-index")
    cls = _num(audits, "cumulative-layout-shift")
    return PageSpeedResult(
        url=url,
        strategy=strategy,
        performance=round(perf * 100, 1) if perf is not None else None,
        lcp_s=round(lcp / 1000, 2) if lcp else None,
        cls=round(cls, 3) if cls is not None else None,
        tbt_ms=round(tbt) if tbt is not None else None,
        fcp_s=round(fcp / 1000, 2) if fcp else None,
        speed_index_s=round(si / 1000, 2) if si else None,
    )


if __name__ == "__main__":
    has_key = bool(os.environ.get("PAGESPEED_API_KEY"))
    print(f"PAGESPEED_API_KEY set: {has_key} (without it, expect 429)")
    try:
        r = analyze("https://example.com", "mobile")
        print(f"perf={r.performance} LCP={r.lcp_s}s CLS={r.cls} TBT={r.tbt_ms}ms "
              f"budget_ok={r.passes_mobile_budget}")
    except Exception as e:  # noqa: BLE001
        print(f"run failed ({type(e).__name__}: {e}). Set PAGESPEED_API_KEY and retry.")
