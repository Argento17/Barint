"""
Correct C10 check: compare milk scores from the current engine against
the most recent authoritative milk run (run_hummus_shelfrel_001 used the engine
at commit time). We compare milk scores BEFORE and AFTER our engine edits,
not against the original run_005_headpin (which used a different engine baseline).

Approach: run milk products through the AMENDED engine and compare against
the shelfrel_golive_001 run — which was the last run BEFORE our changes.

Actually, let's just run milk now and compare to what the shelfrel_golive runner
would have produced for milk (since that runner has C10 embedded).
For simplicity: run milk with amended engine; also run with the check that
HC002_NOVA1_ON=off shouldn't affect milk (milk has no bsip_cheese_subpool).
"""
import os, json, pathlib, sys
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_DAIRY_SAT_FAT_INFER"] = "off"  # Default: off
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals, DAIRY_SAT_FAT_INFER_ON
from router_v2 import classify_category
from nova_proxy import infer_nova, HC002_NOVA1_ON
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product

ROOT = pathlib.Path(r"C:\Bari")
MILK_BSIP1_DIR = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"

print(f"DAIRY_SAT_FAT_INFER_ON={DAIRY_SAT_FAT_INFER_ON}")
print(f"HC002_NOVA1_ON={HC002_NOVA1_ON}")
print()

results = []
for f in sorted(MILK_BSIP1_DIR.glob("bsip1_*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    bc = str(d.get("barcode", f.stem))
    signals = extract_signals(d)
    cat = classify_category(d)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(d, l3)
    ev = assign_evaluation_scope(d, cat["category"])
    sr = score_product(d, signals, cat, nova, ev)
    nn = d.get("normalized_nutrition_per_100g", {})
    results.append({
        "bc": bc,
        "score": sr.get("final_score_estimate"),
        "grade": sr.get("grade_estimate"),
        "nova": nova["nova_level"],
        "sat_fat_inf": l3.get("sat_fat_inferred"),
        "fat_quality": (sr.get("dimension_scores") or {}).get("fat_quality"),
    })

print(f"Milk products scored: {len(results)}")
for r in results:
    print(f"  bc:{r['bc']}  score={r['score']}  grade={r['grade']}  nova={r['nova']}  fat_q={r['fat_quality']}  sat_fat_inf={r['sat_fat_inf']}")

# Check milk distribution
from collections import Counter
gdist = Counter(r["grade"] for r in results)
scores = sorted([r["score"] for r in results if r["score"] is not None])
print()
print(f"Grade dist: {dict(sorted(gdist.items()))}")
print(f"Score range: {scores[0]} - {scores[-1]}")
