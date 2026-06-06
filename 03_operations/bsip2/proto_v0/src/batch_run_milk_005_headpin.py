"""
BSIP2 Prototype v0 — Milk & Alternatives Re-baseline Runner (run_005_headpin)
TASK-180A Step 1.

Rescores the SAME milk BSIP1 corpus that produced the published run_004_recalibrated,
on the PINNED engine baseline tag `engine-baseline-2026-06-04` (HEAD f075d9e).

- Same BSIP1 source as run_004 (so every delta is engine-drift, not corpus change).
- Writes to a NEW dir run_005_headpin — does NOT overwrite run_004_recalibrated.
- Emits a per-product delta table (published run_004 vs HEAD) + run_record.json,
  classifying each delta grade-affecting vs <2pt cosmetic.
- Confirms the frozen invariant: milk top 85/A trio (whole / 4% / goat) reproduces.

SHIPS NOTHING. No frontend JSON, no engine edit. Owner sign-off gate is downstream.
"""
import sys
import json
import pathlib
import logging
import datetime
import subprocess

sys.path.insert(0, str(pathlib.Path(__file__).parent))

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

BSIP1_SOURCE   = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
PUBLISHED_ROOT = pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\products")
OUTPUT_ROOT    = pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin")
CATEGORY_TAG   = "milk_and_alternatives"
RUN_ID         = "run_005_headpin"
BASELINE_TAG   = "engine-baseline-2026-06-04"

# Frozen-invariant top trio (CLAUDE.md): milk top = 85/A (whole / 4% / goat dairy).
INVARIANT_TOP = {
    "bsip1_7290000051352": ("whole 3.4% (taste of old days)", 85, "A"),
    "bsip1_7290019790259": ("natural 4%",                      85, "A"),
    "bsip1_7290102392094": ("goat milk",                       85, "A"),
}


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def load_published():
    pub = {}
    for d in PUBLISHED_ROOT.iterdir():
        tf = d / "bsip2_trace.json"
        if tf.exists():
            t = json.load(open(tf, encoding="utf-8"))
            pid = (t.get("input_reference", {}) or {}).get("canonical_product_id") or d.name
            pub[pid] = t
    return pub


def classify_delta(ps, pg, hs, hg):
    """Return (delta, klass). klass in MATCH / cosmetic / DRIFT>=2 / GRADE_FLIP / NULL_FLIP."""
    if ps is None and hs is None:
        return None, "MATCH"
    if ps is None or hs is None:
        return None, "NULL_FLIP"
    delta = round(hs - ps, 1)
    if pg != hg:
        return delta, "GRADE_FLIP"
    if abs(delta) < 0.05:
        return delta, "MATCH"
    if abs(delta) >= 2:
        return delta, "DRIFT>=2"
    return delta, "cosmetic"


def run_batch():
    head_commit = subprocess.run(
        ["git", "-C", r"C:\Bari", "rev-list", "-n", "1", BASELINE_TAG],
        capture_output=True, text=True
    ).stdout.strip()

    log.info("=== BSIP2 Milk re-baseline — %s on %s (%s) ===", RUN_ID, BASELINE_TAG, head_commit[:7])
    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source missing: %s", BSIP1_SOURCE)
        return
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)

    pub = load_published()
    products = load_batch(BSIP1_SOURCE)
    log.info("Published traces: %d   BSIP1 products loaded: %d", len(pub), len(products))

    head = {}
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            head[pid] = trace
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            head[pid] = {"_error": str(e)}

    # Build delta table over the published set (the authoritative 20).
    rows = []
    matched = grade_flip = drift2 = cosmetic = missing = 0
    for pid, pt in sorted(pub.items()):
        ps = pt.get("final_score_estimate")
        pg = pt.get("grade_estimate")
        name = (pt.get("input_reference", {}) or {}).get("product_name_he", "")
        ht = head.get(pid)
        if ht is None or "_error" in (ht or {}):
            rows.append({"product_id": pid, "name_he": name, "pub_score": ps, "pub_grade": pg,
                         "head_score": None, "head_grade": None, "delta": None,
                         "class": "MISSING_HEAD"})
            missing += 1
            continue
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        delta, klass = classify_delta(ps, pg, hs, hg)
        if klass == "MATCH":
            matched += 1
        elif klass == "GRADE_FLIP":
            grade_flip += 1
        elif klass == "DRIFT>=2":
            drift2 += 1
        elif klass == "cosmetic":
            cosmetic += 1
        rows.append({"product_id": pid, "name_he": name, "pub_score": ps, "pub_grade": pg,
                     "head_score": hs, "head_grade": hg, "delta": delta, "class": klass})

    grade_affecting = grade_flip + drift2

    # Invariant check.
    inv = []
    inv_held = True
    for pid, (label, exp_s, exp_g) in INVARIANT_TOP.items():
        ht = head.get(pid, {})
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        held = (hs == exp_s and hg == exp_g)
        inv_held = inv_held and held
        inv.append({"product_id": pid, "label": label, "expected": f"{exp_s}/{exp_g}",
                    "head": f"{hs}/{hg}", "status": "HELD" if held else "BROKEN"})

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-180A",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine_baseline_tag": BASELINE_TAG,
        "engine_baseline_commit": head_commit,
        "bsip1_source": str(BSIP1_SOURCE),
        "published_compared_against": "run_004_recalibrated",
        "published_count": len(pub),
        "head_scored_count": sum(1 for v in head.values() if "_error" not in v),
        "reproduction": {
            "exact_match": matched,
            "total": len(pub),
            "rate": round(matched / len(pub), 3) if pub else None,
        },
        "delta_classification": {
            "grade_affecting": grade_affecting,
            "grade_flips": grade_flip,
            "drift_ge_2pt_same_grade": drift2,
            "cosmetic_lt_2pt": cosmetic,
            "exact_match": matched,
            "missing_head": missing,
        },
        "frozen_invariant_milk_top_85A": {
            "all_held": inv_held,
            "trio": inv,
        },
        "delta_table": rows,
        "ships_nothing": True,
        "notes": "Rescore-only artifact for owner sign-off. No frontend JSON, no engine edit.",
    }

    rec_path = OUTPUT_ROOT / "run_record.json"
    rec_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("Reproduced exactly: %d/%d (%.0f%%)", matched, len(pub), 100 * matched / len(pub))
    log.info("Grade-affecting: %d (%d flips + %d >=2pt same-grade); cosmetic: %d",
             grade_affecting, grade_flip, drift2, cosmetic)
    log.info("Frozen invariant milk top 85/A: %s", "ALL HELD" if inv_held else "*** BROKEN ***")
    log.info("Run record: %s", rec_path)
    return run_record


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
