"""
BSIP2 Prototype v0 — Hummus Baseline Batch Runner (run_hummus_001)
Source: Shufersal corpus — 69 canonical BSIP1 products (hummus and savory dips)
Framework: BSIP2 proto_v0 — baseline observational run
Purpose: First-ever BSIP2 scoring of the hummus category.
         Score as observed. No fat patching. No score tuning.
         Document reality before any calibration.

Known limitation:
fat_quality dimension may be unreliable for 58/69 products due to confirmed
Shufersal fat-row scraping defect identified in TASK-039.

Output: C:\\Bari\\02_products\\hummus\\intelligence_bsip2\\run_hummus_001\\
Report: C:\\Bari\\02_products\\hummus\\reports\\run_hummus_001_batch_summary.md
"""
import sys
import json
import pathlib
import logging
import datetime
import statistics

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hummus\reports")
CATEGORY_TAG = "hummus_and_savory_dips"
RUN_ID       = "run_hummus_001"

FAT_ANOMALY_PATH = pathlib.Path(r"C:\Bari\02_products\hummus\audit\fat_anomaly_TASK039.json")

KNOWN_LIMITATION = (
    "Known limitation: fat_quality dimension may be unreliable for 58/69 products "
    "due to confirmed Shufersal fat-row scraping defect identified in TASK-039."
)


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    trace["run_id"] = RUN_ID
    trace["known_limitation"] = KNOWN_LIMITATION
    return trace


def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def _infer_product_type(product: dict) -> str:
    name = (product.get("canonical_name_he") or "").lower()
    ing = " ".join(product.get("ingredients_list") or []).lower()
    if "מטבוחה" in name or "matbucha" in name:
        return "matbucha"
    if "חציל" in name or "חצילים" in name:
        return "eggplant_spread"
    if "פלפל" in name and ("קלוי" in name or "salat" in name.lower()):
        return "pepper_spread"
    if "0%" in name or "קל" in name or "דל שומן" in name or "light" in name.lower():
        return "light_hummus"
    if "מסבחה" in name:
        return "masabacha"
    if "פול" in name:
        return "ful_spread"
    if "חומוס" in name or "houmous" in name.lower():
        return "hummus_spread"
    return "other_spread"


def _load_fat_anomaly_register() -> dict:
    """Load fat anomaly TASK-039 register, keyed by product_id."""
    if not FAT_ANOMALY_PATH.exists():
        return {}
    try:
        with open(FAT_ANOMALY_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return {p["product_id"]: p for p in data.get("products", [])}
    except Exception:
        return {}


def run_batch():
    log.info("=== BSIP2 Hummus Baseline — %s ===", RUN_ID)
    log.info("Source: %s", BSIP1_SOURCE)
    log.info("Output: %s", OUTPUT_ROOT)
    log.info("KNOWN LIMITATION: %s", KNOWN_LIMITATION)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)

    fat_register = _load_fat_anomaly_register()
    log.info("Fat anomaly register loaded: %d products", len(fat_register))

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces = []
    errors = []
    product_map = {}

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            product_map[pid] = product

            score   = trace.get("final_score_estimate")
            grade   = trace.get("grade_estimate")
            cat     = trace.get("category")
            nova    = trace.get("nova_proxy")
            ptype   = _infer_product_type(product)
            cap     = trace.get("binding_cap") or "-"
            fat_sev = fat_register.get(pid, {}).get("severity", "?")
            log.info("  %-45s score=%-5s grade=%s  cat=%-18s nova=%s  type=%-18s cap=%-4s fat=%s",
                     pid, score, grade, cat, nova, ptype, cap, fat_sev)
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))
    _write_summary(traces, errors, product_map, fat_register)
    return traces, errors


def _write_summary(traces, errors, product_map, fat_register):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sufficient = [t for t in traces
                  if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    all_scored = [t for t in traces if t.get("final_score_estimate") is not None]
    scores = [t["final_score_estimate"] for t in sufficient]

    # Grade distribution
    grade_counts: dict[str, int] = {}
    for t in sufficient:
        g = str(t.get("grade_estimate", "?"))
        grade_counts[g] = grade_counts.get(g, 0) + 1

    # NOVA distribution
    nova_counts: dict[str, int] = {}
    for t in traces:
        n = str(t.get("nova_proxy", "?"))
        nova_counts[n] = nova_counts.get(n, 0) + 1

    # Category routing distribution
    cat_counts: dict[str, int] = {}
    for t in traces:
        c = str(t.get("category", "?"))
        cat_counts[c] = cat_counts.get(c, 0) + 1

    # Caps applied
    capped = [t for t in traces if t.get("binding_cap")]

    # Dimension average scores
    dim_sums: dict[str, list] = {}
    for t in sufficient:
        ds = t.get("dimension_scores") or {}
        for dim, val in ds.items():
            if val is not None:
                dim_sums.setdefault(dim, []).append(val)
    dim_avgs = {k: round(sum(v) / len(v), 1) for k, v in dim_sums.items() if v}

    # Score statistics
    score_stats = {}
    if scores:
        score_stats = {
            "count": len(scores),
            "mean": round(statistics.mean(scores), 1),
            "median": round(statistics.median(scores), 1),
            "stdev": round(statistics.stdev(scores), 1) if len(scores) > 1 else 0,
            "min": min(scores),
            "max": max(scores),
            "p25": round(sorted(scores)[len(scores) // 4], 1),
            "p75": round(sorted(scores)[3 * len(scores) // 4], 1),
        }

    # Top 10 and Bottom 10
    sorted_sufficient = sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0))
    top_10    = sorted_sufficient[:10]
    bottom_10 = sorted_sufficient[-10:][::-1]  # worst first

    lines = [
        f"# BSIP2 Hummus Baseline — {RUN_ID} Run Report",
        f"\n**Run date:** {run_dt}",
        f"**Category:** {CATEGORY_TAG}",
        f"**Source:** Shufersal corpus — 69 canonical BSIP1 products",
        f"**Framework:** BSIP2 proto_v0 (unmodified baseline run)",
        f"**Products processed:** {len(traces)}",
        f"**Scored (sufficient data):** {len(sufficient)}",
        f"**Insufficient data:** {len(traces) - len(sufficient)}",
        f"**Pipeline errors:** {len(errors)}",
        "",
        f"> **{KNOWN_LIMITATION}**",
        "",
        "---",
        "",
        "## Score Distribution",
        "",
    ]

    if score_stats:
        lines += [
            f"| Statistic | Value |",
            f"|-----------|-------|",
            f"| Count     | {score_stats['count']} |",
            f"| Mean      | {score_stats['mean']} |",
            f"| Median    | {score_stats['median']} |",
            f"| Std Dev   | {score_stats['stdev']} |",
            f"| Min       | {score_stats['min']} |",
            f"| Max       | {score_stats['max']} |",
            f"| P25       | {score_stats['p25']} |",
            f"| P75       | {score_stats['p75']} |",
        ]
    else:
        lines.append("*No scored products.*")

    # Score histogram buckets
    lines += ["", "### Score Buckets (10-point intervals)", ""]
    buckets = [(i, i + 10) for i in range(0, 100, 10)]
    for lo, hi in buckets:
        count = sum(1 for s in scores if lo <= s < hi)
        bar = "█" * count
        lines.append(f"| {lo:>3}–{hi:<3} | {count:>3} | {bar} |")

    lines += [
        "",
        "---",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Score Range | Count | Expected (framework) |",
        "|-------|-------------|-------|----------------------|",
        f"| A     | 85–100      | {grade_counts.get('A', 0)}     | 5–10 |",
        f"| B     | 70–84       | {grade_counts.get('B', 0)}     | 20–28 |",
        f"| C     | 55–69       | {grade_counts.get('C', 0)}     | 20–25 |",
        f"| D     | 40–54       | {grade_counts.get('D', 0)}     | 10–15 |",
        f"| E     | 0–39        | {grade_counts.get('E', 0)}     | 2–5 |",
        f"| insufficient_data | — | {grade_counts.get('insufficient_data', 0)} | — |",
        "",
        "---",
        "",
        "## Top 10 Products",
        "",
    ]

    top_rows = []
    for t in top_10:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id", "")
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        cat  = t.get("category")
        nova = t.get("nova_proxy")
        cap  = t.get("binding_cap") or "-"
        fat  = fat_register.get(pid, {}).get("severity", "?")
        top_rows.append([name[:50], s, g, cat, nova, fat, cap])

    if top_rows:
        lines.append(_md_table(
            ["Product", "Score", "Grade", "Category", "NOVA", "Fat Anomaly", "Cap"],
            top_rows
        ))

    lines += [
        "",
        "---",
        "",
        "## Bottom 10 Products",
        "",
    ]

    bot_rows = []
    for t in bottom_10:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id", "")
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        cat  = t.get("category")
        nova = t.get("nova_proxy")
        cap  = t.get("binding_cap") or "-"
        fat  = fat_register.get(pid, {}).get("severity", "?")
        flags = "; ".join(t.get("unresolved_flags") or [])[:80]
        bot_rows.append([name[:45], s, g, cat, nova, fat, cap, flags[:60]])

    if bot_rows:
        lines.append(_md_table(
            ["Product", "Score", "Grade", "Category", "NOVA", "Fat Anomaly", "Cap", "Key Flags"],
            bot_rows
        ))

    lines += [
        "",
        "---",
        "",
        "## Full Score Table",
        "",
    ]

    all_rows = []
    for t in sorted_sufficient:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id", "")
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        cat  = t.get("category")
        nova = t.get("nova_proxy")
        wds  = t.get("weighted_dimension_score")
        cap  = t.get("binding_cap") or "-"
        conf = (t.get("confidence_score") or
                (t.get("confidence_result") or {}).get("confidence_score") or "-")
        fat  = fat_register.get(pid, {}).get("severity", "?")
        all_rows.append([name[:45], s, g, cat, nova, wds, cap, conf, fat])

    if all_rows:
        lines.append(_md_table(
            ["Product", "Score", "Grade", "Category", "NOVA", "Wtd Dim", "Cap", "Conf", "Fat"],
            all_rows
        ))

    lines += [
        "",
        "---",
        "",
        "## Dimension Contribution Summary",
        "",
        "Average dimension scores across all scored products.",
        "",
        "| Dimension           | Weight | Avg Score | Contribution |",
        "|---------------------|--------|-----------|--------------|",
    ]

    dim_weights = {
        "processing_quality":   0.15,
        "nutrient_density":     0.15,
        "calorie_density":      0.15,
        "glycemic_quality":     0.12,
        "protein_quality":      0.10,
        "additive_quality":     0.10,
        "satiety_support":      0.06,
        "fat_quality":          0.08,
        "regulatory_quality":   0.05,
        "whole_food_integrity": 0.04,
    }

    dim_order = [
        "processing_quality", "nutrient_density", "calorie_density",
        "glycemic_quality", "protein_quality", "additive_quality",
        "satiety_support", "fat_quality", "regulatory_quality", "whole_food_integrity",
    ]

    for dim in dim_order:
        avg = dim_avgs.get(dim, "-")
        w   = dim_weights.get(dim, 0)
        contrib = round(avg * w, 1) if isinstance(avg, (int, float)) else "-"
        fat_note = " ⚠ (fat anomaly)" if dim == "fat_quality" else ""
        lines.append(f"| {dim:<20} | {w:.2f}   | {avg:<9} | {contrib}{fat_note} |")

    lines += [
        "",
        "> ⚠ fat_quality scores are derived from incorrect fat_g values for 58/69 products (TASK-039).",
        "  Scores for this dimension are systematically inflated and should not be used for comparison.",
        "",
        "---",
        "",
        "## NOVA Distribution",
        "",
        "| NOVA | Count | Description |",
        "|------|-------|-------------|",
        f"| NOVA 1 | {nova_counts.get('1', 0)} | Unprocessed or minimally processed |",
        f"| NOVA 2 | {nova_counts.get('2', 0)} | Processed culinary ingredients |",
        f"| NOVA 3 | {nova_counts.get('3', 0)} | Processed foods |",
        f"| NOVA 4 | {nova_counts.get('4', 0)} | Ultra-processed |",
        f"| Unknown | {nova_counts.get('None', 0) + nova_counts.get('?', 0)} | Not inferred |",
        "",
        "---",
        "",
        "## Category Routing Distribution",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]

    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## Guardrail Activity",
        "",
        f"Products with binding cap: **{len(capped)}** of {len(traces)}",
        "",
        "| Cap Rule | Count |",
        "|----------|-------|",
    ]

    cap_rule_counts: dict[str, int] = {}
    for t in traces:
        for c in (t.get("caps_applied") or []):
            rule = c.get("rule", "?")
            cap_rule_counts[rule] = cap_rule_counts.get(rule, 0) + 1

    for rule, cnt in sorted(cap_rule_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {rule} | {cnt} |")

    # Penalty activity
    pen_rule_counts: dict[str, int] = {}
    for t in traces:
        for p in (t.get("penalties_applied") or []):
            rule = p.get("rule", "?")
            pen_rule_counts[rule] = pen_rule_counts.get(rule, 0) + 1

    lines += [
        "",
        "| Penalty Rule | Count |",
        "|-------------|-------|",
    ]
    for rule, cnt in sorted(pen_rule_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {rule} | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## Category Observations",
        "",
        "### Routing",
        "",
    ]

    # Category breakdown by product type
    type_score_map: dict[str, list] = {}
    for t in sufficient:
        pid  = (t.get("input_reference") or {}).get("canonical_product_id", "")
        prod = product_map.get(pid, {})
        ptype = _infer_product_type(prod)
        type_score_map.setdefault(ptype, []).append(t["final_score_estimate"])

    lines.append("| Product Type | Count | Avg Score | Min | Max |")
    lines.append("|--------------|-------|-----------|-----|-----|")
    for ptype, pscores in sorted(type_score_map.items(), key=lambda x: -statistics.mean(x[1]) if x[1] else 0):
        if pscores:
            avg = round(statistics.mean(pscores), 1)
            mn  = min(pscores)
            mx  = max(pscores)
            lines.append(f"| {ptype:<20} | {len(pscores):<5} | {avg:<9} | {mn}  | {mx}  |")

    lines += [
        "",
        "---",
        "",
        "## Fat Anomaly Impact (TASK-039)",
        "",
        "| Severity | Count | Notes |",
        "|----------|-------|-------|",
        f"| CRITICAL | {sum(1 for p in fat_register.values() if p.get('severity') == 'CRITICAL')} | Gap > 15g, tahini declared |",
        f"| HIGH     | {sum(1 for p in fat_register.values() if p.get('severity') == 'HIGH')} | Gap 10–15g |",
        f"| MEDIUM   | {sum(1 for p in fat_register.values() if p.get('severity') == 'MEDIUM')} | Gap 5–10g |",
        f"| LOW      | {sum(1 for p in fat_register.values() if p.get('severity') == 'LOW')} | Gap 2–5g |",
        f"| NONE     | {sum(1 for p in fat_register.values() if p.get('severity') == 'NONE')} | Consistent with caloric balance |",
        "",
        f"> Products with `fat_quality` unreliable: **58/69** (84%)",
        f"> Maximum score impact per product from fat anomaly: ~8 points (fat_quality weight = 8%)",
        "",
    ]

    if errors:
        lines += ["", "---", "", "## Pipeline Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    lines += [
        "",
        "---",
        "",
        f"*Run: {RUN_ID} | Generated: {run_dt}*",
        f"*BSIP2 proto_v0 — Hummus Baseline. Do not modify BSIP1 records. Do not patch fat values.*",
    ]

    path = REPORT_ROOT / f"{RUN_ID}_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)

    # Also write a JSON summary for downstream use
    json_summary = {
        "run_id": RUN_ID,
        "run_date": run_dt,
        "category": CATEGORY_TAG,
        "known_limitation": KNOWN_LIMITATION,
        "products_processed": len(traces),
        "products_scored": len(sufficient),
        "products_insufficient": len(traces) - len(sufficient),
        "pipeline_errors": len(errors),
        "score_statistics": score_stats,
        "grade_distribution": grade_counts,
        "nova_distribution": nova_counts,
        "category_routing": cat_counts,
        "dimension_avg_scores": dim_avgs,
        "caps_applied_counts": cap_rule_counts,
        "penalties_applied_counts": pen_rule_counts,
        "top_10": [
            {
                "product_id": (t.get("input_reference") or {}).get("canonical_product_id"),
                "name": (t.get("input_reference") or {}).get("product_name_he"),
                "score": t.get("final_score_estimate"),
                "grade": t.get("grade_estimate"),
                "category": t.get("category"),
                "nova": t.get("nova_proxy"),
            }
            for t in top_10
        ],
        "bottom_10": [
            {
                "product_id": (t.get("input_reference") or {}).get("canonical_product_id"),
                "name": (t.get("input_reference") or {}).get("product_name_he"),
                "score": t.get("final_score_estimate"),
                "grade": t.get("grade_estimate"),
                "category": t.get("category"),
                "nova": t.get("nova_proxy"),
            }
            for t in bottom_10
        ],
    }

    json_path = REPORT_ROOT / f"{RUN_ID}_summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_summary, f, ensure_ascii=False, indent=2)
    log.info("JSON summary written: %s", json_path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done. Run: %s", RUN_ID)
