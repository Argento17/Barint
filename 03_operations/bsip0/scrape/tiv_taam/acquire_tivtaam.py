"""
BSIP0 Tiv Taam (טיב טעם) — generic, reusable acquisition engine. TASK-518.

Discovered under TASK-518 as a NEW BSIP0-ready retailer. Runs the SAME
`/v2/retailers/<rid>/branches/<bid>/products` JSON search API previously seen
(nutrition-blind) in `multiretailer_olive_oil/01_scrape_carrefour_victory.py` for
Victory/Carrefour -- but on Tiv Taam's OWN domain (www.tivtaam.co.il, retailer_id
1062, branch_id 924, confirmed live via XHR capture in
_smoke_probes/diag_tivtaam_interact.py) this API is NOT behind the "self-point.com"
Cloudflare WAF that hard-blocked Victory/Carrefour mid-TASK-518 ("Sorry, you have
been blocked" -- see module docstring in yohananof/acquire_yohananof.py's sibling
diagnosis notes and the TASK-518 return). Tiv Taam's copy of this API is also
RICHER than what the olive-oil script used: it returns a full per-100g
`nutritionValues` table INLINE on every search result row (not just
`data.<n>.ingredients`) -- no second per-product request needed at all.

API: GET https://www.tivtaam.co.il/v2/retailers/1062/branches/924/products
     ?appId=4&filters=<json>&from=<offset>&isSearch=true&languageId=1&query=<he>&size=<n>
Called via `fetch()` executed inside a Playwright page (same-origin, inherits
whatever cookies the initial page load set; plain `requests` was not attempted
here since the browser-fetch path already works cleanly and cheaply).

Per-product fields used:
  - `image.url` -- cloudfront CDN path `gs1-products/<retailer>/.../<EAN13>-<id>/...`
    -- same barcode-in-path pattern as Victory; barcode extracted via regex, no
    separate identity lookup needed.
  - `data.1.ingredients` -- ingredients text.
  - `nutritionValues.values[]` -- each row: `{names: {"1": "<Hebrew label>"},
    sizeValues: [{value, unitOfMeasure: {names: {"1": "<unit>"}}}]}`, all already
    per-100g (single `sizes` entry observed = "ל-100 גרם" on every sampled row).
    Classified via the SAME Hebrew-label logic as every other retailer
    (`_shared/bsip0_nutrition.py::classify_nutr_label`) -- no bespoke per-field
    parsing.
  - `family.categoriesPaths` -- full category breadcrumb (useful for future
    category-scope work, not required for BSIP0-readiness).

No fallback: a product with no `nutritionValues.values` or unmatched barcode
regex stays NULL -- OFF is banned project-wide.

Output: <caller-set OUT_DIR>/tivtaam_bsip0_raw_<ts>.json
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import classify_nutr_label  # noqa: E402

RETAILER_ID = "tiv_taam"
RETAILER_NAME = "טיב טעם"
HOST = "www.tivtaam.co.il"
API_RETAILER_ID = 1062
API_BRANCH_ID = 924

BASE_FILTERS = json.dumps({
    "must": {
        "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
        "term": {"branch.isActive": True, "branch.isVisible": True},
    },
    "mustNot": {"term": {"branch.regularPrice": 0}},
})

_BARCODE_RE = re.compile(r"/gs1-products/\d+/[^/]+/(\d{8,14})-")


def _api_fetch(page, url: str) -> dict | None:
    result = page.evaluate(
        """
        async (url) => {
            try {
                const res = await fetch(url, {headers: {'Accept': 'application/json'}});
                return {status: res.status, text: await res.text()};
            } catch (e) { return {error: String(e)}; }
        }
        """,
        url,
    )
    if result.get("error") or result.get("status") != 200:
        return None
    try:
        return json.loads(result["text"])
    except Exception:
        return None


def _extract_barcode(product: dict) -> str:
    img_url = ((product.get("image") or {}).get("url") or "")
    m = _BARCODE_RE.search(img_url)
    return m.group(1) if m else ""


def _extract_ingredients(product: dict) -> str:
    inner = ((product.get("data") or {}).get("1") or {})
    return (inner.get("ingredients") or "").strip()


def _extract_nutrition(product: dict) -> dict:
    nv = product.get("nutritionValues") or {}
    bare: dict[str, str] = {}
    for row in nv.get("values") or []:
        label = (row.get("names") or {}).get("1", "")
        field = classify_nutr_label(label)
        if not field or field in bare:
            continue
        size_values = row.get("sizeValues") or []
        if not size_values:
            continue
        val = size_values[0].get("value")
        if val is None:
            continue
        bare[field] = str(val)
    return {
        "energy_kcal_raw": bare.get("energy", ""),
        "protein_raw": bare.get("protein", ""),
        "carbs_raw": bare.get("carbs", ""),
        "fat_raw": bare.get("fat", ""),
        "fiber_raw": bare.get("fiber", ""),
        "sodium_raw": bare.get("sodium", ""),
        "sugar_raw": bare.get("sugar", ""),
        "saturated_fat_raw": bare.get("saturated_fat", ""),
    }


def discover_and_scrape(page, query: str, max_products: int = 30, page_size: int = 20) -> list[dict]:
    """One API is BOTH discovery and panel -- no separate per-product fetch needed."""
    records: list[dict] = []
    offset = 0
    total = None
    while len(records) < max_products:
        params = urllib.parse.urlencode({
            "appId": "4", "filters": BASE_FILTERS, "from": str(offset),
            "isSearch": "true", "languageId": "1", "query": query, "size": str(page_size),
        })
        api_url = f"https://{HOST}/v2/retailers/{API_RETAILER_ID}/branches/{API_BRANCH_ID}/products?{params}"
        data = _api_fetch(page, api_url)
        if not data:
            break
        total = data.get("total", total)
        products = data.get("products") or []
        if not products:
            break
        for p in products:
            barcode = _extract_barcode(p)
            name = p.get("localName") or ((p.get("names") or {}).get("1") or {}).get("long", "")
            ingredients_raw = _extract_ingredients(p)
            nutrition = _extract_nutrition(p)
            status = "scraped" if (barcode and (ingredients_raw or any(nutrition.values()))) else (
                "no_barcode" if not barcode else "empty_panel"
            )
            records.append({
                "retailer_id": RETAILER_ID,
                "retailer_name": RETAILER_NAME,
                "barcode": barcode,
                "name_he": name,
                "status": status,
                "nutrition": nutrition,
                "ingredients_raw": ingredients_raw,
                "category_path": [c.get("names", {}).get("1", "") for c in
                                   ((p.get("family") or {}).get("categories") or [])],
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                "provenance": {
                    "identity_source": "tivtaam_v2_products_api",
                    "nutrition_source": "tivtaam_v2_products_api" if any(nutrition.values()) else None,
                    "ingredients_source": "tivtaam_v2_products_api" if ingredients_raw else None,
                },
            })
            if len(records) >= max_products:
                break
        offset += page_size
        if total is not None and offset >= total:
            break
    return records


def acquire(query: str, category: str, out_dir: Path, max_products: int = 30, headless: bool = True) -> tuple[list[dict], Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000}, locale="he-IL",
            timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()
        page.goto(f"https://{HOST}/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        records = discover_and_scrape(page, query, max_products=max_products)
        context.close()
        browser.close()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = out_dir / f"tivtaam_bsip0_raw_{ts}.json"
    scraped_ok = [r for r in records if r.get("status") == "scraped"]
    out_data = {
        "schema_version": "bsip0_v1",
        "retailer_id": RETAILER_ID,
        "retailer_name": RETAILER_NAME,
        "category": category,
        "query": query,
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "candidates_total": len(records),
        "scraped_ok": len(scraped_ok),
        "empty_panel": sum(1 for r in records if r.get("status") == "empty_panel"),
        "no_barcode": sum(1 for r in records if r.get("status") == "no_barcode"),
        "products": records,
    }
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Wrote: {out_path}")
    return records, out_path
