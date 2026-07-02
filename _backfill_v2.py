import json, glob
from pathlib import Path

ROOT = Path(r"c:\Bari\bari-web\src\data\comparisons")
DASH = [" \u2014 ", " \u2013 ", " - "]

def strip_brand(name, brand):
    name, brand = name.strip(), brand.strip()
    if not name or not brand: return name
    nl, bl = name.lower(), brand.lower()
    for sep in DASH:
        suf = sep + brand
        if nl.endswith(suf.lower()):
            return name[:-len(suf)].strip()
    if nl.startswith(bl):
        rest = name[len(brand):].strip().lstrip(":,\u060C-–— ").strip()
        if rest: return rest
    return name

def load_brands(*dirs):
    m = {}
    for d in dirs:
        for f in glob.glob(str(Path(d) / "*.json")):
            try: rec = json.loads(Path(f).read_text(encoding="utf-8"))
            except: continue
            bc = str(rec.get("barcode") or "").strip()
            if bc and rec.get("brand"):
                m[bc] = str(rec["brand"]).strip()
    return m

brands = load_brands(
    r"c:\Bari\03_operations\bsip1\run_cakes_001\output",
    r"c:\Bari\03_operations\bsip1\run_cookies_001\output",
)

files = [
    "milk_frontend_v1.json",
    "cheese_frontend_v4.json",
    "cakes_hard_cookies_frontend_v1.json",
    "cookies_coffee_frontend_v2.json",
    "brined_cheeses_frontend_v2.json",
    "chocolate_bars_frontend_v1.json",
    "chocolate_tablets_frontend_v1.json",
    "snacks_frontend_v5.json",
    "juices_frontend_v3.json",
    "protein_combined_frontend_v2.json",
    "granola_frontend_v2.json",
    "cereals_frontend_v2.json",
]

for fn in files:
    fp = ROOT / fn
    if not fp.exists(): continue
    fe = json.loads(fp.read_text(encoding="utf-8"))
    products = fe.get("products", [])
    filled = stripped = 0
    for p in products:
        bc = str(p.get("barcode", "")).strip()
        if not p.get("brand") and bc in brands:
            p["brand"] = brands[bc]
            filled += 1
        brand = (p.get("brand") or "").strip()
        if brand:
            new = strip_brand(p.get("name", ""), brand)
            if new != p.get("name"):
                p["name"] = new
                stripped += 1
    fp.write_text(json.dumps(fe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(fn, "filled", filled, "stripped", stripped)
