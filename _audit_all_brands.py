import json, subprocess, glob
from pathlib import Path

ROOT = Path(r"c:\Bari\bari-web\src\data\comparisons")
# map frontend file -> list of corpus dirs to backfill from
CORPUS = {
    "bread_frontend_v3.json": [r"c:\Bari\03_operations\bsip1\run_bread_conform_001\output"],
    "hummus_frontend_v5.json": [r"c:\Bari\03_operations\bsip1\run_hummus_001\output"],
    "hard_cheeses_frontend_v2.json": [r"c:\Bari\02_products\hard_cheeses\bsip1_outputs"],
    "juices_frontend_v3.json": [r"c:\Bari\02_products\juices\bsip1_outputs"],
    "granola_frontend_v2.json": [r"c:\Bari\03_operations\bsip1\run_cereals_005\output", r"c:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output"],
    "cereals_frontend_v2.json": [r"c:\Bari\03_operations\bsip1\run_cereals_008\output"],
    "protein_combined_frontend_v2.json": [r"c:\Bari\03_operations\bsip1\score_bars_task362_20260620_143230\output"],
    "protein_bars_frontend_v1.json": [r"c:\Bari\03_operations\bsip1\score_bars_task362_20260620_143230\output"],
    "snacks_frontend_v5.json": [r"c:\Bari\03_operations\bsip1\run_snacks_005\output"],
}

def load_brands(dirs):
    m = {}
    for d in dirs:
        p = Path(d)
        if not p.exists():
            continue
        for f in p.glob("*.json"):
            try:
                rec = json.loads(f.read_text(encoding="utf-8"))
            except:
                continue
            bc = str(rec.get("barcode") or rec.get("gtin") or "").strip()
            b = rec.get("brand")
            if bc and b and str(b).strip():
                m[bc] = str(b).strip()
    return m

files = sorted(ROOT.glob("*_frontend*.json"))
for fp in files:
    if "archive" in str(fp) or "gates_report" in str(fp):
        continue
    try:
        raw = subprocess.check_output(["git", "show", f"origin/master:{fp.as_posix().replace(chr(92),'/')}"])
        d = json.loads(raw)
    except:
        d = json.loads(fp.read_text(encoding="utf-8"))
    products = d.get("products", [])
    n = len(products)
    has = sum(1 for p in products if p.get("brand"))
    hidden = sum(1 for p in products if p.get("brand") and p["brand"].lower() in (p.get("name") or "").lower())
    corpus_dirs = CORPUS.get(fp.name, [])
    corpus_brands = load_brands(corpus_dirs) if corpus_dirs else {}
    can_fill = sum(1 for p in products if not p.get("brand") and str(p.get("barcode","")).strip() in corpus_brands)
    print(f"{fp.name}: n={n} brand={has} hidden={hidden} null={n-has} corpus_backfill={can_fill} corpus_total={len(corpus_brands)}")
