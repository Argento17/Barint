"""
Victory v2 API — get full product data including nutritionValues.

Discovered from Playwright network intercept:
  GET /v2/retailers/1470/branches/2930/products?appId=4&filters={...}&from=0&size=N

The filters use Elasticsearch-like query with product IDs.
Product IDs were retrieved from /api/products/{barcode}.
"""
from __future__ import annotations
import sys, re, json, requests
from urllib.parse import quote, urlencode
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470
BRANCH_ID = 2930  # First active branch from data.js

# Product IDs from /api/products/{barcode}:
TARGET_PRODUCTS = {
    "4820005195848": {"id": 415280,  "name": "שוקולד מריר 80%",       "label": "Millennium 80%"},
    "3046920023443": {"id": 7872576, "name": "שוקולד קרמי מריר",      "label": "Lindt Excellence dark"},
    "3046920023429": {"id": 7872575, "name": "אקסטרה קרימי שוקולד חלב מעולה", "label": "Lindt caramel milk"},
    "3046920023368": {"id": 7872574, "name": "אקסטרה קרימי שוקולד חלב", "label": "Lindt Excellence milk"},
    "3046920028004": {"id": 6181,    "name": "אקסלנס שוקולד מריר 70%", "label": "Lindt 70%"},
    "4820005198597": {"id": 324953,  "name": "שוקולד מריר 74%",       "label": "Millennium 74%"},
    "5941021001261": {"id": 817732,  "name": "שוקולד מריר 75% קקאו",  "label": "Poiana 75%"},
    "7290119500482": {"id": 7630501, "name": "שוקולד מריר מעולה 62%", "label": "Tosso 62%"},
}

def build_filters(product_ids: list[int]) -> str:
    """Build the Elasticsearch-like filters JSON used by Victory v2 API."""
    filters = {
        "must": {
            "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
            "term": {
                "branch.isActive": True,
                "branch.isVisible": True,
                "id": product_ids,
            }
        },
        "mustNot": {
            "term": {"branch.regularPrice": 0}
        },
        "bool": {
            "should": [
                {"bool": {"must_not": {"exists": {"field": "branch.outOfStockShowUntilDate"}}}},
                {"bool": {"must": [
                    {"range": {"branch.outOfStockShowUntilDate": {"gt": "now"}}},
                    {"term": {"branch.isOutOfStock": True}},
                ]}},
                {"bool": {"must": [{"term": {"branch.isOutOfStock": False}}]}},
            ]
        }
    }
    return json.dumps(filters, ensure_ascii=False, separators=(",", ":"))


def fetch_products_v2(product_ids: list[int], branch_id: int = BRANCH_ID) -> dict | None:
    filters_str = build_filters(product_ids)
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{branch_id}/products"
    params = {
        "appId": 4,
        "filters": filters_str,
        "from": 0,
        "size": len(product_ids) + 5,
    }
    try:
        r = requests.get(url, params=params, timeout=30, headers={
            "Accept": "application/json",
            "Accept-Language": "he-IL,he;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0",
            "Referer": VICTORY_BASE + "/category?search=שוקולד",
        })
        print(f"  {r.status_code} len={len(r.text)}", flush=True)
        if r.status_code == 200 and r.text.strip().startswith("{"):
            return r.json()
        elif r.status_code == 200:
            print(f"  Not JSON: {r.text[:200]}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
    return None


# ── 1. Fetch all targets in one call ─────────────────────────────────────────
print("=== Fetching all target products via v2 API ===", flush=True)
all_ids = [v["id"] for v in TARGET_PRODUCTS.values()]
data = fetch_products_v2(all_ids)

if data:
    products = data.get("items", data.get("products", data.get("results", [])))
    total = data.get("total", len(products))
    print(f"\n  Total products returned: {total}, items: {len(products)}", flush=True)
    print(f"  Response keys: {list(data.keys())[:10]}", flush=True)

    if products:
        # Show structure of first product
        print(f"\n  First product keys: {list(products[0].keys())[:30]}", flush=True)
        print(f"  First product: {json.dumps(products[0], ensure_ascii=False)[:1000]}", flush=True)
else:
    print("  No data returned. Trying other branches...", flush=True)

    # Try different branch IDs
    for branch_id in [2437, 2528, 2529, 2531, 2537, 2543, 2540]:
        print(f"\n  Trying branch {branch_id}...", flush=True)
        d = fetch_products_v2(all_ids[:4], branch_id=branch_id)
        if d:
            products = d.get("items", d.get("products", []))
            if products:
                print(f"  SUCCESS! Got {len(products)} products from branch {branch_id}", flush=True)
                print(f"  Product keys: {list(products[0].keys())[:30]}", flush=True)
                print(f"  Sample: {json.dumps(products[0], ensure_ascii=False)[:1000]}", flush=True)
                data = d
                break

# ── 2. Also try the v2 search endpoint ────────────────────────────────────────
print("\n=== v2 search endpoint ===", flush=True)
SEARCH_CANDIDATES = [
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products/search?q=שוקולד+מריר+80&appId=4",
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/search?q=שוקולד+מריר+80&appId=4",
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/search?q=שוקולד+מריר+80&appId=4",
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products?q=שוקולד+מריר+80&appId=4&from=0&size=20",
    # Try search by barcode
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products/search?q=4820005195848&appId=4",
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/search?barcode=4820005195848&appId=4",
]

for url in SEARCH_CANDIDATES:
    try:
        r = requests.get(url, timeout=15, headers={
            "Accept": "application/json",
            "Accept-Language": "he-IL,he;q=0.9",
            "User-Agent": "Mozilla/5.0",
        })
        is_json = r.text.strip()[:1] in ("{", "[") if r.text else False
        has_nutr = "nutritionValues" in r.text
        has_products = bool(re.search(r'"id":\d+', r.text))
        print(f"  {r.status_code} len={len(r.text)} json={is_json} nutr={has_nutr} | {url}", flush=True)
        if has_nutr:
            print(f"  DATA: {r.text[:500]}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} | {url}", flush=True)

# ── 3. Try to search by barcode via the v2 products endpoint ──────────────────
print("\n=== Search by barcode on v2 products endpoint ===", flush=True)
TEST_BC = "4820005195848"  # Millennium 80%
barcode_filters = {
    "must": {
        "term": {
            "branch.isActive": True,
            "branch.isVisible": True,
            "branch.barcodes": TEST_BC,
        }
    },
    "mustNot": {"term": {"branch.regularPrice": 0}},
}
url_bc = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products"
r = requests.get(url_bc, params={
    "appId": 4,
    "filters": json.dumps(barcode_filters, separators=(",", ":")),
    "from": 0,
    "size": 5,
}, timeout=15, headers={"Accept": "application/json", "Accept-Language": "he-IL,he;q=0.9"})
print(f"  Barcode filter: {r.status_code} len={len(r.text)}", flush=True)
if r.text.strip()[:1] in ("{", "["):
    d = r.json()
    products = d.get("items", d.get("products", []))
    print(f"  Products: {len(products)}", flush=True)
    if products:
        print(f"  {json.dumps(products[0], ensure_ascii=False)[:500]}", flush=True)
