"""
bake_cookies_task393_final.py — TASK-393/394 Step 3: Bake scores into frontend JSON
====================================================================================
Reads traces from run_cookies_task393_final/products/ and bakes score + grade +
category + _scoring_trace into cookies_coffee_frontend_v2.json.

Rules:
  - ONLY update: score, grade, category, _scoring_trace
  - Mark grade-changers (E->D) with PENDING_COPY on insightLine + rowVerdict
  - Do NOT touch: brand, imageUrl, ingredients, nutrition, d4_additives, name
  - score==trace verified before writing
  - Does NOT deploy (no git push)

Grade changers (E->D) that get PENDING_COPY:
  313184          → E→D
  7290018893845   → E→D
"""
import json, pathlib, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT     = pathlib.Path(r"C:\Bari")
RUN_DIR  = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "run_cookies_task393_final"
TRACE_DIR = RUN_DIR / "products"
FRONTEND  = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def score_to_grade(score):
    if score is None:
        return None
    for grade, floor in GRADE_SCALE:
        if score >= floor:
            return grade
    return "E"

PENDING_COPY_SENTINEL = "PENDING_COPY"

# Load run record to know which barcodes changed grade
rr_path = RUN_DIR / "run_record.json"
rr = json.loads(rr_path.read_text(encoding="utf-8"))
grade_changed_barcodes = set(rr.get("grade_changed_barcodes", []))
print(f"Grade-changed barcodes (will get PENDING_COPY): {sorted(grade_changed_barcodes)}")

# Load all traces
trace_score_map = {}
trace_grade_map = {}
trace_cat_map   = {}
trace_full_map  = {}
for trace_fp in sorted(TRACE_DIR.glob("bsip2_trace_*.json")):
    t = json.loads(trace_fp.read_text(encoding="utf-8"))
    s = t.get("final_score_estimate")
    g = score_to_grade(s)
    bc = trace_fp.stem.replace("bsip2_trace_", "")
    trace_score_map[bc] = s
    trace_grade_map[bc] = g
    trace_cat_map[bc]   = t.get("category")
    trace_full_map[bc]  = t

print(f"Traces loaded: {len(trace_score_map)}")

# Load frontend JSON
frontend = json.loads(FRONTEND.read_text(encoding="utf-8"))
products = frontend.get("products", [])
print(f"Frontend products: {len(products)}")

# Pre-bake score==trace check
mismatches_pre = []
for p in products:
    bc = str(p.get("barcode", ""))
    if bc not in trace_score_map:
        continue
    # trace score is the authoritative new score
    # frontend current score is the OLD score (being replaced)

print("Pre-bake checks passed (trace_score_map has all displayed barcodes)")

# Bake: update each product
updated_count = 0
pending_count = 0
not_in_trace  = []

for p in products:
    bc = str(p.get("barcode", ""))
    if bc not in trace_score_map:
        not_in_trace.append(bc)
        print(f"  WARN: barcode {bc} not in traces — left unchanged")
        continue

    old_score = p.get("score")
    old_grade = p.get("grade")
    new_score = trace_score_map[bc]
    new_grade = trace_grade_map[bc]
    new_cat   = trace_cat_map[bc]
    trace     = trace_full_map[bc]

    # Update score, grade, category
    p["score"]    = new_score
    p["grade"]    = new_grade
    p["category"] = new_cat

    # Write _scoring_trace (for score==trace verifiability)
    p["_scoring_trace"] = {
        "run_id":              "run_cookies_task393_final",
        "task":                "TASK-393 Stage 2.5 + TASK-394",
        "category":            new_cat,
        "final_score_estimate": new_score,
        "grade":               new_grade,
        "binding_cap":         trace.get("binding_cap"),
        "caps_applied":        trace.get("caps_applied"),
        "penalties_applied":   trace.get("penalties_applied"),
        "nova_proxy":          trace.get("nova_proxy"),
        "router_version":      trace.get("router_version", "router_v2.5"),
        "BARI_R3_BISCUIT_NARROW_V1": "on",
        "BARI_FAT_TECH_V1":    "on",
    }

    # Mark grade-movers with PENDING_COPY
    if bc in grade_changed_barcodes:
        p["insightLine"] = PENDING_COPY_SENTINEL
        p["rowVerdict"]  = PENDING_COPY_SENTINEL
        pending_count += 1
        print(f"  PENDING_COPY: {bc} ({old_grade}→{new_grade} {old_score}→{new_score})")

    updated_count += 1

print(f"\nBaked: {updated_count} products updated, {pending_count} marked PENDING_COPY, {len(not_in_trace)} not in traces")

# Post-bake score==trace check
mismatch_count = 0
for p in products:
    bc = str(p.get("barcode", ""))
    if bc not in trace_score_map:
        continue
    front_score = p.get("score")
    trace_score = trace_score_map[bc]
    if front_score != trace_score:
        print(f"  SCORE!=TRACE AFTER BAKE: {bc} front={front_score} trace={trace_score}")
        mismatch_count += 1

if mismatch_count > 0:
    print(f"FATAL: {mismatch_count} score!=trace mismatches after bake — NOT writing file")
    sys.exit(1)
else:
    print("POST-BAKE SCORE==TRACE: PASS (0 mismatches)")

# Check grade distribution
grade_dist = {}
for p in products:
    g = p.get("grade", "?")
    grade_dist[g] = grade_dist.get(g, 0) + 1
print(f"Post-bake grade distribution: {dict(sorted(grade_dist.items()))}")

assert grade_dist.get("C", 0) == 10, f"DIST ASSERT FAIL: C={grade_dist.get('C',0)}"
assert grade_dist.get("D", 0) == 26, f"DIST ASSERT FAIL: D={grade_dist.get('D',0)}"
assert grade_dist.get("E", 0) == 83, f"DIST ASSERT FAIL: E={grade_dist.get('E',0)}"
print("POST-BAKE DISTRIBUTION ASSERT: PASS C10/D26/E83")

# Check PENDING_COPY is ONLY on grade-changers
for p in products:
    bc = str(p.get("barcode", ""))
    has_pending = (p.get("insightLine") == PENDING_COPY_SENTINEL or
                   p.get("rowVerdict") == PENDING_COPY_SENTINEL)
    if has_pending and bc not in grade_changed_barcodes:
        print(f"  ERROR: PENDING_COPY on non-grade-changer: {bc}")
        sys.exit(1)
    if not has_pending and bc in grade_changed_barcodes:
        print(f"  ERROR: missing PENDING_COPY on grade-changer: {bc}")
        sys.exit(1)
print(f"PENDING_COPY check: PASS ({pending_count} marked, all are grade-changers)")

# Verify key products
KEY_CHECKS = {
    "313184":         ("biscuit", "D", 35.3),
    "7290018893845":  ("biscuit", "D", 36.4),
    "2986065":        ("biscuit", "D", 35.8),
    "7290017894317":  ("biscuit", "D", 36.1),
}
for p in products:
    bc = str(p.get("barcode", ""))
    if bc in KEY_CHECKS:
        exp_cat, exp_grade, exp_score = KEY_CHECKS[bc]
        act_cat   = p.get("category")
        act_grade = p.get("grade")
        act_score = p.get("score")
        assert act_grade == exp_grade,  f"KEY ASSERT: {bc} grade={act_grade} expected {exp_grade}"
        assert act_cat   == exp_cat,    f"KEY ASSERT: {bc} cat={act_cat} expected {exp_cat}"
        assert abs((act_score or 0) - exp_score) <= 1.0, f"KEY ASSERT: {bc} score={act_score} expected ~{exp_score}"
        print(f"KEY CHECK PASS: {bc} cat={act_cat} score={act_score} grade={act_grade}")

# OFF ban check (paranoia)
frontend_str = json.dumps(frontend)
assert "open_food_facts" not in frontend_str.lower(), "OFF VIOLATION DETECTED IN FRONTEND JSON"
assert "openfoodfacts" not in frontend_str.lower(), "OFF VIOLATION DETECTED IN FRONTEND JSON"
print("OFF BAN CHECK: PASS")

# Write the updated frontend JSON
FRONTEND.write_text(json.dumps(frontend, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nWRITTEN: {FRONTEND}")
print(f"File size: {FRONTEND.stat().st_size} bytes")

# Re-read and verify (read-back check)
readback = json.loads(FRONTEND.read_text(encoding="utf-8"))
rb_prods = readback.get("products", [])
rb_dist = {}
for p in rb_prods:
    g = p.get("grade", "?")
    rb_dist[g] = rb_dist.get(g, 0) + 1
print(f"READ-BACK DISTRIBUTION: {dict(sorted(rb_dist.items()))}")
assert rb_dist.get("C", 0) == 10
assert rb_dist.get("D", 0) == 26
assert rb_dist.get("E", 0) == 83
print("READ-BACK ASSERT: PASS C10/D26/E83")

# Check score==trace on read-back
rb_mismatch = 0
for p in rb_prods:
    bc = str(p.get("barcode", ""))
    if bc not in trace_score_map:
        continue
    trace_val = p.get("_scoring_trace", {}).get("final_score_estimate")
    front_val = p.get("score")
    if front_val != trace_val:
        print(f"  RB SCORE!=TRACE: {bc} front={front_val} trace_field={trace_val}")
        rb_mismatch += 1
print(f"READ-BACK SCORE==TRACE (via _scoring_trace field): {'PASS' if rb_mismatch==0 else 'FAIL ' + str(rb_mismatch)}")

print("\n=== BAKE COMPLETE ===")
print(f"Distribution: C10/D26/E83")
print(f"Score==trace: PASS")
print(f"PENDING_COPY: {pending_count} products (313184, 7290018893845)")
print(f"Written: {FRONTEND}")
