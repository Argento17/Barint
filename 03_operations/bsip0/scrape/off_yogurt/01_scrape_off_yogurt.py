"""
BSIP0 — Real Israeli Yogurt Corpus Scraper (run_yogurt_002)

Source: Open Food Facts (search-a-licious endpoint, search.openfoodfacts.org)
  - Real Israeli barcodes (729...), real brands, real nutrition panels.
  - Provenance: source_url = OFF product page per item.
  - Rationale: the legacy OFF search.pl + v2/search facet endpoints are 503
    (overloaded) as of 2026-06-01; the search-a-licious endpoint is healthy.
    Direct retailer sites (Shufersal/Yohananof) remain auth-walled / blocked
    (see memory: bsip0_retailer_access_001) so OFF is the real-data path,
    exactly as used for real_bread_retail_001/003.

Query: categories_tags:"en:yogurts" AND countries_tags:"en:israel"

Output:
  raw/off_<barcode>.json   — one OFF record per product (raw, preserved)
  scrape_log.json          — query, timestamp, per-product provenance + flags

NO synthetic barcodes. NO invented data. Read-only against OFF.
"""
from __future__ import annotations
import json, time, pathlib, datetime
import requests

# TASK-238: Open Food Facts is BANNED as a Bari data source (owner hard rule 2026-06-10).
# This scraper pulled the ENTIRE yogurt corpus directly from search.openfoodfacts.org and
# is therefore DISABLED. The yogurt corpus must be re-acquired from a direct retailer scrape
# or the category pulled. Never use OFF.
raise RuntimeError(
    "OFF is banned (TASK-238): 01_scrape_off_yogurt.py pulled the yogurt corpus from "
    "search.openfoodfacts.org and is disabled. Re-acquire from a direct retailer scrape; "
    "never use OFF."
)

BASE = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\off_yogurt")
RAW  = BASE / "raw"
RAW.mkdir(parents=True, exist_ok=True)

RUN_ID   = "run_yogurt_002"
ENDPOINT = "https://search.openfoodfacts.org/search"
QUERY    = 'categories_tags:"en:yogurts" AND countries_tags:"en:israel"'
HEADERS  = {"User-Agent": "Bari-research/1.0 (tbarhaim@gmail.com)"}
FIELDS   = [
    "code", "product_name", "product_name_he", "generic_name", "brands",
    "quantity", "categories_tags", "countries_tags", "labels_tags",
    "nova_group", "nutriscore_grade", "ingredients_text", "ingredients_text_he",
    "ingredients_n", "additives_tags", "nutriments", "image_url",
    "serving_size", "completeness", "data_quality_warnings_tags",
]


def fetch() -> list[dict]:
    params = {"q": QUERY, "page_size": 100, "fields": ",".join(FIELDS)}
    for attempt in range(5):
        try:
            r = requests.get(ENDPOINT, params=params, headers=HEADERS, timeout=50)
            if r.status_code == 200:
                return r.json().get("hits", [])
            print(f"  attempt {attempt} HTTP {r.status_code}")
        except Exception as e:
            print(f"  attempt {attempt} ERR {type(e).__name__} {str(e)[:80]}")
        time.sleep(6)
    raise RuntimeError("OFF search unavailable after retries")


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    hits = fetch()
    log = {
        "run_id": RUN_ID, "source": "openfoodfacts.org (search-a-licious)",
        "endpoint": ENDPOINT, "query": QUERY, "scraped_at": ts,
        "raw_count": len(hits), "products": [],
    }
    for p in hits:
        code = p.get("code")
        if not code:
            continue
        (RAW / f"off_{code}.json").write_text(
            json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
        nm = p.get("nutriments", {}) or {}
        log["products"].append({
            "barcode": code,
            "name": p.get("product_name"),
            "brands": p.get("brands"),
            "source_url": f"https://world.openfoodfacts.org/product/{code}",
            "has_ingredients": bool(p.get("ingredients_text_he") or p.get("ingredients_text")),
            "has_protein": nm.get("proteins_100g") is not None,
            "nova_group": p.get("nova_group"),
        })
    (BASE / "scrape_log.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"scraped {len(hits)} raw products -> {RAW}")
    print(f"with ingredients: {sum(1 for x in log['products'] if x['has_ingredients'])}/{len(hits)}")


if __name__ == "__main__":
    main()
