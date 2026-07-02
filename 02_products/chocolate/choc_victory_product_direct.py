"""
Use Victory's /api/products/{barcode} productId to look up via v2 API.
Key insight: /api/products/{barcode} returns productId (e.g. 415280 for Millennium).
The v2 endpoint uses a different 'id' (shelf listing), but productId is the link.

Strategy: search v2 with specific product names, then filter by productId.
Also try /v2/retailers/{r}/products/{productId} and check the structure.
"""
import sys, json, re, requests, pathlib, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
CHOC_DIR = ROOT / "02_products" / "chocolate"
VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470

# Known productIds from /api/products/{barcode}
TARGETS = {
    "4820005195848": {"pid": 415280,  "label": "Millennium 80%",     "search": "שוקולד מריר 80%"},
    "3046920023443": {"pid": 7872576, "label": "Lindt dark",          "search": "שוקולד מריר מעולה לינדט"},
    "3046920023429": {"pid": 7872575, "label": "Lindt caramel milk",  "search": "לינדט שוקולד חלב קרמל"},
    "3046920023368": {"pid": 7872574, "label": "Lindt milk",          "search": "לינדט שוקולד חלב"},
    "3046920028004": {"pid": 6181,    "label": "Lindt 70%",           "search": "שוקולד מריר 70%"},
    "4820005198597": {"pid": 324953,  "label": "Millennium 74%",      "search": "שוקולד מריר 74%"},
    "5941021001261": {"pid": 817732,  "label": "75% dark",            "search": "שוקולד מריר 75%"},
    "7290119500482": {"pid": 7630501, "label": "62% dark",            "search": "שוקולד מריר 62%"},
}

def get_json(url: str, params=None) -> dict:
    try:
        r = requests.get(url, params=params, timeout=20, headers={
            "Accept": "application/json",
            "Accept-Language": "he-IL,he;q=0.9",
        })
        if r.text.strip()[:1] in ("{", "["):
            return r.json()
        return {"_error": f"Not JSON: {r.status_code} len={len(r.text)}", "_text": r.text[:200]}
    except Exception as e:
        return {"_error": str(e)}

# ── 1. Try /v2/retailers/{r}/products/{productId} ─────────────────────────────
print("=== 1. /v2/.../products/{productId} ===", flush=True)
for bc, t in list(TARGETS.items())[:3]:
    pid = t["pid"]
    d = get_json(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products/{pid}")
    print(f"  {bc} pid={pid}: {d.get('_error', list(d.keys())[:5])}", flush=True)

# ── 2. Search by specific Hebrew product name (narrow) ────────────────────────
print("\n=== 2. Search by narrow product name ===", flush=True)
all_found = {}

for bc, t in TARGETS.items():
    r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
        "q": t["search"], "appId": 4, "from": 0, "size": 50
    }, timeout=20)
    prods = r.json().get("products", [])
    # Filter by productId
    matched = [p for p in prods if p.get("productId") == t["pid"]]
    # Also try by barcode field
    bc_matched = [p for p in prods if str(p.get("barcode", "")) == bc]
    found = matched or bc_matched
    print(f"  {bc} ({t['label']}): returned={len(prods)}, pid_match={len(matched)}, bc_match={len(bc_matched)}", flush=True)
    if found:
        p = found[0]
        all_found[bc] = p
        nv = p.get("nutritionValues") or {}
        print(f"    localName={p.get('localName', '')[:50]} | nutr_values={len(nv.get('values') or [])}", flush=True)
    else:
        # Show first 5 productIds from results
        print(f"    Sample productIds: {[p.get('productId') for p in prods[:5]]}", flush=True)

# ── 3. If still not found, try /v2/retailers/{r}/products?productId={pid} ─────
print("\n=== 3. Search via productId param ===", flush=True)
for bc, t in list(TARGETS.items())[:4]:
    if bc in all_found:
        continue
    pid = t["pid"]
    # Try as productId filter
    d = get_json(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", {"productId": pid, "appId": 4, "size": 5})
    if d and not d.get("_error"):
        prods = d.get("products", [])
        print(f"  productId={pid}: returned {len(prods)}", flush=True)
        if prods:
            p = prods[0]
            print(f"    localName={p.get('localName')} pid={p.get('productId')}", flush=True)

# ── 4. Try the branch-specific endpoint with productId filter ─────────────────
print("\n=== 4. Branch products with productId ===", flush=True)
# The Playwright network intercept showed the branch endpoint uses `id` (not productId)
# in the filters. But we found from step 5 above that /api/products/{barcode} returns productId.
# The v2 branch search uses internal listing IDs, not productIds.
# Let's find listing IDs for our targets by scanning the branch endpoint.

# Try to find listing ID for Millennium 80% by searching on its barcode
MILLENNIUM_BC = "4820005195848"
MILLENNIUM_PID = 415280

# Use a targeted search with the actual product barcode
r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
    "q": "Dolina שוקולד מריר 80", "appId": 4, "from": 0, "size": 50
}, timeout=20)
prods = r.json().get("products", [])
print(f"  'Dolina שוקולד מריר 80': {len(prods)} products", flush=True)
for p in prods[:5]:
    print(f"    id={p.get('id')} productId={p.get('productId')} bc={p.get('barcode')} name={p.get('localName', '')[:50]}", flush=True)

# Try product barcode in the v2 query — Victory might support exact barcode search
for bc_search in ["4820005195848", "3046920023443"]:
    r2 = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
        "barcode": bc_search, "appId": 4, "from": 0, "size": 10
    }, timeout=20)
    prods2 = r2.json().get("products", [])
    matched2 = [p for p in prods2 if str(p.get("barcode", "")) == bc_search]
    print(f"  barcode param {bc_search}: {len(prods2)} returned, {len(matched2)} exact matches", flush=True)

# ── 5. v2 product lookup by productId via GS1-products path ──────────────────
print("\n=== 5. Check GS1 products endpoint ===", flush=True)
# The CDN uses /gs1-products/ path, maybe there's a GS1 API
GS1_CANDIDATES = [
    f"https://d226b0iufwcjmj.cloudfront.net/gs1-products/1470/medium/415280-0/415280/medium.json",
    f"https://d226b0iufwcjmj.cloudfront.net/gs1-products/1470/nutrition/415280.json",
    f"{VICTORY_BASE}/api/gs1/products/4820005195848",
    f"{VICTORY_BASE}/api/gs1/{RETAILER_ID}/products/4820005195848",
    # Try v2 with productsIds param (plural)
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products?productsIds=415280&appId=4",
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products?productIds=415280&appId=4",
    f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products?ids=415280&appId=4",
]
for url in GS1_CANDIDATES:
    try:
        r = requests.get(url, timeout=10)
        has_nutr = "nutritionValues" in r.text or "nutrition" in r.text.lower()
        is_json = r.text.strip()[:1] in ("{", "[", "[")
        print(f"  {r.status_code} len={len(r.text)} nutr={has_nutr} json={is_json} | {url}", flush=True)
        if has_nutr:
            print(f"  DATA: {r.text[:500]}", flush=True)
    except Exception as e:
        print(f"  ERR: {e} | {url}", flush=True)
