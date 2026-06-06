"""
Split + promote run_cereals_005 into TWO live frontend corpora (TASK-140, owner 2026-06-05):
  • breakfast-cereals  (standard pool, contaminants removed)
  • granola            (NEW sibling category, the 25-strong granola sub-pool)

Method (corpus-independence proven: scores use fixed per-category constant tables, not
batch statistics — so removing the 13 contaminants does NOT change any survivor's score):
  1. Load run_005 traces → authoritative survivor scores.
  2. Load run_005 BSIP1 files → granola sub-pool tag + governance.
  3. Load the EXISTING live cereals_frontend_v1.json → carry over the hand-AUTHORED
     Hebrew copy (insightLine / rowVerdict / expansion) for every survivor.
  4. REGRESSION ASSERT: round(run_005 score) == live score for every survivor. Any
     drift is reported and blocks promotion.
  5. Emit two BariProductVM[] corpora. Contaminants are simply absent (not re-graded).
"""
import json, pathlib, datetime

TRACE_DIR = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_005\products")
BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_005\output")
LIVE_JSON = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v1.json")
OUT_CEREALS = LIVE_JSON
OUT_GRANOLA = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\granola_frontend_v1.json")

# --- load run_005 traces (authoritative scores) ---
traces = {}
for f in TRACE_DIR.glob("*/bsip2_trace.json"):
    t = json.loads(f.read_text("utf-8"))
    pid = t.get("canonical_product_id") or (t.get("input_reference") or {}).get("canonical_product_id")
    if pid:
        traces[pid] = t

# --- load run_005 BSIP1 (subpool tag) ---
bsip1 = {}
for f in BSIP1_DIR.glob("bsip1_*.json"):
    d = json.loads(f.read_text("utf-8"))
    bsip1[d.get("canonical_product_id")] = d

# --- load existing live authored corpus (keyed by id) ---
# Idempotent: the script overwrites the cereals file, so on re-runs the authored copy
# for granola products lives in the already-split granola file. Read the UNION of both.
authored = {}
for _src in (LIVE_JSON, OUT_GRANOLA):
    if _src.exists():
        for p in json.loads(_src.read_text("utf-8")).get("products", []):
            authored.setdefault(p["id"], p)

survivors = set(traces) & set(bsip1)
cereals, granola, drift, missing_copy = [], [], [], []

for pid in survivors:
    t = traces[pid]
    b = bsip1[pid]
    run_score = t.get("final_score_estimate")
    run_score_int = round(run_score) if run_score is not None else None
    src = authored.get(pid)
    if not src:
        missing_copy.append((pid, b.get("canonical_name_he")))
        continue
    # REGRESSION: survivor score must be unchanged vs live (corpus-independence proof)
    if src.get("score") != run_score_int:
        drift.append({"id": pid, "name": b.get("canonical_name_he"),
                      "live_score": src.get("score"), "run_005_score": run_score_int})
    subpool = (b.get("cereals_governance", {}).get("construct_1_granola_subpool") or {}).get("subpool")
    entry = dict(src)            # preserve ALL authored fields verbatim
    entry["_subpool"] = subpool
    (granola if subpool == "granola" else cereals).append(entry)

# keep leaderboard order (desc by score), as the live file was sorted
cereals.sort(key=lambda x: (x.get("score") or 0), reverse=True)
granola.sort(key=lambda x: (x.get("score") or 0), reverse=True)

print(f"survivors={len(survivors)}  cereals(standard)={len(cereals)}  granola={len(granola)}")
print(f"score drift (should be 0): {len(drift)}")
for d in drift:
    print("   DRIFT", d)
if missing_copy:
    print("MISSING AUTHORED COPY:", missing_copy)

if drift or missing_copy:
    raise SystemExit("ABORT — regression drift or missing authored copy; not promoting.")

# GATE 2 — Leaderboard integrity (corpus_purity_gates_v1). A contaminant must never
# survive to the top of a leaderboard. Defense-in-depth: re-assert that the #1 product
# of each corpus is not a known contamination pattern (ptitim pasta / bread leakage).
import re as _re
_CONTAMINANT = _re.compile(r"^\s*פתיתים\b|פתיתים\s+אפויים|פתיתים\s+אורגנים|חלה|מהלחם")
for _label, _items in (("breakfast-cereals", cereals), ("granola", granola)):
    if _items and _CONTAMINANT.search(_items[0]["name"]):
        raise SystemExit(f"ABORT GATE-2 — leaderboard #1 of {_label} looks like a contaminant: "
                         f"{_items[0]['name']}")

now = datetime.datetime.now(datetime.timezone.utc).isoformat()


def grade_dist(items):
    d = {}
    for p in items:
        d[p["grade"]] = d.get(p["grade"], 0) + 1
    return d


cereals_doc = {
    "_meta": {
        "generated": now, "category": "breakfast-cereals",
        "product_count": len(cereals), "scored_count": len(cereals),
        "schema": "BariProductVM[]", "version": "v2",
        "provenance": "run_cereals_005 (EV-045 corpus purity: 13 non-cereals removed; "
                      "granola split to its own category). Scores byte-identical to run_004 survivors.",
    },
    "products": cereals,
}
granola_doc = {
    "_meta": {
        "generated": now, "category": "granola",
        "product_count": len(granola), "scored_count": len(granola),
        "schema": "BariProductVM[]", "version": "v1",
        "provenance": "run_cereals_005 granola sub-pool, promoted to a standalone category "
                      "(TASK-140, owner 2026-06-05).",
    },
    "products": granola,
}

OUT_CEREALS.write_text(json.dumps(cereals_doc, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_GRANOLA.write_text(json.dumps(granola_doc, ensure_ascii=False, indent=2), encoding="utf-8")
print("cereals grade dist:", grade_dist(cereals))
print("granola grade dist:", grade_dist(granola))
print("wrote", OUT_CEREALS)
print("wrote", OUT_GRANOLA)
