import json
from pathlib import Path

fe = json.loads(Path(r"C:\Bari-brand-fix\bari-web\src\data\comparisons\hard_cheeses_frontend_v3.json").read_text(encoding="utf-8"))
corpus = {}
for f in Path(r"c:\Bari\02_products\hard_cheeses\bsip1_outputs").glob("*.json"):
    rec = json.loads(f.read_text(encoding="utf-8"))
    bc = str(rec.get("barcode") or "").strip()
    if bc and rec.get("brand"):
        corpus[bc] = rec["brand"]

for p in fe["products"]:
    bc = str(p.get("barcode","")).strip()
    b = corpus.get(bc)
    print(bc, "| fe brand:", p.get("brand"), "| corpus:", b, "|", (p.get("name") or "")[:35])
