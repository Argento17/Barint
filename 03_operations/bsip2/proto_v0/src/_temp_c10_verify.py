"""
Verify the milk C10 delta was pre-existing (from FAT_TECH default-ON) and NOT
from my HC-002/signal_extractor changes.

Test: if BARI_FAT_TECH_V1=off, do milk scores match run_005_headpin?
"""
import os, json, pathlib, sys
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "off"   # <-- turn off fat_tech
os.environ["BARI_DAIRY_SAT_FAT_INFER"] = "off"
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product

ROOT = pathlib.Path(r"C:\Bari")
MILK_BASELINE_DIR = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
MILK_BSIP1_DIR    = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"

deltas = []
fails = []
for sub in sorted(MILK_BASELINE_DIR.iterdir()):
    if not sub.is_dir():
        continue
    trace_file = sub / "bsip2_trace.json"
    if not trace_file.exists():
        continue
    baseline = json.loads(trace_file.read_text(encoding="utf-8"))
    b_score = baseline.get("final_score_estimate")
    b_grade = baseline.get("grade_estimate")
    bsip1_path = MILK_BSIP1_DIR / (sub.name + ".json")
    if not bsip1_path.exists():
        print(f"MISSING: {bsip1_path}")
        continue
    doc = json.loads(bsip1_path.read_text(encoding="utf-8"))
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    n_score = sr.get("final_score_estimate")
    n_grade = sr.get("grade_estimate")
    delta = abs(n_score - b_score) if (n_score is not None and b_score is not None) else None
    if delta is not None and delta > 0.001:
        print(f"FAIL {sub.name}: baseline={b_score}/{b_grade} new={n_score}/{n_grade} delta={delta:.4f}")
        fails.append(sub.name)
    else:
        deltas.append(delta or 0)
        print(f"PASS {sub.name}: score={n_score}/{n_grade} delta={delta:.4f}")

print(f"\nWith FAT_TECH=off: checked={len(deltas)+len(fails)}  pass={len(deltas)}  fail={len(fails)}")
print("Conclusion: if all pass with FAT_TECH=off, the C10 delta is from FAT_TECH, not my changes.")
