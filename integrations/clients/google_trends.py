"""Google Trends — Hebrew consumer-demand signal (DORMANT / fenced).

For: Product + Marketing ONLY. Answers one question — "of the candidate next categories,
which has rising/sustained Hebrew search demand?" — to inform roadmap *sequencing* (D1).

HARD FENCE (Product ruling, TASK-170 follow-up):
  * Informs category launch ORDER, never a product's QUALITY/score. Popularity ≠ quality;
    a Trends number must never reach BSIP scoring or any consumer-facing verdict.
  * Dormant by default: not wired into any pipeline, not an agent corpus source. Run it
    manually during a roadmap-sequencing pass.

Caveats: Google Trends has no official API. This uses the same undocumented endpoint flow
pytrends wraps (explore → widgetdata) and can break or rate-limit (429) without warning.
Values are RELATIVE search interest (0–100), not absolute volume. Treat as directional.
"""
from __future__ import annotations

import http.cookiejar
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

EXPLORE = "https://trends.google.com/trends/api/explore"
WIDGET = "https://trends.google.com/trends/api/widgetdata"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


@dataclass
class DemandSeries:
    keyword: str
    geo: str
    timeframe: str
    points: list[tuple[str, int]] = field(default_factory=list)  # (date, 0-100)

    @property
    def average(self) -> float | None:
        vals = [v for _, v in self.points]
        return round(sum(vals) / len(vals), 1) if vals else None

    @property
    def latest(self) -> int | None:
        return self.points[-1][1] if self.points else None

    @property
    def recent_avg(self) -> float | None:
        """Mean of the last quarter of the window (the current demand level)."""
        vals = [v for _, v in self.points]
        if not vals:
            return None
        n = max(1, len(vals) // 4)
        return round(sum(vals[-n:]) / n, 1)

    @property
    def baseline_avg(self) -> float | None:
        """Mean of the first quarter of the window (where demand started)."""
        vals = [v for _, v in self.points]
        if not vals:
            return None
        n = max(1, len(vals) // 4)
        return round(sum(vals[:n]) / n, 1)

    @property
    def momentum(self) -> float | None:
        """Recent level vs baseline as a % change. +ve = rising demand, -ve = fading.
        The sequencing signal: a category trending UP is a stronger launch-order candidate
        than one at the same absolute level but flat/declining."""
        r, b = self.recent_avg, self.baseline_avg
        if r is None or not b:
            return None
        return round((r - b) / b * 100, 1)

    @property
    def is_rising(self) -> bool:
        """True when recent demand is ≥10% above baseline (noise-tolerant)."""
        m = self.momentum
        return m is not None and m >= 10.0

    def summary(self) -> str:
        """One-line sequencing read (directional — relative interest, not volume)."""
        if not self.points:
            return f"{self.keyword}: no data"
        arrow = "↑rising" if self.is_rising else ("↓fading" if (self.momentum or 0) <= -10 else "→flat")
        return (f"{self.keyword} [{self.geo}]: level={self.recent_avg} "
                f"(baseline={self.baseline_avg}, {self.momentum:+}% {arrow})")


_OPENER: urllib.request.OpenerDirector | None = None


def _session() -> urllib.request.OpenerDirector:
    """One warm cookied session, reused across calls (a fresh NID per call trips 429)."""
    global _OPENER
    if _OPENER is None:
        op = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        op.addheaders = [("User-Agent", _UA), ("Accept-Language", "he,en")]
        op.open("https://trends.google.com/trends/?geo=IL", timeout=20).read(50)
        _OPENER = op
    return _OPENER


def _get(op, url: str, retries: int = 2) -> dict:
    for attempt in range(retries + 1):
        try:
            body = op.open(url, timeout=25).read().decode("utf-8", "replace")
            return json.loads(body[body.find("{"):])  # strip ")]}'," XSSI guard prefix
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                time.sleep(2 * (attempt + 1))  # unofficial endpoint throttles aggressively
                continue
            raise


def _explore(op, keyword: str, geo: str, timeframe: str, hl: str) -> list[dict]:
    req = {"comparisonItem": [{"keyword": keyword, "geo": geo, "time": timeframe}],
           "category": 0, "property": ""}
    url = f"{EXPLORE}?" + urllib.parse.urlencode(
        {"hl": hl, "tz": "-120", "req": json.dumps(req, ensure_ascii=False)})
    return _get(op, url).get("widgets", [])


def interest_over_time(keyword: str, geo: str = "IL", timeframe: str = "today 12-m",
                       hl: str = "he") -> DemandSeries:
    """Relative Hebrew search interest (0–100) over time for one keyword."""
    op = _session()
    widgets = _explore(op, keyword, geo, timeframe, hl)
    w = next((x for x in widgets if x.get("id") == "TIMESERIES"), None)
    series = DemandSeries(keyword=keyword, geo=geo, timeframe=timeframe)
    if not w:
        return series
    url = f"{WIDGET}/multiline?" + urllib.parse.urlencode(
        {"hl": hl, "tz": "-120", "req": json.dumps(w["request"], ensure_ascii=False),
         "token": w["token"]})
    data = _get(op, url).get("default", {})
    for row in data.get("timelineData", []):
        vals = row.get("value") or [0]
        series.points.append((row.get("formattedTime", ""), int(vals[0])))
    return series


def rising_queries(keyword: str, geo: str = "IL", timeframe: str = "today 12-m",
                   hl: str = "he") -> list[tuple[str, str]]:
    """Top RISING related Hebrew queries for a keyword — (query, growth). Demand signal."""
    op = _session()
    widgets = _explore(op, keyword, geo, timeframe, hl)
    w = next((x for x in widgets if x.get("id") == "RELATED_QUERIES"), None)
    if not w:
        return []
    url = f"{WIDGET}/relatedsearches?" + urllib.parse.urlencode(
        {"hl": hl, "tz": "-120", "req": json.dumps(w["request"], ensure_ascii=False),
         "token": w["token"]})
    ranked = _get(op, url).get("default", {}).get("rankedList", [])
    rising = ranked[1]["rankedKeyword"] if len(ranked) > 1 else []
    out = []
    for k in rising:
        growth = k.get("formattedValue", "")
        out.append((k.get("query", ""), growth))
    return out


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("DORMANT/fenced — Product+Marketing roadmap sequencing only; never scoring.")
    try:
        # category-sequencing read: compare candidate categories by demand + momentum
        for kw in ("חלבון", "יוגורט", "גרנולה"):
            s = interest_over_time(kw)
            print(f"  {s.summary()}  (n={len(s.points)} weeks)")
        print("rising related queries for חטיף חלבון:")
        for q, g in rising_queries("חטיף חלבון")[:5]:
            print(f"    {q}  ({g})")
    except Exception as e:  # noqa: BLE001
        print(f"Trends run failed ({type(e).__name__}: {str(e)[:60]}). "
              f"Endpoint is unofficial — expect occasional 429/breakage.")
