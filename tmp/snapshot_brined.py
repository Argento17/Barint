import json, pathlib
base = pathlib.Path(r"02_products/brined_cheeses/bsip2_outputs/run_brined_005/products")
pre_scores = {}
for d in sorted(base.iterdir()):
    if not d.is_dir(): continue
    tf = d / "bsip2_trace.json"
    if tf.exists():
        t = json.loads(tf.read_text(encoding="utf-8"))
        ir = t.get("input_reference") or {}
        bc = str( t.get("barcode") or ir.get("barcode") or ir.get("product_id") or d.name or "" )
        pre_scores[bc] = {"score": t.get("final_score_estimate"), "grade": t.get("grade_estimate"), "dir": d.name}
pathlib.Path(r"tmp/brined_pre_scores.json").write_text(json.dumps(pre_scores, indent=2), encoding="utf-8")
print("SNAPSHOT SAVED")
print("TOTAL:", len(pre_scores))
print("SAMPLE KEYS:", list(pre_scores.keys())[:3])
