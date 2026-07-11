"""
TASK-602 batch-5 targeted rescrape — the blind (NO_CAPTURE) products on
cakes_hard_cookies_frontend_v1, cookies_coffee_frontend_v2, crackers_frontend_v1,
protein_combined_frontend_v2, and the juices_frontend_v3 mop-up singletons.

Scope rule (batch-5 spec): scrape ONLY products with no canonical capture in
03_operations/bsip0/manifest/capture_manifest.json. Writes to task-scoped output
dirs only. Does NOT touch the shared manifest/census (concurrency rule — batch-4
runs at the same time). Does NOT edit any served frontend JSON (barcodes are
owner-gated).

Method (mirrors 01_acquire_shufersal.py's TASK-582-fixed direct-by-barcode fetch,
plus a Shufersal-search fallback for 404s, plus reuse of Tiv Taam's v2 products API
for anything Shufersal genuinely can't resolve):

  1. Shufersal direct: GET /online/he/p/p_{barcode} — ld+json gtin must equal the
     served barcode (else page_gone/mismatch).
  2. Shufersal search fallback (barcode still unresolved): GET
     /online/he/search?q={barcode-or-name} → listing items (data-product-code) →
     fetch each candidate PDP → compare ld+json gtin against served barcode.
       - ld+json gtin == served barcode  → benign_retailer_sku (short served code
         IS the real GTIN's own listing/search key; the direct p/p_ URL 404 was a
         template/slug quirk, not a truncation).
       - ld+json gtin != served barcode but same product by name/brand → discovered
         true GTIN; served barcode is a TRUE truncation (record both).
  3. Tiv Taam v2 products API fallback (name search) for anything Shufersal can't
     resolve by either path — same engine acquire_tivtaam.py uses (Playwright,
     same-origin fetch), matching barcode via the image-URL regex.

OFF is never used (project-wide ban). Unresolved after all three passes = genuine
NOT_FOUND, recorded as such — never invented, never substituted.
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(r"C:\Bari")
sys.path.insert(0, str(ROOT / "03_operations/bsip0/scrape/_shared"))
import bsip0_nutrition as bn  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SHUFERSAL_BASE = "https://www.shufersal.co.il"
SHUFERSAL_PRODUCT_URL = SHUFERSAL_BASE + "/online/he/p/p_{barcode}"
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}
REQUEST_TIMEOUT = 25
REQUEST_DELAY_S = 0.6
BLOCK_SIGNALS = ["Maintenance1.jpg", "s3-eu-west-1.amazonaws.com/www.shufersal.co.il"]


def extract_ingredients(soup: BeautifulSoup) -> str:
    container = soup.select_one("div.componentsText")
    if container is not None:
        return container.get_text(" ", strip=True)
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        broad = parent.find_parent() if parent else None
        if broad:
            full_text = broad.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                return m.group(1).strip()
    return ""


def _parse_page(soup: BeautifulSoup, r_url: str, barcode_expected: str | None) -> dict:
    ld_gtin = ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
        except Exception:
            continue
        if isinstance(ld, dict) and ld.get("@type") == "Product":
            ld_gtin = str(ld.get("gtin13", ld.get("gtin", "")) or "")
            break
    title = soup.title.get_text(strip=True) if soup.title else ""
    product_name = title.split("|")[0].strip() if "|" in title else title

    nutr_bare = bn.parse_nutrition_list(soup)
    nutr_for_numeric = bn.bare_to_raw_keys(nutr_bare)
    nutrition = {k: v for k, v in bn.parse_nutrition_numeric(nutr_for_numeric).items()
                 if not k.startswith("_") and v is not None}
    ingredients_text = extract_ingredients(soup)
    sufficient = bool(nutrition.get("energy_kcal") or nutrition.get("fat_g") or nutrition.get("protein_g"))
    return {
        "ld_gtin": ld_gtin,
        "final_url": r_url,
        "name": product_name,
        "nutrition": nutrition,
        "nutrition_raw": nutr_for_numeric,
        "ingredients_raw_he": ingredients_text,
        "sufficient": sufficient,
    }


def fetch_shufersal_direct(barcode: str) -> dict:
    """Direct p/p_{barcode} fetch (TASK-582 verified-live pattern)."""
    url = SHUFERSAL_PRODUCT_URL.format(barcode=barcode)
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except Exception as e:
        return {"status": "scrape_failed", "reason": f"request_exception: {str(e)[:200]}"}
    if r.status_code == 404:
        return {"status": "page_gone", "reason": "http_404_on_direct_barcode_url", "final_url": r.url}
    if r.status_code != 200:
        return {"status": "scrape_failed", "reason": f"http_{r.status_code}"}
    text = r.text
    if len(text) < 5000 and any(s in text.lower() for s in ("maintenance", "אתר בתחזוקה", "בתחזוקה")):
        return {"status": "scrape_failed", "reason": "maintenance_page"}
    if any(sig in text for sig in BLOCK_SIGNALS):
        return {"status": "scrape_failed", "reason": "block_signal_detected"}
    soup = BeautifulSoup(text, "html.parser")
    parsed = _parse_page(soup, r.url, barcode)
    if not parsed["ld_gtin"]:
        return {"status": "scrape_failed", "reason": "no_ld_json_product_block", "final_url": r.url}
    if parsed["ld_gtin"] != barcode:
        return {"status": "page_gone", "reason": f"gtin_mismatch: resolved to {parsed['ld_gtin']}",
                 "final_url": r.url, "resolved_gtin": parsed["ld_gtin"]}
    return {"status": "scraped", "engine": "shufersal_direct", **parsed}


def shufersal_search_items(query: str) -> list[dict]:
    url = f"{SHUFERSAL_BASE}/online/he/search?q={requests.utils.quote(query)}&pageSize=24&currentPage=0"
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT)
    except Exception:
        return []
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    out = []
    for li in items:
        d = li.attrs
        code = (d.get("data-product-code") or "").strip()
        name = (d.get("data-product-name") or "").strip()
        if code:
            out.append({"code": code, "name": name})
    return out


def fetch_shufersal_by_code(code: str) -> dict | None:
    # `code` comes from the listing's data-product-code attribute, which ALREADY
    # carries a "P_" prefix (e.g. "P_6983787") — do not add a second one, or every
    # search-fallback candidate silently 404s (found live in this batch: cakes_hard_cookies
    # 1/7 direct hits masked a double-prefix bug that made 6/7 search-fallback candidates
    # unreachable even though the correct product was in the listing results).
    bare = re.sub(r"^p_", "", code, flags=re.IGNORECASE)
    url = f"{SHUFERSAL_BASE}/online/he/p/p_{bare.lower()}"
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except Exception:
        return None
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    parsed = _parse_page(soup, r.url, None)
    if not parsed["ld_gtin"]:
        return None
    return parsed


def _classify_barcode_relationship(barcode: str, ld_gtin: str) -> str | None:
    """Classify how a discovered ld+json gtin relates to the served barcode.

    Returns one of: "exact" (benign — identical), "synthetic_729000_plu" (benign —
    Shufersal's own in-house fresh/bakery PLU pattern: served = "729000" + a short
    internal SKU that IS the page's own gtin13/sku, common for goods with no real
    GS1 barcode), "true_truncation" (a genuinely different, unrelated GTIN for the
    same product — the served value is corrupted), or None (no relationship / not
    a barcode match at all).
    """
    if not ld_gtin:
        return None
    if ld_gtin == barcode:
        return "exact"
    # Shufersal in-house PLU convention: served 13-digit value is "729000" + a
    # short (5-8 digit) internal code, and that short code IS the page's own
    # gtin13/sku (not a separate, longer, "real" barcode).
    if (barcode.startswith("729000") and len(ld_gtin) in range(5, 9)
            and barcode.endswith(ld_gtin)):
        return "synthetic_729000_plu"
    # served value is a short truncation and the discovered gtin is a longer,
    # unrelated-prefix true GTIN that merely ends in the served digits (the
    # batch-2 yogurt-drinkable pattern).
    if len(barcode) < len(ld_gtin) and ld_gtin.endswith(barcode):
        return "true_truncation"
    return None


def shufersal_search_fallback(barcode: str, name_he: str) -> dict:
    """Search Shufersal by barcode text, then by a shortened product name.

    SAFETY (found live in this batch): an earlier version of this function accepted
    the FIRST candidate whose name loosely shared a 12-character prefix with the
    target name, and returned immediately — for a near-duplicate bakery shelf
    (many "עוגת הבית <flavor>" / "עוגות אישיות <flavor>" SKUs) this matched the
    WRONG product (different flavor, different barcode entirely, e.g. served
    7290006983787 "עוגת הבית שוקולד צ'יפס" got matched to gtin 7290106574793
    "עוגת הבית שוקו שוקוצ'יפס" — a different SKU under a different GS1 prefix)
    before ever reaching the correct candidate later in the list. Per the
    product-names-are-verbatim-strings rule, a fuzzy name match is NEVER accepted
    as identity proof. This function now: (1) collects ALL candidates from BOTH
    queries first, (2) accepts a candidate ONLY on a deterministic barcode
    relationship (exact gtin equality, or the synthetic_729000_plu suffix
    pattern, or a true numeric-suffix truncation) — never on name similarity alone,
    (3) any candidate that matches only by loose name is returned separately as an
    unverified "review_candidate", not as a resolved match.
    """
    tried_codes: set[str] = set()
    candidates: list[dict] = []
    for query in (barcode, name_he.split(" ")[0] + " " + name_he.split(" ")[1] if len(name_he.split(" ")) > 1 else name_he):
        items = shufersal_search_items(query)
        for item in items[:8]:
            code = item["code"]
            if code in tried_codes:
                continue
            tried_codes.add(code)
            parsed = fetch_shufersal_by_code(code)
            time.sleep(REQUEST_DELAY_S)
            if not parsed:
                continue
            candidates.append({"code": code, "listing_name": item["name"], "parsed": parsed})
        if items:
            time.sleep(REQUEST_DELAY_S)

    review_candidates = []
    for cand in candidates:
        parsed = cand["parsed"]
        rel = _classify_barcode_relationship(barcode, parsed["ld_gtin"])
        if rel in ("exact", "synthetic_729000_plu"):
            return {"status": "scraped", "engine": "shufersal_search_benign_sku",
                     "barcode_relationship": rel, "matched_via_code": cand["code"],
                     "discovered_gtin": parsed["ld_gtin"], **parsed}
        if rel == "true_truncation":
            return {"status": "scraped", "engine": "shufersal_search_true_truncation",
                     "barcode_relationship": rel, "matched_via_code": cand["code"],
                     "served_barcode": barcode, "discovered_gtin": parsed["ld_gtin"], **parsed}
        if name_he[:12] and name_he[:12] in parsed["name"]:
            review_candidates.append({"code": cand["code"], "name": parsed["name"],
                                        "gtin": parsed["ld_gtin"]})

    return {"status": "not_found_shufersal", "reason": "no_deterministic_barcode_match",
            "candidates_checked": len(tried_codes),
            "review_candidates_NOT_RETAINED": review_candidates}


# ---------------------------------------------------------------------------
# Tiv Taam fallback (Playwright, v2 products API) — only invoked for barcodes
# Shufersal could not resolve at all.
# ---------------------------------------------------------------------------

def tivtaam_fallback(barcode: str, name_he: str, page) -> dict:
    sys.path.insert(0, str(ROOT / "03_operations/bsip0/scrape/tiv_taam"))
    import acquire_tivtaam as tt  # noqa: E402
    query = name_he.split(" ")[0]
    try:
        records = tt.discover_and_scrape(page, query, max_products=20, page_size=20)
    except Exception as e:
        return {"status": "scrape_failed", "reason": f"tivtaam_exception: {str(e)[:200]}"}
    for rec in records:
        if rec.get("barcode") == barcode:
            return {"status": "scraped", "engine": "tivtaam", **rec}
    return {"status": "not_found_tivtaam", "candidates_checked": len(records)}


# ---------------------------------------------------------------------------
# Shelf configs
# ---------------------------------------------------------------------------

SHELVES = {
    "cakes_hard_cookies_frontend_v1": {
        "frontend_file": "cakes_hard_cookies_frontend_v1.json",
        "out_dir": ROOT / "02_products/cakes_hard_cookies/bsip0_outputs/task602_cakes_hard_cookies_rescrape_20260711",
    },
    "cookies_coffee_frontend_v2": {
        "frontend_file": "cookies_coffee_frontend_v2.json",
        "out_dir": ROOT / "02_products/cookies_coffee/bsip0_outputs/task602_cookies_coffee_rescrape_20260711",
    },
    "crackers_frontend_v1": {
        "frontend_file": "crackers_frontend_v1.json",
        "out_dir": ROOT / "02_products/crackers/bsip0_outputs/task602_crackers_rescrape_20260711",
    },
    "protein_combined_frontend_v2": {
        "frontend_file": "protein_combined_frontend_v2.json",
        "out_dir": ROOT / "02_products/snack_bars/bsip0_outputs/task602_protein_combined_rescrape_20260711",
    },
    "juices_frontend_v3": {
        "frontend_file": "juices_frontend_v3.json",
        "out_dir": ROOT / "02_products/juices/bsip0_outputs/task602_juices_batch5_mopup_20260711",
    },
}

FRONT_DIR = ROOT / "bari-web/src/data/comparisons"
MANIFEST = ROOT / "03_operations/bsip0/manifest/capture_manifest.json"


def gtin(p: dict) -> str | None:
    for k in ("gtin", "barcode", "ean", "upc", "product_code", "product_id"):
        if p.get(k) is not None:
            return str(p[k])
    return None


def load_blind_products(shelf: str) -> list[dict]:
    records = json.loads(MANIFEST.read_text(encoding="utf-8"))["records"]
    canon = {str(x["gtin"]) for x in records if x["canonical"] and x["gtin"]}
    f = FRONT_DIR / SHELVES[shelf]["frontend_file"]
    data = json.loads(f.read_text(encoding="utf-8"))
    products = data.get("products", data if isinstance(data, list) else [])
    blind = []
    for p in products:
        g = gtin(p)
        if g not in canon:
            # Served nutrition lives under expansion.nutrition (energyKcal, fat,
            # satFat, carbs, sugar, protein, sodium, fiber) — NOT top-level.
            served_nutr = ((p.get("expansion") or {}).get("nutrition")) or p.get("nutrition") or {}
            blind.append({
                "barcode": g,
                "name": p.get("name") or p.get("product_name") or p.get("title") or "",
                "brand": p.get("brand", ""),
                "served_fat": served_nutr.get("fat"),
                "served_nutrition": served_nutr,
            })
    return blind


def run_shelf(shelf: str, use_tivtaam_fallback: bool = True) -> dict:
    cfg = SHELVES[shelf]
    cfg["out_dir"].mkdir(parents=True, exist_ok=True)
    blind = load_blind_products(shelf)
    results = []
    print(f"\n=== {shelf}: {len(blind)} blind products ===", flush=True)

    tt_page = None
    tt_browser = None
    tt_pw = None

    for i, prod in enumerate(blind, 1):
        barcode = prod["barcode"]
        name = prod["name"]
        print(f"  [{i}/{len(blind)}] {barcode} {name[:40]}", flush=True)
        rec = {"barcode": barcode, "name": name, "brand": prod["brand"],
               "served_nutrition": prod["served_nutrition"]}

        if not barcode:
            rec["result"] = {"status": "no_barcode"}
            results.append(rec)
            continue

        r1 = fetch_shufersal_direct(barcode)
        time.sleep(REQUEST_DELAY_S)
        if r1["status"] == "scraped":
            rec["result"] = r1
            rec["barcode_class"] = "benign_retailer_sku"
            results.append(rec)
            print(f"      OK direct shufersal ({'panel' if r1['sufficient'] else 'no_panel'})", flush=True)
            continue

        r2 = shufersal_search_fallback(barcode, name)
        if r2["status"] == "scraped":
            rec["result"] = r2
            rec["barcode_class"] = ("benign_retailer_sku" if r2["engine"] == "shufersal_search_benign_sku"
                                     else "true_truncation")
            results.append(rec)
            print(f"      OK shufersal search ({r2['engine']})", flush=True)
            continue

        if use_tivtaam_fallback:
            if tt_page is None:
                try:
                    from playwright.sync_api import sync_playwright
                    tt_pw = sync_playwright().start()
                    tt_browser = tt_pw.chromium.launch(headless=True)
                    ctx = tt_browser.new_context(viewport={"width": 1500, "height": 1000},
                                                  locale="he-IL", timezone_id="Asia/Jerusalem")
                    tt_page = ctx.new_page()
                    tt_page.goto("https://www.tivtaam.co.il/", wait_until="domcontentloaded", timeout=30000)
                    tt_page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"      tivtaam init failed: {e}", flush=True)
                    tt_page = False
            if tt_page:
                r3 = tivtaam_fallback(barcode, name, tt_page)
            else:
                r3 = {"status": "scrape_failed", "reason": "tivtaam_unavailable"}
            if r3["status"] == "scraped":
                rec["result"] = r3
                rec["barcode_class"] = "benign_retailer_sku"
                results.append(rec)
                print(f"      OK tivtaam", flush=True)
                continue
            rec["result"] = {"status": "NOT_FOUND", "shufersal_direct": r1,
                              "shufersal_search": r2, "tivtaam": r3}
        else:
            rec["result"] = {"status": "NOT_FOUND", "shufersal_direct": r1, "shufersal_search": r2}
        results.append(rec)
        print(f"      NOT_FOUND (all engines exhausted)", flush=True)

    if tt_browser:
        tt_browser.close()
    if tt_pw:
        tt_pw.stop()

    out_path = cfg["out_dir"] / f"{shelf}_rescrape_results.json"
    out_data = {
        "shelf": shelf,
        "run_id": f"task602_batch5_{shelf}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_blind": len(blind),
        "results": results,
    }
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Wrote: {out_path}")
    return out_data


if __name__ == "__main__":
    shelves_to_run = sys.argv[1:] or list(SHELVES.keys())
    for shelf in shelves_to_run:
        run_shelf(shelf)
