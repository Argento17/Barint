"""
Call Victory branch API directly using the exact URL format from Playwright intercept.
The key insight: the branch API uses listing IDs in the filters, not barcodes or productIds.

We need to find the listing IDs for our specific products.
Strategy: call branch API with a broad set of product listing IDs to find our targets.
Then extract nutritionValues + ingredients.
"""
import sys, re, json, requests
from urllib.parse import urlencode
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470
BRANCH_ID = 2930

# productIds from /api/products/{barcode} (these are the 'productId' in v2)
TARGETS = {
    "4820005195848": {"pid": 415280,  "label": "Millennium 80%"},
    "3046920023443": {"pid": 7872576, "label": "Lindt Excellence dark"},
    "3046920023429": {"pid": 7872575, "label": "Lindt caramel milk"},
    "3046920023368": {"pid": 7872574, "label": "Lindt Excellence milk"},
    "3046920028004": {"pid": 6181,    "label": "Lindt 70%"},
    "4820005198597": {"pid": 324953,  "label": "Millennium 74%"},
    "5941021001261": {"pid": 817732,  "label": "75% dark"},
    "7290119500482": {"pid": 7630501, "label": "62% dark"},
}

target_pids = {info["pid"] for info in TARGETS.values()}
pid_to_bc = {info["pid"]: bc for bc, info in TARGETS.items()}

def call_branch_api(listing_ids: list[int]) -> list[dict]:
    """
    Call the Victory branch API with listing IDs.
    Uses the exact filter format from Playwright network intercept.
    """
    filters = {
        "must": {
            "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
            "term": {
                "branch.isActive": True,
                "branch.isVisible": True,
                "id": listing_ids,
            }
        },
        "mustNot": {"term": {"branch.regularPrice": 0}},
        "bool": {"should": [
            {"bool": {"must_not": {"exists": {"field": "branch.outOfStockShowUntilDate"}}}},
            {"bool": {"must": [
                {"range": {"branch.outOfStockShowUntilDate": {"gt": "now"}}},
                {"term": {"branch.isOutOfStock": True}},
            ]}},
            {"bool": {"must": [{"term": {"branch.isOutOfStock": False}}]}},
        ]}
    }
    filters_json = json.dumps(filters, ensure_ascii=True, separators=(",", ":"))
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products"
    params = {"appId": 4, "filters": filters_json, "from": 0, "size": len(listing_ids) + 5}
    r = requests.get(url, params=params, timeout=30, headers={"Accept": "application/json"})
    if r.status_code == 200 and r.text.strip()[:1] == "{":
        data = r.json()
        return data.get("products", [])
    return []


def extract_nutrition(p: dict) -> dict:
    """Extract nutritionValues from a branch product object."""
    nv = p.get("nutritionValues") or {}
    sizes = nv.get("sizes") or []
    values = nv.get("values") or []

    # Determine per-100g column index
    col_idx = 0
    for i, sz in enumerate(sizes):
        names = sz.get("names") or {}
        sz_name = (names.get("1") or names.get(1) or "")
        if isinstance(sz_name, dict):
            sz_name = sz_name.get("name", "")
        if any(m in (sz_name or "") for m in ["100", "ל-100", "per 100"]):
            col_idx = i
            break

    LABEL_MAP = [
        (["טראנס", "trans"], "trans_fat"),
        (["רווי", "saturated"], "saturated_fat"),
        (["סוכר", "sugar", "סוכרי"], "sugar"),
        (["פחמימ", "carb"], "carbs"),
        (["סיב", "fiber"], "fiber"),
        (["חלבונ", "protein"], "protein"),
        (["נתרן", "sodium"], "sodium"),
        (["אנרגי", "קלורי", "kcal", "energy"], "energy"),
        (["שומנ", "fat"], "fat"),
    ]

    result = {}
    seen = set()
    for row in values:
        names = row.get("names") or {}
        label = (names.get("1") or names.get(1) or "")
        if isinstance(label, dict):
            label = label.get("name", "")
        sz_vals = row.get("sizeValues") or []
        if col_idx < len(sz_vals):
            sv = sz_vals[col_idx]
            val = sv.get("value") if isinstance(sv, dict) else sv
            try:
                val = float(str(val).replace(",", "."))
            except (ValueError, TypeError):
                continue
        else:
            continue

        ll = (label or "").lower()
        for tokens, canon in LABEL_MAP:
            if canon in seen:
                continue
            if any(t in (label or "") or t in ll for t in tokens):
                if canon in ("fat", "carbs") and any(m in (label or "") for m in ["מתוכ", "מהם"]):
                    continue
                result[canon] = val
                seen.add(canon)
                break
    return result


def extract_ingredients(p: dict) -> str:
    data = p.get("data") or {}
    lang1 = data.get("1") or data.get(1) or {}
    if isinstance(lang1, dict):
        return (lang1.get("ingredients") or lang1.get("componentsString") or "")[:1400]
    return ""


# ── Find listing IDs via the search endpoint ──────────────────────────────────
# Victory search endpoint that returns listing IDs for our products:
# GET /v2/retailers/{r}/branches/{b}/products?appId=4&search={query}

def search_branch_products(query: str, size: int = 50) -> list[dict]:
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products"
    params = {"appId": 4, "search": query, "from": 0, "size": size}
    r = requests.get(url, params=params, timeout=30, headers={"Accept": "application/json"})
    if r.status_code == 200 and r.text.strip()[:1] == "{":
        return r.json().get("products", [])
    # Also try "q" param
    params2 = {"appId": 4, "q": query, "from": 0, "size": size}
    r2 = requests.get(url, params=params2, timeout=30, headers={"Accept": "application/json"})
    if r2.status_code == 200 and r2.text.strip()[:1] == "{":
        return r2.json().get("products", [])
    print(f"  search_branch({query!r}): {r.status_code}/{r2.status_code}", flush=True)
    return []


print("=== 1. Branch search for chocolate products ===", flush=True)
branch_found: dict[str, dict] = {}  # barcode -> product

for bc, info in TARGETS.items():
    label = info["label"]
    pid = info["pid"]
    # Try name-based searches specific to each product
    queries = []
    if bc.startswith("304692"):
        queries = ["לינדט שוקולד", "lindt שוקולד"]
    elif "4820005195848" == bc:
        queries = ["שוקולד מריר 80%", "שוקולד 80%"]
    elif "4820005198597" == bc:
        queries = ["שוקולד מריר 74%"]
    elif "5941021001261" == bc:
        queries = ["שוקולד מריר 75%"]
    elif "7290119500482" == bc:
        queries = ["שוקולד מריר 62%"]
    else:
        queries = ["שוקולד מריר"]

    for q in queries:
        prods = search_branch_products(q, size=100)
        if prods:
            # Look for product by pid
            matched = [p for p in prods if p.get("productId") == pid]
            if matched:
                p = matched[0]
                branch_found[bc] = p
                name = p.get("localName", "")
                nv_count = len((p.get("nutritionValues") or {}).get("values") or [])
                ingr = extract_ingredients(p)
                print(f"  FOUND: {bc} ({label}) | {name[:50]} | nutr_rows={nv_count} | ingr_len={len(ingr)}", flush=True)
                break
        else:
            print(f"  No results for {q!r}", flush=True)

# ── Also try the nutrition image URL as a proxy for per-product full data ──────
print("\n=== 2. Check if nutritionImageUrl provides data ===", flush=True)
# From earlier: p.get("nutritionImageUrl") — check Millennium 80%
for bc, info in list(TARGETS.items())[:2]:
    pid = info["pid"]
    # Get product from /api/products/{barcode}
    r = requests.get(f"{VICTORY_BASE}/api/products/{bc}", timeout=10)
    if r.status_code == 200 and r.text.strip()[:1] == "{":
        p = r.json().get("product", {})
        nutr_img = p.get("nutritionImageUrl")
        print(f"  {bc}: nutritionImageUrl = {nutr_img}", flush=True)

# ── Try the branch API with product barcode filter ─────────────────────────────
print("\n=== 3. Branch API with barcode filter ===", flush=True)
for bc in ["4820005195848", "3046920023443"]:
    filters = {"must": {"term": {"branch.isActive": True, "branch.barcodes": bc}}}
    filters_json = json.dumps(filters, ensure_ascii=True, separators=(",", ":"))
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products"
    r = requests.get(url, params={"appId": 4, "filters": filters_json, "from": 0, "size": 5}, timeout=20)
    prods = r.json().get("products", []) if r.status_code == 200 and r.text.strip()[:1] == "{" else []
    print(f"  barcode filter {bc}: {r.status_code} returned {len(prods)}", flush=True)

# ── Save what we found ───────────────────────────────────────────────────────
print(f"\n=== Summary: {len(branch_found)}/{len(TARGETS)} found ===", flush=True)
result = {}
for bc, p in branch_found.items():
    nutr = extract_nutrition(p)
    ingr = extract_ingredients(p)
    result[bc] = {
        "barcode": bc,
        "name_victory": p.get("localName", ""),
        "productId": p.get("productId"),
        "listing_id": p.get("id"),
        "nutrition": nutr,
        "ingredients": ingr or None,
        "nutrition_complete": bool(nutr.get("energy") and nutr.get("fat") and nutr.get("carbs")),
    }
    print(f"  {bc}: nutr={nutr} | ingr={ingr[:80]}", flush=True)

import pathlib
out = pathlib.Path(r"C:\Bari\02_products\chocolate\victory_branch_found.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved: {out}", flush=True)
