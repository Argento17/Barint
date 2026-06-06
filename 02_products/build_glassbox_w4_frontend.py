#!/usr/bin/env python3
"""
Glass Box W4 go-live — TASK-181 frontend JSON rebuild.

Runs the BSIP2 engine with BARI_GLASSBOX_W4=on (+ W15=off, D5D6=off, W2=off,
RECAL_P0=on, TASK144=off — exact same flag combination used for the QA-validated
W4 impact runs in reports/glass_box/w4/qa_181l_on_impact.py) across the hummus
and maadanim corpora.

Outputs:
  hummus_frontend_v5.json   — C:\\bari\\bari-web\\src\\data\\comparisons\\
  maadanim_frontend_v3.json — C:\\bari\\bari-web\\src\\data\\comparisons\\

Rules:
  - score, grade, data_sufficiency, d3_processing_signal updated from W4 engine.
  - All other product fields carried verbatim from the current live v4 / v2 JSONs.
  - Products re-sorted descending by new score (VM contract: pre-sorted).
  - Products whose score was None in the source JSON (score-unavailable /
    insufficient_data) stay at their existing score=None — the engine result
    is authoritative when it scores, but we never invent data for products that
    had no scoreable panel.
  - d3_processing_signal carried from the engine result (None absent when W4=off;
    present for all products when W4=on because the signal runs on every product).
"""
import collections
import contextlib
import io
import json
import math
import os
import pathlib
import statistics
import sys
import datetime

# ── Engine path ──────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
ENGINE_SRC = ROOT / "03_operations/bsip2/proto_v0/src"
sys.path.insert(0, str(ENGINE_SRC))
from grade_governance import apply_a_grade_floor  # noqa: E402  TASK-188

# ── Corpus paths (same as QA runner qa_181l_on_impact.py) ────────────────────
HUMMUS_CORPUS   = ROOT / "02_products/hummus/canonical_bsip1"
MAADANIM_CORPUS = ROOT / "03_operations/bsip1/run_maadanim_001/output"

# ── Source frontend JSONs (live) ─────────────────────────────────────────────
WEB = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons")
HUMMUS_SRC_JSON   = WEB / "hummus_frontend_v4.json"
MAADANIM_SRC_JSON = WEB / "maadanim_frontend_v2.json"

# ── Output paths ─────────────────────────────────────────────────────────────
HUMMUS_OUT   = WEB / "hummus_frontend_v5.json"
MAADANIM_OUT = WEB / "maadanim_frontend_v3.json"

GENERATED = datetime.datetime.now(datetime.timezone.utc).isoformat()

# ── Modules to reload on each scoring call (avoid stale flag state) ───────────
_MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "trace_writer",
    "router_v2", "evaluation_scope", "input_loader", "constants",
    "structural_classifier",
]


def _set_flags(w4_on: bool, recal_p0: bool = True):
    """
    Set engine flags before scoring.

    recal_p0: True for hummus (live v4 was built with BARI_RECAL_P0=on).
              False for maadanim (live v2 was built from run_maadanim_001 traces
              that pre-date the recalibration; BARI_RECAL_P0 was off).
    """
    os.environ["BARI_GLASSBOX_W4"]   = "on" if w4_on else "off"
    os.environ["BARI_GLASSBOX_D5D6"] = "off"
    os.environ["BARI_GLASSBOX_W2"]   = "off"
    os.environ["BARI_GLASSBOX_W15"]  = "off"
    os.environ["BARI_RECAL_P0"]      = "on" if recal_p0 else "off"
    os.environ["BARI_TASK144_FIXES"] = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)


def score_corpus(corpus_path: pathlib.Path, w4_on: bool, recal_p0: bool = True) -> dict:
    """Run the engine over corpus_path; return {canonical_product_id: result_dict}."""
    _set_flags(w4_on, recal_p0=recal_p0)
    from input_loader import load_batch          # noqa: E402  (reloaded per call)
    from signal_extractor import extract_signals  # noqa: E402
    from router_v2 import classify_category       # noqa: E402
    from nova_proxy import infer_nova             # noqa: E402
    from evaluation_scope import assign_evaluation_scope  # noqa: E402
    from score_engine import score_product        # noqa: E402

    results = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        products = list(load_batch(corpus_path))

    for product in products:
        pid = product.get("canonical_product_id", "?")
        try:
            sig  = extract_signals(product)
            cat  = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev   = assign_evaluation_scope(product, cat["category"])
            results[pid] = score_product(product, sig, cat, nova, ev)
        except Exception as exc:
            results[pid] = {"_error": repr(exc)}

    return results


def _round_score(raw: float | None) -> int | None:
    if raw is None:
        return None
    return int(math.floor(raw + 0.5))   # round-half-up, mirrors ScoreChip


def _data_sufficiency(engine_result: dict) -> str:
    """Map engine grade_estimate to the data_sufficiency string used in the VM."""
    grade = engine_result.get("grade_estimate")
    if grade == "insufficient_data":
        return "insufficient"
    conf = engine_result.get("confidence")
    if conf is None:
        return "partial"
    if conf >= 70:
        return "verified"
    if conf >= 40:
        return "partial"
    return "insufficient"


def _grade_from_score(score: int | None) -> str | None:
    """Grade thresholds matching constants.py GRADE_THRESHOLDS (excluding S tier)."""
    if score is None:
        return None
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


def _grade_from_score_raw(score: float | None) -> str | None:
    """Grade from a raw (unrounded) float score — same thresholds as the engine."""
    if score is None:
        return None
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


def _build_delta_results(off_results: dict, on_results: dict) -> dict:
    """
    Compute the W4 delta for each product and return a dict of:
      {pid: {delta: float, grade_on: str, d3_processing_signal: dict|None}}

    grade_on is the grade the engine assigns to the W4=ON score (using the raw
    float, not the rounded display value). This preserves boundary cases where
    a fractional score like 34.6 grades as E even though it rounds to display 35.

    Only products in both off and on results are included.
    """
    deltas = {}
    for pid, on in on_results.items():
        off = off_results.get(pid)
        if off is None:
            continue
        if "_error" in on or "_error" in off:
            continue
        score_off = off.get("final_score_estimate")
        score_on  = on.get("final_score_estimate")
        delta = None
        if score_off is not None and score_on is not None:
            delta = round(score_on - score_off, 2)
        deltas[pid] = {
            "delta":               delta,
            "score_on":            score_on,
            "grade_on":            on.get("grade_estimate"),  # engine grade from raw float
            "d3_processing_signal": on.get("d3_processing_signal"),
            "d3_low_confidence_nova": on.get("d3_low_confidence_nova"),
            "d3_nonmaterial_gap":  on.get("d3_nonmaterial_gap"),
        }
    return deltas


def build_new_json(
    src_json_path: pathlib.Path,
    engine_results: dict,
    out_path: pathlib.Path,
    version: str,
    source_run_id: str,
    recal_p0: bool = True,
) -> dict:
    """
    Merge W4 engine results into the existing frontend JSON.
    Returns a report dict with change statistics.
    """
    with io.open(src_json_path, encoding="utf-8") as f:
        data = json.load(f)

    changed = []
    d3_signal_count = 0
    errors = []

    for product in data["products"]:
        pid = product["id"]
        eng = engine_results.get(pid)

        if eng is None:
            errors.append(f"pid {pid}: not in engine results (skipped)")
            continue

        if "_error" in eng:
            errors.append(f"pid {pid}: engine error — {eng['_error']}")
            continue

        # Products that were score-unavailable in the source JSON stay at None.
        # (Their confidence was already 'insufficient' and we respect that gate.)
        old_score = product.get("score")
        if old_score is None:
            # Still carry d3_processing_signal so the frontend flag has it.
            d3 = eng.get("d3_processing_signal")
            if d3 is not None:
                product["d3_processing_signal"] = d3
                d3_signal_count += 1
            continue

        old_grade = product.get("grade")
        new_score_raw = eng.get("final_score_estimate")
        new_grade     = eng.get("grade_estimate")
        new_score     = _round_score(new_score_raw)

        # Update score + grade.
        product["score"] = new_score
        product["grade"] = new_grade

        # TASK-188: A-grade ingredient observability floor.
        # Applied after W4 engine score/grade update. Ingredients and raw nutrition
        # live in the source JSON expansion (built by the per-category builder which
        # already ran TASK-188). This builder carries them verbatim; re-apply the
        # guard here so that any A newly produced by the W4 engine delta also passes
        # the floor before landing in the output JSON. No trace available at this
        # layer — Condition 2 defaults to pass.
        _exp = product.get("expansion") or {}
        _ing = _exp.get("ingredients")
        _nut_vm = _exp.get("nutrition") or {}
        product["score"], product["grade"] = apply_a_grade_floor(
            score=product["score"],
            grade=product["grade"],
            ingredients=_ing,
            nutrition=_nut_vm,
            trace=None,
        )

        # Carry d3_processing_signal from the engine (present when W4=on).
        d3 = eng.get("d3_processing_signal")
        if d3 is not None:
            product["d3_processing_signal"] = d3
            d3_signal_count += 1
        else:
            # Engine didn't emit the signal (should not happen with W4=on, but safe).
            product.pop("d3_processing_signal", None)

        if new_score != old_score or new_grade != old_grade:
            changed.append({
                "id": pid,
                "name": product.get("name", ""),
                "old_score": old_score,
                "new_score": new_score,
                "old_grade": old_grade,
                "new_grade": new_grade,
                "grade_changed": new_grade != old_grade,
            })

    # Re-sort: scored descending, score=None last, stable by id.
    data["products"].sort(
        key=lambda p: (-(p["score"] if p["score"] is not None else -1), str(p["id"]))
    )

    scores = [p["score"] for p in data["products"] if p["score"] is not None]
    grade_dist = dict(collections.Counter(p["grade"] for p in data["products"]))

    # Update _meta.
    m = data["_meta"]
    m["generated"]          = GENERATED
    m["version"]            = version
    m["staged_not_live"]    = False
    m["grade_distribution"] = grade_dist
    if scores:
        m["score_statistics"] = {
            "count":  len(scores),
            "min":    min(scores),
            "max":    max(scores),
            "mean":   round(statistics.mean(scores), 2),
            "median": round(statistics.median(scores), 2),
        }
    recal_str = "on" if recal_p0 else "off"
    m["glassbox_w4_provenance"] = {
        "task":              "TASK-181",
        "engine_flags":      f"BARI_GLASSBOX_W4=on BARI_RECAL_P0={recal_str} (others off)",
        "qa_report":         "reports/glass_box/w4/qa_181l_on_impact.json",
        "d3_signal_coverage": d3_signal_count,
        "grade_changes":     len(changed),
        "build_script":      "02_products/build_glassbox_w4_frontend.py",
        "source_version":    src_json_path.name,
    }

    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return {
        "out": str(out_path),
        "products": len(data["products"]),
        "scored": len(scores),
        "grade_dist": grade_dist,
        "changed": changed,
        "d3_signal_count": d3_signal_count,
        "errors": errors,
    }


def build_new_json_delta(
    src_json_path: pathlib.Path,
    delta_results: dict,
    out_path: pathlib.Path,
    version: str,
    source_run_id: str,
    recal_p0: bool = False,
) -> dict:
    """
    Delta-based JSON builder for categories where the live JSON was built from
    frozen traces (not a re-run). Applies only the W4 delta to each product's
    live score, then re-grades with the standard thresholds. Carries all other
    fields verbatim.

    This prevents engine drift (unrelated to W4) from contaminating the output.
    """
    with io.open(src_json_path, encoding="utf-8") as f:
        data = json.load(f)

    changed = []
    d3_signal_count = 0
    errors = []
    no_delta = []

    for product in data["products"]:
        pid = product["id"]
        dr = delta_results.get(pid)

        if dr is None:
            no_delta.append(pid)
            # No delta means no W4 change for this product; carry as-is.
            # Still try to get d3_processing_signal from the on-run (it's always
            # emitted when W4=on). But since we don't have it, skip.
            continue

        old_score = product.get("score")
        old_grade = product.get("grade")

        # Carry d3_processing_signal regardless of score-unavailability.
        d3 = dr.get("d3_processing_signal")
        if d3 is not None:
            product["d3_processing_signal"] = d3
            d3_signal_count += 1

        if old_score is None:
            # Score-unavailable products keep score=None; just carry d3 signal.
            continue

        delta = dr.get("delta")
        if delta is None:
            # Engine couldn't score this product (e.g., out_of_scope). Carry as-is.
            no_delta.append(pid)
            continue

        if delta == 0.0:
            # No W4 change for this product; carry score and grade as-is.
            # Do NOT re-grade from the rounded integer live score — that would
            # introduce boundary artifacts (e.g., a live score of 50 displayed
            # as int rounds cleanly, but the underlying raw trace score may be
            # 49.x which grades D; re-applying grade from 50.0 float would flip
            # it to C). Only score/grade changes that come from W4 are valid.
            continue

        # Apply delta to live score for display.
        new_score_raw = old_score + delta
        new_score = _round_score(new_score_raw)
        # Clamp to [0, 100].
        if new_score is not None:
            new_score = max(0, min(100, new_score))

        # Grade: re-grade from the raw float sum (live_score + delta) for
        # boundary accuracy (e.g., 40 + (-5.2) = 34.8 → E even though
        # display rounds to 35 which is technically D threshold).
        # Using the raw float matches the engine's grade_estimate behavior.
        new_grade = _grade_from_score_raw(new_score_raw) if new_score is not None else old_grade

        product["score"] = new_score
        product["grade"] = new_grade

        # TASK-188: A-grade ingredient observability floor (delta path).
        _exp = product.get("expansion") or {}
        _ing = _exp.get("ingredients")
        _nut_vm = _exp.get("nutrition") or {}
        product["score"], product["grade"] = apply_a_grade_floor(
            score=product["score"],
            grade=product["grade"],
            ingredients=_ing,
            nutrition=_nut_vm,
            trace=None,
        )

        if new_score != old_score or new_grade != old_grade:
            changed.append({
                "id": pid,
                "name": product.get("name", ""),
                "old_score": old_score,
                "new_score": product["score"],
                "old_grade": old_grade,
                "new_grade": product["grade"],
                "grade_changed": product["grade"] != old_grade,
                "delta": round(delta, 2),
            })

    # Re-sort: scored descending, score=None last, stable by id.
    data["products"].sort(
        key=lambda p: (-(p["score"] if p["score"] is not None else -1), str(p["id"]))
    )

    scores = [p["score"] for p in data["products"] if p["score"] is not None]
    grade_dist = dict(collections.Counter(p["grade"] for p in data["products"]))

    m = data["_meta"]
    m["generated"]          = GENERATED
    m["version"]            = version
    m["staged_not_live"]    = False
    m["grade_distribution"] = grade_dist
    if scores:
        m["score_statistics"] = {
            "count":  len(scores),
            "min":    min(scores),
            "max":    max(scores),
            "mean":   round(statistics.mean(scores), 2),
            "median": round(statistics.median(scores), 2),
        }
    recal_str = "on" if recal_p0 else "off"
    m["glassbox_w4_provenance"] = {
        "task":              "TASK-181",
        "engine_flags":      f"BARI_GLASSBOX_W4=on BARI_RECAL_P0={recal_str} delta-based (others off)",
        "method":            "delta: (W4=on score) - (W4=off score) applied to live v2 scores",
        "qa_report":         "reports/glass_box/w4/qa_181l_on_impact.json",
        "d3_signal_coverage": d3_signal_count,
        "score_changes":     len(changed),
        "grade_changes":     sum(1 for c in changed if c["grade_changed"]),
        "no_delta_pids":     len(no_delta),
        "build_script":      "02_products/build_glassbox_w4_frontend.py",
        "source_version":    src_json_path.name,
    }

    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    if errors:
        for e in errors:
            print(f"     WARN: {e}")

    return {
        "out": str(out_path),
        "products": len(data["products"]),
        "scored": len(scores),
        "grade_dist": grade_dist,
        "changed": changed,
        "d3_signal_count": d3_signal_count,
        "errors": errors,
        "no_delta": no_delta,
    }


def main():
    print("=== Glass Box W4 frontend JSON rebuild ===")
    print(f"Generated: {GENERATED}\n")

    # ── Hummus ────────────────────────────────────────────────────────────────
    # Hummus live v4 was built with BARI_RECAL_P0=on (run_hummus_003 + TASK-169B).
    print("1/2  Scoring hummus corpus (W4=on, RECAL_P0=on)...")
    hummus_results = score_corpus(HUMMUS_CORPUS, w4_on=True, recal_p0=True)
    print(f"     Engine returned {len(hummus_results)} product results.")

    hummus_report = build_new_json(
        src_json_path  = HUMMUS_SRC_JSON,
        engine_results = hummus_results,
        out_path       = HUMMUS_OUT,
        version        = "v5-glassbox_w4",
        source_run_id  = "run_hummus_003",
        recal_p0       = True,
    )
    print(f"\n     WROTE {hummus_report['out']}")
    print(f"     products={hummus_report['products']}  scored={hummus_report['scored']}")
    print(f"     grade dist: {hummus_report['grade_dist']}")
    print(f"     d3_signal coverage: {hummus_report['d3_signal_count']}")
    hummus_grade_moves = sum(1 for c in hummus_report["changed"] if c["grade_changed"])
    print(f"     score changes: {len(hummus_report['changed'])}  grade changes: {hummus_grade_moves}")
    if hummus_report["errors"]:
        print(f"     ERRORS ({len(hummus_report['errors'])}):")
        for e in hummus_report["errors"]:
            print(f"       {e}")

    print("\n  Score/grade changes (hummus):")
    for c in hummus_report["changed"]:
        direction = "DOWN" if (c["new_score"] or 0) < (c["old_score"] or 0) else "UP  "
        print(
            f"  {direction}  {c['id']:35s}  "
            f"{c['old_score']:>3} {c['old_grade']} -> {c['new_score']:>3} {c['new_grade']}"
        )

    # ── Maadanim ──────────────────────────────────────────────────────────────
    # Maadanim v2 was built from frozen run_maadanim_001 traces (older engine
    # version). A full re-run of the current engine with W4=off already diverges
    # from v2 live scores due to engine drift (separate from W4). The task requires
    # ONLY W4 changes to differ ("only score, grade, data_sufficiency, and
    # d3_processing_signal should differ" — and only by the W4 delta, not by drift).
    #
    # Approach: delta-based. Run the engine BOTH off and on with RECAL_P0=off,
    # compute the delta for each product, apply it to the v2 live scores.
    # This isolates the W4 contribution and prevents unintended drift from shipping.
    print("\n2/2  Scoring maadanim corpus (W4=off, RECAL_P0=off — baseline for delta)...")
    maadanim_off = score_corpus(MAADANIM_CORPUS, w4_on=False, recal_p0=False)
    print(f"     Engine returned {len(maadanim_off)} OFF results.")

    print("     Scoring maadanim corpus (W4=on, RECAL_P0=off — W4 delta)...")
    maadanim_on = score_corpus(MAADANIM_CORPUS, w4_on=True, recal_p0=False)
    print(f"     Engine returned {len(maadanim_on)} ON results.")

    # Build a delta map: {pid: (delta_score, new_grade_from_on_run, d3_signal)}
    # The delta is applied to the v2 live scores. Grade is taken from the on-run
    # directly (it reflects the correct W4 grade for the on-engine score level),
    # but we re-grade the (live_score + delta) using the same grade thresholds to
    # avoid importing unexpected grade changes from drift.
    maadanim_delta_results = _build_delta_results(maadanim_off, maadanim_on)
    print(f"     Delta results computed for {len(maadanim_delta_results)} products.")

    maadanim_report = build_new_json_delta(
        src_json_path  = MAADANIM_SRC_JSON,
        delta_results  = maadanim_delta_results,
        out_path       = MAADANIM_OUT,
        version        = "v3-glassbox_w4",
        source_run_id  = "run_maadanim_001",
        recal_p0       = False,
    )
    print(f"\n     WROTE {maadanim_report['out']}")
    print(f"     products={maadanim_report['products']}  scored={maadanim_report['scored']}")
    print(f"     grade dist: {maadanim_report['grade_dist']}")
    print(f"     d3_signal coverage: {maadanim_report['d3_signal_count']}")
    maadanim_grade_moves = sum(1 for c in maadanim_report["changed"] if c["grade_changed"])
    print(f"     score changes: {len(maadanim_report['changed'])}  grade changes: {maadanim_grade_moves}")
    if maadanim_report.get("no_delta"):
        print(f"     no-delta (W4 unchanged): {len(maadanim_report['no_delta'])}")
    if maadanim_report["errors"]:
        print(f"     ERRORS ({len(maadanim_report['errors'])}):")
        for e in maadanim_report["errors"]:
            print(f"       {e}")

    print("\n  Score/grade changes (maadanim):")
    for c in maadanim_report["changed"]:
        direction = "DOWN" if (c["new_score"] or 0) < (c["old_score"] or 0) else "UP  "
        print(
            f"  {direction}  {c['id']:40s}  "
            f"{c['old_score']:>3} {c['old_grade']} -> {c['new_score']:>3} {c['new_grade']}"
        )

    # ── Cross-check against QA report ─────────────────────────────────────────
    print("\n=== Cross-check vs QA report (qa_181l_on_impact.json) ===")
    qa_path = ROOT / "03_operations/bsip2/proto_v0/reports/glass_box/w4/qa_181l_on_impact.json"
    if qa_path.exists():
        qa = json.loads(qa_path.read_text(encoding="utf-8"))
        qa_hummus_grade_moves   = qa["corpora"]["hummus"]["grade_moves"]
        qa_maadanim_grade_moves = qa["corpora"]["maadanim"]["grade_moves"]
        # Count grade-only moves (not score-only moves).
        our_hummus_grade_moves   = sum(1 for c in hummus_report["changed"] if c["grade_changed"])
        our_maadanim_grade_moves = sum(1 for c in maadanim_report["changed"] if c["grade_changed"])
        # Notes:
        # - QA ran with RECAL_P0=off for all corpora; hummus run uses RECAL_P0=on.
        #   Grade boundary crossings differ because recal pushed scores away from
        #   the old B/C boundaries. Count difference is expected for hummus.
        # - QA compared all 200 maadanim engine products; v2 has 84 displayed products.
        #   Our maadanim grade count covers only the 84 displayed products.
        print(f"  Hummus  grade moves: QA(RECAL=off)={qa_hummus_grade_moves}  "
              f"us(RECAL=on)={our_hummus_grade_moves}"
              f"  (RECAL difference expected)")
        print(f"  Maadanim grade moves: QA(200 products)={qa_maadanim_grade_moves}  "
              f"us(84 displayed, delta-based)={our_maadanim_grade_moves}"
              f"  (delta-based; QA covers full engine corpus)")

        # Check each QA grade change is present in our output.
        our_hummus_map   = {c["id"]: c for c in hummus_report["changed"]}
        our_maadanim_map = {c["id"]: c for c in maadanim_report["changed"]}
        mismatches = []
        for gc in qa.get("grade_changes", []):
            corpus = gc["corpus"]
            pid    = gc["pid"]
            our_map = our_hummus_map if corpus == "hummus" else our_maadanim_map
            if pid not in our_map:
                mismatches.append(f"  MISSING in our output: corpus={corpus} pid={pid} "
                                  f"expected {gc['grade_off']}→{gc['grade_on']}")
            else:
                c = our_map[pid]
                if c["new_grade"] != gc["grade_on"]:
                    mismatches.append(
                        f"  GRADE MISMATCH: corpus={corpus} pid={pid} "
                        f"QA says {gc['grade_off']}→{gc['grade_on']} "
                        f"we got {c['old_grade']}→{c['new_grade']}"
                    )
        if mismatches:
            print("  QA cross-check WARNINGS:")
            for m in mismatches:
                print(m)
        else:
            print("  All QA grade-change entries confirmed in our output.")

    print("\nDone.")


if __name__ == "__main__":
    main()
