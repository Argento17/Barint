"""
Test: score 7290000525969 (stays A) then 7290110114886 (drops to C in batch).
Looking for state pollution between calls.
"""
import sys, json, pathlib, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from signal_extractor import extract_signals
from nova_proxy import infer_nova
from router_v2 import classify_category
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class

BSIP1_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs")

set_shelf_stats("sugars_g", 9.5, 2.82, "iqr", n=65)

# Score all 17 in order (same as my batch script would)
live_barcodes = [
    "7290000525969",  # stays A
    "7290000136523",
    "7290001247723",
    "7290001247730",
    "7290001247891",
    "7290003009640",  # mover
    "7290004030100",  # mover
    "7290006822192",
    "7290008690713",
    "7290013153395",  # mover
    "7290013153418",
    "7290013608260",  # stays A
    "7290019056355",
    "7290019056591",
    "7290019056720",
    "7290019056737",
    "7290110114886",  # mover
]

for bc in sorted(live_barcodes):  # sorted - same as glob order
    f = BSIP1_DIR / f"bsip1_juice_{bc}.json"
    doc = json.loads(f.read_text(encoding="utf-8"))
    sigs = extract_signals(doc)
    cat = classify_category(doc)
    L3 = sigs["L3_inferred_classifications"]
    nova = infer_nova(doc, L3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, sigs, cat, nova, ev)
    tr = assemble_trace(doc, sigs, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    print(f"{bc}: nova={tr.get('nova_proxy')} score={tr.get('final_score_estimate')} grade={tr.get('grade_estimate')} floors={[f.get('floor_type') for f in (tr.get('floors_applied') or [])]} L1_ing_count={tr.get('L1_observed_signals',{}).get('ingredient_count')}")
