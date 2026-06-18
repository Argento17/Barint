"""
T2 score/grade corrections for two biscuit barcodes.
Source: run_cakes_001 traces (the canonical merge source per task283_restructure.py).

7296073453857: FE=31.5/E → correct to 32.7/E (run_cakes_001 trace; grade unchanged, score update)
313184:        FE=34.9/E → correct to 35.3/D (run_cakes_001 trace; both score and grade corrected)

These are NOT rescores. The engine is frozen. These are trace-reconciliation corrections
to align displayed values with the canonical trace that was supposed to be the source.
"""
import json, sys, pathlib, hashlib, datetime
sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(r"C:\Bari")
BISCUIT_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"

with open(BISCUIT_PATH, "r", encoding="utf-8") as f:
    biscuit = json.load(f)

CORRECTIONS = {
    "7296073453857": {
        "score": 32.7,
        "grade": "E",
        "from_score": 31.5,
        "from_grade": "E",
        "source_run": "run_cakes_001",
        "trace_path": "bsip2_outputs/run_cakes_001/products/bsip1_cakes_7296073453857/bsip2_trace.json",
        "note": "Score was from run_cakes_pilot_ev098; canonical source is run_cakes_001 (grade unchanged E→E)"
    },
    "313184": {
        "score": 35.3,
        "grade": "D",
        "from_score": 34.9,
        "from_grade": "E",
        "source_run": "run_cakes_001",
        "trace_path": "bsip2_outputs/run_cakes_001/products/bsip1_cakes_313184/bsip2_trace.json",
        "note": "Score 34.9/E was from pilot/intermediate; canonical run_cakes_001 trace is 35.3/D — E→D flip corrected"
    }
}

corrections_applied = []
grade_dist_before = {}
grade_dist_after = {}

for p in biscuit["products"]:
    g = p["grade"]
    grade_dist_before[g] = grade_dist_before.get(g, 0) + 1

for p in biscuit["products"]:
    bc = p["barcode"]
    if bc in CORRECTIONS:
        corr = CORRECTIONS[bc]
        old_score = p["score"]
        old_grade = p["grade"]
        p["score"] = corr["score"]
        p["grade"] = corr["grade"]
        # Add trace correction note
        p["_score_correction"] = {
            "task": "TASK-244",
            "date": "2026-06-15",
            "from_score": corr["from_score"],
            "from_grade": corr["from_grade"],
            "to_score": corr["score"],
            "to_grade": corr["grade"],
            "canonical_run": corr["source_run"],
            "note": corr["note"]
        }
        corrections_applied.append({
            "barcode": bc,
            "from": f"{old_score}/{old_grade}",
            "to": f"{corr['score']}/{corr['grade']}",
            "note": corr["note"]
        })
        print(f"Corrected {bc}: {old_score}/{old_grade} → {corr['score']}/{corr['grade']}")

# Recompute grade distribution
for p in biscuit["products"]:
    g = p["grade"]
    grade_dist_after[g] = grade_dist_after.get(g, 0) + 1

print(f"\nGrade distribution change:")
print(f"  Before: {grade_dist_before}")
print(f"  After:  {grade_dist_after}")

# Update meta
biscuit["_meta"]["grade_distribution"] = grade_dist_after
biscuit["_meta"]["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Add to integrity_pass record
if "integrity_pass" in biscuit["_meta"]:
    biscuit["_meta"]["integrity_pass"]["t2_biscuit_score_corrections"] = corrections_applied
else:
    biscuit["_meta"]["t2_biscuit_score_corrections"] = corrections_applied

# Update filter counts
for f in biscuit.get("page_copy", {}).get("filters", []):
    fid = f.get("id")
    if fid == "grade_c":
        f["count"] = grade_dist_after.get("C", 0)
    elif fid == "grade_d":
        f["count"] = grade_dist_after.get("D", 0)
    elif fid == "grade_e":
        f["count"] = grade_dist_after.get("E", 0)

# Write
with open(BISCUIT_PATH, "w", encoding="utf-8") as f:
    json.dump(biscuit, f, ensure_ascii=False, indent=2)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

biscuit_sha = sha256_file(BISCUIT_PATH)
print(f"\nWrote: {BISCUIT_PATH}")
print(f"SHA256: {biscuit_sha}")

# Final state check
total = sum(grade_dist_after.values())
print(f"\nFinal biscuit corpus: {total} products")
print(f"Grade distribution: {grade_dist_after}")
print(f"Corrections applied: {len(corrections_applied)}")
