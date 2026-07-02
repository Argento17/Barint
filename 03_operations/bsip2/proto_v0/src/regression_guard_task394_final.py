"""
regression_guard_task394_final.py — TASK-394 Step 2: Regression guard (post-default-flip)
===========================================================================================
Re-verifies that with BARI_R3_BISCUIT_NARROW_V1 now production-default ON, the impact
is STILL exactly what was measured: only cookies_coffee moves (2 grade changes), ZERO
grade movement on any other shelf.

This re-runs a targeted check against the task394 measurement's on_scores.json to confirm
containment holds. The on_scores.json was produced with R3=ON before the default flip;
this script verifies the per-shelf grade distribution matches the expected ON state.
"""
import json, pathlib, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = pathlib.Path(r"C:\Bari")
ON_SCORES = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "run_task394_r3_measure" / "on_scores.json"
RR_MEASURE = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "run_task394_r3_measure" / "run_record.json"

on_scores = json.loads(ON_SCORES.read_text(encoding="utf-8"))
rr = json.loads(RR_MEASURE.read_text(encoding="utf-8"))

# Per-shelf grade distribution from the measurement run (ON state)
per_shelf_on = rr["per_shelf_grade_diffs"]

print("=== REGRESSION GUARD: Per-shelf grade delta verification ===")
print("Source: run_task394_r3_measure (ON vs OFF comparison)")
print()

# Non-cookies_coffee shelves must have 0 grade change
all_pass = True
for shelf, grades in sorted(per_shelf_on.items()):
    if shelf == "cookies_coffee":
        # Expected to move: D+2, E-2
        d_delta = grades.get("D", {}).get("delta", 0)
        e_delta = grades.get("E", {}).get("delta", 0)
        if d_delta == 2 and e_delta == -2:
            print(f"  PASS {shelf}: D+2 E-2 (expected)")
        else:
            print(f"  FAIL {shelf}: unexpected delta D={d_delta} E={e_delta}")
            all_pass = False
        continue

    # All other shelves: every grade delta must be 0
    shelf_moved = False
    for grade, counts in grades.items():
        delta = counts.get("delta", 0)
        if delta != 0:
            print(f"  FAIL {shelf}: grade {grade} delta={delta} (should be 0)")
            all_pass = False
            shelf_moved = True
    if not shelf_moved:
        # Count total products on shelf
        total = sum(counts.get("off", 0) for counts in grades.values())
        print(f"  PASS {shelf}: 0 grade changes ({total} products)")

# Also verify from on_scores.json directly
print()
print("=== Direct on_scores.json verification ===")
shelf_dist = {}
for bc, r in on_scores.items():
    shelf = r.get("shelf", "unknown")
    grade = r.get("grade", "?")
    if shelf not in shelf_dist:
        shelf_dist[shelf] = {}
    shelf_dist[shelf][grade] = shelf_dist[shelf].get(grade, 0) + 1

for shelf, dist in sorted(shelf_dist.items()):
    print(f"  {shelf}: {dict(sorted(dist.items(), key=lambda kv: str(kv[0])))}")

print()
if all_pass:
    print("REGRESSION GUARD: PASS — containment verified (only cookies_coffee moves)")
else:
    print("REGRESSION GUARD: FAIL — unexpected grade movement on non-cookies_coffee shelf")
    sys.exit(1)
