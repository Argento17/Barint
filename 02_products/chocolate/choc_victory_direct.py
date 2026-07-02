"""
Direct Victory product lookups — try by v2 internal product ID (productId field)
and by barcode search in the v2 API.
"""
import sys, json, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470

# Known product IDs from /api/products/{barcode}:
TARGET_PRODUCTS = {
    "4820005195848": {"api_id": 415280,  "label": "Millennium 80%"},
    "3046920023443": {"api_id": 7872576, "label": "Lindt Excellence dark"},
    "3046920023429": {"api_id": 7872575, "label": "Lindt caramel milk"},
    "3046920023368": {"api_id": 7872574, "label": "Lindt Excellence milk"},
    "3046920028004": {"api_id": 6181,    "label": "Lindt 70%"},
    "4820005198597": {"api_id": 324953,  "label": "Millennium 74%"},
    "5941021001261": {"id": 817732,  "label": "Poiana 75%"},
    "7290119500482": {"api_id": 7630501, "label": "Tosso 62%"},
}

def get_json(url: str, params: dict = None) -> dict:
    try:
        r = requests.get(url, params=params, timeout=20, headers={
            "Accept": "application/json",
            "Accept-Language": "he-IL,he;q=0.9",
        })
        if r.text.strip()[:1] in ("{", "["):
            return r.json()
        return {"_error": f"Not JSON: HTTP {r.status_code}, len={len(r.text)}"}
    except Exception as e:
        return {"_error": str(e)}

# ── 1. Try /v2/retailers/1470/products/{internal_id} ──────────────────────────
print("=== 1. Direct product by ID ===", flush=True)
for bc, info in list(TARGET_PRODUCTS.items())[:4]:
    api_id = info.get("api_id", info.get("id"))
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products/{api_id}"
    d = get_json(url)
    has_nutr = "nutritionValues" in json.dumps(d)
    is_error = "_error" in d
    print(f"  {bc} (id={api_id}): error={is_error}, nutr={has_nutr}", flush=True)
    if not is_error:
        print(f"  Keys: {list(d.keys())[:10]}", flush=True)

# ── 2. v2 products with from/size pagination ───────────────────────────────────
print("\n=== 2. Verify v2 name structure ===", flush=True)
r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
    "q": "שוקולד מריר", "appId": 4, "from": 0, "size": 10
}, timeout=30)
data = r.json()
prods = data.get("products", [])
print(f"  Total: {data.get('total')}, returned: {len(prods)}", flush=True)
for p in prods[:3]:
    names_1 = (p.get("names") or {}).get("1") or {}
    name_long = names_1.get("long", "") if isinstance(names_1, dict) else names_1
    name_short = names_1.get("short", "") if isinstance(names_1, dict) else ""
    localname = p.get("localName", "")
    barcode = p.get("barcode", "")
    pid = p.get("id")
    prod_id = p.get("productId")
    nv = p.get("nutritionValues") or {}
    print(f"  id={pid} productId={prod_id} barcode={barcode}", flush=True)
    print(f"  name_long={name_long} | name_short={name_short} | local={localname}", flush=True)
    print(f"  nutritionValues: {list(nv.keys())}", flush=True)

# ── 3. Search by barcode with v2 products ──────────────────────────────────────
print("\n=== 3. Search by barcode string in v2 ===", flush=True)
TARGET_BARCODES = ["4820005195848", "3046920023443"]
for bc in TARGET_BARCODES:
    r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
        "q": bc, "appId": 4, "from": 0, "size": 10
    }, timeout=20)
    d = r.json()
    prods = d.get("products", [])
    matched = [p for p in prods if str(p.get("barcode", "")) == bc]
    print(f"  {bc}: total={d.get('total')}, matched by barcode={len(matched)}", flush=True)
    if matched:
        p = matched[0]
        nv = p.get("nutritionValues") or {}
        print(f"  id={p.get('id')} | productId={p.get('productId')} | localName={p.get('localName')}", flush=True)
        print(f"  nutritionValues keys: {list(nv.keys())}, values_count={len(nv.get('values') or [])}", flush=True)
    elif prods:
        print(f"  No exact barcode match. Sample barcodes: {[p.get('barcode') for p in prods[:5]]}", flush=True)

# ── 4. Try the products endpoint with barcode filter ──────────────────────────
print("\n=== 4. v2 products with barcode in search field ===", flush=True)
# The v2 search may search by barcode when you pass a numeric string
for bc in ["4820005195848"]:
    r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
        "q": bc, "appId": 4, "from": 0, "size": 20, "includeNutrition": True
    }, timeout=20)
    d = r.json()
    prods = d.get("products", [])
    has_any_nutr = any("nutritionValues" in json.dumps(p) and p.get("nutritionValues") for p in prods)
    barcodes_found = [p.get("barcode") for p in prods[:10]]
    print(f"  {bc}: returned {len(prods)}, has_nutr={has_any_nutr}, barcodes={barcodes_found}", flush=True)
    # Show full first product with nutrition
    for p in prods:
        nv = p.get("nutritionValues") or {}
        if nv.get("values"):
            print(f"  Product with nutritionValues: {json.dumps(p, ensure_ascii=False)[:600]}", flush=True)
            break

# ── 5. Check if the productId (from v2 search) maps to API product ID ─────────
print("\n=== 5. Check productId -> /api/products mapping ===", flush=True)
r = requests.get(f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products", params={
    "q": "שוקולד 80", "appId": 4, "from": 0, "size": 10
}, timeout=20)
prods = r.json().get("products", [])
for p in prods[:5]:
    prod_id = p.get("productId")
    api_id_info = get_json(f"{VICTORY_BASE}/api/products/{prod_id}") if prod_id else {}
    barcode = p.get("barcode", "")
    api_bc_info = get_json(f"{VICTORY_BASE}/api/products/{barcode}") if barcode else {}
    name = p.get("localName", "")
    pid = p.get("id")
    print(f"  v2 id={pid} productId={prod_id} barcode={barcode} name={name[:40]}", flush=True)
    if api_id_info and not api_id_info.get("_error"):
        api_p = api_id_info.get("product", {})
        print(f"    -> api/products/{prod_id}: id={api_p.get('id')} longDes={api_p.get('longDes', '')[:50]}", flush=True)
    if api_bc_info and not api_bc_info.get("_error"):
        api_p = api_bc_info.get("product", {})
        print(f"    -> api/products/{barcode}: id={api_p.get('id')} longDes={api_p.get('longDes', '')[:50]}", flush=True)
