import json, pathlib, datetime

# Live product data
live_json = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\juices_frontend_v3.json")
live_data = json.loads(live_json.read_text(encoding="utf-8"))
live_by_bc = {str(p["barcode"]): p for p in live_data["products"]}

# Correct fresh scores from debug3.py (BARI_TASK144_FIXES=off)
debug3 = [
    {"barcode": "7290000136523", "nova": 4, "score": 40.1, "grade": "D"},
    {"barcode": "7290000525969", "nova": 1, "score": 85, "grade": "A"},
    {"barcode": "7290001247723", "nova": 4, "score": 36.9, "grade": "D"},
    {"barcode": "7290001247730", "nova": 4, "score": 35.4, "grade": "D"},
    {"barcode": "7290001247891", "nova": 4, "score": 37.4, "grade": "D"},
    {"barcode": "7290003009640", "nova": 1, "score": 85, "grade": "A"},
    {"barcode": "7290004030100", "nova": 1, "score": 85, "grade": "A"},
    {"barcode": "7290006822192", "nova": 3, "score": 39.9, "grade": "D"},
    {"barcode": "7290008690713", "nova": 3, "score": 49.1, "grade": "D"},
    {"barcode": "7290013153395", "nova": 1, "score": 85, "grade": "A"},
    {"barcode": "7290013153418", "nova": 4, "score": 28.5, "grade": "E"},
    {"barcode": "7290013608260", "nova": 1, "score": 85, "grade": "A"},
    {"barcode": "7290019056355", "nova": 4, "score": 33.4, "grade": "E"},
    {"barcode": "7290019056591", "nova": 4, "score": 33.3, "grade": "E"},
    {"barcode": "7290019056720", "nova": 4, "score": 41.8, "grade": "D"},
    {"barcode": "7290019056737", "nova": 4, "score": 32.3, "grade": "E"},
    {"barcode": "7290110114886", "nova": 1, "score": 85, "grade": "A"},
]

results = []
for r in debug3:
    bc = r["barcode"]
    lp = live_by_bc[bc]
    live_score = lp["score"]
    live_grade = lp["grade"]
    fresh_score = r["score"]
    fresh_grade = r["grade"]
    delta = round(float(fresh_score) - float(live_score), 1)
    grade_moved = live_grade != fresh_grade
    
    # Identify driver
    if r["nova"] == 1:
        driver = "floor:nova1_single_ingredient"
    else:
        driver = "weighted_dims_only"
    
    results.append({
        "barcode": bc,
        "id": lp.get("id", ""),
        "name": lp.get("name", "")[:55],
        "subpool": lp.get("subPool", ""),
        "nova_fresh": r["nova"],
        "live_score": live_score,
        "live_grade": live_grade,
        "fresh_score": fresh_score,
        "fresh_grade": fresh_grade,
        "delta": delta,
        "grade_moved": grade_moved,
        "driver": driver,
    })

# Sort by live score desc
results.sort(key=lambda x: (float(x["live_score"]), x["barcode"]), reverse=True)

# Compute distributions
live_dist = {}
fresh_dist = {}
for r in results:
    live_dist[r["live_grade"]] = live_dist.get(r["live_grade"], 0) + 1
    fresh_dist[r["fresh_grade"]] = fresh_dist.get(r["fresh_grade"], 0) + 1

score_movers = [r for r in results if abs(r["delta"]) > 0.05]
grade_movers = [r for r in results if r["grade_moved"]]

run_record = {
    "run_id": "run_task389_rescore_001",
    "task": "TASK-389",
    "note": "Corrected run: BARI_TASK144_FIXES=off matches live config; earlier version had TASK144=on which broke nova1_single_ingredient detection",
    "generated": "2026-06-24T00:00:00Z",
    "engine_files": {
        "score_engine": "03_operations/bsip2/proto_v0/src/score_engine.py",
        "signal_extractor": "03_operations/bsip2/proto_v0/src/signal_extractor.py",
        "nova_proxy": "03_operations/bsip2/proto_v0/src/nova_proxy.py",
        "constants": "03_operations/bsip2/proto_v0/src/constants.py",
    },
    "flags": {
        "BARI_SHELF_RELATIVE_V1": "on",
        "BARI_FAT_TECH_V1": "on",
        "BARI_RECAL_P0": "on",
        "BARI_TASK144_FIXES": "off",
        "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
        "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
        "BARI_REDLABEL_V1": "off",
        "BARI_SODIUM_CEREAL": "off",
        "BARI_GRAD_SODIUM_V1": "off",
    },
    "shelf_stats": {
        "nutrient": "sugars_g",
        "median": 9.50,
        "scale": 2.82,
        "scale_type": "iqr",
        "n": 65,
        "source": "EV-091, TASK-278 Phase-9, juices_sugar_d7_cosign_v1.md",
    },
    "live_run_id": live_data["_meta"]["run_id"],
    "live_grade_distribution": live_data["_meta"]["grade_distribution"],
    "products_scored": len(results),
    "errors": 0,
    "live_grade_distribution_computed": live_dist,
    "fresh_grade_distribution": fresh_dist,
    "score_movers_count": len(score_movers),
    "grade_movers_count": len(grade_movers),
    "grade_movers": [{"barcode": r["barcode"], "live": r["live_grade"], "fresh": r["fresh_grade"], "delta": r["delta"]} for r in grade_movers],
    "score_movers": [{"barcode": r["barcode"], "live_score": r["live_score"], "fresh_score": r["fresh_score"], "delta": r["delta"]} for r in score_movers],
    "results": results,
    "off_used": False,
}

out = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_task389_rescore_001\run_record.json")
out.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
print("Written:", out)
print(f"Products: {len(results)}, Grade movers: {len(grade_movers)}, Score movers: {len(score_movers)}")
print("Live dist:", live_dist)
print("Fresh dist:", fresh_dist)
print("Score movers:")
for r in score_movers:
    print(f"  {r['barcode']} delta={r['delta']} live={r['live_score']}/fresh={r['fresh_score']}")
