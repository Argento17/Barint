"""
TASK-516 — Targeted live re-scrape to recover the retailer's structured
`brand` field for the 21 crackers candidate barcodes.

WHY this exists (root-cause finding, not a name-text mining exercise):
  build_crackers_bsip1.py sources from the OLD bread-family BSIP0 raw file
  (real_bread_retail_003_v1, scraped 2026-05-25 by 03_operations/bsip0/scrape/
  shufersal/01_acquire_shufersal.py). A census of `brand` field fill-rate
  across every BSIP0 raw file in the repo shows that scraper NEVER populated
  `brand` (0/110 bread_retail_002, 0/258 bread_retail_003), while every
  scraper written after it (shufersal_cereals, shufersal_cheese,
  shufersal_chocolate, shufersal_cookies_coffee, shufersal_snack_bars —
  see 03_operations/bsip0/scrape/shufersal_cookies_coffee/01_scrape_cookies_coffee.py
  line ~283-296) reads `brand` out of the product page's schema.org
  `application/ld+json` Product block and gets 100% fill. This is a SCRAPER
  COVERAGE GAP on the May bread scrape, not a genuine absence of brand data
  on the retailer page.

  Expanding brand_extractor.py's name-text token list cannot recover this —
  the actual manufacturer strings (e.g. "קופסת העוגיות של רחלי", "פיטנס",
  "הדר", "ARDO", "ריץ", "אביב אורגניק") do NOT appear as substrings in the
  scraped canonical_name_he for most of these products. The correct,
  never-invent-compliant fix is to re-fetch the SAME live retailer pages with
  the modern ld+json-aware parser and read the retailer's own structured
  brand field directly -- literal, retailer-attested, higher-confidence than
  a name-substring match.

OFF ban: N/A — this fetch reads shufersal.co.il product pages only, the
exact same domain/method already used by every category's scraper. No OFF
usage, no other external source.

Output:
  - Raw HTML banked to 03_operations/bsip0/raw_store/shufersal/crackers/<barcode>/<ts>.html
    (manifest.jsonl in the same dir tree) — evidence trail per repo convention.
  - 03_operations/bsip1/run_crackers_conform_001/brand_patch_v1.json — barcode ->
    {brand_field, source_url, fetched_at, content_sha256, http_status} for every
    barcode where the ld+json Product block yielded a non-empty brand.name.
"""
from __future__ import annotations

import json
import pathlib
import sys
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\raw_store")))
from store import store_page  # noqa: E402

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
}

# The 21 candidates named in the Crackers Category Constitution v1 / TASK-433
# inclusion list (same set build_crackers_bsip1.py draws from), so the patch
# covers every barcode the builder might consult, including the 2 that are
# discarded downstream (5317200 blackout, 7290112968807 corrupted-nutrition) —
# harmless to also patch their brand for completeness/audit symmetry.
BARCODES = [
    "7290013740809", "74252", "7290115205176", "7290018790328",
    "7290011489595", "7296073659952", "7296073134442", "7290112963918",
    "74375", "7290112968807", "5317200", "7296073398875", "5000396021202",
    "8434165658523", "7290013740823", "7290112968821", "7296073134459",
    "7290013740083", "7296073659945", "96086000577", "96086000966",
]

RETAILER = "shufersal"
CATEGORY = "crackers"


def fetch_one(barcode: str) -> dict:
    url = f"https://www.shufersal.co.il/online/he/p/p_{barcode}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
    except Exception as exc:
        return {"barcode": barcode, "error": str(exc)}

    entry = store_page(
        content=r.content,
        retailer=RETAILER,
        category=CATEGORY,
        page_id=barcode,
        url=r.url,
        barcode_hint=barcode,
        http_status=r.status_code,
        fetch_engine="requests",
    )

    if r.status_code != 200:
        return {"barcode": barcode, "http_status": r.status_code, "error": "non-200"}

    soup = BeautifulSoup(r.text, "html.parser")
    brand_name = ""
    ld_name = ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
        except Exception:
            continue
        if ld.get("@type") == "Product":
            ld_name = ld.get("name", "")
            brand = ld.get("brand", "")
            brand_name = brand.get("name", "") if isinstance(brand, dict) else (brand or "")
            break

    return {
        "barcode": barcode,
        "http_status": r.status_code,
        "name_he_confirm": ld_name,
        "brand_field": brand_name.strip(),
        "source_url": r.url,
        "content_sha256": entry["content_sha256"],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "method": "live_targeted_rescrape_ld_json",
    }


def main():
    results = {}
    log_lines = []
    for bc in BARCODES:
        res = fetch_one(bc)
        results[bc] = res
        log_lines.append(json.dumps(res, ensure_ascii=False))
        print(f"{bc}: brand={res.get('brand_field')!r} status={res.get('http_status')} err={res.get('error')}")

    patch = {
        bc: {
            "brand_field": r["brand_field"],
            "source_url": r["source_url"],
            "fetched_at": r["fetched_at"],
            "content_sha256": r["content_sha256"],
            "method": r["method"],
        }
        for bc, r in results.items()
        if r.get("brand_field")
    }

    out_path = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_crackers_conform_001\brand_patch_v1.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "schema": "crackers_brand_patch_v1",
                "task": "TASK-516",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "note": (
                    "Live targeted re-scrape of the same Shufersal product pages already "
                    "in the crackers corpus, reading the retailer's schema.org ld+json "
                    "Product.brand field (the original May-2026 bread-family scraper never "
                    "captured this field; every scraper written since does). Literal, "
                    "retailer-attested brand strings only -- never inferred from name text, "
                    "never OFF, never invented."
                ),
                "off_sources": 0,
                "candidates_fetched": len(BARCODES),
                "brands_recovered": len(patch),
                "patch": patch,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"\nWrote patch: {out_path} ({len(patch)}/{len(BARCODES)} brands recovered)")


if __name__ == "__main__":
    main()
