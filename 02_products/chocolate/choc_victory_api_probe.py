"""
Victory API probe — discover nutrition and ingredient endpoints.

We found: /api/products/{barcode} returns product identity.
Now probe for: nutrition panel and ingredient list via API.
"""
from __future__ import annotations
import sys, re, requests, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"
TEST_BARCODE = "3046920023443"  # Lindt Excellence dark (confirmed on Victory API)
TEST_BARCODE_80 = "4820005195848"  # Millennium 80% (to check if it exists)

def get_json(url: str) -> dict | None:
    try:
        r = requests.get(url, timeout=15, headers={"Accept": "application/json", "Accept-Language": "he-IL"})
        if r.status_code == 200 and r.text.strip().startswith("{"):
            return r.json()
        print(f"  {r.status_code} (not JSON) | {url}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} | {url}", flush=True)
    return None

# ── 1. Confirm product identity ───────────────────────────────────────────────
print("=== 1. Product identity via /api/products ===", flush=True)
product_data = get_json(f"{VICTORY_BASE}/api/products/{TEST_BARCODE}")
if product_data:
    p = product_data.get("product", {})
    print(json.dumps({k: v for k, v in p.items() if not isinstance(v, dict)}, ensure_ascii=False, indent=2), flush=True)
    product_id = p.get("id")
    print(f"\n  product_id: {product_id}", flush=True)
else:
    print("  NOT FOUND", flush=True)
    product_id = None

# ── 2. Probe nutrition endpoints by product ID and barcode ────────────────────
print("\n=== 2. Nutrition/ingredient endpoint probes ===", flush=True)

if product_id:
    NUTRITION_CANDIDATES = [
        f"{VICTORY_BASE}/api/products/{TEST_BARCODE}/nutrition",
        f"{VICTORY_BASE}/api/products/{TEST_BARCODE}/nutritionValues",
        f"{VICTORY_BASE}/api/products/{product_id}/nutrition",
        f"{VICTORY_BASE}/api/products/{product_id}/nutritionValues",
        f"{VICTORY_BASE}/api/products/{product_id}/details",
        f"{VICTORY_BASE}/api/nutritionvalues/{product_id}",
        f"{VICTORY_BASE}/api/nutritionvalues/{TEST_BARCODE}",
        f"{VICTORY_BASE}/api/v1/nutrition/{TEST_BARCODE}",
        f"{VICTORY_BASE}/api/v1/products/{TEST_BARCODE}/nutrition",
        f"{VICTORY_BASE}/api/products/{TEST_BARCODE}/ingredients",
        f"{VICTORY_BASE}/api/products/{product_id}/ingredients",
        f"{VICTORY_BASE}/api/v1/ingredients/{TEST_BARCODE}",
        # Full product detail endpoints
        f"{VICTORY_BASE}/api/products/{TEST_BARCODE}/full",
        f"{VICTORY_BASE}/api/v1/products/{product_id}",
        f"{VICTORY_BASE}/api/v1/products?barcode={TEST_BARCODE}&include=nutrition",
        # The SaaS used by Victory/Yochananof may have a specific path
        f"{VICTORY_BASE}/api/catalog/products/{TEST_BARCODE}",
        f"{VICTORY_BASE}/api/catalog/products/{product_id}",
    ]

    for url in NUTRITION_CANDIDATES:
        try:
            r = requests.get(url, timeout=10)
            has_nutr = any(k in r.text for k in ["נתרן", "sodium", "kcal", "קלוריות", "nutritionValues", "protein"])
            has_ingr = any(k in r.text for k in ["רכיב", "ingredient", "קקאו"])
            has_data = len(r.text) > 100 and r.text.strip().startswith(("{", "["))
            print(f"  {r.status_code} len={len(r.text)} nutr={has_nutr} ingr={has_ingr} json={has_data} | {url}", flush=True)
            if has_nutr or has_ingr:
                print(f"  DATA: {r.text[:400]}", flush=True)
        except Exception as e:
            print(f"  ERROR: {e} | {url}", flush=True)

# ── 3. Look at the full product data structure ───────────────────────────────
print("\n=== 3. Full product object ===", flush=True)
if product_data:
    p = product_data.get("product", {})
    print(json.dumps(p, ensure_ascii=False, indent=2)[:2000], flush=True)

# ── 4. Check if Millennium 80% is on Victory ──────────────────────────────────
print("\n=== 4. Check target barcodes on Victory API ===", flush=True)
TARGET_BARCODES = {
    "3046920023443": "Lindt Excellence dark",
    "3046920023429": "Lindt caramel milk",
    "3046920023368": "Lindt Excellence milk",
    "4820005195848": "Millennium 80%",
    "3046920028004": "Lindt 70%",
    "3046920028028": "Lindt 80% candidate",
    "3046920022378": "Lindt 85%",
    # Additional 80% dark chocolate candidates
    "7296073726562": "Lalto 72%",
    "4820005198597": "Millennium 74%",
    "7296073747802": "Lalto premium 75%",
    "5941021001261": "Poiana 75%",
    "7290119500482": "Tosso 62%",
}

found_on_victory = {}
for bc, desc in TARGET_BARCODES.items():
    d = get_json(f"{VICTORY_BASE}/api/products/{bc}")
    if d and d.get("product") and d["product"].get("id"):
        p = d["product"]
        print(f"  FOUND: {bc} = {p.get('longDes', '')} (id={p.get('id')})", flush=True)
        found_on_victory[bc] = p
    else:
        print(f"  NOT FOUND: {bc} ({desc})", flush=True)

print(f"\n  Total found on Victory: {len(found_on_victory)}", flush=True)
