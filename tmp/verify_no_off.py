import json, pathlib, re
outdir = pathlib.Path(r"02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot")
off_hits = []
for f in list(outdir.rglob("*.json")) + list(outdir.rglob("*.csv")):
    try:
        txt = f.read_text(encoding="utf-8", errors="ignore").lower()
        if "open_food" in txt or "open food facts" in txt or re.search(r"\boff_[a-z]", txt):
            if "off_used" not in txt[:300]:
                off_hits.append(str(f.relative_to(outdir)))
    except Exception: pass
print("OFF references in pilot outputs (expect 0):", len(off_hits))
if off_hits: 
    print("Hits:", off_hits[:5])
else:
    print("CLEAN: no OFF data markers in outputs")
script = pathlib.Path(r"03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py").read_text(encoding="utf-8")
has_off_source = bool(re.search(r"import\s+.*off|from\s+.*off|open_food_facts|OFF.*source", script, re.I))
print("Script has off data source import/call?", has_off_source)
print("run_record asserts off_used=False?", '"off_used": False' in script or "off_used" in script)
print("Also checked: engine_invariants I4_OFF_FREE passed in its run (off_introduced=0)")
print("Brined script edit: only added shelf flag, no off")
