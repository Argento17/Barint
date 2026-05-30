"""
BSIP2 Router v2 Regression Check

Loads the router regression corpus and validates each routing decision:
  - Correct category assigned?
  - Anchor override flag matches expectation?
  - No must_not_be category assigned?
  - Subtype expectation met (where declared)?

Output: 03_operations/reports/regression/router_regression_001.md
Run after any change to router_v2.py.
"""

import sys
import json
import pathlib
import datetime
import logging

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from router_v2 import classify_category, ROUTER_VERSION

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

CORPUS_PATH = pathlib.Path(__file__).parent / "router_regression_corpus.json"
REPORT_ROOT = pathlib.Path(r"C:\Bari\03_operations\reports\regression")


def load_corpus() -> dict:
    with open(CORPUS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _check_entry(entry: dict) -> dict:
    product  = entry["product"]
    result   = classify_category(product)
    category = result["category"]
    anchor   = result.get("anchor_override", False)
    subtype  = result.get("category_subtype")
    suppressed = result.get("routing_suppressed_signals", [])
    hybrid   = result.get("is_hybrid", False)
    instability = result.get("routing_instability_warning")

    failures: list[str] = []

    exp_cat = entry.get("expected_category")
    if category != exp_cat:
        failures.append(f"FAIL: category={category!r} (expected {exp_cat!r})")

    for must_not in entry.get("must_not_be", []):
        if category == must_not:
            failures.append(f"FAIL: category={category!r} is in must_not_be")

    if "expected_anchor_override" in entry:
        exp_anchor = entry["expected_anchor_override"]
        if anchor != exp_anchor:
            level = "FAIL" if not exp_anchor else "WARN"
            failures.append(f"{level}: anchor_override={anchor} (expected {exp_anchor})")

    if "expected_subtype" in entry:
        exp_sub = entry["expected_subtype"]
        if subtype != exp_sub:
            failures.append(f"WARN: subtype={subtype!r} (expected {exp_sub!r})")

    has_fail = any(f.startswith("FAIL:") for f in failures)
    has_warn = any(f.startswith("WARN:") for f in failures)
    status   = "FAIL" if has_fail else ("WARN" if has_warn else "PASS")

    return {
        "id":          entry["id"],
        "description": entry.get("description", ""),
        "failure_mode": entry.get("failure_mode", ""),
        "status":      status,
        "reason":      "; ".join(failures) if failures else None,
        "category":    category,
        "expected":    exp_cat,
        "anchor":      anchor,
        "subtype":     subtype,
        "confidence":  result.get("category_confidence"),
        "confidence_band": result.get("confidence_band"),
        "secondary":   result.get("secondary_category"),
        "suppressed":  suppressed,
        "is_hybrid":   hybrid,
        "instability": instability,
        "raw_scores":  result.get("raw_category_scores", {}),
    }


def _write_report(results: list[dict], corpus: dict) -> pathlib.Path:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    n_pass = sum(1 for r in results if r["status"] == "PASS")
    n_warn = sum(1 for r in results if r["status"] == "WARN")
    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    n_tot  = len(results)
    overall = "PASS" if n_fail == 0 and n_warn == 0 else ("WARN" if n_fail == 0 else "FAIL")

    lines = [
        "# BSIP2 Router v2 Regression Report",
        "",
        f"**Run date:** {run_dt}",
        f"**Router:** {ROUTER_VERSION}",
        f"**Corpus:** {corpus.get('corpus_version', '?')}",
        f"**Overall:** {overall}",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| PASS   | {n_pass}  |",
        f"| WARN   | {n_warn}  |",
        f"| FAIL   | {n_fail}  |",
        f"| TOTAL  | {n_tot}   |",
        "",
        "---",
        "",
        "## Results",
        "",
    ]

    for r in results:
        icon = {"PASS": "✓", "WARN": "⚠", "FAIL": "✗"}.get(r["status"], "?")
        lines.append(f"### {icon} `{r['id']}` — {r['status']}")
        lines.append(f"")
        lines.append(f"**{r['description']}**  ")
        lines.append(f"Failure mode tested: `{r['failure_mode']}`  ")
        lines.append(
            f"Category: **{r['category']}** (expected: {r['expected']}) | "
            f"Conf: {r['confidence']} ({r['confidence_band']}) | "
            f"Anchor: {r['anchor']} | Subtype: {r['subtype']}"
        )
        if r["is_hybrid"]:
            lines.append(f"⚠ Hybrid product detected (secondary: {r['secondary']})")
        if r["instability"]:
            lines.append(f"⚠ Instability: {r['instability']}")
        if r["suppressed"]:
            lines.append(f"Suppressed signals: `{'  |  '.join(r['suppressed'][:6])}`")
        if r["raw_scores"]:
            top3 = sorted(r["raw_scores"].items(), key=lambda x: -x[1])[:4]
            score_str = "  ".join(f"{k}={v:.3f}" for k, v in top3 if v > 0)
            lines.append(f"Raw scores: `{score_str}`")
        if r["reason"]:
            lines.append(f"")
            lines.append(f"**Issues:** {r['reason']}")
        lines.append("")

    # Failure summary
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        lines += ["---", "", "## Failures Requiring Action", ""]
        for r in failures:
            lines.append(f"- `{r['id']}`: {r['reason']}")
        lines.append("")

    # Suppression summary (shows that contamination was caught)
    with_suppressed = [r for r in results if r["suppressed"]]
    if with_suppressed:
        lines += ["---", "", "## Signal Suppression Log", "",
                  "These cases had contaminating signals that were suppressed by context gating.", ""]
        for r in with_suppressed:
            lines.append(f"- **{r['id']}** ({r['category']}): {', '.join(r['suppressed'][:4])}")
        lines.append("")

    path = REPORT_ROOT / "router_regression_001.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_router_regression():
    log.info("=== BSIP2 Router v2 Regression Check ===")
    corpus  = load_corpus()
    entries = corpus.get("entries", [])
    log.info("Corpus entries: %d", len(entries))

    results = []
    for entry in entries:
        eid = entry.get("id", "?")
        r   = _check_entry(entry)
        results.append(r)
        log.info("  %-40s → %s  cat=%s  anchor=%s  %s",
                 eid, r["status"], r["category"], r["anchor"],
                 r.get("reason") or "")

    path = _write_report(results, corpus)
    log.info("Report: %s", path)

    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    n_warn = sum(1 for r in results if r["status"] == "WARN")
    if n_fail:
        log.warning("ROUTER REGRESSION: %d failures", n_fail)
    elif n_warn:
        log.warning("ROUTER REGRESSION: %d warnings", n_warn)
    else:
        log.info("ROUTER REGRESSION: all passed")

    return results


if __name__ == "__main__":
    run_router_regression()
