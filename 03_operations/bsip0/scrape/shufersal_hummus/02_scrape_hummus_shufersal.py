"""
Shufersal BSIP0 scraper — Hummus and Savory Dips.

Reads approved candidates from candidate_review.csv and scrapes
each product page for name, nutritional panel, ingredients, and image.

Usage:
    cd C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal_hummus
    python 02_scrape_hummus_shufersal.py

Prerequisites:
    01_discover_hummus_shufersal.py has run.
    candidate_review.csv exists.
    approved_for_scrape is set to YES for desired products.

Output:
    C:\\Bari\\02_products\\hummus\\observations_bsip0\\shufersal\\{code}.json
    One JSON per approved product.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import datetime
import pathlib
import time

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = pathlib.Path(__file__).resolve().parent
REVIEW_CSV = pathlib.Path(r"C:\Bari\02_products\hummus\observations_bsip0\shufersal\candidate_review.csv")
OUT_DIR    = pathlib.Path(r"C:\Bari\02_products\hummus\observations_bsip0\shufersal")

BASE = "https://www.shufersal.co.il"
PRODUCT_PAGE_DELAY = 0.8
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}

# Shared BSIP0 nutrition parser (TASK-142A / EV-026 fix). Replaces the former
# NUTR_LABEL_MAP, whose substring map let trans/saturated "of which" sub-rows
# overwrite total fat (fat→0.5). This is the exact defect TASK-039 audited in
# hummus (59/69 products) but never fixed at the shared scraper path.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, nutrition_implausible  # noqa: E402

_WEIGHT_PATTERNS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*מ[\"']?ל", re.IGNORECASE),
]


def _extract_weight_g(name: str) -> float | None:
    for pat in _WEIGHT_PATTERNS:
        m = pat.search(name)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    val *= 1000
                if 10 < val < 5000:
                    return val
            except ValueError:
                pass
    return None


def _price_per_100g(price_str: str, weight_g: float | None) -> float | None:
    if not price_str or not weight_g:
        return None
    try:
        return round(float(price_str.replace(",", ".")) * 100 / weight_g, 2)
    except (ValueError, ZeroDivisionError):
        return None


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def scrape_product_page(code: str, meta: dict) -> dict | None:
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url, timeout=25)
    if not r or r.status_code != 200:
        print(f"  [SKIP] {code}: HTTP {r.status_code if r else 'error'}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    product_url = r.url

    # LD+JSON extraction
    ld_name, ld_sku, ld_gtin, ld_images = "", "", "", []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name  = ld.get("name", "")
                ld_sku   = ld.get("sku", "")
                ld_gtin  = ld.get("gtin13", ld.get("gtin", ""))
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    # Nutrition panel
    # Shared parser (TASK-142A / EV-026): reads TOTAL fat, captures saturated
    # separately, never lets an "of which" sub-row overwrite a total macro.
    nutr_raw = parse_nutrition_list(soup)
    # Persist raw nutrition source (rows + outer HTML) so any FUTURE parser fix
    # replays offline — an EV-029-class bug never again forces a network re-scrape.
    nutr_src = extract_nutrition_raw(soup)

    # Ingredients
    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"רכיב"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:800]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:800]
                break

    name = ld_name or meta.get("name", "")
    barcode = ld_gtin or ld_sku or code.replace("P_", "")
    weight_g = meta.get("weight_g") or _extract_weight_g(name)

    return {
        "retailer_id":   "shufersal",
        "retailer_name": "שופרסל",
        "source_url":    product_url,
        "scraped_at":    datetime.datetime.utcnow().isoformat(),
        "name_he":       name,
        "name_en":       "",
        "brand":         "",
        "barcode":       barcode,
        "category_raw":  meta.get("categories", ""),
        "source_category": meta.get("source_category", ""),
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""),
            "protein_raw":     nutr_raw.get("protein", ""),
            "carbs_raw":       nutr_raw.get("carbs", ""),
            "fat_raw":         nutr_raw.get("fat", ""),
            "fiber_raw":       nutr_raw.get("fiber", ""),
            "sodium_raw":      nutr_raw.get("sodium", ""),
            "sugar_raw":       nutr_raw.get("sugar", ""),
        },
        "nutrition_raw_source":  nutr_src,
        "ingredients_raw":       ingredients_raw,
        "ingredients_language":  "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else "",
        "image_urls":            [u for u in ld_images[:3] if u],
        "extraction_method":     "html_parse",
        "extraction_confidence": "high" if nutr_raw else "medium",
        "price":                 meta.get("price", ""),
        "weight_g":              weight_g,
        "price_per_100g":        _price_per_100g(meta.get("price", ""), weight_g),
    }


def load_approved_candidates() -> list[dict]:
    if not REVIEW_CSV.exists():
        print(f"ERROR: candidate_review.csv not found at {REVIEW_CSV}")
        print("Run 01_discover_hummus_shufersal.py first.")
        sys.exit(1)

    approved = []
    with REVIEW_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("approved_for_scrape", "").strip().upper() == "YES":
                approved.append(dict(row))
    print(f"Approved candidates: {len(approved)}")
    return approved


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    candidates = load_approved_candidates()

    if not candidates:
        print("No approved candidates found. Set approved_for_scrape = YES in candidate_review.csv")
        sys.exit(1)

    success, failed = 0, 0
    for i, candidate in enumerate(candidates, 1):
        code = candidate.get("code", "").strip()
        name = candidate.get("name", "").strip()
        if not code:
            print(f"  [{i}/{len(candidates)}] SKIP: no code for '{name}'")
            continue

        print(f"  [{i}/{len(candidates)}] Scraping {code}: {name[:50]}")
        product = scrape_product_page(code, candidate)

        if product:
            out_path = OUT_DIR / f"{code}.json"
            out_path.write_text(json.dumps(product, ensure_ascii=False, indent=2), encoding="utf-8")
            has_nutr = bool(product["nutrition"].get("energy_kcal_raw"))
            has_ingr = bool(product["ingredients_raw"])
            print(f"    → nutrition={'OK' if has_nutr else 'MISSING'} ingredients={'OK' if has_ingr else 'MISSING'}")
            success += 1
        else:
            failed += 1

        time.sleep(PRODUCT_PAGE_DELAY)

    print(f"\n{'='*40}")
    print(f"Scraping complete")
    print(f"  Scraped : {success}")
    print(f"  Failed  : {failed}")
    print(f"  Total   : {len(candidates)}")
    print(f"\nNext: run python 03_audit_bsip0_hummus.py")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()
