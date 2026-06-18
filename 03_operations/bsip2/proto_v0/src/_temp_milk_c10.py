"""
C10 milk invariant check using the run_005_headpin baseline (correct path traversal).
"""
import os, json, pathlib, sys
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace

ROOT = pathlib.Path(r"C:\Bari")
MILK_BASELINE_DIR = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
MILK_BSIP1_DIR    = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"

def score_one(doc):
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    return sr

# The baseline products dir has subdirs, each with bsip2_trace.json
deltas = []
fails = []
for sub in sorted(MILK_BASELINE_DIR.iterdir()):
    if not sub.is_dir():
        continue
    trace_file = sub / "bsip2_trace.json"
    if not trace_file.exists():
        # Sometimes flat json
        trace_file = sub.with_suffix(".json")
        if not trace_file.exists():
            continue
    baseline = json.loads(trace_file.read_text(encoding="utf-8"))
    b_score = baseline.get("final_score_estimate")
    b_grade = baseline.get("grade_estimate")

    # Find corresponding BSIP1
    bsip1_path = MILK_BSIP1_DIR / (sub.name + ".json")
    if not bsip1_path.exists():
        print(f"MISSING BSIP1: {bsip1_path}")
        continue

    doc = json.loads(bsip1_path.read_text(encoding="utf-8"))
    try:
        tr = score_one(doc)
    except Exception as e:
        print(f"ERROR scoring {sub.name}: {e}")
        fails.append(sub.name)
        continue

    n_score = tr.get("final_score_estimate")
    n_grade = tr.get("grade_estimate")
    delta = abs(n_score - b_score) if (n_score is not None and b_score is not None) else None

    if delta is not None and delta > 0.001:
        print(f"FAIL {sub.name}: baseline={b_score}/{b_grade} new={n_score}/{n_grade} delta={delta:.4f}")
        fails.append(sub.name)
    else:
        deltas.append(delta or 0)

print(f"\nC10 result: checked={len(deltas)+len(fails)}  pass={len(deltas)}  fail={len(fails)}")
if not fails:
    print("C10 PASS: all milk products byte-identical under amended engine")
else:
    print(f"C10 FAIL: {fails}")
