"""
BSIP2 Structural Class Coherence Report Generator

Scans all canonical scored traces across all categories, runs structural
classification on each, and generates a coherence analysis:
  - Structural class population counts + score ranges
  - Products at class boundaries (between-worlds)
  - Ontology tension zones
  - Score clustering by structural class
  - Ambiguous products that resist clean classification

Output: 03_operations/reports/structural_class_report_001.md
"""

import sys
import json
import pathlib
import datetime
import logging
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from structural_classifier import classify_structural_class, STRUCTURAL_CLASSES, STRUCTURAL_CLASS_SCORE_BANDS, MODULE_VERSION

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

REPORT_PATH = pathlib.Path(r"C:\Bari\03_operations\reports\structural_class_report_001.md")

# Canonical run directories to scan (latest run per category)
CANONICAL_RUNS: list[dict] = [
    {
        "category": "milk_and_alternatives",
        "run_id":   "run_004_recalibrated",
        "products_dir": pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\products"),
    },
    {
        "category": "breakfast_cereals",
        "run_id":   "run_cereals_001",
        "products_dir": pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_001\products"),
    },
    {
        "category": "snack_bars",
        "run_id":   "run_snack_bars_001",
        "products_dir": pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001\products"),
    },
    {
        "category": "yogurt_system",
        "run_id":   "run_yogurt_001",
        "products_dir": pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_001\products"),
    },
]

BETWEEN_WORLDS_THRESHOLD = 0.25  # secondary confidence >= this → between-worlds
AMBIGUOUS_THRESHOLD      = 0.40  # primary confidence < this → ambiguous


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_all_traces() -> list[dict]:
    """Load all trace files from canonical run directories."""
    all_traces = []
    for run in CANONICAL_RUNS:
        products_dir = run["products_dir"]
        if not products_dir.exists():
            log.warning("Directory not found, skipping: %s", products_dir)
            continue

        trace_files = list(products_dir.rglob("bsip2_trace.json"))
        log.info("  %s / %s: %d traces", run["category"], run["run_id"], len(trace_files))

        for tf in trace_files:
            with open(tf, encoding="utf-8") as f:
                trace = json.load(f)
            trace["_category_tag"]  = run["category"]
            trace["_run_id"]        = run["run_id"]
            trace["_trace_path"]    = str(tf)
            all_traces.append(trace)

    log.info("Total traces loaded: %d", len(all_traces))
    return all_traces


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _product_label(trace: dict) -> str:
    ref = trace.get("input_reference") or {}
    name = ref.get("product_name_he") or ref.get("canonical_name_he") or ""
    pid  = ref.get("canonical_product_id") or ref.get("barcode") or "?"
    cat  = trace.get("_category_tag", "?")
    return f"{name[:40]} ({pid}) [{cat}]"


def analyze_traces(traces: list[dict]) -> dict:
    """Run structural classification on all traces and compute coherence statistics."""
    records = []
    skipped = 0

    for trace in traces:
        if trace.get("evaluation_status") == "out_of_scope":
            skipped += 1
            continue
        if trace.get("final_score_estimate") is None:
            skipped += 1
            continue

        sc = classify_structural_class(trace)
        if sc.get("primary") is None:
            skipped += 1
            continue

        records.append({
            "label":      _product_label(trace),
            "pid":        (trace.get("input_reference") or {}).get("canonical_product_id", "?"),
            "category":   trace.get("_category_tag", "?"),
            "run_id":     trace.get("_run_id", "?"),
            "nova":       trace.get("nova_proxy"),
            "score":      trace.get("final_score_estimate"),
            "grade":      trace.get("grade_estimate"),
            "primary":    sc["primary"],
            "secondary":  sc["secondary"],
            "primary_conf":   sc["primary_confidence"],
            "secondary_conf": sc["secondary_confidence"],
            "weights":    sc["class_weights"],
            "is_between_worlds": sc["is_between_worlds"],
            "is_ambiguous": sc["primary_confidence"] < AMBIGUOUS_THRESHOLD,
            "notes":      sc["classification_notes"],
        })

    return {
        "records": records,
        "skipped": skipped,
        "total_classified": len(records),
    }


def _stats(values: list[float]) -> dict:
    if not values:
        return {"n": 0, "min": None, "max": None, "mean": None}
    return {
        "n":    len(values),
        "min":  round(min(values), 1),
        "max":  round(max(values), 1),
        "mean": round(sum(values) / len(values), 1),
    }


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def _md_table(headers: list, rows: list) -> str:
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def write_report(analysis: dict) -> pathlib.Path:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    records   = analysis["records"]
    skipped   = analysis["skipped"]
    total_cl  = analysis["total_classified"]

    # Group by structural class
    by_class: dict[str, list] = defaultdict(list)
    for r in records:
        by_class[r["primary"]].append(r)

    # Between-worlds products
    between_worlds = [r for r in records if r["is_between_worlds"]]
    ambiguous      = [r for r in records if r["is_ambiguous"]]

    lines = [
        "# BSIP2 Structural Class Coherence Report",
        "",
        f"**Generated:** {run_dt}",
        f"**Classifier:** {MODULE_VERSION}",
        f"**Total classified:** {total_cl}",
        f"**Skipped (out-of-scope / no score):** {skipped}",
        "",
        "---",
        "",
        "## 1. Structural Class Population Overview",
        "",
    ]

    overview_rows = []
    for code in ["A", "B", "C", "D", "E", "F"]:
        group = by_class.get(code, [])
        scores = [r["score"] for r in group if r["score"] is not None]
        st = _stats(scores)
        bw_ct = sum(1 for r in group if r["is_between_worlds"])
        expected_band = STRUCTURAL_CLASS_SCORE_BANDS.get(code, (None, None))
        overview_rows.append([
            f"{code}: {STRUCTURAL_CLASSES[code]['label']}",
            st["n"],
            f"{st['min']}–{st['max']}" if st["n"] else "—",
            f"{st['mean']}" if st["mean"] is not None else "—",
            f"{expected_band[0]}–{expected_band[1]}",
            bw_ct,
        ])

    lines.append(_md_table(
        ["Structural Class", "Count", "Score Range", "Mean Score", "Expected Band", "Between-Worlds"],
        overview_rows
    ))

    lines += ["", "---", "", "## 2. Products by Structural Class", ""]

    for code in ["A", "B", "C", "D", "E", "F"]:
        group = by_class.get(code, [])
        sc_info = STRUCTURAL_CLASSES[code]
        lines.append(f"### Structural Class {code}: {sc_info['label']} ({len(group)} products)")
        lines.append(f"")
        lines.append(f"*{sc_info['description']}*")
        lines.append(f"Examples: {', '.join(sc_info['examples'])}")
        lines.append(f"")

        if not group:
            lines.append("*No products classified here in this run.*")
            lines.append("")
            continue

        rows = []
        for r in sorted(group, key=lambda x: -(x["score"] or 0)):
            sec = f"{r['secondary']} ({r['secondary_conf']:.2f})" if r["secondary"] else "—"
            bw  = "⚠" if r["is_between_worlds"] else ""
            rows.append([
                r["label"][:55],
                r["score"],
                r["grade"],
                r["nova"],
                f"{r['primary_conf']:.2f}",
                sec,
                bw,
            ])

        lines.append(_md_table(
            ["Product", "Score", "Grade", "NOVA", "Conf", "Secondary", "⚠"],
            rows
        ))
        lines.append("")

    # Between-worlds analysis
    lines += ["---", "", "## 3. Between-Worlds Products (Ontology Tension Zones)", "",
              "Products where the secondary structural class confidence ≥ {:.0f}%. ".format(BETWEEN_WORLDS_THRESHOLD * 100),
              "These are valuable calibration anchors — they reveal genuine ontology boundaries.", ""]

    if between_worlds:
        bw_rows = []
        for r in sorted(between_worlds, key=lambda x: -(x["secondary_conf"] or 0)):
            bw_rows.append([
                r["label"][:50],
                r["primary"],
                f"{r['primary_conf']:.2f}",
                r["secondary"] or "—",
                f"{r['secondary_conf']:.2f}" if r["secondary_conf"] else "—",
                r["score"],
                r["category"],
            ])
        lines.append(_md_table(
            ["Product", "Primary", "Conf", "Secondary", "Conf", "Score", "Category"],
            bw_rows
        ))
    else:
        lines.append("*No between-worlds products found in this run.*")
    lines.append("")

    # Ambiguous products
    lines += ["---", "", "## 4. Ambiguous Products (Low Primary Confidence)", "",
              f"Products where primary structural class confidence < {AMBIGUOUS_THRESHOLD:.0%}. "
              "These resist clean classification — review whether the ontology needs refinement.", ""]

    if ambiguous:
        amb_rows = []
        for r in sorted(ambiguous, key=lambda x: x["primary_conf"]):
            w = r["weights"] or {}
            top2 = sorted(w.items(), key=lambda x: -x[1])[:2]
            top2_str = "  ".join(f"{k}={v:.2f}" for k, v in top2)
            amb_rows.append([
                r["label"][:50],
                f"{r['primary_conf']:.2f}",
                top2_str,
                r["score"],
                r["category"],
            ])
        lines.append(_md_table(
            ["Product", "Primary Conf", "Top Classes", "Score", "Category"],
            amb_rows
        ))
    else:
        lines.append("*No ambiguous products found in this run.*")
    lines.append("")

    # Overlap zone analysis
    lines += ["---", "", "## 5. Structural Class Boundary Overlap Zones", "",
              "Score ranges where adjacent structural classes overlap — zones of genuine ontology ambiguity.", ""]

    boundaries = [("A/B", "A", "B"), ("B/C", "B", "C"), ("C/D", "C", "D"),
                  ("D/E", "D", "E"), ("E/F", "E", "F")]
    for name, code1, code2 in boundaries:
        g1 = by_class.get(code1, [])
        g2 = by_class.get(code2, [])
        s1 = [r["score"] for r in g1 if r["score"] is not None]
        s2 = [r["score"] for r in g2 if r["score"] is not None]
        if not s1 or not s2:
            continue
        overlap_low  = max(min(s1), min(s2))
        overlap_high = min(max(s1), max(s2))
        if overlap_high > overlap_low:
            overlap_products = [r for r in records
                                if r["primary"] in (code1, code2)
                                and r["score"] is not None
                                and overlap_low <= r["score"] <= overlap_high]
            lines.append(f"**{name} boundary:** overlap zone {overlap_low:.1f}–{overlap_high:.1f} "
                         f"({len(overlap_products)} products in zone)")
            for r in overlap_products[:4]:
                lines.append(f"  - {r['label'][:55]} → {r['primary']} ({r['score']})")
        else:
            lines.append(f"**{name} boundary:** no score overlap (clean separation)")
        lines.append("")

    # Category breakdown
    lines += ["---", "", "## 6. Structural Class Distribution by Category", ""]
    by_cat: dict[str, list] = defaultdict(list)
    for r in records:
        by_cat[r["category"]].append(r)

    for cat, cat_records in sorted(by_cat.items()):
        class_counts = defaultdict(int)
        for r in cat_records:
            class_counts[r["primary"]] += 1
        dist = "  ".join(f"{k}={class_counts[k]}" for k in ["A","B","C","D","E","F"] if class_counts[k])
        lines.append(f"**{cat}** ({len(cat_records)} products): {dist}")
    lines.append("")

    # Ontology notes
    lines += ["---", "", "## 7. Ontology Observations", ""]
    lines.append("Observations derived from this run. Update after each major engine change.")
    lines.append("")
    if len(by_class.get("A", [])) + len(by_class.get("B", [])) > total_cl * 0.6:
        lines.append("- **Bias toward intact structural classes (A/B dominant).** May reflect corpus composition "
                     "(real-food products) more than classification drift.")
    if len(between_worlds) > total_cl * 0.25:
        lines.append("- **High between-worlds rate.** More than 25% of products express two structural classes. "
                     "Consider whether class boundaries need tightening.")
    if len(ambiguous) > total_cl * 0.15:
        lines.append("- **High ambiguity rate.** Classification confidence is low for many products. "
                     "Review signal weights in structural_classifier.py.")
    e_count = len(by_class.get("E", []))
    f_count = len(by_class.get("F", []))
    if e_count == 0 and f_count == 0:
        lines.append("- **No E/F products in corpus.** Add engineered wellness and structurally void "
                     "products to future categories (bread, snacks) to validate these structural classes.")
    c_count = len(by_class.get("C", []))
    if c_count == 0:
        lines.append("- **Structural class C (Mechanically Fragmented) is empty.** No products classified here. "
                     "This likely reflects a corpus gap — nut butters, stone-ground breads, and compressed "
                     "whole-food bars are not yet in the dataset. It may also indicate that the B-C or C-D "
                     "signal boundaries are too narrow. Monitor when bread/cracker category is added.")
    elif c_count < 5:
        lines.append(f"- **Structural class C is sparse ({c_count} products).** The mechanically fragmented zone "
                     "has low representation. Verify C products are not being absorbed into B or D.")

    path = REPORT_PATH
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run():
    log.info("=== BSIP2 Structural Class Coherence Report ===")
    traces = load_all_traces()
    log.info("Analyzing %d traces...", len(traces))
    analysis = analyze_traces(traces)
    path = write_report(analysis)
    log.info("Report written: %s", path)
    log.info("Classified: %d | Skipped: %d", analysis["total_classified"], analysis["skipped"])


if __name__ == "__main__":
    run()
