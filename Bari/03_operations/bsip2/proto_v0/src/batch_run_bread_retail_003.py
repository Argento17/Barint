"""
BSIP2 Batch Runner — Real Bread Retail 003 (Shufersal Representative Shelf)
run_id: real_bread_retail_003_v1

Source: specified via --raw <path>  (default: most recent in bread_retail_003/)
Output: C:/Bari/02_products/bread_retail_003/bsip2/
Reports: C:/Bari/02_products/bread_retail_003/reports/

Same pipeline as 002_v2 plus two new reports:
  - real_bread_retail_003_market_structure.md    (price tiers, brand distribution)
  - real_bread_retail_003_mass_market_anchors.md (commodity bread analysis)
"""

from __future__ import annotations
import sys, json, re, pathlib, logging, datetime, argparse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from input_loader              import validate_product
from signal_extractor          import extract_signals
from router_v2                 import classify_category
from nova_proxy                import infer_nova
from evaluation_scope          import assign_evaluation_scope
from score_engine              import score_product, compute_confidence
from trace_writer              import assemble_trace
from bakery_semantics          import run_bakery_semantics
from structural_classifier     import classify_structural_class
from score_synthesis           import run_synthesis
from interpretation_confidence import compute_interpretation_confidence, apply_confidence_ceiling
from failure_taxonomy          import classify_failures, summarize_failures
from graceful_degradation      import determine_degradation_level, build_degraded_output
from constants                 import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

PRODUCT_DIR = pathlib.Path(r"C:\Bari\02_products\bread_retail_003")
BSIP2_DIR   = PRODUCT_DIR / "bsip2"
REPORT_DIR  = PRODUCT_DIR / "reports"
RUN_ID      = "real_bread_retail_003_v1"
TODAY       = datetime.date.today().isoformat()

for d in (BSIP2_DIR, REPORT_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
# Exclusion filter (same rules as 002_v2, extended for bread_retail_003)
# ──────────────────────────────────────────────────────────────────────────────

EXCLUDE_PATTERNS: list[tuple[str, str]] = [
    (r"שבלול",          "sweet_pastry"),
    (r"רוגלך",          "sweet_pastry"),
    (r"בורקס",          "sweet_pastry"),
    (r"קרואסון",        "sweet_pastry"),
    (r"עוגה",           "sweet_pastry"),
    (r"מאפה מתוק",      "sweet_pastry"),
    (r"עוגיות",         "sweet_pastry"),
    (r"ופל",            "sweet_pastry"),
    (r"^קמח\b",         "raw_ingredient"),
    (r"^שמרים\b",       "raw_ingredient"),
    (r"^סובין\b",       "raw_ingredient"),
    (r"^שיבולת שועל$",  "raw_ingredient"),
]


def _should_exclude(name_he: str) -> tuple[bool, str]:
    n = name_he.strip()
    for pattern, reason in EXCLUDE_PATTERNS:
        if re.search(pattern, n):
            return True, reason
    return False, ""


# ──────────────────────────────────────────────────────────────────────────────
# BSIP0 → BSIP1 normalization
# ──────────────────────────────────────────────────────────────────────────────

def _parse_num(raw: str) -> float | None:
    if not raw:
        return None
    s = str(raw).strip()
    m = re.match(r"(?:פחות מ|<)\s*([\d.]+)", s, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1)) / 2
        except ValueError:
            return None
    m2 = re.match(r"([\d.]+)", s.replace(",", "."))
    if m2:
        try:
            return float(m2.group(1))
        except ValueError:
            return None
    return None


def normalize_to_bsip1(raw: dict) -> dict:
    name_he = (raw.get("name_he") or "").strip()
    barcode = str(raw.get("barcode") or "")
    brand = raw.get("brand") or ""

    nutr_raw = raw.get("nutrition", {})
    energy  = _parse_num(nutr_raw.get("energy_kcal_raw", ""))
    protein = _parse_num(nutr_raw.get("protein_raw", ""))
    carbs   = _parse_num(nutr_raw.get("carbs_raw", ""))
    fat     = _parse_num(nutr_raw.get("fat_raw", ""))
    fiber   = _parse_num(nutr_raw.get("fiber_raw", ""))
    sodium  = _parse_num(nutr_raw.get("sodium_raw", ""))
    sugar   = _parse_num(nutr_raw.get("sugar_raw", ""))

    ingredients_raw = (raw.get("ingredients_raw") or "").strip()

    missing = []
    if not name_he:       missing.append("canonical_name_he")
    if energy is None:    missing.append("energy_kcal")
    if fiber is None:     missing.append("dietary_fiber_g")
    if protein is None:   missing.append("protein_g")
    if not ingredients_raw: missing.append("ingredients_text")

    pid = f"shufersal_{barcode}" if barcode else f"shufersal_{name_he[:20].replace(' ','_')}"

    return {
        "schema_version":             "bsip1_v0_2_shufersal",
        "file_type":                  "product",
        "canonical_product_id":       pid,
        "barcode":                    barcode,
        "canonical_name_he":          name_he,
        "canonical_name_en":          raw.get("name_en") or "",
        "brand":                      brand,
        "source_retailers":           ["shufersal"],
        "source_url":                 raw.get("source_url") or "",
        "scraped_at":                 raw.get("scraped_at") or "",
        "image_urls":                 raw.get("image_urls") or [],
        "category_raw":               raw.get("category_raw") or "",
        "normalized_nutrition_per_100g": {
            "energy_kcal":       energy,
            "fat_g":             fat,
            "fat_saturated_g":   None,
            "fat_trans_g":       None,
            "sodium_mg":         sodium,
            "carbohydrates_g":   carbs,
            "sugars_g":          sugar,
            "dietary_fiber_g":   fiber,
            "protein_g":         protein,
        },
        "ingredients_text_he":        ingredients_raw,
        "ingredients_raw":            ingredients_raw,
        "ingredients_list":           [],
        "allergens_contains":         [],
        "allergens_may_contain":      [],
        "off_categories":             "",
        "claims":                     [],
        "confidence": {
            "scrape_quality_score": 0.85 if (energy is not None and ingredients_raw) else
                                    0.60 if (energy is not None or ingredients_raw) else 0.35,
        },
        "conflicts_summary":          {},
        "missing_fields":             missing,
        "inferred_fields":            [],
        "audit_ref":                  f"bsip0_v3_{RUN_ID}",
        "extraction_method":          raw.get("extraction_method") or "html_parse",
        "extraction_confidence":      raw.get("extraction_confidence") or "medium",
        # v3 additions — price tracking
        "_price":                     raw.get("price", ""),
        "_weight_g":                  raw.get("weight_g"),
        "_price_per_100g":            raw.get("price_per_100g"),
        "_acquisition_query":         raw.get("acquisition_query", ""),
        "_acquisition_tier":          raw.get("acquisition_tier", ""),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline
# ──────────────────────────────────────────────────────────────────────────────

def run_pipeline(product: dict) -> dict:
    prod = {k: v for k, v in product.items() if not k.startswith("_")}
    load_errors = product.get("_load_errors", [])

    signals      = extract_signals(prod)
    cat_result   = classify_category(prod)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(prod, l3)
    eval_result  = assign_evaluation_scope(prod, cat_result["category"])
    score_result = score_product(prod, signals, cat_result, nova_result, eval_result)

    base_conf    = compute_confidence(prod, signals, cat_result, nova_result)
    interp_conf  = compute_interpretation_confidence(base_conf, cat_result, prod, signals)
    score_result = apply_confidence_ceiling(score_result, interp_conf)

    bakery_result  = run_bakery_semantics(prod, cat_result["category"], l3)
    trace          = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
    trace["bakery_semantics"]  = bakery_result
    trace["structural_class"]  = classify_structural_class(trace, bakery_result)
    synth_result   = run_synthesis(trace)
    trace["synthesis_result"]  = synth_result

    final_score  = synth_result.get("synthesis_score") or score_result.get("final_score_estimate")
    final_grade  = score_to_grade(final_score) if final_score is not None else None

    failures          = classify_failures(prod, signals, cat_result, nova_result, score_result, interp_conf)
    fail_summary      = summarize_failures(failures)
    degradation_level = determine_degradation_level(interp_conf, score_result, failures)
    degraded_output   = build_degraded_output(prod, score_result, cat_result, interp_conf, failures, degradation_level)

    return {
        "product_id":        prod.get("canonical_product_id"),
        "barcode":           prod.get("barcode"),
        "name_he":           prod.get("canonical_name_he"),
        "brand":             prod.get("brand"),
        "source_retailers":  prod.get("source_retailers", []),
        "source_url":        prod.get("source_url"),
        "image_urls":        prod.get("image_urls", []),
        "scrape_quality":    prod.get("confidence", {}).get("scrape_quality_score"),
        "missing_fields":    prod.get("missing_fields", []),
        "load_errors":       load_errors,
        "signals":           signals,
        "cat_result":        cat_result,
        "nova_result":       nova_result,
        "score_result":      score_result,
        "synth_result":      synth_result,
        "final_score":       final_score,
        "final_grade":       final_grade,
        "bakery_result":     bakery_result,
        "structural_class":  trace.get("structural_class"),
        "base_conf":         base_conf,
        "interp_conf":       interp_conf,
        "failures":          failures,
        "fail_summary":      fail_summary,
        "degradation_level": degradation_level,
        "degraded_output":   degraded_output,
        "ingredients_text":  prod.get("ingredients_text_he") or "",
        "nutrition":         prod.get("normalized_nutrition_per_100g") or {},
        "claims":            prod.get("claims") or [],
        "off_categories":    prod.get("off_categories", ""),
        # price passthrough
        "price_per_100g":    product.get("_price_per_100g"),
        "weight_g":          product.get("_weight_g"),
        "acquisition_query": product.get("_acquisition_query", ""),
        "acquisition_tier":  product.get("_acquisition_tier", ""),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────────────────────────────────────

def _deg_label(lvl: str) -> str:
    return {"FULL": "Full", "CAUTIOUS": "Cautious",
            "UNCERTAINTY": "Uncertain", "INSUFFICIENT": "Insufficient"}.get(lvl, lvl)

def _conf_label_he(r: dict) -> str:
    deg = r["degradation_level"]
    has_ing = bool(r.get("ingredients_text"))
    if deg == "FULL" and has_ing:            return "נתונים מלאים יחסית"
    if deg == "CAUTIOUS" and has_ing:        return "נתונים חלקיים"
    if deg in ("UNCERTAINTY",) or not has_ing: return "חסרים נתונים מהותיים"
    return "לא מספיק לניתוח ודאי"

def _first_img(r: dict) -> str:
    imgs = r.get("image_urls") or []
    return imgs[0] if imgs else ""

def _price_tier_label(p100g: float | None) -> str:
    if p100g is None: return "unknown"
    if p100g < 1.5:   return "budget"
    if p100g < 3.0:   return "mid"
    if p100g < 5.0:   return "premium"
    return "ultra-premium"


# ──────────────────────────────────────────────────────────────────────────────
# Reports (standard set — same as 002_v2, updated for 003)
# ──────────────────────────────────────────────────────────────────────────────

def report_bsip1_quality(results: list[dict], excluded: list[dict]) -> str:
    n = len(results)
    n_ex = len(excluded)
    has_kcal  = sum(1 for r in results if r["nutrition"].get("energy_kcal") is not None)
    has_fiber = sum(1 for r in results if r["nutrition"].get("dietary_fiber_g") is not None)
    has_prot  = sum(1 for r in results if r["nutrition"].get("protein_g") is not None)
    has_carbs = sum(1 for r in results if r["nutrition"].get("carbohydrates_g") is not None)
    has_fat   = sum(1 for r in results if r["nutrition"].get("fat_g") is not None)
    has_na    = sum(1 for r in results if r["nutrition"].get("sodium_mg") is not None)
    has_sug   = sum(1 for r in results if r["nutrition"].get("sugars_g") is not None)
    has_ing   = sum(1 for r in results if r.get("ingredients_text"))
    has_price = sum(1 for r in results if r.get("price_per_100g") is not None)

    lines = [
        f"# BSIP1 Normalization Quality — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | **Source:** Shufersal acquisition v3 (representative shelf)",
        f"",
        f"**Acquisition v3 improvements:** mainstream-first queries, 5-page pagination, category browsing, brand searches.",
        f"",
        f"---",
        f"",
        f"## Corpus Summary",
        f"",
        f"| Metric | Value |",
        f"|:-------|:------|",
        f"| Raw products from BSIP0 v3 | {n + n_ex} |",
        f"| Excluded (out-of-scope) | {n_ex} |",
        f"| In-scope for scoring | {n} |",
        f"| Retailer | Shufersal only |",
        f"",
        f"## Nutrition Field Coverage",
        f"",
        f"| Field | Present | Coverage |",
        f"|:------|:--------|:---------|",
        f"| Energy (kcal/100g) | {has_kcal} | {100*has_kcal//n if n else 0}% |",
        f"| Dietary fiber | {has_fiber} | {100*has_fiber//n if n else 0}% |",
        f"| Protein | {has_prot} | {100*has_prot//n if n else 0}% |",
        f"| Carbohydrates | {has_carbs} | {100*has_carbs//n if n else 0}% |",
        f"| Fat | {has_fat} | {100*has_fat//n if n else 0}% |",
        f"| Sodium | {has_na} | {100*has_na//n if n else 0}% |",
        f"| Sugars | {has_sug} | {100*has_sug//n if n else 0}% |",
        f"| Ingredient text | {has_ing} | {100*has_ing//n if n else 0}% |",
        f"| Price/100g | {has_price} | {100*has_price//n if n else 0}% |",
        f"",
        f"## Degradation Distribution",
        f"",
    ]
    degs: dict[str, int] = {}
    for r in results:
        degs[r["degradation_level"]] = degs.get(r["degradation_level"], 0) + 1
    for deg in ["FULL", "CAUTIOUS", "UNCERTAINTY", "INSUFFICIENT"]:
        cnt = degs.get(deg, 0)
        lines.append(f"- **{_deg_label(deg)}:** {cnt} ({100*cnt//n if n else 0}%)")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_exclusion(excluded: list[dict]) -> str:
    lines = [
        f"# Product Exclusion Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY}",
        f"",
        f"**Total excluded:** {len(excluded)}",
        f"",
        f"| # | Product (Hebrew) | Exclusion Reason |",
        f"|:--|:----------------|:----------------|",
    ]
    for i, ex in enumerate(excluded, 1):
        name = (ex.get("name_he") or "")[:45]
        reason = ex.get("_exclusion_reason", "")
        lines.append(f"| {i} | {name} | {reason} |")
    lines += [
        "",
        "## Exclusion Rules",
        "",
        "- `sweet_pastry`: שבלול, רוגלך, בורקס, קרואסון, עוגה, עוגיות, ופל",
        "- `raw_ingredient`: standalone קמח, שמרים, סובין, שיבולת שועל",
        "- Note: חלה (challah) is NOT excluded.",
        "",
        f"*Generated by {RUN_ID}*",
    ]
    return "\n".join(lines)


def report_batch_summary(results: list[dict]) -> str:
    n = len(results)
    scored = [r for r in results if r.get("final_score") is not None]
    scores = [r["final_score"] for r in scored]
    cats: dict[str, int] = {}
    degs: dict[str, int] = {}
    grades: dict[str, int] = {}
    tiers: dict[str, int] = {}
    for r in results:
        c = r["cat_result"].get("category", "?")
        cats[c] = cats.get(c, 0) + 1
        degs[r["degradation_level"]] = degs.get(r["degradation_level"], 0) + 1
        g = r.get("final_grade") or "?"
        grades[g] = grades.get(g, 0) + 1
        t = _price_tier_label(r.get("price_per_100g"))
        tiers[t] = tiers.get(t, 0) + 1

    avg = sum(scores)/len(scores) if scores else None
    med = sorted(scores)[len(scores)//2] if scores else None

    lines = [
        f"# Batch Pipeline Summary — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | **Source:** Shufersal representative shelf | **n={n}**",
        f"",
        f"**Acquisition v3:** mainstream-first, 5-page pagination, category traversal, brand searches.",
        f"",
        f"## Overview",
        f"",
        f"| Metric | Value |",
        f"|:-------|:------|",
        f"| Products processed | {n} |",
        f"| Products with score | {len(scored)} ({100*len(scored)//n if n else 0}%) |",
    ]
    if avg:
        lines.append(f"| Average score | {avg:.1f} |")
        lines.append(f"| Median score | {med:.1f} |")
        lines.append(f"| Min / Max score | {min(scores):.0f} / {max(scores):.0f} |")

    lines += ["", "## Routing Distribution", ""]
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        bar = "█" * (cnt * 20 // n) if n else ""
        lines.append(f"- `{cat}`: {cnt} ({100*cnt//n if n else 0}%) {bar}")

    lines += ["", "## Degradation Distribution", ""]
    for deg in ["FULL", "CAUTIOUS", "UNCERTAINTY", "INSUFFICIENT"]:
        cnt = degs.get(deg, 0)
        lines.append(f"- **{_deg_label(deg)}:** {cnt} ({100*cnt//n if n else 0}%)")

    lines += ["", "## Grade Distribution", ""]
    for g in ["A", "B", "C", "D", "E", "?"]:
        cnt = grades.get(g, 0)
        if cnt:
            lines.append(f"- Grade **{g}:** {cnt} ({100*cnt//n if n else 0}%)")

    lines += ["", "## Price Tier Distribution", ""]
    for tier in ["budget", "mid", "premium", "ultra-premium", "unknown"]:
        cnt = tiers.get(tier, 0)
        if cnt:
            lines.append(f"- {tier}: {cnt} ({100*cnt//n if n else 0}%)")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_score_distribution(results: list[dict]) -> str:
    n = len(results)
    scored = [r for r in results if r.get("final_score") is not None]
    scores = [r["final_score"] for r in scored]
    lines = [
        f"# Score Distribution — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n} ({len(scored)} with score)",
        f"",
        f"## Score Bands",
        f"",
        f"| Band | Range | Count | % |",
        f"|:-----|:------|:------|:--|",
    ]
    for label, lo, hi in [("Elite",80,101),("Strong",65,80),("Mid",50,65),("Weak",35,50),("Poor",0,35)]:
        grp = [r for r in scored if lo <= r["final_score"] < hi]
        lines.append(f"| {label} | {lo}–{hi-1} | {len(grp)} | {100*len(grp)//n if n else 0}% |")

    if scores:
        lines += [
            f"",
            f"**Mean:** {sum(scores)/len(scores):.1f} | **Median:** {sorted(scores)[len(scores)//2]:.1f} | "
            f"**Min:** {min(scores):.0f} | **Max:** {max(scores):.0f}",
        ]

    lines += ["", "## Top 15 by Score", ""]
    top = sorted(scored, key=lambda r: r["final_score"], reverse=True)[:15]
    for i, r in enumerate(top, 1):
        name = (r.get("name_he") or "")[:38]
        cat  = r["cat_result"].get("category", "?")
        deg  = _deg_label(r["degradation_level"])
        tier = _price_tier_label(r.get("price_per_100g"))
        p100 = r.get("price_per_100g")
        p_str = f" | {p100:.2f}₪/100g" if p100 else ""
        lines.append(
            f"{i}. **{name}** — {cat} — score={r['final_score']:.0f} "
            f"grade={r.get('final_grade','?')} [{deg}] [{tier}]{p_str}"
        )

    lines += ["", "## Bottom 10 by Score", ""]
    bot = sorted(scored, key=lambda r: r["final_score"])[:10]
    for i, r in enumerate(bot, 1):
        name = (r.get("name_he") or "")[:38]
        cat  = r["cat_result"].get("category", "?")
        deg  = _deg_label(r["degradation_level"])
        lines.append(f"{i}. {name} — {cat} — score={r['final_score']:.0f} [{deg}]")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_routing_distribution(results: list[dict]) -> str:
    n = len(results)
    cat_groups: dict[str, list] = {}
    for r in results:
        cat = r["cat_result"].get("category", "unknown")
        cat_groups.setdefault(cat, []).append(r)
    lines = [
        f"# Routing Distribution — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
    ]
    for cat, group in sorted(cat_groups.items(), key=lambda x: -len(x[1])):
        avg_conf = sum(r["cat_result"].get("category_confidence", 0) for r in group) / len(group)
        anchors  = sum(1 for r in group if r["cat_result"].get("anchor_override"))
        lines += [f"### `{cat}` — {len(group)} products ({100*len(group)//n if n else 0}%)", ""]
        lines.append(f"- Avg confidence: {avg_conf:.2f} | Anchor overrides: {anchors}")
        lines.append("")
        for r in sorted(group, key=lambda x: x.get("final_score") or 0, reverse=True)[:10]:
            name = (r.get("name_he") or "")[:38]
            s = r.get("final_score")
            s_str = f"{s:.0f}" if s is not None else "—"
            anch = "⚓ " if r["cat_result"].get("anchor_override") else ""
            lines.append(f"  - {anch}{name} (score={s_str})")
        if len(group) > 10:
            lines.append(f"  - … +{len(group)-10} more")
        lines.append("")
    lines += [f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_fiber_laundering(results: list[dict]) -> str:
    n = len(results)
    fiber_vals = [(r, r["nutrition"].get("dietary_fiber_g"))
                  for r in results if r["nutrition"].get("dietary_fiber_g") is not None]
    MATRIX_KW = ["אינולין","inulin","psyllium","ציקוריה","chicory","cellulose","גואר","קסנטן"]
    WG_KW     = ["קמח מלא","שיפון מלא","חיטה מלאה","כוסמין מלא","wholegrain","whole grain"]
    lines = [
        f"# Fiber Laundering Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"**Definition:** Product claims or displays high fiber but the fiber comes from isolated",
        f"additives (inulin, chicory, psyllium) rather than intact whole grain.",
        f"",
    ]
    fvals = [v for _, v in fiber_vals]
    if fvals:
        lines += [
            f"**Products with fiber data:** {len(fvals)}/{n}",
            f"**Mean fiber:** {sum(fvals)/len(fvals):.1f}g/100g",
            f"**High fiber (≥6g):** {sum(1 for v in fvals if v>=6)} products",
            f"**Very high (≥10g):** {sum(1 for v in fvals if v>=10)} products",
            "",
        ]
    launder_cases = []
    lines += ["## Fiber Source Assessment", ""]
    for r, fiber in sorted(fiber_vals, key=lambda x: -x[1])[:30]:
        ing  = r.get("ingredients_text","").lower()
        has_matrix = any(kw in ing for kw in MATRIX_KW)
        has_wg     = any(kw in ing for kw in WG_KW)
        if has_matrix and fiber >= 5:
            flag = "⚠ MATRIX-ADDED FIBER"
            launder_cases.append(r)
        elif has_wg:
            flag = "✓ whole grain"
        elif not ing:
            flag = "? no ingredient data"
        else:
            flag = "~ unclear"
        name = (r.get("name_he") or "")[:36]
        p100 = r.get("price_per_100g")
        tier = f" [{_price_tier_label(p100)}]" if p100 else ""
        lines.append(f"- **{name}**: fiber={fiber:.1f}g — {flag}{tier}")
    lines += [
        "",
        f"**Confirmed matrix-added fiber cases:** {len(launder_cases)}",
        "",
        f"*Generated by {RUN_ID}*",
    ]
    return "\n".join(lines)


def report_seed_halo(results: list[dict]) -> str:
    n = len(results)
    SEED_KW = ["שומשום","פשתן","דלעת","גרעיני","זרעי","צ'יה","chia","sunflower","sesame","pumpkin","flax","כוסמת"]
    WG_KW   = ["קמח מלא","שיפון מלא","חיטה מלאה","כוסמין מלא","wholegrain"]
    seeded  = []
    for r in results:
        ing  = r.get("ingredients_text","").lower()
        name = (r.get("name_he") or "").lower()
        seeds = [kw for kw in SEED_KW if kw in ing or kw in name]
        if seeds:
            has_wg = any(kw.lower() in ing for kw in WG_KW)
            seeded.append((r, seeds, has_wg))
    lines = [
        f"# Seed Halo Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"**Definition:** Seeds surface-applied to a refined-flour matrix — premium impression without structural benefit.",
        f"",
        f"**Products with seed signals:** {len(seeded)}/{n} ({100*len(seeded)//n if n else 0}%)",
        f"",
        f"## Assessment",
        f"",
    ]
    for r, seeds, has_wg in sorted(seeded, key=lambda x: x[0].get("final_score") or 0, reverse=True):
        name  = (r.get("name_he") or "")[:38]
        score = r.get("final_score")
        s_str = f"{score:.0f}" if score is not None else "—"
        flag  = "✓ whole grain matrix" if has_wg else "⚠ possible surface seeding"
        p100 = r.get("price_per_100g")
        tier = f" | {_price_tier_label(p100)}" if p100 else ""
        lines.append(f"- **{name}** — score={s_str}{tier} — {flag} — seeds: {', '.join(seeds[:3])}")
    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_fermentation_claims(results: list[dict]) -> str:
    n = len(results)
    FERM_REAL = ["מחמצת","sourdough","חיידקים","תרבויות","חומצה לקטית","fermented","lactobacillus"]
    FERM_IND  = ["שמרים","yeast","חומר מתפיח","E-500","E-450"]
    true_ferm, false_ferm, industrial = [], [], []
    for r in results:
        ing  = r.get("ingredients_text","").lower()
        name = (r.get("name_he") or "").lower()
        has_claim = "מחמצת" in name or "sourdough" in name
        has_real  = any(kw in ing for kw in FERM_REAL)
        has_ind   = any(kw in ing for kw in FERM_IND)
        if has_claim or has_real:
            if has_real and not has_ind:
                true_ferm.append(r)
            elif has_claim and has_ind:
                false_ferm.append(r)
            else:
                true_ferm.append(r)
        elif has_ind:
            industrial.append(r)

    lines = [
        f"# Fermentation Claims Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"| Category | Count |",
        f"|:---------|:------|",
        f"| Genuine fermentation | {len(true_ferm)} |",
        f"| Claim + industrial yeast (mismatch) | {len(false_ferm)} |",
        f"| Industrial yeast only | {len(industrial)} |",
        f"",
        f"## Genuine Fermentation Products",
        f"",
    ]
    for r in sorted(true_ferm, key=lambda x: x.get("final_score") or 0, reverse=True):
        name = (r.get("name_he") or "")[:42]
        s = r.get("final_score")
        p100 = r.get("price_per_100g")
        tier = f" | {_price_tier_label(p100)}" if p100 else ""
        lines.append(f"- **{name}** — score={s:.0f}{tier}" if s else f"- **{name}**{tier}")

    if false_ferm:
        lines += ["", "## ⚠ Fermentation Label / Industrial Mismatch", ""]
        for r in false_ferm:
            p100 = r.get("price_per_100g")
            tier = f" | {_price_tier_label(p100)}" if p100 else ""
            lines.append(f"- **{(r.get('name_he') or '')[:42]}** — claims מחמצת + industrial yeast{tier}")

    if industrial:
        lines += [f"", f"## Industrial Yeast Only (no claim): {len(industrial)}", ""]
        for r in industrial[:15]:
            lines.append(f"- {(r.get('name_he') or '')[:42]}")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_deceptive_patterns(results: list[dict]) -> str:
    n = len(results)
    SUGAR_ALIASES = ["סוכר","גלוקוז","פרוקטוז","דקסטרוז","מלטוז","סירופ","syrup","honey","דבש","מלאס","molasses","ממתיק"]
    REFINED_KW    = ["קמח חיטה","קמח לבן","white flour","wheat flour"]
    WG_CLAIM      = ["מלא","whole","integrale","כוסמין"]
    sugar_camouflage, refined_wg, high_sodium = [], [], []
    for r in results:
        ing  = r.get("ingredients_text","").lower()
        name = (r.get("name_he") or "").lower()
        nn   = r["nutrition"]
        cnt  = sum(1 for a in SUGAR_ALIASES if a in ing)
        if cnt >= 3:
            sugar_camouflage.append((r, cnt))
        if any(k in ing for k in REFINED_KW) and any(k in name for k in WG_CLAIM):
            refined_wg.append(r)
        na = nn.get("sodium_mg")
        if na is not None and na > 600:
            high_sodium.append((r, na))

    lines = [
        f"# Deceptive Patterns Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"## Multi-Sugar Camouflage (≥3 sugar aliases)",
        f"",
        f"**{len(sugar_camouflage)} products detected.**",
        f"",
    ]
    for r, cnt in sorted(sugar_camouflage, key=lambda x: -x[1]):
        lines.append(f"- **{(r.get('name_he') or '')[:42]}** — {cnt} sugar forms")

    lines += [f"", f"## Refined Flour with Whole Grain Name Claim", f"", f"**{len(refined_wg)} products detected.**", ""]
    for r in refined_wg:
        lines.append(f"- **{(r.get('name_he') or '')[:42]}**")

    lines += [f"", f"## High Sodium (>600mg/100g)", f"", f"**{len(high_sodium)} products detected.**", ""]
    for r, na in sorted(high_sodium, key=lambda x: -x[1]):
        lines.append(f"- **{(r.get('name_he') or '')[:42]}** — {na:.0f}mg/100g")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_top_coherent(results: list[dict]) -> str:
    n = len(results)
    coherent = sorted(
        [r for r in results
         if r.get("final_score") is not None
         and r["degradation_level"] in ("FULL","CAUTIOUS")
         and r.get("ingredients_text")],
        key=lambda r: r["final_score"], reverse=True
    )
    lines = [
        f"# Top Coherent Products — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"Coherent = score present, degradation FULL or CAUTIOUS, ingredient text available.",
        f"",
        f"**Coherent products:** {len(coherent)}/{n}",
        f"",
    ]
    for i, r in enumerate(coherent[:25], 1):
        name  = (r.get("name_he") or "")[:42]
        cat   = r["cat_result"].get("category","?")
        deg   = _deg_label(r["degradation_level"])
        score = r["final_score"]
        grade = r.get("final_grade") or "?"
        fiber = r["nutrition"].get("dietary_fiber_g")
        f_str = f" | fiber={fiber:.1f}g" if fiber is not None else ""
        ing   = r.get("ingredients_text","").lower()
        ferm  = " | מחמצת ✓" if "מחמצת" in ing else ""
        p100  = r.get("price_per_100g")
        p_str = f" | {p100:.2f}₪/100g [{_price_tier_label(p100)}]" if p100 else ""
        lines.append(f"{i}. **{name}** — {cat} — score={score:.0f} grade={grade} [{deg}]{f_str}{ferm}{p_str}")
    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_website_handoff(results: list[dict], excluded: list[dict]) -> str:
    n = len(results)
    scored   = [r for r in results if r.get("final_score") is not None]
    verified = [r for r in scored if r["degradation_level"] in ("FULL","CAUTIOUS") and r.get("ingredients_text")]
    insufficient = [r for r in results if r["degradation_level"] == "INSUFFICIENT"]
    top_v    = sorted(verified, key=lambda r: r["final_score"], reverse=True)[:5]
    fibers   = [r["nutrition"]["dietary_fiber_g"] for r in verified if r["nutrition"].get("dietary_fiber_g") is not None]
    avg_fiber = sum(fibers)/len(fibers) if fibers else None
    ferm_count = sum(1 for r in verified if "מחמצת" in r.get("ingredients_text","").lower())

    lines = [
        f"# Website Handoff — {RUN_ID}",
        f"",
        f"**Generated:** {TODAY} | **Source:** Shufersal real-shelf scrape — acquisition v3 (representative shelf)",
        f"",
        f"---",
        f"",
        f"## 1. Data Transparency — Mandatory Framing",
        f"",
        f"> ניתחנו מוצרי לחם, פיתה וקרקרים ממדף שופרסל האמיתי.",
        f"> הנתונים לקוחים ישירות מדפי המוצר של שופרסל — כולל לוח תזונה ורשימת רכיבים.",
        f"> {len(verified)} מוצרים עמדו בסף הנתונים הנדרש לניתוח מלא.",
        f"> זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא.",
        f"",
        f"> We analyzed {n} bread, pita and cracker products from a real Shufersal shelf (acquisition v3).",
        f"> {len(verified)} products had sufficient data for reliable scoring.",
        f"> This is a Shufersal shelf snapshot, not a full Israeli market survey.",
        f"",
        f"---",
        f"",
        f"## 2. Key Stats — Safe to Publish",
        f"",
        f"Based on {len(verified)} verified products:",
        f"",
    ]
    if avg_fiber:
        lines.append(f"- **Average fiber (verified):** {avg_fiber:.1f}g per 100g")
    lines.append(f"- **Genuine fermentation:** {ferm_count}/{len(verified)}")
    grade_dist: dict[str, int] = {}
    for r in verified:
        g = r.get("final_grade") or "?"
        grade_dist[g] = grade_dist.get(g, 0) + 1
    lines.append(f"- **Grade distribution (verified):**")
    for g in ["A","B","C","D","E"]:
        if grade_dist.get(g):
            lines.append(f"  - Grade {g}: {grade_dist[g]} products")

    lines += [f"", f"---", f"", f"## 3. Top Verified Products", f""]
    for r in top_v:
        name  = r.get("name_he","")
        score = r["final_score"]
        grade = r.get("final_grade","?")
        fiber = r["nutrition"].get("dietary_fiber_g")
        ferm  = "✓" if "מחמצת" in r.get("ingredients_text","").lower() else "✗"
        conf  = _conf_label_he(r)
        url   = r.get("source_url","")
        img   = _first_img(r)
        cat   = r["cat_result"].get("category","?")
        p100  = r.get("price_per_100g")
        lines += [
            f"**{name}**",
            f"- Score: {score:.0f} | Grade: {grade} | {conf}",
            f"- Fiber: {fiber:.1f}g/100g" if fiber else "- Fiber: לא זמין",
            f"- Fermentation: {ferm}",
            f"- Category: {cat}",
        ]
        if p100:
            lines.append(f"- Price: {p100:.2f}₪/100g [{_price_tier_label(p100)}]")
        lines.append(f"- Source: {url}")
        if img:
            lines.append(f"- Image: {img}")
        lines.append("")

    lines += ["", f"*Handoff generated by {RUN_ID} — {TODAY}*"]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# New reports: market structure + mass market anchors
# ──────────────────────────────────────────────────────────────────────────────

def report_market_structure(results: list[dict]) -> str:
    n = len(results)
    scored = [r for r in results if r.get("final_score") is not None]

    # Price tier vs score
    tier_scores: dict[str, list[float]] = {}
    for r in scored:
        t = _price_tier_label(r.get("price_per_100g"))
        tier_scores.setdefault(t, []).append(r["final_score"])

    # Category vs price tier
    cat_tiers: dict[str, dict[str, int]] = {}
    for r in results:
        cat = r["cat_result"].get("category","?")
        t   = _price_tier_label(r.get("price_per_100g"))
        cat_tiers.setdefault(cat, {})
        cat_tiers[cat][t] = cat_tiers[cat].get(t, 0) + 1

    # Acquisition tier breakdown
    acq_tier_counts: dict[str, int] = {}
    for r in results:
        t = r.get("acquisition_tier","unknown")
        acq_tier_counts[t] = acq_tier_counts.get(t, 0) + 1

    lines = [
        f"# Market Structure Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"Answers: how does price tier correlate with product score? Does the 'healthy bread'",
        f"premium actually correspond to better nutritional quality?",
        f"",
        f"---",
        f"",
        f"## 1. Price Tier Distribution",
        f"",
        f"| Price Tier | Count | Share | Avg Score | Score Range |",
        f"|:-----------|:------|:------|:----------|:------------|",
    ]
    for tier in ["budget","mid","premium","ultra-premium","unknown"]:
        scores = tier_scores.get(tier, [])
        cnt    = acq_tier_counts.get("unknown",0) if tier == "unknown" else sum(
            1 for r in results if _price_tier_label(r.get("price_per_100g")) == tier
        )
        cnt    = sum(1 for r in results if _price_tier_label(r.get("price_per_100g")) == tier)
        avg_s  = f"{sum(scores)/len(scores):.1f}" if scores else "—"
        rng    = f"{min(scores):.0f}–{max(scores):.0f}" if scores else "—"
        lines.append(f"| {tier} | {cnt} | {cnt*100//n if n else 0}% | {avg_s} | {rng} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## 2. Price-Score Correlation Analysis",
        f"",
    ]
    tier_order = ["budget","mid","premium","ultra-premium"]
    for tier in tier_order:
        scores = tier_scores.get(tier, [])
        if scores:
            lines.append(f"**{tier}** (n={len(scores)}): avg={sum(scores)/len(scores):.1f}, "
                         f"min={min(scores):.0f}, max={max(scores):.0f}")

    lines += [
        f"",
        f"**Interpretation:** Do higher-priced products score better?",
        f"If budget products score comparably to premium — the price premium buys label claims, not nutrition.",
        f"",
        f"---",
        f"",
        f"## 3. Category vs Price Tier",
        f"",
    ]
    for cat, tier_dist in sorted(cat_tiers.items(), key=lambda x: -sum(x[1].values())):
        total_cat = sum(tier_dist.values())
        tier_str = " | ".join(f"{t}: {c}" for t, c in sorted(tier_dist.items()) if c > 0)
        lines.append(f"- **{cat}** ({total_cat}): {tier_str}")

    lines += [
        f"",
        f"---",
        f"",
        f"## 4. Acquisition Source Breakdown",
        f"",
        f"Shows which query tiers contributed products — test for query bias.",
        f"",
        f"| Tier | Count | Share |",
        f"|:-----|:------|:------|",
    ]
    for tier, cnt in sorted(acq_tier_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {tier} | {cnt} | {cnt*100//n if n else 0}% |")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_mass_market_anchors(results: list[dict]) -> str:
    n = len(results)

    COMMODITY_NAMES = [
        "לחם לבן","לחם אחיד","לחם חלב","לחם רגיל",
        "ברמן","וונדר","wonder","berman","אנג'ל","דגנית",
        "פיתה","לאפה","טוסט","חלה",
    ]
    WELLNESS_NAMES = [
        "כוסמין","מחמצת","אורגני","שיפון","ללא גלוטן","gluten","פסיליום",
        "נבטים","ספלט","spelt","sourdough",
    ]

    def is_commodity(r: dict) -> bool:
        name = (r.get("name_he") or "").lower()
        return any(kw.lower() in name for kw in COMMODITY_NAMES)

    def is_wellness(r: dict) -> bool:
        name = (r.get("name_he") or "").lower()
        return any(kw.lower() in name for kw in WELLNESS_NAMES)

    commodity = [r for r in results if is_commodity(r)]
    wellness  = [r for r in results if is_wellness(r)]
    both      = [r for r in results if is_commodity(r) and is_wellness(r)]
    neither   = [r for r in results if not is_commodity(r) and not is_wellness(r)]

    def avg_score(group: list[dict]) -> str:
        s = [r["final_score"] for r in group if r.get("final_score") is not None]
        return f"{sum(s)/len(s):.1f}" if s else "—"

    def avg_fiber(group: list[dict]) -> str:
        f = [r["nutrition"]["dietary_fiber_g"] for r in group if r["nutrition"].get("dietary_fiber_g") is not None]
        return f"{sum(f)/len(f):.1f}g" if f else "—"

    def avg_price(group: list[dict]) -> str:
        p = [r["price_per_100g"] for r in group if r.get("price_per_100g") is not None]
        return f"{sum(p)/len(p):.2f}₪" if p else "—"

    lines = [
        f"# Mass Market Anchors Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | n={n}",
        f"",
        f"**Research question:** Does commodity bread in the Israeli mass market differ",
        f"structurally from wellness bread? Does the wellness premium deliver better nutrition,",
        f"or is it a labeling effect?",
        f"",
        f"---",
        f"",
        f"## 1. Segment Classification",
        f"",
        f"| Segment | Count | Avg Score | Avg Fiber | Avg Price/100g |",
        f"|:--------|:------|:----------|:----------|:---------------|",
        f"| Commodity (mainstream) | {len(commodity)} | {avg_score(commodity)} | {avg_fiber(commodity)} | {avg_price(commodity)} |",
        f"| Wellness/specialty | {len(wellness)} | {avg_score(wellness)} | {avg_fiber(wellness)} | {avg_price(wellness)} |",
        f"| Both signals | {len(both)} | {avg_score(both)} | {avg_fiber(both)} | {avg_price(both)} |",
        f"| Unclassified | {len(neither)} | {avg_score(neither)} | {avg_fiber(neither)} | {avg_price(neither)} |",
        f"",
        f"---",
        f"",
        f"## 2. Commodity Bread Analysis",
        f"",
        f"Products matching mass-market anchors ({len(commodity)} total):",
        f"",
    ]
    for r in sorted(commodity, key=lambda x: x.get("final_score") or 0, reverse=True):
        name  = (r.get("name_he") or "")[:40]
        s     = r.get("final_score")
        g     = r.get("final_grade","?")
        fiber = r["nutrition"].get("dietary_fiber_g")
        deg   = _deg_label(r["degradation_level"])
        p100  = r.get("price_per_100g")
        p_str = f" | {p100:.2f}₪/100g [{_price_tier_label(p100)}]" if p100 else ""
        f_str = f" | fiber={fiber:.1f}g" if fiber is not None else ""
        s_str = f"score={s:.0f} grade={g}" if s is not None else "score=—"
        lines.append(f"- **{name}** — {s_str} [{deg}]{f_str}{p_str}")

    lines += [
        f"",
        f"---",
        f"",
        f"## 3. Structural Questions Answered",
        f"",
        f"### Q1: Are commodity breads structurally coherent?",
        f"Commodity avg score: {avg_score(commodity)} | Wellness avg score: {avg_score(wellness)}",
        f"Conclusion: If scores are similar → wellness premium is a label effect, not structural.",
        f"",
        f"### Q2: Do wellness products actually have more fiber?",
        f"Commodity avg fiber: {avg_fiber(commodity)} | Wellness avg fiber: {avg_fiber(wellness)}",
        f"",
        f"### Q3: Price-score relationship in mass market vs wellness",
        f"Commodity avg price: {avg_price(commodity)} | Wellness avg price: {avg_price(wellness)}",
        f"If wellness is 2–3× more expensive with similar scores → the premium is marketing, not nutrition.",
        f"",
        f"### Q4: Fermentation in mainstream vs wellness",
    ]
    ferm_commodity = sum(1 for r in commodity if "מחמצת" in r.get("ingredients_text","").lower())
    ferm_wellness  = sum(1 for r in wellness  if "מחמצת" in r.get("ingredients_text","").lower())
    lines += [
        f"Genuine fermentation in commodity: {ferm_commodity}/{len(commodity)}",
        f"Genuine fermentation in wellness: {ferm_wellness}/{len(wellness)}",
        f"",
        f"### Q5: Fiber laundering in wellness segment",
        f"MATRIX_KW = inulin/chicory/psyllium signals",
    ]
    MATRIX_KW = ["אינולין","inulin","psyllium","ציקוריה","chicory","cellulose"]
    launder_wellness = [r for r in wellness if any(kw in r.get("ingredients_text","").lower() for kw in MATRIX_KW)]
    launder_commodity = [r for r in commodity if any(kw in r.get("ingredients_text","").lower() for kw in MATRIX_KW)]
    lines += [
        f"Fiber laundering in wellness: {len(launder_wellness)}/{len(wellness)}",
        f"Fiber laundering in commodity: {len(launder_commodity)}/{len(commodity)}",
        f"",
        f"*Generated by {RUN_ID}*",
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def _find_latest_raw() -> pathlib.Path | None:
    candidates = sorted(PRODUCT_DIR.glob("*_bsip0_raw.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def main() -> None:
    parser = argparse.ArgumentParser(description="BSIP2 batch runner — bread_retail_003")
    parser.add_argument("--raw", type=str, default=None, help="Path to raw BSIP0 JSON")
    args = parser.parse_args()

    if args.raw:
        raw_path = pathlib.Path(args.raw)
    else:
        raw_path = _find_latest_raw()
        if not raw_path:
            log.error("No raw JSON found in %s. Run acquisition_v3.py first.", PRODUCT_DIR)
            sys.exit(1)

    log.info("=== BSIP2 Real Bread Retail 003 ===")
    log.info("Source: %s", raw_path)

    raw_products = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raw_products))

    # Step 1 — exclusion filter
    in_scope, excluded_raw = [], []
    for raw in raw_products:
        name_he = (raw.get("name_he") or "").strip()
        excl, reason = _should_exclude(name_he)
        if excl:
            raw["_exclusion_reason"] = reason
            excluded_raw.append(raw)
        else:
            in_scope.append(raw)
    log.info("Excluded: %d | In scope: %d", len(excluded_raw), len(in_scope))

    # Step 2 — normalize to BSIP1
    bsip1_products = []
    for raw in in_scope:
        p = normalize_to_bsip1(raw)
        p["_load_errors"] = validate_product(p)
        bsip1_products.append(p)

    # Step 3 — run pipeline
    results, errors = [], []
    for product in bsip1_products:
        pid = product.get("canonical_product_id", "?")
        try:
            result = run_pipeline(product)
            results.append(result)
            deg   = _deg_label(result["degradation_level"])
            cat   = result["cat_result"].get("category", "?")
            score = result.get("final_score")
            s_str = f"{score:.0f}" if score is not None else "—"
            log.info("  %-40s cat=%-18s deg=%-12s score=%s",
                     (product.get("canonical_name_he") or "")[:40], cat, deg, s_str)
        except Exception as e:
            log.error("Pipeline error for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Pipeline complete: %d results, %d errors", len(results), len(errors))

    # Step 4 — save BSIP2 outputs
    for r in results:
        out = {
            "run_id":            RUN_ID,
            "product_id":        r["product_id"],
            "barcode":           r["barcode"],
            "name_he":           r["name_he"],
            "brand":             r.get("brand"),
            "source_retailers":  r.get("source_retailers"),
            "source_url":        r.get("source_url"),
            "image_urls":        r.get("image_urls", []),
            "final_score":       r.get("final_score"),
            "final_grade":       r.get("final_grade"),
            "degradation_level": r["degradation_level"],
            "confidence_label_he": _conf_label_he(r),
            "category":          r["cat_result"].get("category"),
            "nutrition":         r["nutrition"],
            "has_ingredients":   bool(r.get("ingredients_text")),
            "price_per_100g":    r.get("price_per_100g"),
            "weight_g":          r.get("weight_g"),
            "acquisition_tier":  r.get("acquisition_tier",""),
        }
        fname = f"bsip2_{r['product_id'] or 'unknown'}.json"
        (BSIP2_DIR / fname).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    if errors:
        (BSIP2_DIR / "pipeline_errors.json").write_text(
            json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")

    # Step 5 — reports
    RID = RUN_ID
    report_map = [
        (f"{RID}_bsip1_quality.md",          lambda: report_bsip1_quality(results, excluded_raw)),
        (f"{RID}_exclusion_report.md",         lambda: report_exclusion(excluded_raw)),
        (f"{RID}_batch_summary.md",            lambda: report_batch_summary(results)),
        (f"{RID}_score_distribution.md",       lambda: report_score_distribution(results)),
        (f"{RID}_routing_distribution.md",     lambda: report_routing_distribution(results)),
        (f"{RID}_fiber_laundering.md",         lambda: report_fiber_laundering(results)),
        (f"{RID}_seed_halo.md",                lambda: report_seed_halo(results)),
        (f"{RID}_fermentation_claims.md",      lambda: report_fermentation_claims(results)),
        (f"{RID}_deceptive_patterns.md",       lambda: report_deceptive_patterns(results)),
        (f"{RID}_top_coherent_products.md",    lambda: report_top_coherent(results)),
        (f"{RID}_website_handoff.md",          lambda: report_website_handoff(results, excluded_raw)),
        # New reports for 003
        (f"{RID}_market_structure.md",         lambda: report_market_structure(results)),
        (f"{RID}_mass_market_anchors.md",      lambda: report_mass_market_anchors(results)),
    ]

    for fname, fn in report_map:
        try:
            content = fn()
            path = REPORT_DIR / fname
            path.write_text(content, encoding="utf-8")
            log.info("Report: %s", path.name)
        except Exception as e:
            log.error("Failed %s: %s", fname, e)
            import traceback; traceback.print_exc()

    print(f"\nDone.")
    print(f"  In-scope products: {len(results)}")
    print(f"  Excluded: {len(excluded_raw)}")
    print(f"  Pipeline errors: {len(errors)}")
    print(f"  Reports: {REPORT_DIR}")
    print(f"  Raw source: {raw_path}")


if __name__ == "__main__":
    main()
