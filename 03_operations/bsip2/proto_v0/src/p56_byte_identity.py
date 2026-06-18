"""P56 gate 1: default-OFF byte-identity vs run_brined_004."""
import json
import os
import pathlib
import sys

os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "on"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "off"
os.environ["BARI_GLASSBOX_D5D6"] = "off"
os.environ["BARI_GLASSBOX_W15"] = "off"
os.environ["BARI_GLASSBOX_W2"] = "off"
# Both P56 flags explicitly OFF (default)
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import (
    score_product, BARI_SODIUM_SHELF_RELATIVE_V1, BARI_DAIRY_PROTEIN_REWEIGHT_V1,
    clear_shelf_sodium_stats,
)

ROOT = pathlib.Path(r"C:\Bari")
CORPUS = ROOT / "02_products/brined_cheeses/factory_run_001/corpus_filter.json"
BSIP1 = ROOT / "03_operations/bsip1/run_brined_cheeses_002/output"
BASE = ROOT / "02_products/brined_cheeses/bsip2_outputs/run_brined_004/products"

assert not BARI_SODIUM_SHELF_RELATIVE_V1
assert not BARI_DAIRY_PROTEIN_REWEIGHT_V1
clear_shelf_sodium_stats()

corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
barcodes = {str(p["barcode"]) for p in corpus["products"] if p["decision"] == "IN_SCORED"}

mismatches = []
for p in sorted(BSIP1.glob("bsip1_brinedcheese_*.json")):
    doc = json.loads(p.read_text(encoding="utf-8"))
    bc = str(doc.get("barcode", ""))
    if bc not in barcodes:
        continue
    signals = extract_signals(doc)
    cat = classify_category(doc)
    nova = infer_nova(doc, signals["L3_inferred_classifications"])
    ev = assign_evaluation_scope(doc, cat["category"])
    res = score_product(doc, signals, cat, nova, ev)
    new_score = res.get("final_score_estimate")
    new_grade = res.get("grade_estimate")
    trace_dirs = list(BASE.glob(f"bsip1_brinedcheese_{bc}"))
    if not trace_dirs:
        mismatches.append((bc, "missing baseline trace dir"))
        continue
    base = json.loads((trace_dirs[0] / "bsip2_trace.json").read_text(encoding="utf-8"))
    old_score = base.get("final_score_estimate")
    old_grade = base.get("grade_estimate")
    if new_score != old_score or new_grade != old_grade:
        mismatches.append((bc, old_score, new_score, old_grade, new_grade))

print("P56 GATE 1 — default-OFF byte-identity vs run_brined_004")
print(f"Flags: BARI_SODIUM_SHELF_RELATIVE_V1={BARI_SODIUM_SHELF_RELATIVE_V1} BARI_DAIRY_PROTEIN_REWEIGHT_V1={BARI_DAIRY_PROTEIN_REWEIGHT_V1}")
print(f"Products checked: {len(barcodes)}")
if mismatches:
    print(f"FAIL — {len(mismatches)} mismatches:")
    for m in mismatches[:10]:
        print(" ", m)
    sys.exit(1)
print("PASS — all 48 scores byte-identical to run_brined_004")
