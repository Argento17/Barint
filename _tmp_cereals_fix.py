import os, sys, importlib, json, statistics
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
print(f"Live products: {len(live_map)}")

for k in list(os.environ.keys()):
    if k.startswith("BARI_"): del os.environ[k]
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_SODIUM_CEREAL"] = "on"
os.environ["BARI_GRAN_SUGAR_25G_V1"] = "on"
os.environ["BARI_D4_SCORE_V1"] = "on"

se = importlib.reload(__import__("score_engine"))

bsip1_dir = Path("C:/Bari/03_operations/bsip1/run_cereals_008/output")
bsip1_map = {}
for f in bsip1_dir.glob("bsip1_*.json"):
    if "audit" in f.name: continue
    try:
        rec = json.loads(f.read_text(encoding="utf-8"))
        bc = str(rec.get("barcode", "")).strip()
        if bc and bc not in bsip1_map: bsip1_map[bc] = f
    except: pass
print(f"BSIP1 files: {len(bsip1_map)}")

matched = 0
movers = []
for bc, live_p in live_map.items():
    live_s = live_p.get("score")
    live_g = live_p.get("grade")
    if bc not in bsip1_map:
        print(f"  NOT IN BSIP1: {bc}")
        continue
    prod = load_product(bsip1_map[bc])
    signals = extract_signals(prod)
    cat_result = classify_category(prod)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(prod, l3)
    eval_result = assign_evaluation_scope(prod, cat_result["category"])
    score_result = se.score_product(prod, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
    rs = trace.get("final_score_estimate")
    rs_f = round(float(rs), 1) if rs is not None else None
    live_f = float(live_s) if live_s is not None else None
    diff = round(abs(rs_f - live_f), 4) if rs_f is not None and live_f is not None else None
    match = diff is not None and diff <= 0.05
    if match:
        matched += 1
    else:
        movers.append({"barcode": bc, "live": live_f, "live_g": live_g, "new": rs_f, "new_g": score_to_grade(rs_f), "diff": diff, "delta": round(rs_f-live_f, 1)})

print(f"Match: {matched}/{len(live_map)}")
if movers:
    print("Movers:")
    for m in sorted(movers, key=lambda x: -(x.get("diff") or 0)):
        print(f"  {m['barcode']}: live={m['live']}/{m['live_g']} new={m['new']}/{m['new_g']} delta={m['delta']}")
