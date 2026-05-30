"""
BSIP2 Robustness & Uncertainty Sprint v1 — Main Runner

Runs the 50-product noisy corpus through the full BSIP2 pipeline,
applies interpretation_confidence, failure_taxonomy, and graceful_degradation,
then generates 8 validation reports.

Reports generated:
  robustness_validation_001.md          — Full sprint overview + summary table
  uncertainty_behavior_001.md           — How confidence bands behave by group
  noisy_corpus_failures_001.md          — Failure taxonomy breakdown by product
  routing_under_noise_001.md            — Router stability: expected vs actual routing
  missingness_resilience_001.md         — How missing fields affect confidence + score
  confidence_distribution_001.md       — Distribution of confidence bands across corpus
  ambiguity_patterns_001.md            — Hybrid/ambiguous product behavior
  retailer_noise_examples_001.md       — Concrete before/after examples (worst cases)

Output directory: C:/Bari/03_operations/reports/robustness/
"""

import sys
import json
import pathlib
import logging
import datetime
import copy
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader           import validate_product
from signal_extractor       import extract_signals
from router_v2              import classify_category
from nova_proxy             import infer_nova
from evaluation_scope       import assign_evaluation_scope
from score_engine           import score_product, compute_confidence
from trace_writer           import assemble_trace
from interpretation_confidence import compute_interpretation_confidence, apply_confidence_ceiling
from failure_taxonomy          import classify_failures, summarize_failures
from graceful_degradation      import determine_degradation_level, build_degraded_output
from create_robustness_corpus  import CORPUS, OUTPUT_PATH as CORPUS_PATH, main as build_corpus

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

REPORT_DIR = pathlib.Path(r"C:\Bari\03_operations\reports\robustness")
TODAY = datetime.date.today().isoformat()


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline_robust(product: dict) -> dict:
    """
    Full pipeline with robustness layer applied on top of standard BSIP2.
    Returns extended trace dict.
    """
    # Strip test metadata before running through pipeline
    prod = {k: v for k, v in product.items() if not k.startswith("_")}

    # Standard BSIP2 pipeline
    signals     = extract_signals(prod)
    cat_result  = classify_category(prod)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(prod, l3)
    eval_result = assign_evaluation_scope(prod, cat_result["category"])
    score_result = score_product(prod, signals, cat_result, nova_result, eval_result)

    # Base confidence (from score_engine)
    base_conf = compute_confidence(prod, signals, cat_result, nova_result)

    # Robustness layer
    interp_conf = compute_interpretation_confidence(base_conf, cat_result, prod, signals)
    score_result = apply_confidence_ceiling(score_result, interp_conf)

    # Failure taxonomy
    failures = classify_failures(prod, signals, cat_result, nova_result, score_result, interp_conf)
    fail_summary = summarize_failures(failures)

    # Graceful degradation
    degradation_level = determine_degradation_level(interp_conf, score_result, failures)
    degraded_output   = build_degraded_output(prod, score_result, cat_result, interp_conf, failures, degradation_level)

    return {
        "product_id":        product.get("canonical_product_id"),
        "name_he":           product.get("canonical_name_he"),
        "brand":             product.get("brand"),
        "robustness_meta":   product.get("_robustness_meta", {}),
        "category_result":   cat_result,
        "nova_result":       nova_result,
        "score_result":      score_result,
        "base_conf":         base_conf,
        "interp_conf":       interp_conf,
        "failures":          failures,
        "fail_summary":      fail_summary,
        "degradation_level": degradation_level,
        "degraded_output":   degraded_output,
    }


# ---------------------------------------------------------------------------
# Report helpers
# ---------------------------------------------------------------------------

def _grade_bar(score: float | None, width: int = 20) -> str:
    if score is None:
        return "░" * width + " [N/A]"
    filled = int((score / 100) * width)
    return "█" * filled + "░" * (width - filled) + f" {score:.1f}"


def _band_emoji(band: str) -> str:
    return {
        "very_high":          "●",
        "high":               "●",
        "moderate":           "◐",
        "low":                "○",
        "insufficient_context": "◌",
    }.get(band, "?")


def _degradation_label(level: str) -> str:
    return {
        "FULL":         "Full",
        "CAUTIOUS":     "Cautious",
        "UNCERTAINTY":  "Uncertain",
        "INSUFFICIENT": "Insufficient",
    }.get(level, level)


def _routing_match(result: dict) -> str:
    meta = result["robustness_meta"]
    expected = meta.get("expected_routing", "")
    actual   = result["category_result"].get("category", "")
    if not expected:
        return "N/A"
    return "PASS" if expected == actual else f"FAIL (got {actual})"


def _conf_match(result: dict) -> str:
    meta = result["robustness_meta"]
    expected = meta.get("expected_confidence_band", "")
    actual   = result["interp_conf"].get("interpretation_confidence_band", "")
    if not expected:
        return "N/A"
    # Allow ±1 band
    order = ["insufficient_context", "low", "moderate", "high", "very_high"]
    if expected in order and actual in order:
        delta = abs(order.index(expected) - order.index(actual))
        if delta == 0:
            return "EXACT"
        if delta == 1:
            return "CLOSE"
        return f"DRIFT (got {actual})"
    return f"UNK ({actual})"


# ---------------------------------------------------------------------------
# Report 1: robustness_validation_001.md
# ---------------------------------------------------------------------------

def report_robustness_validation(results: list[dict]) -> str:
    lines = [
        f"# BSIP2 Robustness Validation — Sprint v1",
        f"",
        f"Generated: {TODAY}  |  Corpus: robustness_corpus_001 ({len(results)} products)  |  Pipeline: BSIP2 proto_v0",
        f"",
        f"## Sprint Scope",
        f"",
        f"Stress-test BSIP2 against messy real-world data patterns: OCR corruption, missing fields,",
        f"routing instability, claim-vs-reality gaps, hybrid products, and impossible data values.",
        f"",
        f"**Core principle:** When information quality drops, confidence should drop faster than interpretive ambition.",
        f"",
        f"---",
        f"",
        f"## Summary Table",
        f"",
        f"| ID | Name | Group | Routing | Conf Band | Degradation | Failures |",
        f"|:---|:-----|:------|:--------|:----------|:------------|:---------|",
    ]

    group_stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "routing_pass": 0, "degraded": 0, "failures": 0})

    for r in results:
        meta  = r["robustness_meta"]
        gid   = meta.get("test_id", "?")
        grp   = gid[0] if gid else "?"
        name  = (r["name_he"] or "")[:30]
        rmatch = _routing_match(r)
        band  = r["interp_conf"].get("interpretation_confidence_band", "?")
        deg   = _degradation_label(r["degradation_level"])
        nfail = r["fail_summary"].get("failure_count", 0)

        lines.append(f"| {gid} | {name} | {grp} | {rmatch} | {band} | {deg} | {nfail} |")

        group_stats[grp]["total"] += 1
        if "PASS" in rmatch or "EXACT" in rmatch or "CLOSE" in rmatch:
            group_stats[grp]["routing_pass"] += 1
        if r["degradation_level"] in ("UNCERTAINTY", "INSUFFICIENT"):
            group_stats[grp]["degraded"] += 1
        group_stats[grp]["failures"] += nfail

    # Overall stats
    total     = len(results)
    routing_pass = sum(1 for r in results if "PASS" in _routing_match(r) or "EXACT" in _routing_match(r) or "CLOSE" in _routing_match(r))
    full_deg  = sum(1 for r in results if r["degradation_level"] == "FULL")
    cautious  = sum(1 for r in results if r["degradation_level"] == "CAUTIOUS")
    uncertain = sum(1 for r in results if r["degradation_level"] == "UNCERTAINTY")
    insuf     = sum(1 for r in results if r["degradation_level"] == "INSUFFICIENT")
    total_failures = sum(r["fail_summary"].get("failure_count", 0) for r in results)

    lines += [
        f"",
        f"---",
        f"",
        f"## Group Summary",
        f"",
        f"| Group | Products | Routing Pass | Degraded (U/I) | Total Failures |",
        f"|:------|:---------|:-------------|:---------------|:---------------|",
    ]
    for grp, s in sorted(group_stats.items()):
        lines.append(f"| {grp} | {s['total']} | {s['routing_pass']}/{s['total']} | {s['degraded']} | {s['failures']} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Overall Metrics",
        f"",
        f"- **Total products:** {total}",
        f"- **Routing accuracy (pass/close):** {routing_pass}/{total} ({routing_pass/total*100:.0f}%)",
        f"- **Degradation levels:**",
        f"  - FULL: {full_deg} ({full_deg/total*100:.0f}%)",
        f"  - CAUTIOUS: {cautious} ({cautious/total*100:.0f}%)",
        f"  - UNCERTAINTY: {uncertain} ({uncertain/total*100:.0f}%)",
        f"  - INSUFFICIENT: {insuf} ({insuf/total*100:.0f}%)",
        f"- **Total failure instances:** {total_failures}",
        f"- **Average failures per product:** {total_failures/total:.1f}",
        f"",
        f"---",
        f"",
        f"## Key Findings",
        f"",
    ]

    # Auto-generate findings from results
    routing_failures = [r for r in results if "FAIL" in _routing_match(r)]
    high_failure = [r for r in results if r["fail_summary"].get("composite_risk") in ("critical", "high")]
    overconfident = [r for r in results if r["fail_summary"].get("categories_fired", []) and
                     "CONFIDENCE_OVERSTATEMENT" in r["fail_summary"].get("categories_fired", [])]

    if routing_failures:
        lines.append(f"**{len(routing_failures)} routing failures detected:** " +
                     ", ".join(r["robustness_meta"].get("test_id", "?") for r in routing_failures[:5]))
    if high_failure:
        lines.append(f"**{len(high_failure)} products at high/critical failure risk** — require data collection before scoring")
    if overconfident:
        lines.append(f"**{len(overconfident)} confidence overstatement instances** — pipeline confidence does not match data quality")

    lines += [
        f"",
        f"---",
        f"",
        f"*Report generated by run_robustness_sprint.py — BSIP2 Robustness Sprint v1*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 2: uncertainty_behavior_001.md
# ---------------------------------------------------------------------------

def report_uncertainty_behavior(results: list[dict]) -> str:
    lines = [
        f"# Uncertainty Behavior — Confidence Band Analysis",
        f"",
        f"Generated: {TODAY}  |  Corpus: robustness_corpus_001",
        f"",
        f"## How Confidence Bands Respond to Data Quality",
        f"",
        f"This report verifies that confidence degrades appropriately when data quality drops.",
        f"The goal: confidence should drop FASTER than interpretive ambition.",
        f"",
        f"---",
        f"",
        f"## Band Distribution",
        f"",
    ]

    by_band: dict[str, list] = defaultdict(list)
    for r in results:
        band = r["interp_conf"].get("interpretation_confidence_band", "unknown")
        by_band[band].append(r)

    band_order = ["very_high", "high", "moderate", "low", "insufficient_context"]
    for band in band_order:
        products = by_band.get(band, [])
        lines += [
            f"### {band.upper()} — {len(products)} products",
            f"",
        ]
        if not products:
            lines.append("*(none)*\n")
            continue

        for r in products:
            meta = r["robustness_meta"]
            score = r["score_result"].get("final_score_estimate")
            ic    = r["interp_conf"].get("interpretation_confidence_score", 0)
            score_str = f"{score:.1f}" if score is not None else "N/A"
            lines.append(
                f"- **{meta.get('test_id')}** {r['name_he'] or '(no name)'[:25]} "
                f"| score={score_str} "
                f"| ic_score={ic:.0f} "
                f"| scenarios={meta.get('noise_scenarios', [])}"
            )
        lines.append("")

    lines += [
        f"---",
        f"",
        f"## Confidence Reduction Analysis",
        f"",
        f"Products where interpretation_confidence dropped most from base confidence:",
        f"",
        f"| ID | Base Score | IC Score | Drop | Reason |",
        f"|:---|:-----------|:---------|:-----|:-------|",
    ]

    drops = []
    for r in results:
        base = r["interp_conf"].get("base_confidence_score", 0)
        ic   = r["interp_conf"].get("interpretation_confidence_score", 0)
        drop = base - ic
        if drop > 0:
            drops.append((r, drop))
    drops.sort(key=lambda x: x[1], reverse=True)

    for r, drop in drops[:15]:
        meta = r["robustness_meta"]
        reasons = "; ".join(
            d.get("factor", "")[:40]
            for d in r["interp_conf"].get("additional_reductions", [])[:2]
        )
        base = r["interp_conf"].get("base_confidence_score", 0)
        ic   = r["interp_conf"].get("interpretation_confidence_score", 0)
        lines.append(f"| {meta.get('test_id')} | {base:.0f} | {ic:.0f} | {drop:.0f} | {reasons} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Confidence vs Expected Band Match",
        f"",
        f"| ID | Expected Band | Actual Band | Match |",
        f"|:---|:--------------|:------------|:------|",
    ]
    for r in results:
        meta     = r["robustness_meta"]
        expected = meta.get("expected_confidence_band", "")
        actual   = r["interp_conf"].get("interpretation_confidence_band", "")
        match    = _conf_match(r)
        lines.append(f"| {meta.get('test_id')} | {expected} | {actual} | {match} |")

    lines += [
        f"",
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 3: noisy_corpus_failures_001.md
# ---------------------------------------------------------------------------

def report_noisy_corpus_failures(results: list[dict]) -> str:
    lines = [
        f"# Noisy Corpus Failure Taxonomy",
        f"",
        f"Generated: {TODAY}",
        f"",
        f"## Failure Categories in Corpus",
        f"",
    ]

    cat_counts: dict[str, int] = defaultdict(int)
    sev_counts: dict[str, int] = defaultdict(int)
    for r in results:
        for f in r["failures"]:
            cat_counts[f["category"]] += 1
            sev_counts[f["severity"]] += 1

    lines += [
        f"| Failure Category | Count | Description |",
        f"|:-----------------|:------|:------------|",
    ]
    from failure_taxonomy import FAILURE_CATEGORIES
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        desc = FAILURE_CATEGORIES.get(cat, "")[:60]
        lines.append(f"| {cat} | {count} | {desc} |")

    lines += [
        f"",
        f"| Severity | Count |",
        f"|:---------|:------|",
    ]
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        lines.append(f"| {sev} | {sev_counts.get(sev, 0)} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Product-Level Failure Detail",
        f"",
    ]

    for r in results:
        if not r["failures"]:
            continue
        meta     = r["robustness_meta"]
        summary  = r["fail_summary"]
        lines += [
            f"### {meta.get('test_id')} — {r['name_he'] or '(no name)'}",
            f"",
            f"**Risk:** {summary.get('composite_risk', 'none').upper()}  "
            f"| **Failures:** {summary.get('failure_count', 0)}  "
            f"| **Max severity:** {summary.get('max_severity', 'none')}",
            f"",
        ]
        for f in r["failures"]:
            lines += [
                f"- **[{f['severity']}] {f['category']}**",
                f"  - Evidence: {f['evidence'][:100]}",
                f"  - Recommendation: {f['recommendation'][:100]}",
            ]
        lines.append("")

    lines += [
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 4: routing_under_noise_001.md
# ---------------------------------------------------------------------------

def report_routing_under_noise(results: list[dict]) -> str:
    lines = [
        f"# Router Stability Under Noise",
        f"",
        f"Generated: {TODAY}",
        f"",
        f"Tests whether the router produces stable, correct routing under conditions",
        f"that degrade routing signals: OCR, missing names, contaminated ingredients.",
        f"",
        f"---",
        f"",
        f"## Routing Results",
        f"",
        f"| ID | Noise | Expected | Actual | Confidence | Match | Anchor? | Instability? |",
        f"|:---|:------|:---------|:-------|:-----------|:------|:--------|:-------------|",
    ]

    for r in results:
        meta     = r["robustness_meta"]
        cat_r    = r["category_result"]
        expected = meta.get("expected_routing", "")
        actual   = cat_r.get("category", "")
        conf     = cat_r.get("category_confidence", 0)
        match    = _routing_match(r)
        anchor   = "yes" if cat_r.get("anchor_override") else "no"
        unstable = "yes" if cat_r.get("category_instability_flag") else "no"
        scenarios = "; ".join(meta.get("noise_scenarios", []))[:35]
        lines.append(f"| {meta.get('test_id')} | {scenarios} | {expected} | {actual} | {conf:.2f} | {match} | {anchor} | {unstable} |")

    routing_failures = [r for r in results if "FAIL" in _routing_match(r)]
    lines += [
        f"",
        f"---",
        f"",
        f"## Routing Failures Detail ({len(routing_failures)} products)",
        f"",
    ]

    for r in routing_failures:
        meta  = r["robustness_meta"]
        cat_r = r["category_result"]
        scores = cat_r.get("raw_category_scores", {})
        top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        lines += [
            f"### {meta.get('test_id')} — {r['name_he'] or '(no name)'}",
            f"",
            f"- Expected: **{meta.get('expected_routing')}**",
            f"- Actual: **{cat_r.get('category')}** (conf={cat_r.get('category_confidence', 0):.2f})",
            f"- Top signals: {top3}",
            f"- Suppressed: {cat_r.get('routing_suppressed_signals', [])[:3]}",
            f"- Test purpose: {meta.get('test_purpose', '')}",
            f"",
        ]

    lines += [
        f"---",
        f"",
        f"## Anchor Reliability",
        f"",
        f"Products where a hard anchor fired:",
        f"",
    ]
    anchored = [r for r in results if r["category_result"].get("anchor_override")]
    for r in anchored:
        meta  = r["robustness_meta"]
        cat_r = r["category_result"]
        basis = cat_r.get("classification_basis", [])
        lines.append(f"- **{meta.get('test_id')}** {r['name_he'] or ''}[:30] → {cat_r.get('category')} via {basis}")

    lines += [
        f"",
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 5: missingness_resilience_001.md
# ---------------------------------------------------------------------------

def report_missingness_resilience(results: list[dict]) -> str:
    lines = [
        f"# Missingness Resilience",
        f"",
        f"Generated: {TODAY}",
        f"",
        f"How does BSIP2 behave when critical data fields are absent?",
        f"This report focuses on Group B (missing nutrition) and Group C (missing ingredients).",
        f"",
        f"---",
        f"",
        f"## Missing Nutrition Field Impact",
        f"",
        f"| ID | Missing Field | IC Score | IC Band | Score Impact |",
        f"|:---|:-------------|:---------|:--------|:-------------|",
    ]

    group_b = [r for r in results if r["robustness_meta"].get("test_id", "").startswith("B")]
    for r in group_b:
        meta     = r["robustness_meta"]
        scenarios = meta.get("noise_scenarios", [])
        missing  = "; ".join(s.replace("missing_nutrition:", "") for s in scenarios)
        ic_score = r["interp_conf"].get("interpretation_confidence_score", 0)
        ic_band  = r["interp_conf"].get("interpretation_confidence_band", "")
        score    = r["score_result"].get("final_score_estimate")
        score_str = f"{score:.1f}" if score is not None else "N/A"
        lines.append(f"| {meta.get('test_id')} | {missing} | {ic_score:.0f} | {ic_band} | {score_str} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Missing Ingredients Impact",
        f"",
        f"| ID | Scenario | IC Score | IC Band | NOVA Level | Degradation |",
        f"|:---|:---------|:---------|:--------|:-----------|:------------|",
    ]

    group_c = [r for r in results if r["robustness_meta"].get("test_id", "").startswith("C")]
    for r in group_c:
        meta    = r["robustness_meta"]
        scenario = "; ".join(meta.get("noise_scenarios", []))[:40]
        ic_score = r["interp_conf"].get("interpretation_confidence_score", 0)
        ic_band  = r["interp_conf"].get("interpretation_confidence_band", "")
        nova     = r["nova_result"].get("nova_level", "?")
        deg      = _degradation_label(r["degradation_level"])
        lines.append(f"| {meta.get('test_id')} | {scenario} | {ic_score:.0f} | {ic_band} | {nova} | {deg} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Dimension Fallbacks Under Missingness",
        f"",
        f"When fields are missing, these dimensions use neutral fallback (50):",
        f"",
        f"- **energy_kcal absent** → calorie_density = 50 (neutral)",
        f"- **fat_saturated_g absent** → fat_quality = 50 (neutral)",
        f"- **dietary_fiber_g absent** → fiber-dependent dimensions use 0",
        f"- **protein_g absent** → protein_quality and nutrient_density degraded",
        f"- **Full nutrition absent** → most dimensions return neutral; confidence → insufficient_context",
        f"",
        f"---",
        f"",
        f"## Scoring Behavior: All-Null Nutrition (B5)",
        f"",
    ]

    b5 = next((r for r in results if r["robustness_meta"].get("test_id") == "B5"), None)
    if b5:
        lines += [
            f"- IC Score: {b5['interp_conf'].get('interpretation_confidence_score'):.0f}",
            f"- IC Band: {b5['interp_conf'].get('interpretation_confidence_band')}",
            f"- Degradation: {b5['degradation_level']}",
            f"- Score: {b5['score_result'].get('final_score_estimate')}",
            f"- Cautions: {b5['interp_conf'].get('interpretation_cautions', [])}",
        ]

    lines += [
        f"",
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 6: confidence_distribution_001.md
# ---------------------------------------------------------------------------

def report_confidence_distribution(results: list[dict]) -> str:
    lines = [
        f"# Confidence Distribution Across Corpus",
        f"",
        f"Generated: {TODAY}",
        f"",
        f"Distribution of interpretation_confidence_score and band across the 50-product corpus.",
        f"",
        f"---",
        f"",
        f"## Score Distribution",
        f"",
        f"| Range | Count | Products |",
        f"|:------|:------|:---------|",
    ]

    ranges = [(90, 100), (75, 89), (55, 74), (35, 54), (0, 34)]
    for lo, hi in ranges:
        products = [r for r in results
                    if lo <= r["interp_conf"].get("interpretation_confidence_score", 0) <= hi]
        ids = ", ".join(r["robustness_meta"].get("test_id", "?") for r in products)
        lines.append(f"| {lo}–{hi} | {len(products)} | {ids} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Base vs Interpretation Confidence Comparison",
        f"",
        f"This compares score_engine.compute_confidence (base) with interpretation_confidence (full).",
        f"A large gap indicates that router instability, OCR quality, or ingredient gaps are",
        f"materially reducing confidence beyond what the base scoring captures.",
        f"",
        f"| ID | Base | IC | Gap | Gap Drivers |",
        f"|:---|:-----|:---|:----|:-----------|",
    ]

    for r in results:
        base    = r["interp_conf"].get("base_confidence_score", 0)
        ic      = r["interp_conf"].get("interpretation_confidence_score", 0)
        gap     = base - ic
        drivers = "; ".join(
            d.get("factor", "")[:30]
            for d in r["interp_conf"].get("additional_reductions", [])[:2]
        )
        lines.append(f"| {r['robustness_meta'].get('test_id')} | {base:.0f} | {ic:.0f} | {gap:.0f} | {drivers} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Ceiling Applications",
        f"",
        f"Products where interpretation_confidence applied a score ceiling:",
        f"",
    ]

    ceilinged = [r for r in results
                 if r["score_result"].get("interpretation_confidence_ceiling_applied")]
    if ceilinged:
        for r in ceilinged:
            meta = r["robustness_meta"]
            note = r["score_result"].get("interpretation_confidence_ceiling_applied", "")
            lines.append(f"- **{meta.get('test_id')}** {r['name_he'] or ''}[:25]: {note}")
    else:
        lines.append("*No ceiling applications in this corpus run.*")

    lines += [
        f"",
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 7: ambiguity_patterns_001.md
# ---------------------------------------------------------------------------

def report_ambiguity_patterns(results: list[dict]) -> str:
    lines = [
        f"# Ambiguity Patterns — Hybrid and Borderline Products",
        f"",
        f"Generated: {TODAY}",
        f"",
        f"How BSIP2 handles products that genuinely span two categories,",
        f"or whose signals create routing tension.",
        f"",
        f"---",
        f"",
    ]

    group_d = [r for r in results if r["robustness_meta"].get("test_id", "").startswith("D")]
    group_h = [r for r in results if r["robustness_meta"].get("test_id", "").startswith("H")]
    hybrid = [r for r in results if r["category_result"].get("is_hybrid")]
    unstable = [r for r in results if r["category_result"].get("category_instability_flag")]

    lines += [
        f"## Routing Instability Group (D) — {len(group_d)} products",
        f"",
        f"| ID | Scenario | Expected | Actual | Hybrid? | Unstable? | Conf |",
        f"|:---|:---------|:---------|:-------|:--------|:----------|:-----|",
    ]

    for r in group_d + group_h:
        meta    = r["robustness_meta"]
        cat_r   = r["category_result"]
        expected = meta.get("expected_routing", "?")
        actual   = cat_r.get("category", "?")
        is_hyb   = "yes" if cat_r.get("is_hybrid") else "no"
        is_uns   = "yes" if cat_r.get("category_instability_flag") else "no"
        conf     = cat_r.get("category_confidence", 0)
        scenario = "; ".join(meta.get("noise_scenarios", []))[:35]
        lines.append(f"| {meta.get('test_id')} | {scenario} | {expected} | {actual} | {is_hyb} | {is_uns} | {conf:.2f} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Hybrid Products Detected: {len(hybrid)}",
        f"",
    ]
    for r in hybrid:
        meta  = r["robustness_meta"]
        cat_r = r["category_result"]
        lines += [
            f"- **{meta.get('test_id')}** {r['name_he'] or ''}[:30]",
            f"  → Primary: {cat_r.get('category')} / Secondary: {cat_r.get('secondary_category')}",
            f"  → Degradation: {r['degradation_level']}",
        ]

    lines += [
        f"",
        f"---",
        f"",
        f"## Routing Instability Warnings: {len(unstable)}",
        f"",
    ]
    for r in unstable:
        meta  = r["robustness_meta"]
        cat_r = r["category_result"]
        lines.append(
            f"- **{meta.get('test_id')}**: {cat_r.get('routing_instability_warning', 'unknown')}"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## Anchor vs Signal Tension",
        f"",
        f"Cases where a hard anchor overrode competing signal-score routing:",
        f"",
    ]
    anchor_tension = [r for r in results
                      if r["category_result"].get("anchor_override")
                      and r["category_result"].get("secondary_confidence", 0) > 0.30]
    for r in anchor_tension:
        cat_r = r["category_result"]
        meta  = r["robustness_meta"]
        lines.append(
            f"- **{meta.get('test_id')}**: anchor→{cat_r.get('category')} "
            f"(sec={cat_r.get('secondary_category')}, sec_conf={cat_r.get('secondary_confidence', 0):.2f})"
        )

    lines += [
        f"",
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report 8: retailer_noise_examples_001.md
# ---------------------------------------------------------------------------

def report_retailer_noise_examples(results: list[dict]) -> str:
    lines = [
        f"# Retailer Noise Examples — Concrete Case Studies",
        f"",
        f"Generated: {TODAY}",
        f"",
        f"Worst-case failure examples with full pipeline trace.",
        f"Each case shows what the system received and how it responded.",
        f"",
        f"---",
        f"",
    ]

    # Pick the worst cases: highest composite_risk + most interesting failure patterns
    critical = [r for r in results if r["fail_summary"].get("max_severity") == "CRITICAL"]
    high_risk = [r for r in results if r["fail_summary"].get("composite_risk") in ("critical", "high")]
    # OCR cases
    ocr_cases = [r for r in results if "OCR_DEGRADATION" in r["fail_summary"].get("categories_fired", [])]
    # Claim vs reality
    claim_cases = [r for r in results if r["robustness_meta"].get("test_id", "").startswith("E")]

    case_groups = [
        ("Critical Failures", critical[:3]),
        ("OCR Degradation Cases", ocr_cases[:3]),
        ("Claim vs Reality Cases", claim_cases[:4]),
    ]

    for group_title, cases in case_groups:
        if not cases:
            continue
        lines += [
            f"## {group_title}",
            f"",
        ]
        for r in cases:
            meta     = r["robustness_meta"]
            score_r  = r["score_result"]
            cat_r    = r["category_result"]
            interp   = r["interp_conf"]
            deg_out  = r["degraded_output"]
            failures = r["failures"]

            lines += [
                f"### {meta.get('test_id')} — {r['name_he'] or '(no name)'}",
                f"",
                f"**Test purpose:** {meta.get('test_purpose', '')}",
                f"",
                f"**Noise applied:** {', '.join(meta.get('noise_scenarios', ['none']))}",
                f"",
                f"**Pipeline output:**",
                f"- Category: {cat_r.get('category')} (conf={cat_r.get('category_confidence', 0):.2f}, anchor={cat_r.get('anchor_override')})",
                f"- Base confidence: {interp.get('base_confidence_score', 0):.0f} ({interp.get('base_confidence_band')})",
                f"- Interpretation confidence: {interp.get('interpretation_confidence_score', 0):.0f} ({interp.get('interpretation_confidence_band')})",
                f"- Final score: {score_r.get('final_score_estimate')}",
                f"- Degradation level: **{r['degradation_level']}**",
                f"- Presented to consumer: score={deg_out.get('presented_score')}, grade={deg_out.get('presented_grade')}, provisional={deg_out.get('grade_is_provisional')}",
                f"",
                f"**Failures detected:**",
            ]
            for f in failures:
                lines.append(f"- [{f['severity']}] **{f['category']}**: {f['evidence'][:80]}")

            lines += [
                f"",
                f"**Interpretation narrative:**",
                f"> {interp.get('interpretation_narrative', '')}",
                f"",
                f"**Recommendation:**",
            ]
            if failures:
                lines.append(f"> {failures[0].get('recommendation', '')}")
            lines.append("")

    lines += [
        f"---",
        f"",
        f"## Graceful Degradation Showcase",
        f"",
        f"Products demonstrating each degradation level:",
        f"",
        f"| Level | ID | Name | Score | Grade | Provisional |",
        f"|:------|:---|:-----|:------|:------|:------------|",
    ]

    by_deg: dict[str, list] = defaultdict(list)
    for r in results:
        by_deg[r["degradation_level"]].append(r)

    for level in ["FULL", "CAUTIOUS", "UNCERTAINTY", "INSUFFICIENT"]:
        examples = by_deg.get(level, [])[:2]
        for r in examples:
            out  = r["degraded_output"]
            meta = r["robustness_meta"]
            score = out.get("presented_score")
            grade = out.get("presented_grade")
            prov  = "yes" if out.get("grade_is_provisional") else "no"
            lines.append(
                f"| {level} | {meta.get('test_id')} | {r['name_he'] or ''}[:25] "
                f"| {score if score else 'N/A'} | {grade or 'N/A'} | {prov} |"
            )

    lines += [
        f"",
        f"---",
        f"*Report generated by run_robustness_sprint.py*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Build corpus if needed
    if not CORPUS_PATH.exists():
        log.info("Building corpus...")
        build_corpus()

    # Prepare output directory
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    log.info("Running %d products through pipeline...", len(CORPUS))
    results = []
    errors  = []
    for product in CORPUS:
        pid = product.get("_robustness_meta", {}).get("test_id", product.get("canonical_product_id", "?"))
        try:
            result = run_pipeline_robust(product)
            results.append(result)
            deg  = result["degradation_level"]
            band = result["interp_conf"].get("interpretation_confidence_band", "?")
            score = result["score_result"].get("final_score_estimate")
            log.info("  %-4s %-35s → cat=%-20s | ic_band=%-20s | deg=%-12s | score=%s",
                     pid, (product.get("canonical_name_he") or "")[:34],
                     result["category_result"].get("category", "?"),
                     band, deg, f"{score:.1f}" if score else "N/A")
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            errors.append({"test_id": pid, "error": str(e)})

    log.info("Pipeline complete. %d products processed, %d errors.", len(results), len(errors))

    # Generate all 8 reports
    reports = [
        ("robustness_validation_001.md",      report_robustness_validation),
        ("uncertainty_behavior_001.md",        report_uncertainty_behavior),
        ("noisy_corpus_failures_001.md",       report_noisy_corpus_failures),
        ("routing_under_noise_001.md",         report_routing_under_noise),
        ("missingness_resilience_001.md",      report_missingness_resilience),
        ("confidence_distribution_001.md",     report_confidence_distribution),
        ("ambiguity_patterns_001.md",          report_ambiguity_patterns),
        ("retailer_noise_examples_001.md",     report_retailer_noise_examples),
    ]

    for filename, fn in reports:
        path = REPORT_DIR / filename
        try:
            content = fn(results)
            path.write_text(content, encoding="utf-8")
            log.info("Report written: %s", path)
        except Exception as e:
            log.error("Failed to generate %s: %s", filename, e)

    if errors:
        err_path = REPORT_DIR / "pipeline_errors.json"
        err_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
        log.warning("%d pipeline errors logged to %s", len(errors), err_path)

    print(f"\nSprint complete. Reports in: {REPORT_DIR}")
    print(f"Products: {len(results)} processed, {len(errors)} errors")
    print(f"Reports: {len(reports)} generated")


if __name__ == "__main__":
    main()
