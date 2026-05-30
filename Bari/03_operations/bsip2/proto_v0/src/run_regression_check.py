"""
BSIP2 Regression Check Runner v1

Loads the golden corpus manifest and validates each entry against expectations:
  - Score within expected band?
  - Primary structural class matches expected?
  - Required signals present?
  - No must_not_primary structural class assigned?

Outputs a regression report to 03_operations/reports/regression/.
Run this after any engine change to detect unintended behavioral drift.
"""

import sys
import json
import pathlib
import datetime
import logging

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from structural_classifier import classify_structural_class, classify_from_bundle, MODULE_VERSION

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

CORPUS_PATH  = pathlib.Path(r"C:\Bari\01_framework\bsip2_framework\validation\golden_corpus\golden_corpus_manifest.json")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\03_operations\reports\regression")
SCORE_DRIFT_THRESHOLD = 5.0  # flag if score moves more than this from prior baseline


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def load_corpus() -> dict:
    with open(CORPUS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_trace(path: str) -> dict | None:
    p = pathlib.Path(path)
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

def _check_real_product(entry: dict) -> dict:
    trace = load_trace(entry.get("trace_path", ""))
    if trace is None:
        return _make_result(entry, status="SKIP", reason="trace file not found", trace=None)

    structural_result = classify_structural_class(trace)
    primary   = structural_result.get("primary")
    score     = trace.get("final_score_estimate")
    nova      = trace.get("nova_proxy")

    failures = []

    # Structural class checks
    exp_sc      = entry.get("expected_structural_class", {})
    exp_primary = exp_sc.get("primary")
    must_not    = exp_sc.get("must_not_primary", [])

    if primary != exp_primary:
        acceptable = exp_sc.get("acceptable_secondary", []) or []
        if primary in acceptable:
            failures.append(f"WARN: structural_class={primary} (expected {exp_primary}, but acceptable as secondary)")
        else:
            failures.append(f"FAIL: structural_class={primary} (expected {exp_primary})")

    if primary in must_not:
        failures.append(f"FAIL: structural_class={primary} is in must_not_primary={must_not}")

    # Score band
    band = entry.get("expected_score_band", {})
    if score is not None and band:
        if score < band.get("min", 0):
            failures.append(f"FAIL: score={score} below expected minimum {band['min']}")
        elif score > band.get("max", 100):
            failures.append(f"FAIL: score={score} above expected maximum {band['max']}")

    # NOVA band
    nova_band = entry.get("expected_nova_band")
    if nova_band and nova is not None:
        if nova not in nova_band:
            failures.append(f"WARN: nova={nova} not in expected band {nova_band}")

    # Signal checks
    exp_signals = entry.get("expected_signals", {})
    l3 = trace.get("L3_inferred_classifications") or {}
    dim = trace.get("dimension_scores") or {}

    if "sweetener_detected" in exp_signals:
        actual_sw = l3.get("sweetener_detected", False)
        if actual_sw != exp_signals["sweetener_detected"]:
            failures.append(f"WARN: sweetener_detected={actual_sw} (expected {exp_signals['sweetener_detected']})")

    if "additive_quality_min" in exp_signals:
        actual_aq = dim.get("additive_quality", 0)
        if actual_aq < exp_signals["additive_quality_min"]:
            failures.append(f"FAIL: additive_quality={actual_aq} below minimum {exp_signals['additive_quality_min']}")

    if "additive_marker_count_min" in exp_signals:
        actual_ct = l3.get("additive_marker_count", 0)
        if actual_ct < exp_signals["additive_marker_count_min"]:
            failures.append(f"WARN: additive_marker_count={actual_ct} below minimum {exp_signals['additive_marker_count_min']}")

    if "additive_marker_count_max" in exp_signals:
        actual_ct = l3.get("additive_marker_count", 0)
        if actual_ct > exp_signals["additive_marker_count_max"]:
            failures.append(f"WARN: additive_marker_count={actual_ct} above maximum {exp_signals['additive_marker_count_max']}")

    has_failures = any(f.startswith("FAIL:") for f in failures)
    has_warnings = any(f.startswith("WARN:") for f in failures)
    status = "FAIL" if has_failures else ("WARN" if has_warnings else "PASS")

    return _make_result(entry, status=status, reason="; ".join(failures) if failures else None,
                        trace=trace, structural_result=structural_result,
                        score=score, nova=nova, primary=primary)


def _check_signal_bundle(entry: dict) -> dict:
    bundle = entry.get("signal_bundle", {})
    if not bundle:
        return _make_result(entry, status="SKIP", reason="no signal_bundle defined", trace=None)

    structural_result = classify_from_bundle(bundle)
    primary = structural_result.get("primary")

    failures = []
    exp_sc      = entry.get("expected_structural_class", {})
    exp_primary = exp_sc.get("primary")
    must_not    = exp_sc.get("must_not_primary", [])

    if primary != exp_primary:
        acceptable = exp_sc.get("acceptable_secondary") or []
        if primary in acceptable:
            failures.append(f"WARN: structural_class={primary} (expected {exp_primary}, acceptable as secondary)")
        else:
            failures.append(f"FAIL: structural_class={primary} (expected {exp_primary})")

    if primary in must_not:
        failures.append(f"FAIL: structural_class={primary} is in must_not_primary={must_not}")

    has_failures = any(f.startswith("FAIL:") for f in failures)
    has_warnings = any(f.startswith("WARN:") for f in failures)
    status = "FAIL" if has_failures else ("WARN" if has_warnings else "PASS")

    return _make_result(entry, status=status, reason="; ".join(failures) if failures else None,
                        trace=None, structural_result=structural_result,
                        score=None, nova=bundle.get("nova_proxy"), primary=primary)


def _make_result(entry, status, reason, trace, structural_result=None, score=None, nova=None, primary=None):
    return {
        "id":               entry["id"],
        "description":      entry.get("description", ""),
        "type":             entry.get("type", "unknown"),
        "status":           status,
        "reason":           reason,
        "score":            score,
        "nova":             nova,
        "structural_class":  primary,
        "class_weights":    structural_result.get("class_weights") if structural_result else None,
        "is_between_worlds": structural_result.get("is_between_worlds") if structural_result else False,
        "expected_primary": entry.get("expected_structural_class", {}).get("primary"),
        "expected_band":    entry.get("expected_score_band"),
    }


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def _write_report(results: list[dict], corpus: dict) -> pathlib.Path:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    n_total = len(results)
    n_pass  = sum(1 for r in results if r["status"] == "PASS")
    n_warn  = sum(1 for r in results if r["status"] == "WARN")
    n_fail  = sum(1 for r in results if r["status"] == "FAIL")
    n_skip  = sum(1 for r in results if r["status"] == "SKIP")

    overall = "PASS" if n_fail == 0 and n_warn == 0 else ("WARN" if n_fail == 0 else "FAIL")

    lines = [
        f"# BSIP2 Regression Check Report",
        f"",
        f"**Run date:** {run_dt}",
        f"**Corpus version:** {corpus.get('manifest_version', '?')}",
        f"**Classifier:** {MODULE_VERSION}",
        f"**Overall status:** {overall}",
        f"",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| PASS   | {n_pass}     |",
        f"| WARN   | {n_warn}     |",
        f"| FAIL   | {n_fail}     |",
        f"| SKIP   | {n_skip}     |",
        f"| TOTAL  | {n_total}    |",
        f"",
        f"---",
        f"",
        f"## Results by Entry",
        f"",
    ]

    for r in results:
        icon = {"PASS": "✓", "WARN": "⚠", "FAIL": "✗", "SKIP": "—"}.get(r["status"], "?")
        lines.append(f"### {icon} `{r['id']}` — {r['status']}")
        lines.append(f"")
        lines.append(f"**{r['description']}**  ")
        lines.append(f"Type: {r['type']} | Score: {r['score']} | NOVA: {r['nova']} | "
                     f"Structural class: **{r['structural_class']}** (expected: {r['expected_primary']})")
        if r["expected_band"]:
            lines.append(f"Expected score band: {r['expected_band']['min']}–{r['expected_band']['max']}")
        if r["is_between_worlds"]:
            lines.append(f"⚠ Between-worlds product (strong secondary structural class)")
        if r["class_weights"]:
            weights_str = "  |  ".join(f"{k}={v:.2f}" for k, v in r["class_weights"].items())
            lines.append(f"Class weights: `{weights_str}`")
        if r["reason"]:
            lines.append(f"")
            lines.append(f"**Issues:** {r['reason']}")
        lines.append(f"")

    # Summary of failures
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        lines += [
            "---",
            "",
            "## Failures Requiring Action",
            "",
        ]
        for r in failures:
            lines.append(f"- `{r['id']}`: {r['reason']}")

    # Between-worlds products (calibration interest)
    btw = [r for r in results if r.get("is_between_worlds")]
    if btw:
        lines += [
            "",
            "---",
            "",
            "## Between-Worlds Products (Ontology Tension Zones)",
            "",
            "These products express two structural classes strongly. They are valuable calibration anchors.",
            "",
        ]
        for r in btw:
            lines.append(f"- `{r['id']}` ({r['structural_class']}): weights = {r['class_weights']}")

    path = REPORT_ROOT / "regression_check_001.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_regression_check():
    log.info("=== BSIP2 Regression Check ===")
    log.info("Corpus: %s", CORPUS_PATH)

    corpus = load_corpus()
    entries = corpus.get("entries", [])
    log.info("Entries to check: %d", len(entries))

    results = []
    for entry in entries:
        eid = entry.get("id", "unknown")
        entry_type = entry.get("type", "unknown")
        log.info("  Checking: %s (%s)", eid, entry_type)

        if entry_type == "real_product":
            result = _check_real_product(entry)
        elif entry_type == "signal_bundle":
            result = _check_signal_bundle(entry)
        else:
            result = _make_result(entry, status="SKIP", reason=f"unknown type: {entry_type}", trace=None)

        results.append(result)
        log.info("    → %s  structural_class=%s  score=%s  %s",
                 result["status"], result["structural_class"], result["score"],
                 result.get("reason") or "")

    report_path = _write_report(results, corpus)
    log.info("Report written: %s", report_path)

    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    n_warn = sum(1 for r in results if r["status"] == "WARN")
    if n_fail:
        log.warning("REGRESSION CHECK: %d failures detected", n_fail)
    elif n_warn:
        log.warning("REGRESSION CHECK: %d warnings", n_warn)
    else:
        log.info("REGRESSION CHECK: all entries passed")

    return results


if __name__ == "__main__":
    run_regression_check()
