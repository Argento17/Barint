"""
Build run_cereals_008 frontend corpus (TASK-198 pipeline bug fixes).

This script packages the corrected run_cereals_008 BSIP2 traces into
cereals_frontend_v1.json (standard cereals pool).

Changes from run_005 (current live):
  - Lion (ליון דגני שוקולד וקרמל): 78/B → 55/C (Bug 1 + Bug 2 fixes)
  - Wittebix (דגני בוקר ויטביקס): 75/B (unchanged; inversion resolved)
  - Other products: scores corrected with Glass Box W4 (shipped) + fermentation fix

Method:
  1. Load run_008 traces → authoritative corrected scores
  2. Load run_008 BSIP1 files → subpool + governance
  3. Load existing authored Hebrew copy → carry forward where grade unchanged
  4. For products with grade changes: update insightLine + rowVerdict to match
     the corrected score (Lion requires new copy; others get carry-forward with
     score updated)
  5. Gate: verify inversion resolved (Wittebix > Lion)
  6. Write cereals_frontend_v1.json
"""
import sys, io, json, pathlib, datetime, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TRACE_DIR  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008\products")
BSIP1_DIR  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_008\output")
LIVE_JSON  = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v1.json")
GRANOLA_JSON = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\granola_frontend_v1.json")
OUT_CEREALS = LIVE_JSON  # overwrite in-place

# --- load run_008 traces (authoritative scores) ---
traces = {}
for f in TRACE_DIR.glob("*/bsip2_trace.json"):
    t = json.loads(f.read_text("utf-8"))
    pid = t.get("canonical_product_id") or (t.get("input_reference") or {}).get("canonical_product_id")
    if pid:
        traces[pid] = t

# --- load run_008 BSIP1 ---
bsip1 = {}
for f in BSIP1_DIR.glob("bsip1_*.json"):
    d = json.loads(f.read_text("utf-8"))
    bsip1[d.get("canonical_product_id")] = d

# --- load existing authored corpus ---
# Pool composition DOES NOT CHANGE in this build. TASK-198 fixes are data bugs only.
# The cereals_frontend_v1.json pool (38 products) is authoritative; subpool routing
# decisions for future re-pooling are a separate task (flagged below).
authored = {}
for _src in (LIVE_JSON, GRANOLA_JSON):
    if _src.exists():
        for p in json.loads(_src.read_text("utf-8")).get("products", []):
            authored.setdefault(p["id"], p)

# The pool is the 38 products that were in cereals_frontend_v1.json
live_cereals_pool = json.loads(LIVE_JSON.read_text("utf-8")).get("products", [])
live_granola_pool = json.loads(GRANOLA_JSON.read_text("utf-8")).get("products", []) if GRANOLA_JSON.exists() else []
cereals_pool_ids = [p["id"] for p in live_cereals_pool]
granola_pool_ids = [p["id"] for p in live_granola_pool]

print(f"run_008 traces: {len(traces)}, BSIP1: {len(bsip1)}, authored: {len(authored)}")
print(f"pool sizes: cereals={len(cereals_pool_ids)}, granola={len(granola_pool_ids)}")

# --- Updated authored copy for products whose grade changed ---
# These are written by hand for the products whose score/grade changed materially.
# Rule: grade unchanged → carry authored insightLine/rowVerdict verbatim (only update score).
# Grade changed → use updated copy that reflects the corrected score.

UPDATED_COPY = {
    # Lion: 78/B → 55/C
    # Bug 1: fat (0.5→6.2g), sugar (null→24.7g), sat_fat (null→2.5g) now correctly reported.
    # Bug 2: ingredient list was marketing copy; fermentation false positive removed.
    "bsip1_cereal_5900020036407": {
        "insightLine": "24.7 גרם סוכר ל-100 גרם, שומן רווי 2.5 גרם. הציון הקודם היה שגוי — נתוני שומן וסוכר לא הועברו למנוע.",
        "rowVerdict": "ליון: דגני שוקולד וקרמל עם 24.7 גרם סוכר ו-6.2 גרם שומן ל-100 גרם — ערכים שלא הועברו לגרסה הקודמת. הציון הנכון הוא 55/C. 8.5 גרם חלבון ו-6.5 גרם סיבים, אך גלוקוז גבוה וארכיטקטורת שומן בינונית מורידים את הציון.",
    },
    # Nesquik: 77.7→55/C — was inflated by same Bug 1 class (no fat/sugar data in run_005)
    "bsip1_cereal_5900020012814": {
        "insightLine": "מוצר ילדים שהציון הקודם שלו היה מנופח. 24.7 גרם סוכר ל-100 גרם — גבוה לקטגוריה.",
        "rowVerdict": "נסקוויק: חיטה מלאה ראשונה ברשימה, 8.9 גרם חלבון ו-8 גרם סיבים — אבל 24.7 גרם סוכר ל-100 גרם. הציון הקודם (78/B) לא כלל נתוני סוכר ושומן מלאים. הציון הנכון 55/C.",
    },
}

# Iterate over the EXISTING cereals pool (preserves pool composition).
# Only scores/grades are updated from run_008. Pool membership changes are out of scope.
#
# NOTE: 22 products in the existing pool are now tagged subpool=granola by run_008
# governance rules. This is flagged for a separate pooling review task — NOT changed here.

cereals = []
grade_changes = []
no_run008_trace = []

for src in live_cereals_pool:
    pid = src["id"]
    entry = dict(src)
    t = traces.get(pid)

    # Apply updated authored copy for grade-changed products
    if pid in UPDATED_COPY:
        entry["insightLine"] = UPDATED_COPY[pid]["insightLine"]
        entry["rowVerdict"] = UPDATED_COPY[pid]["rowVerdict"]

    if t:
        run_score = t.get("final_score_estimate")
        run_score_int = round(run_score) if run_score is not None else None
        grade = t.get("grade_estimate")
        old_score = entry.get("score")
        old_grade = entry.get("grade")
        if old_score != run_score_int or old_grade != grade:
            grade_changes.append({
                "pid": pid,
                "name": (entry.get("name") or pid)[:50],
                "old_score": old_score,
                "old_grade": old_grade,
                "new_score": run_score_int,
                "new_grade": grade,
            })
        entry["score"] = run_score_int
        entry["grade"] = grade
        entry["confidence_level"] = t.get("data_sufficiency") or "sufficient"
    else:
        # Product not in run_008 (may have been dropped from scrape) — keep old score
        no_run008_trace.append(pid)

    cereals.append(entry)

# Granola pool — update scores for products in BOTH pools, keep others at existing score
granola = []
granola_grade_changes = []
for src in live_granola_pool:
    pid = src["id"]
    entry = dict(src)
    t = traces.get(pid)
    if t:
        run_score = t.get("final_score_estimate")
        run_score_int = round(run_score) if run_score is not None else None
        grade = t.get("grade_estimate")
        old_score = entry.get("score")
        old_grade = entry.get("grade")
        if old_score != run_score_int or old_grade != grade:
            granola_grade_changes.append({
                "pid": pid,
                "name": (entry.get("name") or pid)[:50],
                "old_score": old_score,
                "old_grade": old_grade,
                "new_score": run_score_int,
                "new_grade": grade,
            })
        entry["score"] = run_score_int
        entry["grade"] = grade
        entry["confidence_level"] = t.get("data_sufficiency") or "sufficient"
    granola.append(entry)

# Sort leaderboard descending by score
cereals.sort(key=lambda x: (x.get("score") or 0), reverse=True)
granola.sort(key=lambda x: (x.get("score") or 0), reverse=True)

# GATE 1 — Inversion check: Wittebix must be above Lion
lion_entry = next((p for p in cereals if "5900020036407" in p.get("id","")), None)
witt_entry = next((p for p in cereals if "5010029000061" in p.get("id","")), None)
assert lion_entry and witt_entry, "ABORT: Lion or Wittebix not found in cereals pool"
assert (witt_entry.get("score") or 0) > (lion_entry.get("score") or 0), (
    f"ABORT GATE-1 — Inversion NOT resolved: Wittebix={witt_entry.get('score')} "
    f"Lion={lion_entry.get('score')}"
)
print(f"GATE-1 PASS: Wittebix {witt_entry.get('score')}/{witt_entry.get('grade')} > "
      f"Lion {lion_entry.get('score')}/{lion_entry.get('grade')}")

# GATE 2 — Leaderboard #1 not a contaminant
_CONTAMINANT = re.compile(r"^\s*פתיתים\b|פתיתים\s+אפויים|פתיתים\s+אורגנים|חלה|מהלחם")
for _label, _items in (("breakfast-cereals", cereals), ("granola", granola)):
    if _items and _CONTAMINANT.search(_items[0]["name"]):
        raise SystemExit(f"ABORT GATE-2 — leaderboard #1 of {_label} looks like a contaminant: {_items[0]['name']}")

print(f"GATE-2 PASS: no contaminant at leaderboard #1")

# Report
print(f"\ncereals score changes: {len(grade_changes)}")
for c in sorted(grade_changes, key=lambda x: abs((x.get('old_score') or 0) - (x.get('new_score') or 0)), reverse=True):
    print(f"  {c['name']}: {c['old_score']}/{c['old_grade']} → {c['new_score']}/{c['new_grade']}")
if no_run008_trace:
    print(f"WARN: no run_008 trace for (kept old score): {no_run008_trace}")
print(f"\ngranola score changes: {len(granola_grade_changes)}")
for c in sorted(granola_grade_changes, key=lambda x: abs((x.get('old_score') or 0) - (x.get('new_score') or 0)), reverse=True):
    print(f"  {c['name']}: {c['old_score']}/{c['old_grade']} → {c['new_score']}/{c['new_grade']}")
print()

now = datetime.datetime.now(datetime.timezone.utc).isoformat()

def grade_dist(items):
    d = {}
    for p in items:
        d[p["grade"]] = d.get(p["grade"], 0) + 1
    return d

cereals_doc = {
    "_meta": {
        "generated": now,
        "category": "breakfast-cereals",
        "product_count": len(cereals),
        "scored_count": len(cereals),
        "schema": "BariProductVM[]",
        "version": "v2",
        "provenance": (
            "run_cereals_008 (TASK-198 pipeline bug fixes). "
            "Bug1 (EV-029/EV-051): fat/sugar/sat-fat null fixed — Lion fat 0.5→6.2g, sugar null→24.7g. "
            "Bug2 (EV-051): marketing-bleed ingredient detection added; fermentation false-positive fixed. "
            "Lion inversion resolved: 78/B → 55/C; Wittebix unchanged 75/B."
        ),
    },
    "products": cereals,
}

OUT_CEREALS.write_text(json.dumps(cereals_doc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"cereals grade dist: {grade_dist(cereals)}")
print(f"wrote {OUT_CEREALS}")

# Write updated granola pool
if granola and GRANOLA_JSON.exists():
    existing_granola_meta = json.loads(GRANOLA_JSON.read_text("utf-8")).get("_meta", {})
    granola_doc = {
        "_meta": {
            **existing_granola_meta,
            "generated": now,
            "provenance": (
                existing_granola_meta.get("provenance", "") +
                " | run_cereals_008 score update (TASK-198 fermentation word-boundary fix, EV-051). "
                "Pool composition unchanged."
            ),
        },
        "products": granola,
    }
    GRANOLA_JSON.write_text(json.dumps(granola_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"granola grade dist: {grade_dist(granola)}")
    print(f"wrote {GRANOLA_JSON}")

print(f"\nLion: {lion_entry.get('score')}/{lion_entry.get('grade')}")
print(f"Wittebix: {witt_entry.get('score')}/{witt_entry.get('grade')}")
print("\nFLAG for separate task: 22 products in the cereals pool are tagged")
print("subpool=granola by run_008 governance rules. Pool re-routing review needed.")
