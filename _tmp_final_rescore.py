"""
TASK-395 Phase 0 — Final canonical rescore for all 6 categories.
Canonical flags from archaeology (all include D4=on as LEGITIMATE per surgical patch).
"""
import os, sys, importlib, json, statistics, hashlib
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

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def rescore_category(canonical_flags, baseline_path, bsip1_dir, shelf_rel=None, bsip1_glob="bsip1_*.json"):
    for k in list(os.environ.keys()):
        if k.startswith("BARI_"): del os.environ[k]
    for k, v in canonical_flags.items():
        os.environ[k] = v

    se = importlib.reload(__import__("score_engine"))
    if shelf_rel:
        se.set_shelf_stats(shelf_rel["nutrient"], shelf_rel["median"], shelf_rel["scale"], shelf_rel.get("scale_type", "iqr"))

    live_data = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    live_products = {}
    for p in live_data.get("products", []):
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
            results.append({"barcode": bc, "name": live_name, "live_score": live_s, "live_grade": live_g,
                "new_score": None, "new_grade": None, "diff": None, "delta": None,
                "match": False, "mclass": "data", "grade_move": False, "note": "not in bsip1"})
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
            cls = "ok" if match else ("config" if diff and diff > 3.0 else "engine")
            delta = round(rs_f - live_f, 1) if rs_f is not None and live_f is not None else None
            new_g = score_to_grade(rs_f)
            grade_move = (live_g != new_g) if rs_f is not None else False
            results.append({"barcode": bc, "name": live_name, "live_score": live_f, "live_grade": live_g,
                "new_score": rs_f, "new_grade": new_g, "diff": diff, "delta": delta,
                "match": match, "mclass": cls, "grade_move": grade_move})
        except Exception as e:
            results.append({"barcode": bc, "name": live_name, "live_score": live_s, "live_grade": live_g,
                "new_score": None, "new_grade": None, "diff": None, "delta": None,
                "match": False, "mclass": "error", "grade_move": False, "note": str(e)})

    if shelf_rel:
        try:
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
        # Canonical: RECAL_P0=on, FAT_TECH=on, GRAN_SUGAR_25G=on, D4=on, SODIUM_CEREAL=off
        # Source: batch_run_cereals_task387_25g.py lines 8-14 explicit
        "flags": {"BARI_RECAL_P0": "on", "BARI_FAT_TECH_V1": "on", "BARI_GRAN_SUGAR_25G_V1": "on",
                  "BARI_D4_SCORE_V1": "on", "BARI_SODIUM_CEREAL": "off",
                  "BARI_SHELF_RELATIVE_V1": "off", "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
                  "BARI_GRAD_SODIUM_V1": "off", "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
                  "BARI_REDLABEL_V1": "off"},
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
summary_rows = []

for cat, cfg in CANONICAL.items():
    print(f"\n=== {cat.upper()} ===")
    r = rescore_category(cfg["flags"], cfg["baseline"], cfg["bsip1"], cfg.get("shelf_rel"), cfg.get("glob", "bsip1_*.json"))
    all_results[cat] = r
    matched = sum(1 for x in r if x["match"])
    total = len(r)
    movers = [x for x in r if not x["match"] and x.get("new_score") is not None]
    data_missing = [x for x in r if x.get("mclass") == "data"]
    grade_movers = [x for x in movers if x.get("grade_move")]
    diffs = [x["diff"] for x in movers if x["diff"] is not None]
    up_moves = [x for x in movers if x.get("delta") is not None and x["delta"] > 0]
    down_moves = [x for x in movers if x.get("delta") is not None and x["delta"] < 0]

    if diffs:
        mn = min(diffs); mx = max(diffs)
        med = statistics.median(diffs)
        sd = statistics.stdev(diffs) if len(diffs) > 1 else 0.0
    else:
        mn = mx = med = sd = 0.0

    print(f"  {matched}/{total} match | movers={len(movers)} | grade_movers={len(grade_movers)} | up={len(up_moves)} | down={len(down_moves)} | data_missing={len(data_missing)}")
    if movers:
        print(f"  Diff range: min={mn:.3f} median={med:.3f} max={mx:.3f} sd={sd:.3f}")
        print("  Full mover list (barcode | live→new | grade_move):")
        for m in sorted(movers, key=lambda x: -(x.get("diff") or 0)):
            gm = f" GRADE:{m['live_grade']}->{m['new_grade']}" if m.get("grade_move") else ""
            name_safe = m["name"].encode("ascii", errors="replace").decode("ascii")[:40]
            print(f"    {m['barcode']}: {m['live_score']}/{m['live_grade']} -> {m['new_score']}/{m['new_grade']} (delta={m['delta']}) {name_safe}{gm}")
    if data_missing:
        print(f"  Data missing from BSIP1 ({len(data_missing)}): {[x['barcode'] for x in data_missing]}")

    summary_rows.append({
        "category": cat, "total": total, "matched": matched, "movers": len(movers),
        "grade_movers": len(grade_movers), "up_moves": len(up_moves), "down_moves": len(down_moves),
        "data_missing": len(data_missing),
        "diff_min": round(mn,3), "diff_med": round(med,3), "diff_max": round(mx,3), "diff_sd": round(sd,3),
        "mover_barcodes": [x["barcode"] for x in sorted(movers, key=lambda x: -(x.get("diff") or 0))],
        "grade_mover_barcodes": [x["barcode"] for x in grade_movers],
    })

print("\n\n=== AGGREGATE SUMMARY ===")
print(f"{'Cat':<12} {'matched':>8} {'total':>6} {'movers':>7} {'grade_mv':>9} {'up':>4} {'down':>5} | diff min/med/max")
for s in summary_rows:
    print(f"  {s['category']:<10} {s['matched']:>8}/{s['total']:<6} {s['movers']:>7} {s['grade_movers']:>9} {s['up_moves']:>4} {s['down_moves']:>5} | {s['diff_min']:.2f}/{s['diff_med']:.2f}/{s['diff_max']:.2f}")

total_products = sum(s["total"] for s in summary_rows)
total_matched = sum(s["matched"] for s in summary_rows)
total_movers = sum(s["movers"] for s in summary_rows)
total_grade_movers = sum(s["grade_movers"] for s in summary_rows)
total_up = sum(s["up_moves"] for s in summary_rows)
print(f"\n  TOTAL: {total_matched}/{total_products} match | movers={total_movers} | grade_movers={total_grade_movers} | up={total_up}")

# Compute sha256 of baseline JSONs
baseline_sha256 = {}
for cat, cfg in CANONICAL.items():
    p = Path(cfg["baseline"])
    if p.exists():
        baseline_sha256[cat] = sha256_file(p)

output = {
    "task": "TASK-395",
    "phase": "Phase-0-Step-3",
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "engine_state": "c90d49ef6 (2026-06-23)",
    "canonical_flags": {k: v["flags"] for k, v in CANONICAL.items()},
    "baseline_sha256": baseline_sha256,
    "summary": summary_rows,
    "results": all_results,
}
out_path = Path("C:/Bari/_baselines/rescore_results_v1.json")
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved to {out_path}")
print(f"SHA256: {sha256_file(out_path)}")
