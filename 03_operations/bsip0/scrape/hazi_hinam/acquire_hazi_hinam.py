"""
BSIP0 Hazi Hinam (חצי חינם) — generic, reusable acquisition engine. TASK-518.

Discovered under TASK-518 as a NEW BSIP0-ready retailer (not previously scraped
for nutrition/ingredients -- only a half-finished DOM exploration existed at
hazi_hinam/test_hazi_hinam_explore.py, which found product cards but never
cracked the per-product detail view).

Platform: Angular SPA on shop.hazi-hinam.co.il, own CDN, NO Cloudflare/WAF (this
matters -- Victory/Carrefour/Yohananof all sit behind a shared "self-point.com"
security service that hard-blocked this session mid-TASK-518; Hazi Hinam is a
completely separate platform and was unaffected).

THE KEY FINDING: this retailer exposes clean, fully-structured JSON REST APIs
(reachable via `fetch()` executed inside a Playwright page after just loading the
homepage -- no login, no special cookies) instead of requiring DOM/modal scraping:

  1. Category tree + subcategories:
     GET /proxy/api/Item/GetItemsByCategory/?Id=<category_id>
     -> {Results: {SubCategories: [{Id, Name, Items: [...5-item preview...]}]}}
     Use this ONCE to map a category (e.g. 78 = dairy/eggs) to its subcategory ids.

  2. Full item list for one subcategory (the discovery step):
     GET /proxy/api/item/getItemsBySubCategory?Id=<subcategory_id>&IsDescending=false&SortBy=-1
     -> {Results: {Category: {SubCategory: {Id, Name, Items: [...ALL items...]}}}}
     Each item already carries Id, BarKod (EAN barcode), Name, brand, price -- a
     complete, non-virtualized, non-paginated identity list. Confirmed: subcategory
     10868 ("חמאה ומרגרינה" / butter+margarine) returned all 28 items in ONE call.

  3. Per-item nutrition + ingredients + allergens (the panel step):
     GET /proxy/api/item/GetItemGS1Details/<item_id>
     -> {Results: {IngredientSequenceandName, TypeCodes: [...allergens/kosher/diet
        info...], NutritionalValues_For100Gr: [{NutritionalCode, NutritionalValue,
        NutritionalValueDescription, Quantity, UnitType, MidaValue}, ...]}}
     Already per-100g (MidaValue == "ל-100 גרם" observed on every row so far).
     Field classification reuses the SAME Hebrew-label logic as the shared parser
     (`_shared/bsip0_nutrition.py::classify_nutr_label`) rather than hardcoding
     NutritionalCode integers (which are not guaranteed stable across products) --
     `NutritionalValueDescription` is plain Hebrew text ("אנרגיה", "חלבונים",
     "שומנים", ...) and classifies identically to Shufersal/Victory/Yohananof rows.

No fallback: a product with no GS1Details (IsAdditionalGS1Details == False, or
NutritionalValues_For100Gr empty) stays NULL -- OFF is banned project-wide.

Output: <caller-set OUT_DIR>/hazi_hinam_bsip0_raw_<ts>.json
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import classify_nutr_label  # noqa: E402

RETAILER_ID = "hazi_hinam"
RETAILER_NAME = "חצי חינם"
BASE_URL = "https://shop.hazi-hinam.co.il"


def _api_fetch(page, url: str) -> dict | None:
    result = page.evaluate(
        """
        async (url) => {
            try {
                const res = await fetch(url, {headers: {'Accept': 'application/json'}});
                return {status: res.status, text: await res.text()};
            } catch (e) {
                return {error: String(e)};
            }
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


def get_subcategories(page, category_id: int) -> list[dict]:
    """Return [{id, name}] subcategories under a top-level category id."""
    data = _api_fetch(page, f"{BASE_URL}/proxy/api/Item/GetItemsByCategory/?Id={category_id}")
    if not data or not data.get("IsOK"):
        return []
    subs = (data.get("Results") or {}).get("SubCategories") or []
    return [{"id": s.get("Id"), "name": s.get("Name")} for s in subs if s.get("Id")]


def discover_items_in_subcategory(page, subcategory_id: int) -> list[dict]:
    """Full item list for one subcategory -- NOT paginated/virtualized, one call."""
    url = f"{BASE_URL}/proxy/api/item/getItemsBySubCategory?Id={subcategory_id}&IsDescending=false&SortBy=-1"
    data = _api_fetch(page, url)
    if not data or not data.get("IsOK"):
        return []
    sc = ((data.get("Results") or {}).get("Category") or {}).get("SubCategory") or {}
    items = sc.get("Items") or []
    return [
        {"id": it.get("Id"), "barcode": str(it.get("BarKod") or ""), "name": it.get("Name") or ""}
        for it in items
        if it.get("Id")
    ]


_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _clean_quantity(raw: str) -> str:
    """Strip the 'L ' (less-than) marker this retailer's GS1 feed uses (e.g.
    'L 0.5' for trans fat) down to a bare numeric string; the shared parser's
    downstream parse_num just needs the digits."""
    if not raw:
        return raw
    m = _NUM_RE.search(str(raw).replace(",", "."))
    return m.group(1) if m else raw


def scrape_item_panel(page, item_id, barcode: str, name: str) -> dict:
    url = f"{BASE_URL}/proxy/api/item/GetItemGS1Details/{item_id}"
    data = _api_fetch(page, url)
    if not data or not data.get("IsOK"):
        return {"barcode": barcode, "name_he": name, "status": "not_found", "source_url": url}

    results = data.get("Results") or {}
    ingredients_raw = (results.get("IngredientSequenceandName") or "").strip()
    nutr_rows = results.get("NutritionalValues_For100Gr") or []

    bare: dict[str, str] = {}
    for row in nutr_rows:
        label = row.get("NutritionalValueDescription") or row.get("NutritionalValue") or ""
        field = classify_nutr_label(label)
        if field and field not in bare:
            bare[field] = _clean_quantity(row.get("Quantity"))

    nutrition = {
        "energy_kcal_raw": bare.get("energy", ""),
        "protein_raw": bare.get("protein", ""),
        "carbs_raw": bare.get("carbs", ""),
        "fat_raw": bare.get("fat", ""),
        "fiber_raw": bare.get("fiber", ""),
        "sodium_raw": bare.get("sodium", ""),
        "sugar_raw": bare.get("sugar", ""),
        "saturated_fat_raw": bare.get("saturated_fat", ""),
    }
    status = "scraped" if (ingredients_raw or any(nutrition.values())) else "empty_panel"
    return {
        "retailer_id": RETAILER_ID,
        "retailer_name": RETAILER_NAME,
        "barcode": barcode,
        "name_he": name,
        "status": status,
        "nutrition": nutrition,
        "nutrition_raw_source": {"rows": nutr_rows},
        "ingredients_raw": ingredients_raw,
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "provenance": {
            "identity_source": "hazi_hinam_subcategory_api",
            "nutrition_source": "hazi_hinam_gs1_api" if nutr_rows else None,
            "ingredients_source": "hazi_hinam_gs1_api" if ingredients_raw else None,
        },
    }


def acquire(subcategory_id: int, category: str, out_dir: Path, max_products: int = 30, headless: bool = True) -> tuple[list[dict], Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    run_report: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000},
            locale="he-IL",
            timezone_id="Asia/Jerusalem",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()
        page.goto(BASE_URL + "/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        candidates = discover_items_in_subcategory(page, subcategory_id)[:max_products]
        print(f"  [hazi_hinam] discovered {len(candidates)} candidates in subcategory {subcategory_id}")

        for i, cand in enumerate(candidates, 1):
            print(f"  [{i}/{len(candidates)}] scraping {cand['barcode']} | {cand['name'][:50]}")
            try:
                rec = scrape_item_panel(page, cand["id"], cand["barcode"], cand["name"])
            except Exception as e:
                rec = {"barcode": cand["barcode"], "name_he": cand["name"], "status": "failed", "error": str(e)[:300]}
            run_report.append(rec)

        context.close()
        browser.close()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = out_dir / f"hazi_hinam_bsip0_raw_{ts}.json"
    scraped_ok = [r for r in run_report if r.get("status") == "scraped"]
    out_data = {
        "schema_version": "bsip0_v1",
        "retailer_id": RETAILER_ID,
        "retailer_name": RETAILER_NAME,
        "category": category,
        "subcategory_id": subcategory_id,
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "candidates_total": len(candidates),
        "scraped_ok": len(scraped_ok),
        "empty_panel": sum(1 for r in run_report if r.get("status") == "empty_panel"),
        "not_found": sum(1 for r in run_report if r.get("status") == "not_found"),
        "failed": sum(1 for r in run_report if r.get("status") == "failed"),
        "products": run_report,
    }
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Wrote: {out_path}")
    return run_report, out_path
