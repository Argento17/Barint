import os, sys, importlib, json, statistics
from pathlib import Path
from datetime import datetime, timezone
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

def rescore_category(canonical_flags, baseline_path, bsip1_dir, shelf_rel=None, bsip1_glob="bsip1_*.json"):
    for k in list(os.environ.keys()):
        if k.startswith("BARI_"): del os.environ[k]
    for k, v in canonical_flags.items():
        os.environ[k] = v

    se = importlib.reload(__import__("score_engine"))
    if shelf_rel:
        if shelf_rel.get("api") == "sodium_ev056":
            se.set_shelf_sodium_stats(shelf_rel["median"], shelf_rel["scale"])
        else:
            se.set_shelf_stats(shelf_rel["nutrient"], shelf_rel["median"], shelf_rel["scale"], shelf_rel.get("scale_type", "iqr"))

    live_products = {}
    data = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    for p in data.get("products", []):
        bc = str(p.get("barcode", "")).strip()
        if bc: live_products[bc] = p

    bsip1_map = {}
    for f in Path(bsip1_dir).glob(bsip1_glob):
        if "audit" in f.name: continue
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            bc = str(rec.get("barcode", "")).strip()
            if bc and bc not in bsip1_map and rec.get("file_type") != "report":
                bsip1_map[bc] = f
        except: pass

    results = []
    for bc, live_p in live_products.items():
        live_s = live_p.get("score")
        live_g = live_p.get("grade")
        live_name = live_p.get("name", "")
        if bc not in bsip1_map:
            results.append({"barcode": bc, "name": live_name, "live_score": live_s, "live_grade": live_g, "new_score": None, "new_grade": None, "diff": None, "delta": None, "match": False, "mclass": "data", "grade_move": False, "note": "not in bsip1"})
            continue
        try:
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
            cls = "ok" if match else ("data" if bc not in bsip1_map else ("config" if diff and diff > 3.0 else "engine"))
            delta = round(rs_f - live_f, 1) if rs_f is not None and live_f is not None else None
            grade_move = (live_g != score_to_grade(rs_f)) if rs_f is not None else False
            results.append({"barcode": bc, "name": live_name, "live_score": live_f, "live_grade": live_g, "new_score": rs_f, "new_grade": score_to_grade(rs_f), "diff": diff, "delta": delta, "match": match, "mclass": cls, "grade_move": grade_move})
        except Exception as e:
            results.append({"barcode": bc, "name": live_name, "live_score": live_s, "live_grade": live_g, "new_score": None, "new_grade": None, "diff": None, "delta": None, "match": False, "mclass": "error", "grade_move": False, "note": str(e)})

    if shelf_rel:
        try:
            if shelf_rel.get("api") == "sodium_ev056":
                se.clear_shelf_sodium_stats()
            else:
                se.clear_shelf_stats(shelf_rel["nutrient"])
        except: pass

    return results

CANONICAL = {
    "bread": {
        "flags": {"BARI_RECAL_P0": "on", "BARI_FAT_TECH_V1": "on", "BARI_D4_SCORE_V1": "on",
                  "BARI_SHELF_RELATIVE_V1": "off", "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
                  "BARI_GRAD_SODIUM_V1": "off", "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
                  "BARI_REDLABEL_V1": "off", "BARI_SODIUM_CEREAL": "off"},
        "baseline": "C:/Bari/bari-web/src/data/comparisons/bread_frontend_v3.json",
        "bsip1": "C:/Bari/03_operations/bsip1/run_bread_conform_001/output",
        "shelf_rel": None,
        "glob": "bsip1_*.json",
    },
    "cakes": {
        "flags": {"BARI_SHELF_RELATIVE_V1": "on", "BARI_FAT_TECH_V1": "on", "BARI_D4_SCORE_V1": "on",
                  "BARI_RECAL_P0": "off", "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
                  "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off", "BARI_REDLABEL_V1": "off",
                  "BARI_SODIUM_CEREAL": "off", "BARI_GRAD_SODIUM_V1": "off"},
        "baseline": "C:/Bari/bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json",
        "bsip1": "C:/Bari/03_operations/bsip1/run_cakes_001/output",
        "shelf_rel": {"nutrient": "sugars_g", "median": 29.0, "scale": 9.044, "scale_type": "iqr"},
        "glob": "bsip1_cakes_*.json",
    },
    "cereals": {
        "flags": {"BARI_RECAL_P0": "on", "BARI_FAT_TECH_V1": "on", "BARI_SODIUM_CEREAL": "on",
                  "BARI_D4_SCORE_V1": "on", "BARI_SHELF_RELATIVE_V1": "off",
                  "BARI_SODIUM_SHELF_RELATIVE_V1": "off", "BARI_GRAD_SODIUM_V1": "off",
                  "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off", "BARI_REDLABEL_V1": "off"},
        "baseline": "C:/Bari/bari-web/src/data/comparisons/cereals_frontend_v2.json",
        "bsip1": "C:/Bari/03_operations/bsip1/run_cereals_008/output",
        "shelf_rel": None,
        "glob": "bsip1_*.json",
    },
    "cheese": {
        "flags": {"BARI_SHELF_RELATIVE_V1": "on", "BARI_FAT_TECH_V1": "on", "BARI_RECAL_P0": "on",
                  "BARI_D4_SCORE_V1": "on", "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
                  "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off", "BARI_REDLABEL_V1": "off",
                  "BARI_SODIUM_CEREAL": "off", "BARI_GRAD_SODIUM_V1": "off"},
        "baseline": "C:/Bari/bari-web/src/data/comparisons/cheese_frontend_v4.json",
        "bsip1": "C:/Bari/03_operations/bsip1/run_cheese_003/output",
        "shelf_rel": {"nutrient": "fat_saturated_g", "median": 16.05, "scale": 2.0756, "scale_type": "iqr"},
        "glob": "bsip1_*.json",
    },
    "granola": {
        "flags": {"BARI_RECAL_P0": "on", "BARI_FAT_TECH_V1": "on", "BARI_D4_SCORE_V1": "on",
                  "BARI_SHELF_RELATIVE_V1": "off", "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
                  "BARI_GRAD_SODIUM_V1": "off", "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
                  "BARI_REDLABEL_V1": "off", "BARI_SODIUM_CEREAL": "off"},
        "baseline": "C:/Bari/bari-web/src/data/comparisons/granola_frontend_v1.json",
        "bsip1": "C:/Bari/03_operations/bsip1/run_cereals_005/output",
        "shelf_rel": None,
        "glob": "bsip1_*.json",
    },
    "milk": {
        "flags": {"BARI_FAT_TECH_V1": "on", "BARI_D4_SCORE_V1": "on",
                  "BARI_RECAL_P0": "off", "BARI_SHELF_RELATIVE_V1": "on",
                  "BARI_REDLABEL_V1": "off", "BARI_DAIRY_SAT_FAT_INFER": "off",
                  "BARI_SODIUM_SHELF_RELATIVE_V1": "off", "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
                  "BARI_GRAD_SODIUM_V1": "off", "BARI_SODIUM_CEREAL": "off"},
        "baseline": "C:/Bari/bari-web/src/data/comparisons/milk_frontend_v1.json",
        "bsip1": "C:/Bari/03_operations/bsip1/run_milk_002/output",
        "shelf_rel": None,
        "glob": "bsip1_*.json",
    },
}

all_results = {}
summary_table = []
for cat, cfg in CANONICAL.items():
    print(f"Rescoring {cat}...")
    r = rescore_category(cfg["flags"], cfg["baseline"], cfg["bsip1"], cfg.get("shelf_rel"), cfg.get("glob", "bsip1_*.json"))
    all_results[cat] = r
    matched = sum(1 for x in r if x["match"])
    total = len(r)
    movers = [x for x in r if not x["match"] and x.get("new_score") is not None]
    grade_movers = [x for x in movers if x.get("grade_move")]
    diffs = [x["diff"] for x in movers if x["diff"] is not None]
    up_moves = [x for x in movers if x.get("delta") is not None and x["delta"] > 0]
    if diffs:
        mn = min(diffs)
        mx = max(diffs)
        med = statistics.median(diffs)
        sd = statistics.stdev(diffs) if len(diffs) > 1 else 0.0
    else:
        mn = mx = med = sd = 0.0
    entry = {
        "category": cat, "total": total, "matched": matched, "movers": len(movers),
        "grade_movers": len(grade_movers), "up_moves": len(up_moves),
        "diff_min": round(mn,3), "diff_max": round(mx,3), "diff_med": round(med,3), "diff_sd": round(sd,3)
    }
    summary_table.append(entry)
    print(f"  {matched}/{total} match | movers={len(movers)} | grade_movers={len(grade_movers)} | up={len(up_moves)}")
    if movers:
        print(f"  Movers (diff range {mn:.2f}-{mx:.2f}):")
        for m in sorted(movers, key=lambda x: -(x.get("diff") or 0))[:5]:
            print(f"    {m['barcode']}: live={m['live_score']}/{m['live_grade']} new={m['new_score']}/{m['new_grade']} delta={m['delta']}")

print("\nSummary table:")
for s in summary_table:
    print(f"  {s['category']}: {s['matched']}/{s['total']} | movers={s['movers']} | grade_movers={s['grade_movers']} | up={s['up_moves']} | diff[min/med/max]={s['diff_min']}/{s['diff_med']}/{s['diff_max']}")

output = {
    "results": all_results,
    "summary": summary_table,
    "canonical_flags": {k: v["flags"] for k, v in CANONICAL.items()},
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
}
with open("C:/Bari/_tmp_canonical_rescore.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("Saved to C:/Bari/_tmp_canonical_rescore.json")
