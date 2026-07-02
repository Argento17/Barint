"""
Victory final data acquisition — uses the live-verified /v2/retailers/1470/products endpoint.

Retrieves full product data including nutritionValues and ingredients.
"""
from __future__ import annotations
import sys, re, json, requests, datetime, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
CHOC_DIR = ROOT / "02_products" / "chocolate"

sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470

def v2_search(query: str, size: int = 30) -> list[dict]:
    """Search Victory v2 API and return product list with full data including nutritionValues."""
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/products"
    params = {"q": query, "appId": 4, "from": 0, "size": size}
    try:
        r = requests.get(url, params=params, timeout=30, headers={
            "Accept": "application/json",
            "Accept-Language": "he-IL,he;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0",
            "Referer": VICTORY_BASE + "/",
        })
        if r.status_code == 200 and r.text.strip().startswith("{"):
            data = r.json()
            return data.get("products", [])
        print(f"  v2_search error: HTTP {r.status_code}", flush=True)
    except Exception as e:
        print(f"  v2_search exception: {e}", flush=True)
    return []


def parse_nutrition_values(product: dict) -> dict:
    """
    Extract nutrition from Victory product's nutritionValues structure.

    Structure from app.js template:
      product.nutritionValues.sizes: [{names: {1: {name: "ל-100 גרם"}}}]  (column headers)
      product.nutritionValues.values: [{names: {1: {name: "שומנים"}}, sizeValues: [{value: "35"}]}]

    We always take the first column (per-100g) when available.
    """
    nv = product.get("nutritionValues") or {}
    sizes = nv.get("sizes") or []
    values = nv.get("values") or []
    if not values:
        return {}

    # Determine which column is per-100g
    col_idx = 0  # default first column
    for i, sz in enumerate(sizes):
        sz_name = ""
        names = sz.get("names") or {}
        for lang_key in ["1", "2", 1, 2]:
            nm = names.get(str(lang_key)) or names.get(lang_key) or {}
            if isinstance(nm, dict):
                sz_name = nm.get("name", "") or nm.get("unitOfMeasure", "") or ""
            elif isinstance(nm, str):
                sz_name = nm
            if sz_name:
                break
        if any(m in (sz_name or "") for m in ["100 גרם", "100g", "ל-100", "per 100"]):
            col_idx = i
            break

    # Map label -> canonical
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

    result: dict[str, float] = {}
    seen_keys: set = set()

    for row in values:
        names_obj = row.get("names") or {}
        label = ""
        for lang_key in ["1", 1, "2", 2]:
            nm = names_obj.get(str(lang_key)) or names_obj.get(lang_key)
            if isinstance(nm, dict):
                label = nm.get("name", "")
            elif isinstance(nm, str):
                label = nm
            if label:
                break

        sz_vals = row.get("sizeValues") or []
        if col_idx < len(sz_vals):
            val_obj = sz_vals[col_idx]
            if isinstance(val_obj, dict):
                raw_val = str(val_obj.get("value", "") or "")
            else:
                raw_val = str(val_obj or "")
        else:
            continue

        # Extract numeric
        num_m = re.search(r"([\d,.]+)", raw_val)
        if not num_m:
            continue
        try:
            val = float(num_m.group(1).replace(",", "."))
        except ValueError:
            continue

        # Classify
        ll = label.lower()
        for tokens, canon_key in LABEL_MAP:
            if canon_key in seen_keys:
                continue
            if any(t in label or t in ll for t in tokens):
                # Skip "of-which" subrows for fat and carbs (don't overwrite totals)
                if canon_key == "fat" and any(m in label for m in ["מתוכ", "מתוכם", "מהם"]):
                    continue
                if canon_key == "carbs" and any(m in label for m in ["מתוכ", "מתוכם", "מהם"]):
                    continue
                result[canon_key] = val
                seen_keys.add(canon_key)
                break

    return result


def parse_ingredients(product: dict) -> str:
    """Extract ingredients text from Victory product object."""
    # Try ingredients field directly
    ingr = product.get("ingredients") or ""
    if isinstance(ingr, dict):
        # May be {"1": "text...", "2": "text..."}
        for lang_key in ["1", 1]:
            v = ingr.get(str(lang_key)) or ingr.get(lang_key) or ""
            if v:
                ingr = v
                break
        else:
            ingr = str(ingr)

    if ingr and len(str(ingr).strip()) > 10:
        return str(ingr).strip()[:1400]

    # Try ingredients inside names or description
    for field in ["description", "longDes", "extraInfo"]:
        val = product.get(field) or ""
        if "רכיב" in (val or ""):
            m = re.search(r"רכיב[ים:]*\s*(.+)", val, re.DOTALL)
            if m:
                return m.group(1).strip()[:1400]

    return ""


def is_boilerplate(ingr: str) -> bool:
    return "כפי שרשום על גבי האריזה עלול להכיל" in (ingr or "")

def has_real_ingredients(ingr: str) -> bool:
    if not ingr or is_boilerplate(ingr):
        return False
    real_markers = ["קקאו", "סוכר", "חלב", "שומן", "שמן", "חמאה", "וניל", "לציטין", "אמולגטור"]
    return any(m in ingr for m in real_markers)


# ── Searches ──────────────────────────────────────────────────────────────────

print("=== Searching Victory v2 for target products ===", flush=True)

# Index products by ID and barcode from search results
fetched: dict[int, dict] = {}  # id -> product
fetched_by_barcode: dict[str, dict] = {}  # barcode_str -> product

TARGET_PRODUCT_IDS = {
    415280:  "4820005195848",  # Millennium 80%
    7872576: "3046920023443",  # Lindt Excellence dark
    7872575: "3046920023429",  # Lindt caramel milk
    7872574: "3046920023368",  # Lindt Excellence milk
    6181:    "3046920028004",  # Lindt 70%
    324953:  "4820005198597",  # Millennium 74%
    817732:  "5941021001261",  # Poiana 75%
    7630501: "7290119500482",  # Tosso 62%
}

def register_products(products: list[dict]) -> None:
    for p in products:
        pid = p.get("id") or p.get("productId")
        barcodes = p.get("barcodes") or []
        if pid:
            fetched[pid] = p
        for bc in barcodes:
            fetched_by_barcode[str(bc)] = p
        # Also check family barcodes
        family = p.get("family") or {}
        family_barcodes = family.get("barcodes") or []
        for bc in family_barcodes:
            fetched_by_barcode[str(bc)] = p


# Search 1: dark chocolate 80%
print("\n1. שוקולד מריר 80%", flush=True)
results = v2_search("שוקולד מריר 80%", size=50)
print(f"   Returned {len(results)} products", flush=True)
register_products(results)

# Search 2: Millennium chocolate
print("\n2. שוקולד מריר 80 קקאו", flush=True)
results2 = v2_search("שוקולד מריר 80 קקאו", size=30)
print(f"   Returned {len(results2)} products", flush=True)
register_products(results2)

# Search 3: Lindt Excellence dark
print("\n3. שוקולד מריר מעולה לינדט", flush=True)
results3 = v2_search("שוקולד מריר מעולה לינדט", size=20)
print(f"   Returned {len(results3)} products", flush=True)
register_products(results3)

# Search 4: Lindt caramel
print("\n4. שוקולד חלב קרמל לינדט", flush=True)
results4 = v2_search("שוקולד חלב קרמל לינדט", size=20)
print(f"   Returned {len(results4)} products", flush=True)
register_products(results4)

# Search 5: dark chocolate general
print("\n5. שוקולד מריר (broad)", flush=True)
results5 = v2_search("שוקולד מריר", size=100)
print(f"   Returned {len(results5)} products", flush=True)
register_products(results5)

print(f"\nTotal unique products in index: {len(fetched)} (by id), {len(fetched_by_barcode)} (by barcode)", flush=True)

# ── Find our targets ──────────────────────────────────────────────────────────
print("\n=== Finding target products ===", flush=True)
target_found = {}
for pid, bc in TARGET_PRODUCT_IDS.items():
    p = fetched.get(pid) or fetched_by_barcode.get(bc)
    if p:
        nutr = parse_nutrition_values(p)
        ingr = parse_ingredients(p)
        # Get the product name
        name = ""
        names = p.get("names") or {}
        for lang_key in ["1", 1]:
            nm = names.get(str(lang_key)) or names.get(lang_key) or {}
            if isinstance(nm, dict):
                name = nm.get("name", "")
            elif isinstance(nm, str):
                name = nm
            if name:
                break
        if not name:
            name = p.get("longDes", "") or p.get("shortDes", "") or p.get("name", "")
        target_found[bc] = {
            "product_id": pid,
            "barcode": bc,
            "name_victory": name,
            "nutrition_parsed": nutr,
            "nutrition_has_energy": nutr.get("energy") is not None,
            "nutrition_has_fat": nutr.get("fat") is not None,
            "nutrition_has_sat_fat": nutr.get("saturated_fat") is not None,
            "nutrition_has_sugar": nutr.get("sugar") is not None,
            "ingredients_raw": ingr or None,
            "ingredients_status": (
                "REAL_INGREDIENTS" if has_real_ingredients(ingr) else
                "STILL_BOILERPLATE" if is_boilerplate(ingr) else
                "TEXT_BUT_UNVERIFIED" if ingr else
                "NULL"
            ),
            "nutrition_image_url": p.get("nutritionImageUrl"),
            "image_url": p.get("filename") or p.get("imageUrl"),
        }
        nutr_complete = all(target_found[bc]["nutrition_" + k] for k in ["has_energy", "has_fat", "has_sugar"])
        print(f"  FOUND: {bc} = {name[:50]}", flush=True)
        print(f"    Nutrition: {nutr}", flush=True)
        print(f"    Complete: {nutr_complete}", flush=True)
        print(f"    Ingredients: {(ingr or '')[:150]}", flush=True)
    else:
        target_found[bc] = None
        print(f"  NOT FOUND in search results: {bc} (id={pid})", flush=True)

# ── Also look for 80% products in all results ─────────────────────────────────
print("\n=== Browsing all fetched for 80% (75-82%) dark chocolate ===", flush=True)
all_products = list(fetched.values())

near_80_products = []
for p in all_products:
    name = ""
    names = p.get("names") or {}
    for lang_key in ["1", 1]:
        nm = names.get(str(lang_key)) or names.get(lang_key) or {}
        if isinstance(nm, dict):
            name = nm.get("name", "")
        elif isinstance(nm, str):
            name = nm
        if name:
            break
    if not name:
        name = p.get("longDes") or p.get("name") or ""

    pct_m = re.search(r'(\d{2,3})\s*%', name or "")
    if pct_m:
        pct = int(pct_m.group(1))
        if 75 <= pct <= 82:
            nutr = parse_nutrition_values(p)
            barcodes = p.get("barcodes") or (p.get("family") or {}).get("barcodes") or []
            near_80_products.append({
                "id": p.get("id"),
                "name": name,
                "cocoa_pct": pct,
                "barcodes": barcodes,
                "nutrition_summary": nutr,
                "has_full_panel": bool(nutr.get("energy") and nutr.get("fat")),
            })
            print(f"  {pct}% | {name[:60]} | {barcodes} | nutr={bool(nutr)}", flush=True)

print(f"\nTotal near-80% products: {len(near_80_products)}", flush=True)

# Save raw data for full analysis
out = {
    "fetched_ids": list(fetched.keys()),
    "fetched_barcodes": list(fetched_by_barcode.keys()),
    "targets": target_found,
    "near_80_products": near_80_products,
}
out_path = CHOC_DIR / "victory_v2_raw.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRaw data written: {out_path}", flush=True)
