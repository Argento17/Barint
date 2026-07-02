import json
from pathlib import Path

ROOT = Path(r"C:\Bari-brand-fix\bari-web\src\data\comparisons")
CORPUS = {
    "bread_frontend_v3.json": [r"c:\Bari\03_operations\bsip1\run_bread_conform_001\output"],
    "hummus_frontend_v5.json": [r"c:\Bari\02_products\hummus\canonical_bsip1"],
    "hard_cheeses_frontend_v3.json": [r"c:\Bari\02_products\hard_cheeses\bsip1_outputs"],
    "juices_frontend_v3.json": [r"c:\Bari\02_products\juices\bsip1_outputs"],
    "cereals_frontend_v2.json": [r"c:\Bari\03_operations\bsip1\run_cereals_008\output"],
    "granola_frontend_v2.json": [r"c:\Bari\03_operations\bsip1\run_cereals_005\output", r"c:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output"],
}

def load_brands(dirs):
    m = {}
    for d in dirs:
        p = Path(d)
        if not p.exists(): continue
        for f in p.glob("*.json"):
            try: rec = json.loads(f.read_text(encoding="utf-8"))
            except: continue
            bc = str(rec.get("barcode") or "").strip()
            b = rec.get("brand")
            if bc and b and str(b).strip(): m[bc] = str(b).strip()
    return m

for fn in sorted(ROOT.glob("*_frontend*.json")):
    if "archive" in str(fn) or "gates" in str(fn) or "v1.json" in fn.name and fn.name != "milk_frontend_v1.json":
        if fn.name in ("granola_frontend_v1.json", "protein_bars_frontend_v1.json", "cakes_hard_cookies_frontend_v1.json", "milk_frontend_v1.json", "chocolate_bars_frontend_v1.json", "chocolate_tablets_frontend_v1.json"):
            pass
        elif "v1" in fn.name and fn.name not in ("milk_frontend_v1.json", "cakes_hard_cookies_frontend_v1.json", "protein_bars_frontend_v1.json", "chocolate_bars_frontend_v1.json", "chocolate_tablets_frontend_v1.json"):
            continue
    fp = fn
    d = json.loads(fp.read_text(encoding="utf-8"))
    products = d.get("products", [])
    n = len(products)
    has = sum(1 for p in products if p.get("brand"))
    hidden = sum(1 for p in products if p.get("brand") and p["brand"].lower() in (p.get("name") or "").lower())
    corpus = load_brands(CORPUS.get(fn.name, []))
    can = sum(1 for p in products if not p.get("brand") and str(p.get("barcode","")).strip() in corpus)
    miss_bc = [p.get("barcode") for p in products if not p.get("brand") and str(p.get("barcode","")).strip() not in corpus][:2]
    print(f"{fn.name}: n={n} has={has} hidden={hidden} corpus_fill={can} miss_sample={miss_bc}")
