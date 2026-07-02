import os, sys, importlib, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "C:/Bari/03_operations/bsip2/proto_v0/src")
sys.path.insert(0, "C:/Bari/03_operations/page_generator")

from input_loader import load_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from trace_writer import assemble_trace

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]
def score_to_grade(s):
    if s is None: return None
    for grade, threshold in GRADE_SCALE:
        if s >= threshold: return grade
    return "E"

live = json.loads(Path("C:/Bari/bari-web/src/data/comparisons/cereals_frontend_v2.json").read_text(encoding="utf-8"))
live_map = {str(p["barcode"]): p for p in live.get("products", [])}

# Also check what the task387 OFF run produced for mover barcodes
task387_off_dir = Path("C:/Bari/02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_off/products")
task387_on_dir = Path("C:/Bari/02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_25g/products")

print("Checking task387 traces for key barcodes:")
for bc in ["7297488199590", "7290112495433", "7613030979647"]:
    on_trace_f = task387_on_dir / f"bsip1_cereal_{bc}" / "bsip2_trace.json"
    off_trace_f = task387_off_dir / f"bsip1_cereal_{bc}" / "bsip2_trace.json"
    on_score = None
    off_score = None
    if on_trace_f.exists():
        t = json.loads(on_trace_f.read_text(encoding="utf-8"))
        on_score = t.get("final_score_estimate")
    if off_trace_f.exists():
        t = json.loads(off_trace_f.read_text(encoding="utf-8"))
        off_score = t.get("final_score_estimate")
    live_s = live_map.get(bc, {}).get("score")
    print(f"  {bc}: task387_off={off_score} task387_on={on_score} live={live_s}")

print()
print("Key insight: did task387 rescore ALL 20 products or only the sugar>=25 movers?")
print("The live page scores = task387_on scores (applied over the D4 patched live page)")
