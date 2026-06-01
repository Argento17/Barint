"""
Routing Fix Comparison — Hummus Corpus
Loads run_hummus_001 traces (old routing) and re-scores with fixed router_v2.
Produces per-product delta table and summary for routing_fix_hummus_v1.md.
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

BSIP1_SOURCE  = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
OLD_TRACES    = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_001\products")
NEW_OUTPUT    = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\products")
REPORT_DIR    = pathlib.Path(r"C:\Bari\03_operations\bsip2")


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


def _load_old_trace(pid: str) -> dict | None:
    p = OLD_TRACES / pid / "bsip2_trace.json"
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def run():
    log.info("=== Routing Fix Comparison — Hummus Corpus ===")

    NEW_OUTPUT.mkdir(parents=True, exist_ok=True)
    NEW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    deltas = []
    errors = []

    for product in products:
        pid  = product.get("canonical_product_id", "unknown")
        name = product.get("canonical_name_he") or ""

        old_trace = _load_old_trace(pid)
        try:
            new_trace = run_pipeline(product)
            write_trace(new_trace, NEW_OUTPUT.parent)
        except Exception as e:
            log.error("PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"pid": pid, "error": str(e)})
            continue

        old_cat   = (old_trace or {}).get("category", "?")
        new_cat   = new_trace.get("category", "?")
        old_score = (old_trace or {}).get("final_score_estimate")
        new_score = new_trace.get("final_score_estimate")
        old_grade = (old_trace or {}).get("grade_estimate", "?")
        new_grade = new_trace.get("grade_estimate", "?")
        old_conf  = (old_trace or {}).get("category_confidence", 0)
        new_conf  = new_trace.get("category_confidence", 0)
        rerouted  = (old_cat != new_cat)

        score_delta = None
        if old_score is not None and new_score is not None:
            score_delta = round(new_score - old_score, 1)

        deltas.append({
            "pid":         pid,
            "name":        name,
            "old_cat":     old_cat,
            "new_cat":     new_cat,
            "rerouted":    rerouted,
            "old_conf":    old_conf,
            "new_conf":    new_conf,
            "old_score":   old_score,
            "new_score":   new_score,
            "score_delta": score_delta,
            "old_grade":   old_grade,
            "new_grade":   new_grade,
            "grade_changed": (old_grade != new_grade),
        })

        change_marker = "REROUTED" if rerouted else "same"
        delta_str = f"{score_delta:+.1f}" if score_delta is not None else "N/A"
        log.info("  %-40s  old=%-16s  new=%-16s  %-8s  Δ=%s",
                 name[:40], old_cat, new_cat, change_marker, delta_str)

    _write_report(deltas, errors)
    return deltas


def _write_report(deltas, errors):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    rerouted    = [d for d in deltas if d["rerouted"]]
    unchanged   = [d for d in deltas if not d["rerouted"]]
    grade_chg   = [d for d in deltas if d["grade_changed"]]
    score_ups   = [d for d in rerouted if (d["score_delta"] or 0) > 0]
    score_downs = [d for d in rerouted if (d["score_delta"] or 0) < 0]

    scored_deltas = [d["score_delta"] for d in deltas if d["score_delta"] is not None]
    rerouted_deltas = [d["score_delta"] for d in rerouted if d["score_delta"] is not None]

    old_scores = [d["old_score"] for d in deltas if d["old_score"] is not None]
    new_scores = [d["new_score"] for d in deltas if d["new_score"] is not None]

    # Category routing change summary
    cat_changes: dict[str, dict[str, int]] = {}
    for d in rerouted:
        key = f"{d['old_cat']} → {d['new_cat']}"
        cat_changes[key] = cat_changes.get(key, 0) + 1

    lines = [
        "# Hummus Routing Fix — Comparison Report",
        "",
        f"**Generated:** {run_dt}",
        f"**Fix:** router_v2.py — added savory-spread hard anchors and exclusions",
        f"**Corpus:** Shufersal hummus, 69 products",
        f"**Baseline run:** run_hummus_001 (old routing)",
        f"**Fixed run:** run_hummus_002 (router_v2 with savory anchors)",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total products | {len(deltas)} |",
        f"| Products rerouted | **{len(rerouted)}** |",
        f"| Products unchanged | {len(unchanged)} |",
        f"| Grade changes | {len(grade_chg)} |",
        f"| Score increases (rerouted) | {len(score_ups)} |",
        f"| Score decreases (rerouted) | {len(score_downs)} |",
        f"| Old corpus mean score | {round(statistics.mean(old_scores), 1) if old_scores else 'N/A'} |",
        f"| New corpus mean score | {round(statistics.mean(new_scores), 1) if new_scores else 'N/A'} |",
        f"| Mean score delta (all) | {round(statistics.mean(scored_deltas), 1) if scored_deltas else 'N/A'} |",
        f"| Mean score delta (rerouted only) | {round(statistics.mean(rerouted_deltas), 1) if rerouted_deltas else 'N/A'} |",
        "",
        "---",
        "",
        "## Root Causes Fixed",
        "",
        '**RC-1: `"מוס"` (mousse) substring fires on `"חומוס"` (hummus)**',
        "",
        'The Stage 2 signal `("מוס", 0.85, "name_weighted")` in `_DESSERT` matches as a',
        'substring of "חומוס", giving dessert score = 1.70. The `"חומוס"` signal in `_SAUCE`',
        "also gives sauce_spread = 1.70. They tie; Python's stable dict sort puts `dessert`",
        "before `sauce_spread` in CATEGORIES ordering → dessert wins every tie.",
        "",
        '**Fix:** Added `"חומוס"` as a hard anchor for `sauce_spread` at confidence 0.94.',
        "Hard anchors bypass Stage 2 entirely, eliminating the substring collision.",
        "",
        '**RC-2: `"טחינה"` anchor (conf=0.93) reroutes hummus+tahini products to `whole_food_fat`**',
        "",
        'Products named e.g. "חומוס עם טחינה 16.9%" triggered the `"טחינה"` anchor first.',
        'Since `"טחינה"` conf=0.93 > `"חומוס"` was not in anchors, tahini won.',
        "",
        '**Fix:** `"חומוס"` anchor at conf=0.94 beats `"טחינה"` at 0.93. Added ANCHOR_EXCLUSIONS',
        'for `"טחינה"`: excludes when `"חציל"` or `"חצילים"` appears in name (eggplant+tahini',
        "dishes are spreads, not tahini products).",
        "",
        '**RC-3: `"מטבוחה"`, `"מסבחה"`, `"חציל"`, `"חצילים"` had zero sauce_spread signals**',
        "",
        "These product types had no matching signals and fell through to `default` with",
        "low-confidence routing.",
        "",
        '**Fix:** Added hard anchors: `"מטבוחה"` and `"מסבחה"` at 0.92; `"חצילים"` and',
        '`"חציל"` at 0.91; `"ממרח פלפלים"` at 0.92; `"פלפל צ\'ומה"` at 0.91.',
        'Also added backup `_SAUCE` signals for all terms.',
        "",
        '**RC-4: `"מעדן"` anchor fires on `"מעדן חצילים"` (eggplant delicacy) → dessert**',
        "",
        '**Fix:** Added `"חציל"` and `"חצילים"` to ANCHOR_EXCLUSIONS for `"מעדן"`.',
        "",
        "---",
        "",
        "## Routing Change Summary",
        "",
        "| Old Category → New Category | Count |",
        "|---|---|",
    ]
    for key, cnt in sorted(cat_changes.items(), key=lambda x: -x[1]):
        lines.append(f"| {key} | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## Per-Product Delta Table",
        "",
        "Products that changed category (sorted by score delta descending):",
        "",
    ]

    rerouted_sorted = sorted(rerouted, key=lambda d: -(d["score_delta"] or 0))
    rows = []
    for d in rerouted_sorted:
        delta_str = f"{d['score_delta']:+.1f}" if d["score_delta"] is not None else "N/A"
        grade_str = f"{d['old_grade']}→{d['new_grade']}" if d["grade_changed"] else d["new_grade"]
        rows.append([
            d["name"][:42],
            d["old_cat"],
            d["new_cat"],
            d["old_score"],
            d["new_score"],
            delta_str,
            grade_str,
        ])

    if rows:
        lines.append(_md_table(
            ["Product", "Old Category", "New Category", "Old Score", "New Score", "Δ Score", "Grade"],
            rows
        ))

    lines += [
        "",
        "---",
        "",
        "## Unchanged Routing (for completeness)",
        "",
        f"| Product | Category | Score |",
        f"|---------|----------|-------|",
    ]
    for d in sorted(unchanged, key=lambda x: -(x["new_score"] or 0)):
        lines.append(f"| {d['name'][:40]} | {d['new_cat']} | {d['new_score']} |")

    # New grade distribution
    new_grade_counts: dict[str, int] = {}
    old_grade_counts: dict[str, int] = {}
    for d in deltas:
        g = str(d.get("new_grade", "?"))
        new_grade_counts[g] = new_grade_counts.get(g, 0) + 1
        g2 = str(d.get("old_grade", "?"))
        old_grade_counts[g2] = old_grade_counts.get(g2, 0) + 1

    lines += [
        "",
        "---",
        "",
        "## Grade Distribution Comparison",
        "",
        "| Grade | Old Count | New Count | Change |",
        "|-------|-----------|-----------|--------|",
    ]
    for g in ["A", "B", "C", "D", "E", "insufficient_data"]:
        old_c = old_grade_counts.get(g, 0)
        new_c = new_grade_counts.get(g, 0)
        chg = f"{new_c - old_c:+d}" if new_c != old_c else "—"
        lines.append(f"| {g} | {old_c} | {new_c} | {chg} |")

    # Old category distribution for new
    new_cat_counts: dict[str, int] = {}
    for d in deltas:
        c = d["new_cat"]
        new_cat_counts[c] = new_cat_counts.get(c, 0) + 1

    lines += [
        "",
        "---",
        "",
        "## New Category Routing Distribution",
        "",
        "| Category | Old Count | New Count |",
        "|----------|-----------|-----------|",
    ]
    old_cat_counts: dict[str, int] = {}
    for d in deltas:
        c = d["old_cat"]
        old_cat_counts[c] = old_cat_counts.get(c, 0) + 1

    all_cats = sorted(set(list(old_cat_counts.keys()) + list(new_cat_counts.keys())))
    for cat in all_cats:
        lines.append(f"| {cat} | {old_cat_counts.get(cat, 0)} | {new_cat_counts.get(cat, 0)} |")

    # Top 10 old vs new
    def _top10(data, score_key, n=10):
        scored = [d for d in data if d.get(score_key) is not None]
        return sorted(scored, key=lambda x: -(x[score_key] or 0))[:n]

    lines += [
        "",
        "---",
        "",
        "## Top 10 — Old vs New",
        "",
        "### Old Top 10 (run_hummus_001)",
        "",
    ]
    old_rows = []
    for d in _top10(deltas, "old_score"):
        delta_str = f"{d['score_delta']:+.1f}" if d["score_delta"] is not None else "N/A"
        old_rows.append([d["name"][:42], d["old_score"], d["old_grade"], d["old_cat"], d["new_score"], delta_str])
    if old_rows:
        lines.append(_md_table(
            ["Product", "Old Score", "Old Grade", "Old Category", "New Score", "Δ Score"],
            old_rows
        ))

    lines += ["", "### New Top 10 (run_hummus_002 — fixed routing)", ""]
    new_rows = []
    for d in _top10(deltas, "new_score"):
        delta_str = f"{d['score_delta']:+.1f}" if d["score_delta"] is not None else "N/A"
        new_rows.append([d["name"][:42], d["new_score"], d["new_grade"], d["new_cat"], d["old_score"], delta_str])
    if new_rows:
        lines.append(_md_table(
            ["Product", "New Score", "New Grade", "New Category", "Old Score", "Δ Score"],
            new_rows
        ))

    # Bottom 10 old vs new
    def _bottom10(data, score_key, n=10):
        scored = [d for d in data if d.get(score_key) is not None]
        return sorted(scored, key=lambda x: x[score_key] or 0)[:n]

    lines += [
        "",
        "---",
        "",
        "## Bottom 10 — Old vs New",
        "",
        "### Old Bottom 10 (run_hummus_001)",
        "",
    ]
    old_bot_rows = []
    for d in _bottom10(deltas, "old_score"):
        delta_str = f"{d['score_delta']:+.1f}" if d["score_delta"] is not None else "N/A"
        old_bot_rows.append([d["name"][:42], d["old_score"], d["old_grade"], d["old_cat"], d["new_score"], delta_str])
    if old_bot_rows:
        lines.append(_md_table(
            ["Product", "Old Score", "Old Grade", "Old Category", "New Score", "Δ Score"],
            old_bot_rows
        ))

    lines += ["", "### New Bottom 10 (run_hummus_002 — fixed routing)", ""]
    new_bot_rows = []
    for d in _bottom10(deltas, "new_score"):
        delta_str = f"{d['score_delta']:+.1f}" if d["score_delta"] is not None else "N/A"
        new_bot_rows.append([d["name"][:42], d["new_score"], d["new_grade"], d["new_cat"], d["old_score"], delta_str])
    if new_bot_rows:
        lines.append(_md_table(
            ["Product", "New Score", "New Grade", "New Category", "Old Score", "Δ Score"],
            new_bot_rows
        ))

    lines += [
        "",
        "---",
        "",
        "## Recommendation: Should Hummus BSIP2 Be Refreshed?",
        "",
    ]

    # Append placeholder — will be filled after analysis
    lines += [
        "_[Populated after comparison data is reviewed]_",
        "",
        "---",
        "",
        f"*Generated: {run_dt} | Router fix: router_v2.py savory-spread anchors v1*",
    ]

    out_path = REPORT_DIR / "routing_fix_hummus_v1_draft.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Draft report written: %s", out_path)

    # Also export raw deltas JSON for reference
    json_path = REPORT_DIR / "routing_fix_hummus_delta.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(deltas, f, ensure_ascii=False, indent=2)
    log.info("Delta JSON written: %s", json_path)

    return deltas


if __name__ == "__main__":
    deltas = run()
    rerouted = [d for d in deltas if d["rerouted"]]
    log.info("Rerouted: %d/%d products", len(rerouted), len(deltas))
    log.info("Done.")
