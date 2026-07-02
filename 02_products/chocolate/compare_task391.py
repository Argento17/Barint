"""
TASK-391 Stage 1 — Compare live frontend scores vs fresh re-score.
Reads the live JSON and the fresh manifest; produces the 38-product comparison table.
All numbers derived from the written artifacts.
"""
from __future__ import annotations
import sys, io, json, pathlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")

# ── Load live frontend ─────────────────────────────────────────────────────────
live_path = ROOT / "bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json"
live_data = json.load(open(live_path, encoding="utf-8"))
live_products = live_data["products"]
print(f"Live frontend: {len(live_products)} products")

# Build barcode→{score, grade, name, rank} lookup
live_by_barcode = {}
for p in live_products:
    live_by_barcode[p["barcode"]] = {
        "name": p["name"],
        "brand": p.get("brand",""),
        "score": p["score"],
        "grade": p["grade"],
        "rank": p.get("rank"),
    }

# ── Load fresh re-score manifest ───────────────────────────────────────────────
import glob
manifests = sorted(glob.glob(str(ROOT / "02_products/chocolate/fresh_rescore_task391_*_manifest.json")))
fresh_manifest = json.load(open(manifests[-1], encoding="utf-8"))
fresh_run_id = fresh_manifest["run_id"]
print(f"Fresh manifest: {fresh_run_id}")

# Build barcode→{score, grade, name} lookup for tablets only
fresh_by_barcode = {}
for t in fresh_manifest["chocolate_tablet"]:
    fresh_by_barcode[t["barcode"]] = {
        "name": t["name"],
        "score": t["score"],
        "grade": t["grade"],
    }

print(f"\nFresh tablet corpus size: {len(fresh_manifest['chocolate_tablet'])}")
print(f"Live frontend product count: {len(live_products)}")

# ── Compare all 38 live products ───────────────────────────────────────────────
print("\n=== 38-PRODUCT COMPARISON: live vs fresh ===")
print(f"{'bc':>14} {'name'[:32]:<34} {'live_sc':>8} {'live_gr':>7} {'fresh_sc':>9} {'fresh_gr':>8} {'delta':>6} {'grade_move':>10}")
print("-" * 110)

grade_order = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, None: 0}
score_movers = []
grade_movers = []
exact_matches = 0
no_fresh_data = []

rows = []
for p in live_products:
    bc = p["barcode"]
    lv = live_by_barcode[bc]
    fr = fresh_by_barcode.get(bc)

    live_score = lv["score"]
    live_grade = lv["grade"]

    if fr is None:
        # Not found in fresh run — in fresh tablet corpus?
        rows.append((bc, lv["name"], live_score, live_grade, "N/A", "N/A", "N/A", "MISSING_FROM_FRESH"))
        no_fresh_data.append(bc)
        continue

    fresh_score = fr["score"]
    fresh_grade = fr["grade"]

    # Delta
    if live_score is not None and fresh_score is not None:
        try:
            delta = round(float(fresh_score) - float(live_score), 1)
        except (TypeError, ValueError):
            delta = "ERR"
    else:
        delta = "N/A"

    # Grade move
    grade_move = ""
    if live_grade != fresh_grade:
        grade_move = f"{live_grade}→{fresh_grade}"
        grade_movers.append(bc)

    # Exact match?
    if delta == 0.0 and not grade_move:
        exact_matches += 1
    elif isinstance(delta, float) and delta != 0.0:
        score_movers.append(bc)

    rows.append((bc, lv["name"], live_score, live_grade, fresh_score, fresh_grade, delta, grade_move))

for bc, name, ls, lg, fs, fg, delta, gm in rows:
    name_short = name[:32] if name else ""
    print(f"{bc:>14} {name_short:<34} {str(ls):>8} {str(lg):>7} {str(fs):>9} {str(fg):>8} {str(delta):>6} {gm:>10}")

# ── Summary ────────────────────────────────────────────────────────────────────
print(f"\n=== SUMMARY ===")
print(f"Total live products compared: {len(live_products)}")
print(f"Exact matches (score+grade): {exact_matches} / {len(live_products)}")
print(f"Score movers (delta != 0, no grade change): {len(score_movers)}")
print(f"Grade movers (grade changed): {len(grade_movers)}")
print(f"Missing from fresh corpus: {len(no_fresh_data)}")

print(f"\nLive grade distribution: ", end="")
from collections import Counter
live_dist = dict(Counter(p["grade"] for p in live_products))
print(live_dist)

print(f"Fresh grade distribution (tablet corpus, all 92): ", end="")
fresh_dist = dict(Counter(t["grade"] for t in fresh_manifest["chocolate_tablet"]))
print(fresh_dist)

# Distribution of the 38 live products by fresh score
fresh_grades_for_38 = []
for p in live_products:
    bc = p["barcode"]
    fr = fresh_by_barcode.get(bc)
    if fr:
        fresh_grades_for_38.append(fr["grade"])
print(f"Fresh grade distribution (38 live products): ", end="")
print(dict(Counter(fresh_grades_for_38)))

if grade_movers:
    print(f"\nGRADE MOVERS (require co-sign):")
    for bc in grade_movers:
        lv = live_by_barcode[bc]
        fr = fresh_by_barcode[bc]
        print(f"  {bc} {lv['name'][:40]}: {lv['grade']}→{fr['grade']} (live={lv['score']}, fresh={fr['score']})")

if no_fresh_data:
    print(f"\nMISSING FROM FRESH CORPUS (barcode not scored):")
    for bc in no_fresh_data:
        print(f"  {bc} {live_by_barcode[bc]['name']}")

# ── Cluster analysis ────────────────────────────────────────────────────────────
print(f"\n=== CLUSTER ANALYSIS ===")
# Look at the C/D/E split and what's driving scores
# C products: scores 50-55 — what do they share?
c_prods = [(bc, live_by_barcode[bc], fresh_by_barcode.get(bc))
           for p in live_products if p["grade"]=="C"
           for bc in [p["barcode"]]]
print(f"\nC-grade products in live (top tier): {len([p for p in live_products if p['grade']=='C'])}")
print(f"Score range of C: {min(p['score'] for p in live_products if p['grade']=='C')} – {max(p['score'] for p in live_products if p['grade']=='C')}")
print(f"Score range of D: {min(p['score'] for p in live_products if p['grade']=='D')} – {max(p['score'] for p in live_products if p['grade']=='D')}")
print(f"Score range of E: {min(p['score'] for p in live_products if p['grade']=='E')} – {max(p['score'] for p in live_products if p['grade']=='E')}")

# Check: is any single cap/signal pinning all E's?
# We can inspect a few BSIP2 traces for the E products
bsip2_dir = pathlib.Path(fresh_manifest["bsip2_dir"])
e_barcodes = [p["barcode"] for p in live_products if p["grade"]=="E"][:3]
print(f"\nSample E-grade BSIP2 trace inspection (3 products):")
for bc in e_barcodes:
    trace_path = bsip2_dir.parent / f"bsip1_{bc}" / "products" / f"bsip1_{bc}" / "bsip2_trace.json"
    # Try the path pattern from the fresh run
    candidates = list(bsip2_dir.rglob(f"*{bc}*/bsip2_trace.json"))
    if not candidates:
        print(f"  {bc}: trace not found at {bsip2_dir}")
        continue
    trace = json.load(open(candidates[0], encoding="utf-8"))
    score = trace.get("final_score_estimate", trace.get("score"))
    grade = trace.get("grade_estimate", trace.get("grade"))
    # Find penalty/cap signals
    penalties = []
    raw = trace.get("raw_signals", {}) or trace.get("signals", {}) or {}
    for k, v in raw.items():
        if isinstance(v, (int, float)) and v < 0:
            penalties.append(f"{k}={v}")
    print(f"  {bc}: score={score} grade={grade} penalties={penalties[:5]}")

print("\nDone.")
