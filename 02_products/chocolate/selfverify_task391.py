"""Self-verify counts from written artifacts for TASK-391."""
import sys, io, json, pathlib, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")

# Fresh manifest
mf_paths = sorted(glob.glob(str(ROOT / "02_products/chocolate/fresh_rescore_task391_*_manifest.json")))
mf = json.load(open(mf_paths[-1], encoding="utf-8"))
print("=== SELF-VERIFY from written artifacts ===")
print(f"Fresh run_id: {mf['run_id']}")
print(f"Source scrape: {mf['source_scrape']}")
print(f"Funnel: {mf['funnel']}")
tablets = mf['chocolate_tablet']
print(f"Fresh tablet count: {len(tablets)}")
grade_dist = {k: sum(1 for t in tablets if t['grade'] == k) for k in ['C','D','E']}
print(f"Fresh tablet grade dist: {grade_dist}")

# Live frontend
live = json.load(open(ROOT / "bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json", encoding="utf-8"))
prods = live['products']
print(f"\nLive product count: {len(prods)}")
live_dist = {k: sum(1 for p in prods if p['grade'] == k) for k in ['C','D','E']}
print(f"Live grade dist: {live_dist}")

# Match analysis
fresh_bc = {t['barcode']: t for t in tablets}
exact_both = 0
score_drift = 0
grade_moved = 0
missing = []

for p in prods:
    bc = p['barcode']
    if bc not in fresh_bc:
        missing.append(bc)
        continue
    fr = fresh_bc[bc]
    score_match = (str(fr['score']) == str(p['score'])) or (float(fr['score'] or 0) == float(p['score'] or 0))
    grade_match = fr['grade'] == p['grade']
    if score_match and grade_match:
        exact_both += 1
    elif not grade_match:
        grade_moved += 1
    else:
        score_drift += 1

print(f"\nExact score+grade matches: {exact_both} / {len(prods)}")
print(f"Score-only drift (no grade change): {score_drift}")
print(f"Grade movers: {grade_moved}")
print(f"Missing from fresh (not in Shufersal scrape): {len(missing)} -> {missing}")
print(f"\nFlag snapshot: {mf['flag_snapshot']}")
