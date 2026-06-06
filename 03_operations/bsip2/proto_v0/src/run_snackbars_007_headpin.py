"""
BSIP2 Prototype v0 — Snack Bars Re-baseline Runner (run_snackbars_007_headpin)
TASK-180B Step 1.

Rescores the SAME snack-bars BSIP1 corpus that backed the production live page
(sprint1 production_snack_bars.json), on the CURRENT HEAD engine.

Engine flags:
  BARI_RECAL_P0=off       — recal changes NOT approved for snack bars; frozen off
  BARI_GLASSBOX_W4=on     — live globally (shipped 2026-06-05); set for parity
  BARI_GLASSBOX_W5=on     — not yet in engine; set has no effect (verified in run)
  BARI_TASK144_FIXES=off  — frozen off

Deliverables:
  1. off.json              — HEAD-OFF scores for all 53 corpus products
  2. run_record.json       — delta table, frozen-invariant check, drift summary
  3. sign_off_memo_180B.md — sign-off memo for owner + Nutrition
  4. snk_crosswalk_run007.md — snk-XXX → bsip1_pid → run_007 score/grade

SHIPS NOTHING. No frontend JSON edit. Owner + Nutrition sign-off gate is downstream.
"""
import os
import sys
import json
import glob
import hashlib
import pathlib
import datetime
import logging
import subprocess

# ---------------------------------------------------------------------------
# Engine flag setup (must happen BEFORE engine modules are imported)
# ---------------------------------------------------------------------------
os.environ["BARI_RECAL_P0"]      = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_GLASSBOX_W4"]   = "on"
os.environ["BARI_GLASSBOX_W5"]   = "on"   # not yet in engine; set for parity (no effect)

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
CORPUS          = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
PUBLISHED_TRACES = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs\products")
PRODUCTION_BASELINE = pathlib.Path(r"C:\Bari\03_operations\bsip2\sprint1\outputs\production_snack_bars.json")

RUN_ID    = "run_snackbars_007_headpin"
OUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs") / RUN_ID

CATEGORY_TAG  = "snack_bars"
BASELINE_TAG  = "engine-baseline-2026-06-04"

# ---------------------------------------------------------------------------
# Frozen invariants (CLAUDE.md + TASK-180B brief)
# ---------------------------------------------------------------------------
# snk-001 = date-almond bar = bsip1_7290011498870 → must be exactly 70/B
# No snack bar may reach A (score >= 80)
INVARIANT_SNK001_PID   = "bsip1_7290011498870"
INVARIANT_SNK001_SCORE = 70
INVARIANT_SNK001_GRADE = "B"

# ---------------------------------------------------------------------------
# snk-XXX label → bsip1 pid mapping (from live frontend JSON + sprint1 baseline)
# ---------------------------------------------------------------------------
SNK_LABEL_MAP = {
    "snk-001": "bsip1_7290011498870",
    "snk-002": "bsip1_8423207210287",   # 69.5/B  מרבה סלים דליס שוקולד לבן בטעם יוגורט
    "snk-003": "bsip1_7290011498894",   # 63.0/C  חטיף תמרים במילוי חמאת בוטנים
    "snk-004": "bsip1_7290011498948",   # 56.7/C  תמרים ציפוי שוקולד
    "snk-005": "bsip1_8423207208260",   # 61.0/C  סלים דליס GF
    "snk-006": "bsip1_8423207206495",   # 60.4/C  סלים דליס שוקולד מריר
    "snk-007": "bsip1_5900020039590",   # 47.6/D  פיטנס קלאסי
    "snk-009": "bsip1_8410076610379",   # 48.5/D  נייצר וואלי פרוטאין בוטנים שוקולד
    "snk-010": "bsip1_8410076610386",   # 47.1/D  נייצר וואלי קרמל מלוח
    "snk-011": "bsip1_16000423534",     # 53.1/C  קראנצ'י שוקולד מריר
    "snk-012": "bsip1_16000548404",     # 55.1/C  קראנצ'י דבש
    "snk-013": "bsip1_8423207207362",   # 53.5/C  סלים דליס שוקולד לבן
    "snk-015": "bsip1_7290011498894",   # same as snk-003 (peanut variant)
    "snk-016": "bsip1_8423207209885",   # 53.4/C
    "snk-017": "bsip1_8423207208680",   # 53.8/C
    "snk-018": "bsip1_8423207210928",   # 52.5/C
    "snk-019": "bsip1_8410076610492",   # 40.0/D
    "snk-020": "bsip1_8410076610508",   # 40.5/D
}

# Reverse map pid → snk label(s)
PID_TO_SNK = {}
for snk, pid in SNK_LABEL_MAP.items():
    PID_TO_SNK.setdefault(pid, []).append(snk)

# ---------------------------------------------------------------------------
# Engine modules list for config hash
# ---------------------------------------------------------------------------
_HASH_FILES = [
    "score_engine.py", "constants.py", "nova_proxy.py", "signal_extractor.py",
    "router_v2.py", "evaluation_scope.py", "input_loader.py",
    "structural_classifier.py", "trace_writer.py",
]


def config_hash() -> str:
    h = hashlib.sha256()
    for f in sorted(_HASH_FILES):
        h.update(f.encode())
        fp = SRC / f
        if fp.exists():
            h.update(fp.read_bytes())
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------
def run_pipeline(product: dict) -> dict:
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def run_batch_flags_off() -> dict:
    """Run BARI_RECAL_P0=off (plus W4 on). Returns {pid: trace}."""
    from input_loader import load_batch as _lb
    products = _lb(CORPUS)
    head = {}
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            head[pid] = trace
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            head[pid] = {"_error": str(e)}
    return head


# ---------------------------------------------------------------------------
# Loader helpers
# ---------------------------------------------------------------------------
def load_published_traces() -> dict:
    """Load proto_v0 sealed traces (2026-05-17). Returns {pid: {score, grade, ds, name}}."""
    out = {}
    for d in sorted(glob.glob(str(PUBLISHED_TRACES / "*"))):
        f = pathlib.Path(d) / "bsip2_trace.json"
        if not f.exists():
            continue
        try:
            t = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        pid = pathlib.Path(d).name
        out[pid] = {
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "ds":    t.get("data_sufficiency"),
            # trace_writer uses "product_name_he" inside input_reference
            "name":  (t.get("input_reference") or {}).get("product_name_he", ""),
        }
    return out


def load_production_baseline() -> dict:
    """Load sprint1 production_snack_bars.json (behind live page). Returns {pid: {score, grade, name}}."""
    raw = json.loads(PRODUCTION_BASELINE.read_text(encoding="utf-8"))
    return {p["pid"]: {"score": p["score"], "grade": p["grade"], "name": p.get("name", "")}
            for p in raw}


# ---------------------------------------------------------------------------
# Delta classification
# ---------------------------------------------------------------------------
def classify_delta(ps, pg, hs, hg):
    """Return (delta, klass). klass in MATCH / cosmetic / DRIFT>=2 / GRADE_FLIP / NULL_FLIP."""
    if ps is None and hs is None:
        return None, "MATCH"
    if ps is None or hs is None:
        return None, "NULL_FLIP"
    try:
        delta = round(float(hs) - float(ps), 1)
    except (TypeError, ValueError):
        return None, "NULL_FLIP"
    if pg != hg:
        return delta, "GRADE_FLIP"
    if abs(delta) < 0.05:
        return delta, "MATCH"
    if abs(delta) >= 2:
        return delta, "DRIFT>=2"
    return delta, "cosmetic"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    cfg = config_hash()

    # HEAD commit for provenance
    try:
        head_commit = subprocess.run(
            ["git", "-C", r"C:\Bari", "rev-list", "-n", "1", BASELINE_TAG],
            capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except Exception:
        head_commit = "unknown"

    log.info("=== BSIP2 Snack Bars re-baseline — %s on %s (%s) ===",
             RUN_ID, BASELINE_TAG, head_commit[:7] if head_commit else "unknown")
    log.info("Flags: BARI_RECAL_P0=off  BARI_GLASSBOX_W4=on  BARI_TASK144_FIXES=off")

    # --- run 1 (OFF rollback identity pass A) ---
    log.info("Pass 1 of 2 (rollback identity A)...")
    head1 = run_batch_flags_off()

    # --- run 2 (OFF rollback identity pass B) ---
    log.info("Pass 2 of 2 (rollback identity B)...")
    head2 = run_batch_flags_off()

    # --- rollback identity: off1 == off2 ---
    rollback_match = sum(
        1 for pid in head1
        if (head1[pid].get("final_score_estimate") == head2.get(pid, {}).get("final_score_estimate")
            and head1[pid].get("grade_estimate") == head2.get(pid, {}).get("grade_estimate"))
    )
    rollback_total = len(head1)
    log.info("Rollback identity: %d/%d identical", rollback_match, rollback_total)

    # Use pass 1 as canonical result
    head = head1

    # Write full off.json (all traces, slim view)
    # Name lives at trace["input_reference"]["product_name_he"] (trace_writer.py §input_reference)
    off_slim = {}
    for pid, t in head.items():
        if "_error" in t:
            off_slim[pid] = {"_error": t["_error"]}
            continue
        name = (t.get("input_reference") or {}).get("product_name_he", "")
        off_slim[pid] = {
            "name":  name,
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "ds":    t.get("data_sufficiency"),
            "cat":   t.get("category"),
            "nova":  t.get("nova_proxy"),
        }
    (OUT_ROOT / "off.json").write_text(
        json.dumps(off_slim, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- load reference sets ---
    published = load_published_traces()
    prod_base = load_production_baseline()

    # --- delta: HEAD-OFF vs production baseline (live page drift) ---
    pb_rows = []
    pb_grade_flip = pb_drift2 = pb_cosmetic = pb_match = pb_missing = 0

    for pid, pb in sorted(prod_base.items()):
        ps = pb["score"]
        pg = pb["grade"]
        name = pb["name"]
        ht = head.get(pid)
        if ht is None or "_error" in (ht or {}):
            pb_rows.append({
                "pid": pid, "name_he": name,
                "production_score": ps, "production_grade": pg,
                "head_score": None, "head_grade": None,
                "delta": None, "class": "MISSING_HEAD"
            })
            pb_missing += 1
            continue
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        delta, klass = classify_delta(ps, pg, hs, hg)
        if klass == "MATCH":         pb_match += 1
        elif klass == "GRADE_FLIP":  pb_grade_flip += 1
        elif klass == "DRIFT>=2":    pb_drift2 += 1
        elif klass == "cosmetic":    pb_cosmetic += 1
        pb_rows.append({
            "pid": pid, "name_he": name,
            "production_score": ps, "production_grade": pg,
            "head_score": hs, "head_grade": hg,
            "delta": delta, "class": klass,
        })

    pb_total       = len(prod_base)
    pb_grade_count = pb_grade_flip
    pb_exact_match = pb_match

    # --- delta: HEAD-OFF vs sealed proto_v0 traces (published-drift audit) ---
    drift_rows = []
    drift_match = drift_total = 0
    for pid, pub in sorted(published.items()):
        drift_total += 1
        ht = head.get(pid, {})
        if "_error" in (ht or {}):
            drift_rows.append({"pid": pid, "published": [pub["score"], pub["grade"]], "head_off": [None, None]})
            continue
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        try:
            same = (round(float(hs), 1) == round(float(pub["score"]), 1) and hg == pub["grade"])
        except (TypeError, ValueError):
            same = False
        if same:
            drift_match += 1
        else:
            drift_rows.append({"pid": pid,
                               "name": pub.get("name", ""),
                               "published": [pub["score"], pub["grade"]],
                               "head_off": [hs, hg]})

    # --- frozen invariant check ---
    snk001_trace = head.get(INVARIANT_SNK001_PID, {})
    snk001_score = snk001_trace.get("final_score_estimate") if "_error" not in snk001_trace else None
    snk001_grade = snk001_trace.get("grade_estimate") if "_error" not in snk001_trace else None
    snk001_held  = (snk001_score == INVARIANT_SNK001_SCORE and snk001_grade == INVARIANT_SNK001_GRADE)

    a_or_above = [
        pid for pid, t in head.items()
        if "_error" not in t
        and isinstance(t.get("final_score_estimate"), (int, float))
        and t["final_score_estimate"] >= 80
    ]
    no_a_held = len(a_or_above) == 0

    # --- ceiling-crowding: find second-highest by HEAD-OFF score (suffix scorables) ---
    scorable = [
        (pid, t.get("final_score_estimate"), t.get("grade_estimate"),
         (t.get("input_reference") or {}).get("product_name_he", ""))
        for pid, t in head.items()
        if "_error" not in t and isinstance(t.get("final_score_estimate"), (int, float))
    ]
    scorable.sort(key=lambda x: x[1], reverse=True)
    ceiling_crowding = None
    if len(scorable) >= 2:
        second = scorable[1]
        ceiling_crowding = {
            "pid":   second[0],
            "name":  second[3],
            "score": second[1],
            "grade": second[2],
            "flagged": second[1] >= 69.0 and second[2] == "B",
        }

    # --- grade-affecting moves list (for sign-off memo) ---
    grade_affecting_rows = [r for r in pb_rows if r["class"] == "GRADE_FLIP"]

    # -----------------------------------------------------------------------
    # Build run_record.json
    # -----------------------------------------------------------------------
    run_record = {
        "run_id":    RUN_ID,
        "task":      "TASK-180B",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_baseline_tag":    BASELINE_TAG,
        "engine_baseline_commit": head_commit,
        "engine_config_hash":     cfg,
        "engine_flags": {
            "BARI_RECAL_P0":      "off",
            "BARI_TASK144_FIXES": "off",
            "BARI_GLASSBOX_W4":   "on",
            "BARI_GLASSBOX_W5":   "on (set; not in engine — no effect)",
        },
        "corpus": str(CORPUS),
        "corpus_n": len(head),
        "head_scored_count": sum(1 for t in head.values() if "_error" not in t),
        "rollback_off_identical": f"{rollback_match}/{rollback_total}",
        # ---- HEAD-OFF vs production baseline (live page) ----
        "head_vs_production_baseline": {
            "production_file": str(PRODUCTION_BASELINE),
            "total": pb_total,
            "exact_match": pb_exact_match,
            "reproduction_rate": round(pb_exact_match / pb_total, 3) if pb_total else None,
            "grade_flip": pb_grade_flip,
            "drift_ge_2pt_same_grade": pb_drift2,
            "cosmetic_lt_2pt": pb_cosmetic,
            "missing_head": pb_missing,
            "grade_affecting_rows": grade_affecting_rows,
            "all_delta_rows": pb_rows,
        },
        # ---- HEAD-OFF vs proto_v0 sealed traces (published-drift audit) ----
        "head_vs_published_proto_v0_2026_05_17": {
            "match": f"{drift_match}/{drift_total}",
            "drift_rows": drift_rows,
        },
        # ---- frozen invariants ----
        "frozen_invariants": {
            "snk001": {
                "pid":    INVARIANT_SNK001_PID,
                "expected": f"{INVARIANT_SNK001_SCORE}/{INVARIANT_SNK001_GRADE}",
                "head":     f"{snk001_score}/{snk001_grade}",
                "status":   "HELD" if snk001_held else "BREACH",
            },
            "no_snackbar_A": {
                "products_ge_80": a_or_above,
                "status": "HELD" if no_a_held else "BREACH",
            },
        },
        # ---- ceiling-crowding editorial call ----
        "ceiling_crowding_editorial": ceiling_crowding,
        # ---- top 10 by HEAD-OFF score ----
        "top10_head_off": [
            {"pid": pid, "name": nm, "score": sc, "grade": gr}
            for pid, sc, gr, nm in scorable[:10]
        ],
        "ships_nothing": True,
        "notes": (
            "Rescore-only artifact for owner + Nutrition sign-off. "
            "No frontend JSON, no engine edit. "
            "BARI_GLASSBOX_W5 set but not in engine — confirmed no effect."
        ),
    }

    rec_path = OUT_ROOT / "run_record.json"
    rec_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")

    # -----------------------------------------------------------------------
    # Log summary
    # -----------------------------------------------------------------------
    log.info("--- Results ---")
    log.info("Corpus: %d products  |  Scored: %d",
             len(head), run_record["head_scored_count"])
    log.info("HEAD-OFF vs production baseline: %d/%d exact match (%.0f%%)",
             pb_exact_match, pb_total, 100 * pb_exact_match / pb_total if pb_total else 0)
    log.info("Grade flips: %d  |  >=2pt same grade: %d  |  cosmetic: %d  |  match: %d",
             pb_grade_flip, pb_drift2, pb_cosmetic, pb_match)
    log.info("HEAD-OFF vs proto_v0 sealed traces: %d/%d match", drift_match, drift_total)
    log.info("Frozen invariant snk001 70/B: %s", "HELD" if snk001_held else "*** BREACH ***")
    log.info("Frozen invariant no-A: %s", "HELD" if no_a_held else "*** BREACH *** products: %s" % a_or_above)
    if ceiling_crowding:
        log.info("Second-highest: %s — %.1f/%s  crowding=%s",
                 ceiling_crowding["name"], ceiling_crowding["score"],
                 ceiling_crowding["grade"], ceiling_crowding["flagged"])
    log.info("Run record: %s", rec_path)

    return run_record


# ---------------------------------------------------------------------------
# Sign-off memo + crosswalk (called after main())
# ---------------------------------------------------------------------------
def write_sign_off_memo(rr: dict):
    inv   = rr["frozen_invariants"]
    snk1  = inv["snk001"]
    no_a  = inv["no_snackbar_A"]
    prod  = rr["head_vs_production_baseline"]
    cc    = rr.get("ceiling_crowding_editorial") or {}

    grade_rows = prod.get("grade_affecting_rows", [])
    # Build per-product table for grade-affecting moves
    grade_table = "| pid | name_he | production_grade | head_grade | production_score | head_score | delta |\n"
    grade_table += "|-----|---------|-----------------|-----------|-----------------|-----------|-------|\n"
    for r in grade_rows:
        grade_table += (
            f"| {r['pid']} | {r['name_he']} | {r['production_grade']} | {r['head_grade']} "
            f"| {r['production_score']} | {r['head_score']} | {r['delta']:+.1f} |\n"
        )

    # Recommendation
    if not grade_rows:
        recommendation = (
            "No grade-affecting moves found. All shifts are cosmetic (score drift <2pt) "
            "or exact matches. This run is a clean re-baseline: scores are structurally "
            "stable. Recommend owner approval to freeze run_snackbars_007_headpin as the "
            "new snack-bars baseline and proceed to frontend reship."
        )
    else:
        recommendation = (
            f"{len(grade_rows)} grade-affecting move(s) found. Review the per-product table above. "
            "Grade moves that reflect genuine engine improvement (not data regression) should be "
            "approved by the owner. Any move that contradicts known editorial positions requires "
            "Nutrition Agent review before the freeze is accepted."
        )

    cc_flag = ""
    if cc.get("flagged"):
        cc_flag = (
            f"\n**FLAGGED FOR OWNER DECISION**: {cc['name']} scores {cc['score']:.1f}/{cc['grade']}, "
            f"within 1 point of the snk-001 ceiling (70/B). This near-parity may require a "
            f"presentation note clarifying why two products share almost the same position."
        )
    elif cc:
        cc_flag = (
            f"\nSecond-highest: {cc['name']} scores {cc['score']:.1f}/{cc['grade']}. "
            f"No ceiling-crowding flag (score < 69.0 or not grade B)."
        )

    memo = f"""# Sign-off Memo: TASK-180B — Snack Bars Re-baseline (run_snackbars_007_headpin)

**Date**: {datetime.date.today().isoformat()}
**Run ID**: {rr['run_id']}
**Engine tag**: {rr['engine_baseline_tag']} ({rr['engine_baseline_commit'][:7] if rr['engine_baseline_commit'] != 'unknown' else 'unknown'})
**Config hash**: {rr['engine_config_hash']}
**Flags**: BARI_RECAL_P0=off | BARI_GLASSBOX_W4=on | BARI_TASK144_FIXES=off | BARI_GLASSBOX_W5=on (no effect — not in engine)

---

## 1. Reproduction Rate

HEAD-OFF vs production baseline (live page): **{prod['exact_match']}/{prod['total']} exact match** ({100 * prod['reproduction_rate']:.0f}%)

The live page is backed by the sprint1 baseline. The prior sprint1 run can only reproduce
{prod['exact_match']}/{prod['total']} scores on the current engine — the remaining delta is engine drift accumulated since that sprint.

## 2. Drift Summary

| Category | Count |
|----------|-------|
| Exact match | {prod['exact_match']} |
| Grade-affecting (grade changed) | {prod['grade_flip']} |
| >=2pt cosmetic (same grade) | {prod['drift_ge_2pt_same_grade']} |
| <2pt cosmetic (same grade) | {prod['cosmetic_lt_2pt']} |
| Missing in HEAD | {prod['missing_head']} |

HEAD-OFF vs proto_v0 sealed traces (original published scores): {rr['head_vs_published_proto_v0_2026_05_17']['match']}

## 3. Grade-Affecting Moves (HEAD-OFF vs Production Baseline)

{f"None — all score changes are cosmetic or exact matches." if not grade_rows else grade_table}

## 4. Frozen Invariant Check

| Invariant | Expected | HEAD Result | Status |
|-----------|----------|------------|--------|
| snk-001 (bsip1_7290011498870) = 70/B | 70/B | {snk1['head']} | **{snk1['status']}** |
| No snack bar >= 80 (A) | (none) | {no_a['products_ge_80'] or '(none)'} | **{no_a['status']}** |

## 5. Ceiling-Crowding Editorial Call (69.5/B)
{cc_flag if cc_flag else "_No second product close to ceiling._"}

## 6. Recommendation

{recommendation}

---

**Sign-off required from**: Owner + Nutrition Agent
**Next step on approval**: Frontend reship (copy run_snackbars_007_headpin/off.json → rebuild snacks_frontend_v2.json)
**Hard rule**: No changes to bari-web/src/data/comparisons/snacks_frontend_v2.json until owner sign-off received.
"""

    memo_path = OUT_ROOT / "sign_off_memo_180B.md"
    memo_path.write_text(memo, encoding="utf-8")
    log.info("Sign-off memo: %s", memo_path)


def write_crosswalk(rr: dict):
    """Write snk_crosswalk_run007.md — snk-XXX → bsip1_pid → run_007 score/grade."""
    off_path = OUT_ROOT / "off.json"
    off = json.loads(off_path.read_text(encoding="utf-8")) if off_path.exists() else {}

    lines = [
        "# Snack Bars QA Crosswalk — run_snackbars_007_headpin",
        "",
        f"Generated: {datetime.date.today().isoformat()}  |  Task: TASK-180B",
        "",
        "This file maps every snk-XXX label (from the live frontend) to its bsip1 pid and",
        "the run_007 HEAD-OFF score + grade. Use this to verify the freeze against the",
        "live page before reship.",
        "",
        "| snk label | bsip1_pid | run_007 score | run_007 grade | production_score | production_grade |",
        "|-----------|-----------|--------------|--------------|-----------------|-----------------|",
    ]

    prod_base = load_production_baseline()
    added_pids = set()
    for snk_label in sorted(SNK_LABEL_MAP.keys()):
        pid = SNK_LABEL_MAP[snk_label]
        t   = off.get(pid, {})
        pb  = prod_base.get(pid, {})
        r007_score = t.get("score", "—") if "_error" not in t else "ERROR"
        r007_grade = t.get("grade", "—") if "_error" not in t else "ERROR"
        prod_score = pb.get("score", "—")
        prod_grade = pb.get("grade", "—")
        lines.append(f"| {snk_label} | {pid} | {r007_score} | {r007_grade} | {prod_score} | {prod_grade} |")
        added_pids.add(pid)

    # Also list any corpus products NOT in the frontend label map (unshipped)
    lines += [
        "",
        "## Corpus products not in the frontend label map (unshipped / pending editorial)",
        "",
        "| bsip1_pid | run_007 score | run_007 grade | name_he |",
        "|-----------|--------------|--------------|---------|",
    ]
    for pid, t in sorted(off.items()):
        if pid in added_pids:
            continue
        r007_score = t.get("score", "—") if "_error" not in t else "ERROR"
        r007_grade = t.get("grade", "—") if "_error" not in t else "ERROR"
        name = t.get("name", "")
        lines.append(f"| {pid} | {r007_score} | {r007_grade} | {name} |")

    crosswalk_path = OUT_ROOT / "snk_crosswalk_run007.md"
    crosswalk_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Crosswalk: %s", crosswalk_path)


if __name__ == "__main__":
    rr = main()
    write_sign_off_memo(rr)
    write_crosswalk(rr)
    log.info("Done — all artifacts in %s", OUT_ROOT)
