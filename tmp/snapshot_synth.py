import json, pathlib
base = pathlib.Path(r"02_products/breakfast_cereals/bsip2_outputs/run_cereals_synthesis_001/products")
synth = {}
for d in sorted(base.iterdir()):
    if not d.is_dir(): continue
    tf = d / "bsip2_trace.json"
    if tf.exists():
        t = json.loads(tf.read_text(encoding="utf-8"))
        bc = str( t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or d.name.replace("bsip1_","") )
        synth[bc] = {"score": t.get("final_score_estimate"), "grade": t.get("grade_estimate")}
pathlib.Path(r"tmp/synthesis_001_scores.json").write_text(json.dumps(synth, indent=2), encoding="utf-8")
print("SYNTHESIS SNAPSHOT SAVED, TOTAL:", len(synth))
print("SAMPLE bc 7290100000042:", synth.get("7290100000042"))
print("SAMPLE bc 5054568100022:", synth.get("5054568100022"))
print("SAMPLE bc 4013228100001:", synth.get("4013228100001"))
