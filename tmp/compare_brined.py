import json, pathlib
pre = json.loads(pathlib.Path(r"tmp/brined_pre_scores.json").read_text(encoding="utf-8"))
base = pathlib.Path(r"02_products/brined_cheeses/bsip2_outputs/run_brined_005/products")
post_scores = {}
for d in sorted(base.iterdir()):
    if not d.is_dir(): continue
    tf = d / "bsip2_trace.json"
    if tf.exists():
        t = json.loads(tf.read_text(encoding="utf-8"))
        ir = t.get("input_reference") or {}
        bc = str( t.get("barcode") or ir.get("barcode") or ir.get("product_id") or d.name or "" )
        post_scores[bc] = {"score": t.get("final_score_estimate"), "grade": t.get("grade_estimate"), "dir": d.name}
pathlib.Path(r"tmp/brined_post_scores.json").write_text(json.dumps(post_scores, indent=2), encoding="utf-8")
print("POST SNAPSHOT SAVED, TOTAL:", len(post_scores))

mismatches = []
for bc, p in pre.items():
    q = post_scores.get(bc, {})
    if p.get("score") != q.get("score") or p.get("grade") != q.get("grade"):
        mismatches.append({"bc": bc, "pre": p, "post": q})
print("MISMATCH COUNT (score or grade):", len(mismatches))
if mismatches:
    print("First few mismatches:", mismatches[:3])
else:
    print("ALL 48 MATCH — byte-identical (score/grade) under flag=on")
print("Brined byte-id check complete.")
