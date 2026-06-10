"""
Update hard_cheeses_frontend_v2.json with BARI_REDLABEL_V1+BARI_RECAL_P0 scores.
TASK-REDLABEL-001 — pilot activation run 2026-06-08.

Reads: bsip2_trace.json files from run_hardcheese_redlabel_v1_001
Writes: C:\\Bari\\02_products\\hard_cheeses\\hard_cheeses_frontend_v2.json (score fields only)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json, pathlib, datetime

TRACE_ROOT   = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hardcheese_redlabel_v1_001\products")
FRONTEND_IN  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\hard_cheeses_frontend_v2.json")
FRONTEND_OUT = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\hard_cheeses_frontend_v2.json")
BSIP1_DIR    = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_outputs")

ENGINE_TAG   = "BARI_REDLABEL_V1+BARI_RECAL_P0"
RUN_DATE     = "2026-06-08"
RUN_ID       = "run_hardcheese_redlabel_v1_001"

# ------------------------------------------------------------------
# 1. Build barcode → trace map from all trace files
# ------------------------------------------------------------------
barcode_to_trace = {}
pid_to_trace = {}

for product_dir in sorted(TRACE_ROOT.iterdir()):
    trace_file = product_dir / "bsip2_trace.json"
    if not trace_file.exists():
        continue
    with open(trace_file, encoding='utf-8') as f:
        trace = json.load(f)

    ref = trace.get("input_reference") or {}
    barcode = ref.get("barcode")
    pid = ref.get("canonical_product_id")

    if barcode:
        barcode_to_trace[str(barcode)] = trace
    if pid:
        pid_to_trace[pid] = trace

print(f"Traces loaded: {len(barcode_to_trace)} (by barcode), {len(pid_to_trace)} (by pid)")

# ------------------------------------------------------------------
# 2. Load frontend JSON
# ------------------------------------------------------------------
with open(FRONTEND_IN, encoding='utf-8') as f:
    frontend = json.load(f)

products = frontend["products"]
print(f"Frontend products: {len(products)}")

# ------------------------------------------------------------------
# 3. Capture before-state for delta reporting
# ------------------------------------------------------------------
before_scores = {}
for p in products:
    before_scores[p["id"]] = {"score": p.get("score"), "grade": p.get("grade")}

# ------------------------------------------------------------------
# 4. Update score-related fields from traces
# ------------------------------------------------------------------
updated_count = 0
grade_changed = []
not_scored = []     # insufficient_data or error
unmatched = []      # no trace found for this barcode

for product in products:
    barcode = str(product.get("barcode", ""))
    pid_guess = f"bsip1_hardcheese_{barcode}"

    trace = barcode_to_trace.get(barcode) or pid_to_trace.get(pid_guess)

    if trace is None:
        unmatched.append({"id": product["id"], "barcode": barcode, "name": product.get("name")})
        continue

    score_val = trace.get("final_score_estimate")
    grade_val = trace.get("grade_estimate")

    # Products with insufficient_data grade — flag but still record score
    if grade_val == "insufficient_data":
        not_scored.append({
            "id": product["id"],
            "barcode": barcode,
            "name": product.get("name"),
            "score": score_val,
            "grade_estimate": grade_val,
            "reason": "insufficient_data from engine"
        })
        # Do NOT update the frontend score for insufficient_data products
        continue

    old_score = product.get("score")
    old_grade = product.get("grade")

    # Update score fields
    product["score"] = round(score_val) if score_val is not None else product["score"]
    product["grade"] = grade_val if grade_val not in (None, "insufficient_data") else product["grade"]

    # bsip2_trace metadata block (score provenance, not full trace)
    product["bsip2_score_trace"] = {
        "run_id": RUN_ID,
        "engine_tag": ENGINE_TAG,
        "run_date": RUN_DATE,
        "final_score_raw": score_val,
        "grade_estimate": grade_val,
        "binding_cap": trace.get("binding_cap"),
        "caps_fired": trace.get("caps_fired"),
        "penalties_applied": trace.get("penalties_applied"),
        "dimension_scores": trace.get("dimension_scores"),
        "dimension_notes": trace.get("dimension_notes"),
        "data_sufficiency": trace.get("data_sufficiency"),
        "regulatory_quality_note": (
            (trace.get("dimension_notes") or {}).get("regulatory_quality")
            if isinstance(trace.get("dimension_notes"), dict) else None
        ),
    }

    updated_count += 1

    if old_grade != grade_val:
        grade_changed.append({
            "id": product["id"],
            "name": product.get("name"),
            "barcode": barcode,
            "before_score": old_score,
            "before_grade": old_grade,
            "after_score": product["score"],
            "after_grade": product["grade"],
        })

# ------------------------------------------------------------------
# 5. Add/update top-level score_metadata block
# ------------------------------------------------------------------
frontend["score_metadata"] = {
    "engine_tag": ENGINE_TAG,
    "flags": ["BARI_REDLABEL_V1", "BARI_RECAL_P0"],
    "run_date": RUN_DATE,
    "run_id": RUN_ID,
    "d7_approved": RUN_DATE,
    "pilot_scope": "hard_cheese",
    "task": "TASK-REDLABEL-001",
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
}

# Update _meta
frontend["_meta"]["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
frontend["_meta"]["run_id"] = RUN_ID

# Update grade distribution in _meta
dist = {}
for p in products:
    g = p.get("grade")
    if g:
        dist[g] = dist.get(g, 0) + 1
frontend["_meta"]["grade_distribution"] = dist

# ------------------------------------------------------------------
# 6. Score range statistics
# ------------------------------------------------------------------
after_scores_all = [p["score"] for p in products if p.get("score") is not None]
before_scores_all = [v["score"] for v in before_scores.values() if v["score"] is not None]

def stats(vals):
    if not vals: return {}
    return {
        "min": min(vals),
        "max": max(vals),
        "mean": round(sum(vals) / len(vals), 1)
    }

# ------------------------------------------------------------------
# 7. Write updated frontend JSON
# ------------------------------------------------------------------
with open(FRONTEND_OUT, 'w', encoding='utf-8') as f:
    json.dump(frontend, f, ensure_ascii=False, indent=2)

print(f"\n=== REDLABEL V1 Frontend Update ===")
print(f"Products in frontend: {len(products)}")
print(f"Products updated: {updated_count}")
print(f"Products with insufficient_data (not updated): {len(not_scored)}")
print(f"Products unmatched (no trace): {len(unmatched)}")
print(f"Grade changes: {len(grade_changed)}")
print()

print("BEFORE score range:", stats(before_scores_all))
print("AFTER score range: ", stats(after_scores_all))
print()

if grade_changed:
    print("Grade changes:")
    for g in grade_changed:
        print(f"  {g['id']} {g['name'][:40]:40s}  {g['before_score']}/{g['before_grade']} -> {g['after_score']}/{g['after_grade']}")
print()

if not_scored:
    print("Not scored (insufficient_data — kept original score):")
    for ns in not_scored:
        print(f"  {ns['id']} {ns['barcode']:20s} {ns['name'][:35]:35s}  engine_score={ns['score']}")
print()

if unmatched:
    print("WARNING — Unmatched (no trace, score not updated):")
    for u in unmatched:
        print(f"  {u['id']} {u['barcode']}")

print(f"\nWritten: {FRONTEND_OUT}")
