"""
BSIP2 Router v2 Validation Report Generator

Loads all BSIP1 canonical products from all 4 active categories,
runs router_v2.classify_category() on each, and compares against
the v1 routing stored in the existing BSIP2 traces.

Generates: 03_operations/reports/router_validation_001.md

Sections:
  1. Routing distribution (v2)
  2. Anchor activation rate
  3. Suppressed contamination cases
  4. Instability and hybrid products
  5. V1 vs V2 routing delta
  6. Contamination analysis by type (WFF / dairy / protein / beverage)
  7. Remaining weak zones
"""

import sys
import json
import pathlib
import datetime
import logging
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from router_v2 import classify_category, ROUTER_VERSION
from input_loader import load_batch

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

REPORT_PATH = pathlib.Path(r"C:\Bari\03_operations\reports\router_validation_001.md")

BSIP1_SOURCES: list[dict] = [
    {
        "category": "milk_and_alternatives",
        "bsip1_dir": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output"),
        "trace_dir": pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\products"),
    },
    {
        "category": "breakfast_cereals",
        "bsip1_dir": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_001\output"),
        "trace_dir": pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_001\products"),
    },
    {
        "category": "snack_bars",
        "bsip1_dir": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output"),
        "trace_dir": pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001\products"),
    },
    {
        "category": "yogurt_system",
        "bsip1_dir": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output"),
        "trace_dir": pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_001\products"),
    },
]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def _load_v1_routing(trace_dir: pathlib.Path) -> dict[str, str]:
    """Return {canonical_product_id: v1_category} from existing BSIP2 traces."""
    mapping: dict[str, str] = {}
    if not trace_dir.exists():
        return mapping
    for tf in trace_dir.rglob("bsip2_trace.json"):
        try:
            with open(tf, encoding="utf-8") as f:
                trace = json.load(f)
            pid = (trace.get("input_reference") or {}).get("canonical_product_id")
            cat = trace.get("category")
            if pid and cat:
                mapping[pid] = cat
        except Exception:
            pass
    return mapping


def load_all() -> list[dict]:
    """Load all BSIP1 products with v1 routing attached."""
    all_records: list[dict] = []
    for src in BSIP1_SOURCES:
        bsip1_dir = src["bsip1_dir"]
        trace_dir = src["trace_dir"]

        if not bsip1_dir.exists():
            log.warning("BSIP1 dir not found, skipping: %s", bsip1_dir)
            continue

        products = load_batch(bsip1_dir)
        v1_routing = _load_v1_routing(trace_dir)
        log.info("  %s: %d products, %d v1 routes", src["category"], len(products), len(v1_routing))

        for p in products:
            pid = p.get("canonical_product_id", "?")
            all_records.append({
                "product":   p,
                "category_tag": src["category"],
                "pid":       pid,
                "v1_cat":    v1_routing.get(pid),
            })

    log.info("Total records: %d", len(all_records))
    return all_records


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(records: list[dict]) -> dict:
    results: list[dict] = []
    for rec in records:
        product = rec["product"]
        name    = (product.get("canonical_name_he") or "").lower()

        r2 = classify_category(product)
        v2_cat = r2["category"]
        v1_cat = rec["v1_cat"]

        results.append({
            "pid":          rec["pid"],
            "name":         product.get("canonical_name_he") or "",
            "cat_tag":      rec["category_tag"],
            "v2_cat":       v2_cat,
            "v1_cat":       v1_cat,
            "changed":      (v1_cat is not None and v1_cat != v2_cat),
            "anchor":       r2.get("anchor_override", False),
            "subtype":      r2.get("category_subtype"),
            "conf":         r2.get("category_confidence"),
            "conf_band":    r2.get("confidence_band"),
            "secondary":    r2.get("secondary_category"),
            "instability":  r2.get("category_instability_flag", False),
            "instability_w": r2.get("routing_instability_warning"),
            "is_hybrid":    r2.get("is_hybrid", False),
            "suppressed":   r2.get("routing_suppressed_signals", []),
            "basis":        r2.get("classification_basis", []),
            "raw_scores":   r2.get("raw_category_scores", {}),
        })

    return {"results": results}


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
    run_dt  = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    results = analysis["results"]
    n_total = len(results)

    # Grouped tallies
    by_v2:   dict[str, list] = defaultdict(list)
    by_cat:  dict[str, list] = defaultdict(list)
    for r in results:
        by_v2[r["v2_cat"]].append(r)
        by_cat[r["cat_tag"]].append(r)

    anchored   = [r for r in results if r["anchor"]]
    suppressed = [r for r in results if r["suppressed"]]
    changed    = [r for r in results if r["changed"]]
    hybrid     = [r for r in results if r["is_hybrid"]]
    unstable   = [r for r in results if r["instability"]]

    lines = [
        "# BSIP2 Router v2 Validation Report",
        "",
        f"**Generated:** {run_dt}",
        f"**Router:** {ROUTER_VERSION}",
        f"**Products analyzed:** {n_total}",
        f"**Anchor activations:** {len(anchored)} ({100*len(anchored)/max(n_total,1):.0f}%)",
        f"**V1→V2 routing changes:** {len(changed)}",
        f"**Suppression events:** {len(suppressed)} products with ≥1 suppressed signal",
        f"**Instability flags:** {len(unstable)}",
        f"**Hybrid products:** {len(hybrid)}",
        "",
        "---",
        "",
        "## 1. V2 Routing Distribution",
        "",
    ]

    KNOWN_CATS = ["beverage", "cereal", "dairy_protein", "snack_bar_granola",
                  "whole_food_fat", "dessert", "sauce_spread", "default"]
    dist_rows = []
    for c in KNOWN_CATS:
        group = by_v2.get(c, [])
        n_anchor = sum(1 for r in group if r["anchor"])
        n_hybrid = sum(1 for r in group if r["is_hybrid"])
        confs    = [r["conf"] for r in group if r["conf"] is not None]
        mean_conf = f"{sum(confs)/len(confs):.2f}" if confs else "—"
        dist_rows.append([c, len(group), n_anchor, n_hybrid, mean_conf])

    lines.append(_md_table(
        ["Category", "Count", "Anchor-driven", "Hybrid", "Mean Conf"],
        dist_rows
    ))
    lines.append("")

    # Section 2: Anchor activations
    lines += ["---", "", "## 2. Anchor Activation Rate", "",
              f"{len(anchored)}/{n_total} products ({100*len(anchored)/max(n_total,1):.0f}%) "
              "routed via hard anchor. Anchors reflect stable, high-confidence routing decisions.", ""]

    if anchored:
        anchor_rows = []
        for r in anchored[:20]:
            anchor_rows.append([r["name"][:50], r["v2_cat"], r["subtype"] or "—", f"{r['conf']:.2f}"])
        lines.append(_md_table(["Product", "Category", "Subtype", "Conf"], anchor_rows))
        if len(anchored) > 20:
            lines.append(f"*... and {len(anchored)-20} more anchor-routed products.*")
    lines.append("")

    # Section 3: Suppressed contamination
    lines += ["---", "", "## 3. Suppressed Contamination Signals", "",
              "Products where context gating prevented ingredient-text signals from "
              "contaminating the routing decision.", ""]

    # Categorize by contamination type
    wff_suppressed  = [r for r in suppressed if any("whole_food_fat" in s for s in r["suppressed"])]
    bev_suppressed  = [r for r in suppressed if any("beverage:zeroed" in s for s in r["suppressed"])]
    dairy_suppressed = [r for r in suppressed if any("flavor_suppressor" in s for s in r["suppressed"])]

    lines.append(f"**A. WFF ingredient contamination suppressed:** {len(wff_suppressed)} products")
    for r in wff_suppressed[:8]:
        sigs = [s for s in r["suppressed"] if "whole_food_fat" in s]
        lines.append(f"  - {r['name'][:55]} → routed to **{r['v2_cat']}**; suppressed: {', '.join(sigs[:3])}")
    lines.append("")

    lines.append(f"**B. Beverage signal zeroed (no liquid context):** {len(bev_suppressed)} products")
    for r in bev_suppressed[:5]:
        lines.append(f"  - {r['name'][:55]} → routed to **{r['v2_cat']}**")
    lines.append("")

    lines.append(f"**C. Dairy flavor-descriptor suppression:** {len(dairy_suppressed)} products")
    for r in dairy_suppressed[:5]:
        sigs = [s for s in r["suppressed"] if "flavor_suppressor" in s]
        lines.append(f"  - {r['name'][:55]} → routed to **{r['v2_cat']}**; suppressed: {', '.join(sigs[:2])}")
    lines.append("")

    # Section 4: Instability and hybrids
    lines += ["---", "", "## 4. Routing Instability and Hybrid Products", ""]
    lines.append(f"**Unstable routes ({len(unstable)} products):** top-2 category delta < 0.3")
    for r in sorted(unstable, key=lambda x: x["conf"])[:10]:
        lines.append(
            f"  - {r['name'][:50]} → **{r['v2_cat']}** ({r['conf']:.2f}) vs {r['secondary']};  "
            f"{r['instability_w'] or ''}"
        )
    lines.append("")
    lines.append(f"**Hybrid products ({len(hybrid)}):** genuinely straddle two routing contexts")
    for r in hybrid[:8]:
        lines.append(f"  - {r['name'][:50]} → **{r['v2_cat']}** + {r['secondary']}")
    lines.append("")

    # Section 5: V1 vs V2 delta
    lines += ["---", "", "## 5. V1 → V2 Routing Changes", "",
              f"{len(changed)} products changed category between v1 and v2. "
              "Changes are expected where v1 misrouted due to the failure modes this router fixes.", ""]

    if changed:
        chg_rows = []
        for r in changed:
            chg_rows.append([r["name"][:50], r["v1_cat"] or "—", r["v2_cat"],
                             "anchor" if r["anchor"] else "signal", r["cat_tag"]])
        lines.append(_md_table(["Product", "V1 Category", "V2 Category", "Routing Basis", "Dataset"], chg_rows))
    else:
        lines.append("*No routing changes detected. Either v1 traces not available or routing is stable.*")
    lines.append("")

    # Section 6: Distribution by source category
    lines += ["---", "", "## 6. V2 Routing Distribution by Source Category", ""]
    for cat_tag, group in sorted(by_cat.items()):
        v2_counts: dict[str, int] = defaultdict(int)
        for r in group:
            v2_counts[r["v2_cat"]] += 1
        dist_str = "  ".join(f"{k}={v}" for k, v in sorted(v2_counts.items(), key=lambda x: -x[1]))
        lines.append(f"**{cat_tag}** ({len(group)} products): {dist_str}")
    lines.append("")

    # Section 7: Remaining weak zones
    lines += ["---", "", "## 7. Remaining Weak Zones", "",
              "Products with low confidence or instability that may need further attention.", ""]

    weak = [r for r in results if (r["conf"] or 0) < 0.55 and r["v2_cat"] != "default"]
    if weak:
        weak_rows = []
        for r in sorted(weak, key=lambda x: x["conf"] or 0)[:15]:
            weak_rows.append([r["name"][:50], r["v2_cat"], f"{r['conf']:.2f}", r["conf_band"], r["cat_tag"]])
        lines.append(_md_table(["Product", "Category", "Conf", "Band", "Dataset"], weak_rows))
    else:
        lines.append("*No low-confidence routes detected.*")
    lines.append("")

    lines += ["---", "", "## 8. Bread/Crackers Readiness Assessment", "",
              "Products that would be affected by bread/crackers category launch:"]
    bread_adjacent = [r for r in results
                      if any(b in (r.get("name") or "").lower() for b in ["לחם", "פיתה", "קרקר", "לאפה"])
                      or r["v2_cat"] == "default"]
    if bread_adjacent:
        for r in bread_adjacent[:10]:
            lines.append(f"  - {r['name'][:55]} → {r['v2_cat']} (conf={r['conf']:.2f})")
    else:
        lines.append("*No bread-adjacent products detected in current corpus.*")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_PATH


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run():
    log.info("=== BSIP2 Router v2 Validation ===")
    records  = load_all()
    analysis = analyze(records)
    path     = write_report(analysis)
    log.info("Report: %s", path)
    results  = analysis["results"]
    log.info("Products: %d | Changed: %d | Anchored: %d | Suppressed: %d | Unstable: %d",
             len(results),
             sum(1 for r in results if r["changed"]),
             sum(1 for r in results if r["anchor"]),
             sum(1 for r in results if r["suppressed"]),
             sum(1 for r in results if r["instability"]))


if __name__ == "__main__":
    run()
