"""
TASK-389 STAGE 1: Juices freshness re-score check.

Scores the 17 curated live products with the current engine using the
documented shelf-relative config (BARI_SHELF_RELATIVE_V1=on, median=9.50, scale=2.82, n=65).
Outputs a comparison table: live score/grade vs fresh score/grade.

OFF ban: absolute. No external data sources used.
Traces written to run_task389_rescore_001 directory for auditability.
"""
import os, sys, json, pathlib, datetime

# ── Flag config (must match live config) ──────────────────────────────────────
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_TASK144_FIXES"] = "on"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    score_to_grade,
    SUGAR_SHELF_REL_JUICES_MEDIAN,
    SUGAR_SHELF_REL_JUICES_SCALE,
)

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_DIR = ROOT / "02_products" / "juices" / "bsip1_outputs"
LIVE_JSON = ROOT / "bari-web" / "src" / "data" / "comparisons" / "juices_frontend_v3.json"
OUT_DIR = ROOT / "02_products" / "juices" / "bsip2_outputs" / "run_task389_rescore_001"
(OUT_DIR / "products").mkdir(parents=True, exist_ok=True)

def score_one(doc):
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    tr = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    return tr


def main():
    # Load live page products
    live_data = json.loads(LIVE_JSON.read_text(encoding="utf-8"))
    live_products = live_data["products"]
    live_by_barcode = {str(p["barcode"]): p for p in live_products}
    live_barcodes = set(live_by_barcode.keys())

    print(f"Live page: {len(live_products)} products")
    print(f"Live run_id: {live_data['_meta']['run_id']}")
    print(f"Live grade dist: {live_data['_meta']['grade_distribution']}")
    print()

    # Set juices shelf stats
    set_shelf_stats(
        "sugars_g",
        SUGAR_SHELF_REL_JUICES_MEDIAN,
        SUGAR_SHELF_REL_JUICES_SCALE,
        "iqr",
        n=65,  # corpus size per EV-091
    )
    print(f"Shelf stats set: sugars_g median={SUGAR_SHELF_REL_JUICES_MEDIAN} scale={SUGAR_SHELF_REL_JUICES_SCALE} n=65")
    print()

    # Load and score only the 17 curated products
    results = []
    errors = []

    for bsip1_file in sorted(BSIP1_DIR.glob("bsip1_juice_*.json")):
        doc = json.loads(bsip1_file.read_text(encoding="utf-8"))
        bc = str(doc.get("barcode", ""))
        if bc not in live_barcodes:
            continue  # only score the 17 curated live products

        try:
            tr = score_one(doc)
            write_trace(tr, OUT_DIR)
        except Exception as e:
            errors.append({"barcode": bc, "error": str(e)})
            print(f"ERROR [{bc}]: {e}")
            continue

        fresh_score = tr.get("final_score_estimate")
        fresh_grade = tr.get("grade_estimate")
        live_p = live_by_barcode[bc]
        live_score = live_p["score"]
        live_grade = live_p["grade"]
        name = doc.get("canonical_name_he", live_p.get("name", ""))

        delta = round(float(fresh_score) - float(live_score), 1) if fresh_score is not None else None
        grade_moved = live_grade != fresh_grade

        # Identify driver from trace
        floors_applied = tr.get("floors_applied", [])
        caps_applied = tr.get("caps_applied", [])
        pens_applied = [p for p in (tr.get("penalties_considered") or []) if p.get("fired")]
        sr_note = None
        # Look for shelf-rel note in trace
        for key in ("_sr_juice_sugar_note", "sr_juice_sugar_note"):
            if key in tr:
                sr_note = tr[key]
                break

        driver_parts = []
        if floors_applied:
            for f in floors_applied:
                driver_parts.append(f"floor:{f.get('floor_type', f.get('floor_value', '?'))}")
        if caps_applied:
            for c in caps_applied:
                driver_parts.append(f"cap:{c.get('rule', '?')}")
        if pens_applied:
            for p in pens_applied:
                driver_parts.append(f"pen:{p.get('rule', '?')}")
        driver = "; ".join(driver_parts) if driver_parts else "weighted_dims"

        results.append({
            "barcode": bc,
            "id": live_p.get("id", ""),
            "name": name[:50],
            "subpool": live_p.get("subPool", doc.get("juice_sub_pool", "")),
            "sugars_g": doc.get("normalized_nutrition_per_100g", {}).get("sugars_g"),
            "live_score": live_score,
            "live_grade": live_grade,
            "fresh_score": fresh_score,
            "fresh_grade": fresh_grade,
            "delta": delta,
            "grade_moved": grade_moved,
            "driver": driver,
        })

    clear_shelf_stats("sugars_g")

    # Sort by live score desc
    results.sort(key=lambda x: (x["live_score"], x["barcode"]), reverse=True)

    # Print table
    print("=" * 120)
    print(f"{'Barcode':<15} {'ID':<8} {'SubPool':<12} {'Sugar':<6} {'Live':>10} {'Fresh':>10} {'Delta':>6} {'GradeMov':<9} Driver")
    print("=" * 120)
    for r in results:
        gm = "*** GRADE ***" if r["grade_moved"] else ""
        print(f"{r['barcode']:<15} {r['id']:<8} {r['subpool']:<12} {str(r.get('sugars_g','?')):<6} "
              f"{str(r['live_score'])+'/'+r['live_grade']:>10} {str(r['fresh_score'])+'/'+str(r['fresh_grade']):>10} "
              f"{('+' if r['delta'] and r['delta']>0 else '')+str(r['delta'] or '?'):>6} {gm:<13} {r['driver']}")

    print()
    print(f"Total scored: {len(results)}, Errors: {len(errors)}")

    # Grade distributions
    live_dist = {}
    fresh_dist = {}
    score_movers = [r for r in results if r["delta"] is not None and abs(r["delta"]) > 0.05]
    grade_movers = [r for r in results if r["grade_moved"]]

    for r in results:
        live_dist[r["live_grade"]] = live_dist.get(r["live_grade"], 0) + 1
        if r["fresh_grade"]:
            fresh_dist[str(r["fresh_grade"])] = fresh_dist.get(str(r["fresh_grade"]), 0) + 1

    print()
    print("=== GRADE DISTRIBUTION ===")
    all_grades = sorted(set(list(live_dist.keys()) + list(fresh_dist.keys())))
    for g in all_grades:
        print(f"  {g}: live={live_dist.get(g, 0)}  fresh={fresh_dist.get(g, 0)}")

    print()
    print(f"Score movers (|delta|>0): {len(score_movers)}")
    print(f"Grade movers: {len(grade_movers)}")
    if grade_movers:
        print("  GRADE MOVERS (TRIPWIRE-1):")
        for r in grade_movers:
            print(f"    {r['barcode']} {r['name']}: {r['live_grade']} -> {r['fresh_grade']} (delta={r['delta']})")

    print()
    print("=== MOVER DETAIL ===")
    for r in score_movers:
        print(f"  {r['barcode']} {r['id']} delta={r['delta']} live={r['live_score']}/{r['live_grade']} fresh={r['fresh_score']}/{r['fresh_grade']} driver={r['driver']}")

    # Save run record
    run_record = {
        "run_id": "run_task389_rescore_001",
        "task": "TASK-389",
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GRAD_SODIUM_V1": "off",
        },
        "shelf_stats": {
            "nutrient": "sugars_g",
            "median": SUGAR_SHELF_REL_JUICES_MEDIAN,
            "scale": SUGAR_SHELF_REL_JUICES_SCALE,
            "scale_type": "iqr",
            "n": 65,
        },
        "live_run_id": live_data["_meta"]["run_id"],
        "live_grade_distribution": live_data["_meta"]["grade_distribution"],
        "products_scored": len(results),
        "errors": len(errors),
        "fresh_grade_distribution": fresh_dist,
        "score_movers_count": len(score_movers),
        "grade_movers_count": len(grade_movers),
        "grade_movers": [{"barcode": r["barcode"], "live": r["live_grade"], "fresh": r["fresh_grade"], "delta": r["delta"]} for r in grade_movers],
        "results": results,
        "off_used": False,
    }
    record_path = OUT_DIR / "run_record.json"
    record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRun record → {record_path}")
    print(f"Traces → {OUT_DIR / 'products'}")


if __name__ == "__main__":
    main()
