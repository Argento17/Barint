import sys, json, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")

corpus = json.loads(pathlib.Path(r"C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_33_20260621_fix.json").read_text(encoding="utf-8"))
products = corpus["products"]

print("=== WIN products ===")
for i, p in enumerate(products):
    if "WIN" in (p.get("name") or "") or "win" in (p.get("name") or "").lower():
        print(f"  #{i+1} barcode={p['barcode']} name={p['name']}")
        ing = p.get("ingredients_full") or ""
        print(f"  ing: {ing[:300]}")
        print()

print("\n=== Finding collagen products ===")
from constants import PROTEIN_ISOLATE_FAMILIES
collagen_tokens = PROTEIN_ISOLATE_FAMILIES.get("collagen", ())
print(f"Collagen tokens: {collagen_tokens}")
print()
for i, p in enumerate(products):
    ing = (p.get("ingredients_full") or "").lower()
    detected = [tok for tok in collagen_tokens if tok.lower() in ing]
    if detected:
        print(f"#{i+1} barcode={p['barcode']} name={p['name']}")
        print(f"  Detected collagen tokens: {detected}")
        print(f"  ing snippet: {ing[:200]}")
        print()

print("\n=== Rerank table scan for pb-008 (WIN cream milk) ===")
fe = json.loads(pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\protein_combined_frontend_v2.json").read_text(encoding="utf-8"))
for p in fe["products"]:
    if p.get("barcode") == "7290015130028":
        print(f"barcode=7290015130028 name={p.get('name')} score={p.get('score')} grade={p.get('grade')} rank={p.get('rank')}")
        trace = p.get("_scoring_trace", {})
        print(f"  category_subtype={trace.get('category_subtype')}")
        print(f"  caps_applied={trace.get('caps_applied')}")
        ks = trace.get("key_signals", {})
        print(f"  collagen_detected={ks.get('collagen_detected')}")
        print(f"  wholefood_protein={ks.get('wholefood_protein')}")
        print()
