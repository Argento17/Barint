"""
Full HC corpus rescore under amended engine (EV-099 revert).
Sanity check only — no comp JSON update, no go-live.
"""
import os, json, pathlib, sys
from collections import Counter
import statistics

os.environ.setdefault("BARI_RECAL_P0", "on")
os.environ.setdefault("BARI_SHELF_RELATIVE_V1", "on")
os.environ.setdefault("BARI_FAT_TECH_V1", "on")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from constants import FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE

HC_BSIP1_DIR = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_outputs")

set_shelf_stats("fat_saturated_g", FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE, "mad", 22)

results = []
for fpath in sorted(HC_BSIP1_DIR.glob("bsip1_*.json")):
    d = json.loads(fpath.read_text(encoding="utf-8"))
    bc = str(d.get("barcode", fpath.stem))
    signals = extract_signals(d)
    cat = classify_category(d)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(d, l3)
    ev = assign_evaluation_scope(d, cat["category"])
    sr = score_product(d, signals, cat, nova, ev)
    nn = d.get("normalized_nutrition_per_100g", {})
    results.append({
        "bc": bc,
        "nova": nova["nova_level"],
        "score": sr.get("final_score_estimate"),
        "grade": sr.get("grade_estimate"),
        "sat_fat_g": nn.get("fat_saturated_g"),
        "fat_g": nn.get("fat_g"),
        "sat_fat_inferred": l3.get("sat_fat_inferred"),
        "binding_cap": sr.get("binding_cap"),
        "caps": [c["rule"] for c in sr.get("caps_applied", [])],
    })

clear_shelf_stats("fat_saturated_g")

# Distribution
scores = [r["score"] for r in results if r["score"] is not None]
grades = Counter(r["grade"] for r in results)
print(f"=== HC SANITY RESCORE (EV-099 engine) ===")
print(f"N={len(results)}")
print(f"Grade dist: {dict(sorted(grades.items()))}")
if scores:
    print(f"Score range: min={min(scores)} max={max(scores)} mean={statistics.mean(scores):.1f}")

print()
print("Products at score <= 45 (should be the ~8 affected by revert):")
low = sorted([r for r in results if r["score"] is not None and r["score"] <= 45], key=lambda x: x["score"])
for r in low:
    print(f"  bc:{r['bc']}  nova={r['nova']}  score={r['score']}  grade={r['grade']}  sat_fat_inf={r['sat_fat_inferred']}  fat={r['fat_g']}  sat_fat_label={r['sat_fat_g']}")

print()
print("Products with nova=1 (should be 0 after revert if all are short-ingredient dairy):")
nova1 = [r for r in results if r["nova"] == 1]
print(f"  count={len(nova1)}")
for r in nova1:
    print(f"  bc:{r['bc']}  score={r['score']}  grade={r['grade']}")
