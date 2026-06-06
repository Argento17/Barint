"""iHerb Supplement-Facts panel-extract pipeline  (TASK-171G, parent TASK-171).

Turns an iHerb product page into a BSIP0-S `SupplementLabel` candidate. The Phase-3
feasibility probe (`02_products/supplements/phase3_sourcing_feasibility_v1.md`) proved
firecrawl extracts active · per-serving amount · unit · form · primary-claim · blend-flag
cleanly from iHerb PDPs (5/5 dossier actives). This module productionizes that path:

  * one firecrawl_scrape(json) call per PDP with a fixed BSIP0-S extraction schema,
  * a local JSON cache (re-runs are free; respectful low-volume; honor ToS),
  * strict lossiness rules — any field firecrawl cannot return is recorded `missing`,
    NEVER fabricated,
  * a `Provenance` stamp, born `verification_status="candidate"` (EDPG firewall).

FIRE­CRAWL BOUNDARY. This client does NOT import an MCP/firecrawl SDK directly — in the
Bari agent runtime the firecrawl scrape is a *tool call* the agent makes, not a library
call. So `extract_panel()` takes a `scraper` callable: `scraper(url, schema) -> dict`.
  * In production the agent passes a thin adapter that calls the firecrawl_scrape tool.
  * For offline/CI the module ships a `cache_scraper(cache_dir)` that replays cached
    extractions (the 5 real PoC panels live in `02_products/supplements/poc_real_skus/`
    and are loadable as fixtures — same data the probe pulled live 2026-06-03).

NOTHING here is admitted to a published score. The engine reads in-house labels only;
this produces a *candidate* label that must still clear BSIP0/QA to be promoted.
"""
from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional

from .provenance import Provenance, stamp

CLIENT_VERSION = "iherb_panel/0.1 (firecrawl_scrape json + iHerb PDP)"

# The BSIP0-S extraction schema handed to firecrawl. Mirrors the fields the probe proved
# extractable; "missing -> null, never guess" is stated in the prompt AND enforced below.
PANEL_SCHEMA = {
    "type": "object",
    "properties": {
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "barcode_upc": {"type": "string"},
        "serving_size": {"type": "string"},
        "servings_per_container": {"type": "string"},
        "proprietary_blend": {"type": "boolean"},
        "primary_on_label_claim": {"type": "string"},
        "actives": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ingredient": {"type": "string"},
                    "amount": {"type": "number"},
                    "unit": {"type": "string"},
                    "form": {"type": "string"},
                },
            },
        },
    },
}
PANEL_PROMPT = (
    "Extract the Supplement Facts panel and product identity for this supplement product. "
    "For each active ingredient give ingredient name, per-serving amount, unit, and chemical "
    "form if shown. Also the brand, product name, UPC/barcode, serving size, servings per "
    "container, whether a proprietary blend is declared, and the primary on-label benefit "
    "claim. Return any field you cannot find as null. NEVER guess or fabricate a value."
)


@dataclass
class PanelActive:
    ingredient: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None
    form: Optional[str] = None
    form_from_name: bool = False  # form inferred from product NAME, not the Facts table (lossy)


@dataclass
class IherbPanel:
    """A candidate Supplement-Facts panel extracted from one iHerb PDP."""
    url: str
    brand: Optional[str] = None
    product_name: Optional[str] = None
    barcode: Optional[str] = None
    serving_size: Optional[str] = None
    servings_per_container: Optional[str] = None
    proprietary_blend: Optional[bool] = None
    primary_claim: Optional[str] = None
    actives: list[PanelActive] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    provenance: Optional[Provenance] = None
    raw: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "url": self.url,
            "brand": self.brand,
            "product_name": self.product_name,
            "barcode": self.barcode,
            "serving_size": self.serving_size,
            "servings_per_container": self.servings_per_container,
            "proprietary_blend": self.proprietary_blend,
            "primary_claim": self.primary_claim,
            "actives": [vars(a) for a in self.actives],
            "missing_fields": self.missing_fields,
            "provenance": self.provenance.as_dict() if self.provenance else None,
        }


# Which extracted fields are required-ish; absence is recorded as lossy (never filled).
_TRACKED = ["brand", "product_name", "barcode", "serving_size", "primary_claim"]


def _norm_num(v) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def _coerce(raw: dict, url: str, source_id: str | None) -> IherbPanel:
    """Map a firecrawl JSON extraction into an IherbPanel, marking lossy fields. The
    firecrawl wrapper may return the extraction under .json / .data / .extract — unwrap."""
    data = raw
    for key in ("json", "data", "extract", "llm_extraction"):
        if isinstance(data, dict) and key in data and isinstance(data[key], dict):
            data = data[key]
    p = IherbPanel(url=url, raw=raw)
    p.brand = data.get("brand") or None
    p.product_name = data.get("product_name") or None
    p.barcode = (str(data.get("barcode_upc")).strip() or None) if data.get("barcode_upc") else None
    p.serving_size = data.get("serving_size") or None
    p.servings_per_container = data.get("servings_per_container") or None
    p.proprietary_blend = data.get("proprietary_blend")
    p.primary_claim = data.get("primary_on_label_claim") or None
    for a in (data.get("actives") or []):
        if not isinstance(a, dict):
            continue
        p.actives.append(PanelActive(
            ingredient=a.get("ingredient") or None,
            amount=_norm_num(a.get("amount")),
            unit=a.get("unit") or None,
            form=a.get("form") or None,
        ))
    # lossiness pass — record, never fill.
    for f in _TRACKED:
        if getattr(p, f) in (None, ""):
            p.missing_fields.append(f)
    if not p.actives:
        p.missing_fields.append("actives (none extracted)")
    for i, a in enumerate(p.actives):
        if a.form in (None, ""):
            p.missing_fields.append(f"actives[{i}].form (not on panel)")
        if a.amount is None:
            p.missing_fields.append(f"actives[{i}].amount (hidden/blend?)")
    p.provenance = stamp(
        source="iherb.com",
        source_id=source_id or url,
        source_url=url,
        client_version=CLIENT_VERSION,
    )
    return p


def extract_panel(url: str, scraper: Callable[[str, dict], dict],
                  source_id: str | None = None) -> IherbPanel:
    """Extract a BSIP0-S panel from one iHerb PDP.

    `scraper(url, schema) -> dict` is the firecrawl_scrape(json) adapter (injected so the
    module stays SDK-free and testable). Returns an IherbPanel (candidate, provenance-
    stamped). Missing fields are recorded in `.missing_fields`, never fabricated.
    """
    raw = scraper(url, PANEL_SCHEMA)
    return _coerce(raw or {}, url, source_id)


# --------------------------------------------------------------------------- #
# Scrapers                                                                     #
# --------------------------------------------------------------------------- #
def firecrawl_tool_scraper(firecrawl_scrape_tool: Callable) -> Callable[[str, dict], dict]:
    """Adapter: wrap the agent's firecrawl_scrape tool into a scraper(url, schema) callable.

    `firecrawl_scrape_tool` must accept (url, formats, jsonOptions, ...) and return the
    tool result dict. Use in the agent runtime where the firecrawl MCP tool is available.
    """
    def _scrape(url: str, schema: dict) -> dict:
        res = firecrawl_scrape_tool(
            url=url,
            formats=["json"],
            onlyMainContent=False,
            jsonOptions={"prompt": PANEL_PROMPT, "schema": schema},
        )
        if isinstance(res, dict):
            return res
        return {"json": res}
    return _scrape


def cache_scraper(cache_dir: str | pathlib.Path) -> Callable[[str, dict], dict]:
    """A scraper that replays cached firecrawl extractions keyed by URL.

    The cache is a dir of `<slug>.json` files each holding the firecrawl extraction dict
    plus a `url`. Lets the pipeline run offline/CI against the 5 real PoC panels (same
    data the probe pulled 2026-06-03) without re-hitting iHerb. Returns {} on a miss
    (=> 'not found', honest, never a fabricated panel)."""
    cache_dir = pathlib.Path(cache_dir)
    index: dict[str, dict] = {}
    if cache_dir.exists():
        for fp in cache_dir.glob("*.json"):
            try:
                obj = json.loads(fp.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            u = obj.get("url")
            if u:
                index[u] = obj.get("extraction", obj)

    def _scrape(url: str, schema: dict) -> dict:
        return index.get(url, {})
    return _scrape


def poc_fixture_scraper() -> Callable[[str, dict], dict]:
    """A cache_scraper pre-loaded from the 5 real PoC SKU JSONs. Each PoC file holds the
    real `raw_extracted_panel` firecrawl returned on 2026-06-03; this re-shapes it into
    the firecrawl extraction schema so the pipeline can be exercised end-to-end offline."""
    poc_dir = pathlib.Path(r"C:\Bari\02_products\supplements\poc_real_skus")
    index: dict[str, dict] = {}
    for fp in poc_dir.glob("POC-*.json"):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        url = obj.get("provenance", {}).get("source_url")
        rp = obj.get("raw_extracted_panel", {})
        if not url or not rp:
            continue
        active = rp.get("active") or (rp.get("scored_active"))
        actives = []
        if active:
            actives = [{
                "ingredient": active.get("ingredient"),
                "amount": active.get("amount"),
                "unit": active.get("unit"),
                "form": active.get("form"),
            }]
        index[url] = {
            "brand": rp.get("brand"),
            "product_name": rp.get("product_name"),
            "barcode_upc": rp.get("barcode"),
            "serving_size": rp.get("serving_size"),
            "servings_per_container": rp.get("servings_per_day_label"),
            "proprietary_blend": rp.get("proprietary_blend"),
            "primary_on_label_claim": rp.get("primary_claim_on_label"),
            "actives": actives,
        }

    def _scrape(url: str, schema: dict) -> dict:
        return index.get(url, {})
    return _scrape


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = poc_fixture_scraper()
    url = ("https://www.iherb.com/pr/california-gold-nutrition-sport-pure-creatine-"
           "monohydrate-unflavored-0-18-oz-5-g/149273")
    panel = extract_panel(url, sc, source_id="iherb:149273")
    print("panel:", json.dumps(panel.as_dict(), ensure_ascii=False, indent=2))
