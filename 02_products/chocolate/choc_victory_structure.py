"""Analyze the Victory v2 product structure to find IDs and nutrition."""
import sys, json, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
raw = json.loads((ROOT / "02_products" / "chocolate" / "victory_v2_raw.json").read_text(encoding="utf-8"))

# Get the raw JSON from v2 search again to look at structure
import requests
VICTORY_BASE = "https://www.victoryonline.co.il"
r = requests.get(f"{VICTORY_BASE}/v2/retailers/1470/products", params={
    "q": "שוקולד מריר 80%", "appId": 4, "from": 0, "size": 5
}, timeout=30)
data = r.json()
products = data.get("products", [])

print(f"Total from query: {data.get('total')}, returned: {len(products)}", flush=True)
if products:
    p = products[0]
    print(f"\nFirst product keys: {list(p.keys())}", flush=True)
    # Show full product without giant lists
    for k, v in p.items():
        if isinstance(v, (str, int, float, bool)):
            print(f"  {k}: {v}", flush=True)
        elif isinstance(v, dict):
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:200]}", flush=True)
        elif isinstance(v, list):
            print(f"  {k}: [{len(v)} items] {json.dumps(v[:2], ensure_ascii=False)[:200]}", flush=True)

    # Check all barcodes across first 5 products
    print("\nBarcodes across first 5 products:", flush=True)
    for p in products[:5]:
        pid = p.get("id")
        barcodes = p.get("barcodes") or []
        family = p.get("family") or {}
        fam_barcodes = family.get("barcodes") or []
        name_obj = (p.get("names") or {}).get("1") or (p.get("names") or {}).get(1) or {}
        name = name_obj.get("name") if isinstance(name_obj, dict) else name_obj
        print(f"  id={pid} | name={name} | barcodes={barcodes} | family_barcodes={fam_barcodes}", flush=True)

        # Check nutritionValues
        nv = p.get("nutritionValues") or {}
        print(f"    nutritionValues keys: {list(nv.keys())}", flush=True)
        sizes = nv.get("sizes") or []
        values = nv.get("values") or []
        print(f"    sizes: {len(sizes)}, values: {len(values)}", flush=True)
        if values:
            v0 = values[0]
            print(f"    first value: {json.dumps(v0, ensure_ascii=False)[:300]}", flush=True)

    # Find if our Lindt 70% or Millennium are in any product
    print("\n--- Searching all 50 results for target products ---", flush=True)
    r2 = requests.get(f"{VICTORY_BASE}/v2/retailers/1470/products", params={
        "q": "שוקולד מריר 80%", "appId": 4, "from": 0, "size": 50
    }, timeout=30)
    data2 = r2.json()
    all_prods = data2.get("products", [])
    print(f"All products (50): checking names...", flush=True)
    for p in all_prods:
        name_obj = (p.get("names") or {}).get("1") or (p.get("names") or {}).get(1) or {}
        name = name_obj.get("name") if isinstance(name_obj, dict) else (name_obj or "")
        pct_m = re.search(r'(\d{2,3})\s*%', name or "")
        if pct_m:
            pct = int(pct_m.group(1))
            pid = p.get("id")
            barcodes = p.get("barcodes") or []
            nv = p.get("nutritionValues") or {}
            has_nutr = bool(nv.get("values"))
            ingr = p.get("ingredients") or p.get("ingredientsInfo") or ""
            print(f"  {pct}% | {name[:60]} | id={pid} | barcodes={barcodes} | nutr={has_nutr} | ingr={bool(ingr)}", flush=True)
