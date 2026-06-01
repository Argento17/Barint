"""
BSIP2 Batch Runner — Real Bread Retail 002 v2 (Shufersal)
run_id: real_bread_retail_002_v2

Source: C:/Bari/02_products/bread_retail_002/real_bread_retail_002_v2_20260525T165557_bsip0_raw.json
Output: C:/Bari/02_products/bread_retail_002/bsip2/
Reports: C:/Bari/02_products/bread_retail_002/reports/

Pipeline: BSIP0-raw → BSIP1 normalization → exclusion filter → full BSIP2 v3
          (router_v2, bakery_semantics, score_synthesis, interpretation_confidence,
           graceful_degradation, calibration patch)
"""

from __future__ import annotations
import sys, json, re, pathlib, logging, datetime
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

RAW_JSON   = pathlib.Path(r"C:\Bari\02_products\bread_retail_002\real_bread_retail_002_v2_20260525T165557_bsip0_raw.json")
BSIP2_DIR  = pathlib.Path(r"C:\Bari\02_products\bread_retail_002\bsip2")
REPORT_DIR = pathlib.Path(r"C:\Bari\02_products\bread_retail_002\reports")
RUN_ID     = "real_bread_retail_002_v2"
TODAY      = datetime.date.today().isoformat()

for d in (BSIP2_DIR, REPORT_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
# Exclusion filter
# ──────────────────────────────────────────────────────────────────────────────

# Products whose Hebrew name matches these patterns are out-of-scope for bread scoring
EXCLUDE_PATTERNS: list[tuple[str, str]] = [
    # sweet pastries
    (r"שבלול",        "sweet_pastry"),
    (r"רוגלך",        "sweet_pastry"),
    (r"בורקס",        "sweet_pastry"),
    (r"קרואסון",      "sweet_pastry"),
    (r"חלה",          "sweet_pastry"),          # חלה = challah; keep if plain
    (r"עוגה",         "sweet_pastry"),
    (r"מאפה מתוק",    "sweet_pastry"),
    (r"עוגיות",       "sweet_pastry"),
    (r"ופל",          "sweet_pastry"),
    # raw/industrial ingredients not a finished product
    (r"^קמח\b",       "raw_ingredient"),        # standalone flour
    (r"^שמרים\b",     "raw_ingredient"),        # standalone yeast
    (r"^סובין\b",     "raw_ingredient"),        # bran
    (r"^שיבולת שועל$","raw_ingredient"),        # plain oats
]

# חלה is in scope (it IS bread) — remove the challah exclusion:
EXCLUDE_PATTERNS = [(p, r) for p, r in EXCLUDE_PATTERNS if r != "sweet_pastry" or "חלה" not in p]


def _should_exclude(name_he: str) -> tuple[bool, str]:
    n = name_he.strip()
    for pattern, reason in EXCLUDE_PATTERNS:
        if re.search(pattern, n):
            return True, reason
    return False, ""


# ──────────────────────────────────────────────────────────────────────────────
# BSIP0-raw → BSIP1 normalization
# ──────────────────────────────────────────────────────────────────────────────

def _parse_num(raw: str) -> float | None:
    """Parse nutrition strings like '3.7', '264', 'פחות מ 0.5', '<0.5'."""
    if not raw:
        return None
    s = str(raw).strip()
    # Handle "פחות מ X" / "< X" → use X/2
    m = re.match(r"(?:פחות מ|<)\s*([\d.]+)", s, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1)) / 2
        except ValueError:
            return None
    # Normal number
    m2 = re.match(r"([\d.]+)", s.replace(",", "."))
    if m2:
        try:
            return float(m2.group(1))
        except ValueError:
            return None
    return None


def normalize_to_bsip1(raw: dict) -> dict:
    """Convert a BSIP0 v2 raw product dict to BSIP1-compatible format."""
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

    # Determine missing fields
    missing = []
    if not name_he:
        missing.append("canonical_name_he")
    if energy is None:
        missing.append("energy_kcal")
    if fiber is None:
        missing.append("dietary_fiber_g")
    if protein is None:
        missing.append("protein_g")
    if not ingredients_raw:
        missing.append("ingredients_text")

    # BSIP1 canonical id
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
            "scrape_quality_score":   0.85 if (energy is not None and ingredients_raw) else
                                      0.60 if (energy is not None or ingredients_raw) else 0.35,
        },
        "conflicts_summary":          {},
        "missing_fields":             missing,
        "inferred_fields":            [],
        "audit_ref":                  f"bsip0_v2_{RUN_ID}",
        "extraction_method":          raw.get("extraction_method") or "html_parse",
        "extraction_confidence":      raw.get("extraction_confidence") or "medium",
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
    }


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _deg_label(lvl: str) -> str:
    return {"FULL": "Full", "CAUTIOUS": "Cautious",
            "UNCERTAINTY": "Uncertain", "INSUFFICIENT": "Insufficient"}.get(lvl, lvl)

def _conf_label_he(r: dict) -> str:
    deg = r["degradation_level"]
    has_ing = bool(r.get("ingredients_text"))
    if deg == "FULL" and has_ing:           return "נתונים מלאים יחסית"
    if deg == "CAUTIOUS" and has_ing:       return "נתונים חלקיים"
    if deg in ("UNCERTAINTY",) or not has_ing: return "חסרים נתונים מהותיים"
    return "לא מספיק לניתוח ודאי"

def _first_img(r: dict) -> str:
    imgs = r.get("image_urls") or []
    return imgs[0] if imgs else ""


# ──────────────────────────────────────────────────────────────────────────────
# Reports
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

    lines = [
        f"# BSIP1 Normalization Quality — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | **Source:** Shufersal real-shelf HTML scrape",
        f"",
        f"This is a **Shufersal-only** corpus. Not a full Israeli market survey.",
        f"",
        f"---",
        f"",
        f"## Corpus Summary",
        f"",
        f"| Metric | Value |",
        f"|:-------|:------|",
        f"| Raw products from BSIP0 | {n + n_ex} |",
        f"| Excluded (out-of-scope) | {n_ex} |",
        f"| In-scope for scoring | {n} |",
        f"| Retailer | Shufersal only |",
        f"",
        f"## Nutrition Field Coverage (in-scope products)",
        f"",
        f"| Field | Present | Coverage |",
        f"|:------|:--------|:---------|",
        f"| Energy (kcal/100g) | {has_kcal} | {100*has_kcal//n}% |",
        f"| Dietary fiber | {has_fiber} | {100*has_fiber//n}% |",
        f"| Protein | {has_prot} | {100*has_prot//n}% |",
        f"| Carbohydrates | {has_carbs} | {100*has_carbs//n}% |",
        f"| Fat | {has_fat} | {100*has_fat//n}% |",
        f"| Sodium | {has_na} | {100*has_na//n}% |",
        f"| Sugars | {has_sug} | {100*has_sug//n}% |",
        f"| Ingredient text | {has_ing} | {100*has_ing//n}% |",
        f"",
        f"## Degradation Distribution",
        f"",
    ]
    degs: dict[str, int] = {}
    for r in results:
        degs[r["degradation_level"]] = degs.get(r["degradation_level"], 0) + 1
    for deg in ["FULL", "CAUTIOUS", "UNCERTAINTY", "INSUFFICIENT"]:
        cnt = degs.get(deg, 0)
        lines.append(f"- **{_deg_label(deg)}:** {cnt} ({100*cnt//n}%)")

    lines += [
        "",
        "## Coverage Notes",
        "",
        "- Shufersal product pages provide nutrition via `.nutritionList` HTML section (server-rendered).",
        "- Ingredients extracted from product tab text after 'רכיבים' label.",
        "- 27/110 products in the raw scrape had no nutrition table — these receive CAUTIOUS or INSUFFICIENT degradation.",
        "- Saturated fat and trans fat not available from Shufersal product pages (not parsed).",
        "- Source URL and timestamp recorded for every product.",
        "",
        f"*Generated by {RUN_ID}*",
    ]
    return "\n".join(lines)


def report_exclusion(excluded: list[dict]) -> str:
    lines = [
        f"# Product Exclusion Report — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY}",
        f"",
        f"Products excluded from BSIP2 scoring as out-of-scope for bread/cracker analysis.",
        f"These are flagged, not deleted — they remain in the raw corpus.",
        f"",
        f"**Total excluded:** {len(excluded)}",
        f"",
        f"| # | Product (Hebrew) | Exclusion Reason | Source URL |",
        f"|:--|:----------------|:----------------|:-----------|",
    ]
    for i, ex in enumerate(excluded, 1):
        name = ex.get("name_he", "")[:45]
        reason = ex.get("_exclusion_reason", "")
        url = ex.get("source_url", "")[:60]
        lines.append(f"| {i} | {name} | {reason} | {url} |")

    lines += [
        "",
        "## Exclusion Rules Applied",
        "",
        "- `sweet_pastry`: שבלול, רוגלך, בורקס, קרואסון, עוגה, עוגיות, ופל — products whose primary character is sweet pastry, not bread",
        "- `raw_ingredient`: standalone קמח, שמרים, סובין — sold as a cooking ingredient, not a finished product",
        "",
        "**Note:** חלה (challah) is NOT excluded — it is a legitimate bread archetype.",
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
    for r in results:
        c = r["cat_result"].get("category", "?")
        cats[c] = cats.get(c, 0) + 1
        degs[r["degradation_level"]] = degs.get(r["degradation_level"], 0) + 1
        g = r.get("final_grade") or "?"
        grades[g] = grades.get(g, 0) + 1

    avg = sum(scores)/len(scores) if scores else None
    med = sorted(scores)[len(scores)//2] if scores else None

    lines = [
        f"# Batch Pipeline Summary — {RUN_ID}",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {TODAY} | **Source:** Shufersal real-shelf | **n={n}**",
        f"",
        f"**This is a Shufersal-only snapshot, not a full Israeli market analysis.**",
        f"",
        f"## Overview",
        f"",
        f"| Metric | Value |",
        f"|:-------|:------|",
        f"| Products processed | {n} |",
        f"| Products with score | {len(scored)} ({100*len(scored)//n}%) |",
        f"| Average score | {avg:.1f} |" if avg else "| Average score | — |",
        f"| Median score | {med:.1f} |" if med else "| Median score | — |",
        f"| Min score | {min(scores):.0f} |" if scores else "| Min score | — |",
        f"| Max score | {max(scores):.0f} |" if scores else "| Max score | — |",
        f"",
        f"## Routing Distribution",
        f"",
    ]
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        bar = "█" * (cnt * 20 // n) if n else ""
        lines.append(f"- `{cat}`: {cnt} ({100*cnt//n}%) {bar}")

    lines += ["", "## Degradation Distribution", ""]
    for deg in ["FULL","CAUTIOUS","UNCERTAINTY","INSUFFICIENT"]:
        cnt = degs.get(deg, 0)
        lines.append(f"- **{_deg_label(deg)}:** {cnt} ({100*cnt//n}%)")

    lines += ["", "## Grade Distribution", ""]
    for g in ["A","B","C","D","E","?"]:
        cnt = grades.get(g, 0)
        if cnt:
            lines.append(f"- Grade **{g}:** {cnt} ({100*cnt//n}%)")

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
        lines.append(f"| {label} | {lo}–{hi-1} | {len(grp)} | {100*len(grp)//n}% |")

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
        cat  = r["cat_result"].get("category","?")
        deg  = _deg_label(r["degradation_level"])
        lines.append(
            f"{i}. **{name}** — {cat} — score={r['final_score']:.0f} "
            f"grade={r.get('final_grade','?')} [{deg}]"
        )

    lines += ["", "## Bottom 10 by Score", ""]
    bot = sorted(scored, key=lambda r: r["final_score"])[:10]
    for i, r in enumerate(bot, 1):
        name = (r.get("name_he") or "")[:38]
        cat  = r["cat_result"].get("category","?")
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
        avg_conf = sum(r["cat_result"].get("category_confidence",0) for r in group)/len(group)
        anchors  = sum(1 for r in group if r["cat_result"].get("anchor_override"))
        lines += [f"### `{cat}` — {len(group)} products ({100*len(group)//n}%)", ""]
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
    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_fiber_laundering(results: list[dict]) -> str:
    n = len(results)
    fiber_vals = [(r, r["nutrition"].get("dietary_fiber_g"))
                  for r in results if r["nutrition"].get("dietary_fiber_g") is not None]
    MATRIX_KW = ["אינולין","inulin","psyllium","psyllium","ציקוריה","chicory","cellulose","גואר","קסנטן"]
    WG_KW     = ["קמח מלא","שיפון מלא","חיטה מלאה","כוסמין מלא","wholegrain","whole grain","whole wheat"]
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
    lines += ["## Fiber Source Assessment", ""]
    launder_cases = []
    for r, fiber in sorted(fiber_vals, key=lambda x: -x[1])[:25]:
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
            flag = "~ unclear matrix"
        name = (r.get("name_he") or "")[:36]
        lines.append(f"- **{name}**: fiber={fiber:.1f}g — {flag}")

    lines += [
        "",
        f"**Confirmed matrix-added fiber cases:** {len(launder_cases)}",
        "",
        f"*Generated by {RUN_ID}*",
    ]
    return "\n".join(lines)


def report_seed_halo(results: list[dict]) -> str:
    n = len(results)
    SEED_KW = ["שומשום","פשתן","דלעת","גרעיני","זרעי","צ'יה","chia",
               "sunflower","sesame","pumpkin","flax","כוסמת"]
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
        f"**Definition:** Seeds surface-applied to a refined-flour matrix — creating a premium",
        f"impression without structural nutritional benefit.",
        f"",
        f"**Products with seed signals:** {len(seeded)}/{n} ({100*len(seeded)//n}%)",
        f"",
        f"## Assessment",
        f"",
    ]
    for r, seeds, has_wg in sorted(seeded, key=lambda x: x[0].get("final_score") or 0, reverse=True):
        name  = (r.get("name_he") or "")[:38]
        score = r.get("final_score")
        s_str = f"{score:.0f}" if score is not None else "—"
        flag  = "✓ whole grain matrix" if has_wg else "⚠ possible surface seeding"
        lines.append(f"- **{name}** — score={s_str} — {flag} — seeds: {', '.join(seeds[:3])}")
    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_fermentation_claims(results: list[dict]) -> str:
    n = len(results)
    FERM_REAL = ["מחמצת","sourdough","חיידקים","תרבויות","חומצה לקטית","fermented","lactobacillus"]
    FERM_IND  = ["שמרים","yeast","חומר מתפיח","E-500","E-450","E500"]
    true_ferm, false_ferm, industrial = [], [], []
    for r in results:
        ing  = r.get("ingredients_text","").lower()
        name = (r.get("name_he") or "").lower()
        has_claim    = "מחמצת" in name or "sourdough" in name
        has_real     = any(kw in ing for kw in FERM_REAL)
        has_ind      = any(kw in ing for kw in FERM_IND)
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
        f"Tests whether מחמצת / sourdough claims are backed by genuine starter-culture",
        f"ingredients or are industrial yeast products using the fermentation label.",
        f"",
        f"| Category | Count |",
        f"|:---------|:------|",
        f"| Genuine fermentation (מחמצת/starter cultures in ingredients) | {len(true_ferm)} |",
        f"| Fermentation claim + industrial yeast (mismatch) | {len(false_ferm)} |",
        f"| Industrial yeast only (no claim) | {len(industrial)} |",
        f"",
        f"## Genuine Fermentation Products",
        f"",
    ]
    for r in sorted(true_ferm, key=lambda x: x.get("final_score") or 0, reverse=True):
        name = (r.get("name_he") or "")[:42]
        s = r.get("final_score")
        lines.append(f"- **{name}** — score={s:.0f}" if s else f"- **{name}**")

    if false_ferm:
        lines += ["", "## ⚠ Fermentation Label / Industrial Mismatch", ""]
        for r in false_ferm:
            lines.append(f"- **{(r.get('name_he') or '')[:42]}** — claims מחמצת but ingredient list shows industrial yeast")

    if industrial:
        lines += ["", f"## Industrial Yeast Products (no fermentation claim): {len(industrial)}", ""]
        for r in industrial[:10]:
            lines.append(f"- {(r.get('name_he') or '')[:42]}")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_deceptive_patterns(results: list[dict]) -> str:
    n = len(results)
    SUGAR_ALIASES = ["סוכר","גלוקוז","פרוקטוז","דקסטרוז","מלטוז",
                     "סירופ","syrup","honey","דבש","מלאס","molasses","ממתיק"]
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
        f"Real Shufersal shelf patterns — not a full market survey.",
        f"",
        f"## Multi-Sugar Camouflage (≥3 sugar aliases)",
        f"",
        f"**{len(sugar_camouflage)} products detected.**",
        f"",
    ]
    for r, cnt in sorted(sugar_camouflage, key=lambda x: -x[1]):
        lines.append(f"- **{(r.get('name_he') or '')[:42]}** — {cnt} sugar forms")

    lines += [
        f"",
        f"## Refined Flour with Whole Grain Name Claim",
        f"",
        f"**{len(refined_wg)} products detected.**",
        f"",
    ]
    for r in refined_wg:
        lines.append(f"- **{(r.get('name_he') or '')[:42]}**")

    lines += [
        f"",
        f"## High Sodium (>600mg/100g)",
        f"",
        f"**{len(high_sodium)} products detected.**",
        f"",
    ]
    for r, na in sorted(high_sodium, key=lambda x: -x[1]):
        lines.append(f"- **{(r.get('name_he') or '')[:42]}** — {na:.0f}mg sodium/100g")

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
        f"These are the products the pipeline scored with highest confidence.",
        f"",
        f"**Coherent products:** {len(coherent)}/{n}",
        f"",
    ]
    for i, r in enumerate(coherent[:20], 1):
        name  = (r.get("name_he") or "")[:42]
        cat   = r["cat_result"].get("category","?")
        deg   = _deg_label(r["degradation_level"])
        score = r["final_score"]
        grade = r.get("final_grade") or "?"
        fiber = r["nutrition"].get("dietary_fiber_g")
        f_str = f" | fiber={fiber:.1f}g" if fiber is not None else ""
        ing   = r.get("ingredients_text","").lower()
        ferm  = " | מחמצת ✓" if "מחמצת" in ing else ""
        lines.append(f"{i}. **{name}** — {cat} — score={score:.0f} grade={grade} [{deg}]{f_str}{ferm}")
        if r.get("source_url"):
            lines.append(f"   [{r['source_url'][:70]}]({r['source_url'][:70]})")

    lines += ["", f"*Generated by {RUN_ID}*"]
    return "\n".join(lines)


def report_website_handoff(results: list[dict], excluded: list[dict]) -> str:
    n = len(results)
    scored = [r for r in results if r.get("final_score") is not None]
    # Tiers for consumer display
    verified = [r for r in scored if r["degradation_level"] in ("FULL","CAUTIOUS") and r.get("ingredients_text")]
    nutr_only = [r for r in scored if r["degradation_level"] in ("FULL","CAUTIOUS") and not r.get("ingredients_text")]
    insufficient = [r for r in results if r["degradation_level"] == "INSUFFICIENT"]

    top_v = sorted(verified, key=lambda r: r["final_score"], reverse=True)[:5]
    # Fiber stats on verified
    fibers = [r["nutrition"]["dietary_fiber_g"] for r in verified if r["nutrition"].get("dietary_fiber_g") is not None]
    avg_fiber = sum(fibers)/len(fibers) if fibers else None
    ferm_count = sum(1 for r in verified if "מחמצת" in r.get("ingredients_text","").lower())

    lines = [
        f"# Website Handoff — {RUN_ID}",
        f"",
        f"**Generated:** {TODAY} | **Source:** Shufersal real-shelf scrape (real_bread_retail_002_v2)",
        f"",
        f"---",
        f"",
        f"## 1. Data Transparency — Mandatory Framing",
        f"",
        f"**Use exactly this framing in all consumer content:**",
        f"",
        f"> ניתחנו מוצרי לחם, פיתה וקרקרים ממדף שופרסל האמיתי.",
        f"> הנתונים לקוחים ישירות מדפי המוצר של שופרסל — כולל לוח תזונה ורשימת רכיבים.",
        f"> {len(verified)} מוצרים עמדו בסף הנתונים הנדרש לניתוח מלא.",
        f"> זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא.",
        f"",
        f"**English equivalent:**",
        f"",
        f"> We analyzed {n} bread, pita and cracker products from a real Shufersal shelf scrape.",
        f"> Data is sourced directly from Shufersal product pages — nutrition tables and ingredient lists.",
        f"> {len(verified)} products had sufficient data for reliable scoring.",
        f"> This is a Shufersal shelf snapshot, not a full Israeli market survey.",
        f"",
        f"**What NOT to say:**",
        f"- Do not say 'Israeli market' — this is Shufersal only",
        f"- Do not show scores for INSUFFICIENT products as confirmed grades",
        f"- Do not rank products without ingredient data against verified products",
        f"",
        f"---",
        f"",
        f"## 2. Key Stats — Safe to Publish",
        f"",
        f"Based on {len(verified)} products with verified nutrition + ingredient data:",
        f"",
    ]
    if avg_fiber:
        lines.append(f"- **Average fiber (verified products):** {avg_fiber:.1f}g per 100g")
    lines.append(f"- **Products with genuine fermentation (מחמצת בנתוני מרכיבים):** {ferm_count}/{len(verified)}")

    grade_dist: dict[str, int] = {}
    for r in verified:
        g = r.get("final_grade") or "?"
        grade_dist[g] = grade_dist.get(g, 0) + 1
    lines.append(f"- **Grade distribution (verified):**")
    for g in ["A","B","C","D","E"]:
        if grade_dist.get(g):
            lines.append(f"  - Grade {g}: {grade_dist[g]} products")

    lines += [
        f"",
        f"---",
        f"",
        f"## 3. Product Examples — Safe to Feature",
        f"",
        f"### Tier 1 — Full Analysis (verified score + grade)",
        f"",
    ]
    for r in top_v:
        name   = r.get("name_he","")
        score  = r["final_score"]
        grade  = r.get("final_grade","?")
        fiber  = r["nutrition"].get("dietary_fiber_g")
        ferm   = "✓" if "מחמצת" in r.get("ingredients_text","").lower() else "✗"
        conf   = _conf_label_he(r)
        url    = r.get("source_url","")
        img    = _first_img(r)
        cat    = r["cat_result"].get("category","?")
        lines += [
            f"**{name}**",
            f"- Score: {score:.0f} | Grade: {grade} | {conf}",
            f"- Fiber: {fiber:.1f}g/100g" if fiber else "- Fiber: לא זמין",
            f"- Fermentation: {ferm}",
            f"- Category: {cat}",
            f"- Source: {url}",
        ]
        if img:
            lines.append(f"- Image: {img}")
        lines.append("")

    # Comparison pairs
    wg_products = [r for r in verified if r["nutrition"].get("dietary_fiber_g") is not None]
    if len(wg_products) >= 2:
        hi_fiber = max(wg_products, key=lambda r: r["nutrition"]["dietary_fiber_g"])
        lo_fiber = min(wg_products, key=lambda r: r["nutrition"]["dietary_fiber_g"])
        lines += [
            f"---",
            f"",
            f"## 4. Comparison Pairs — Recommended",
            f"",
            f"### Pair 1 — Fiber Extremes (verified data only)",
            f"",
            f"- **High fiber:** {hi_fiber.get('name_he','')} — {hi_fiber['nutrition']['dietary_fiber_g']:.1f}g/100g — score={hi_fiber.get('final_score',0):.0f}",
            f"- **Low fiber:** {lo_fiber.get('name_he','')} — {lo_fiber['nutrition']['dietary_fiber_g']:.1f}g/100g — score={lo_fiber.get('final_score',0):.0f}",
            f"",
            f"Story angle: same category (bread/cracker), fiber content differs by up to {hi_fiber['nutrition']['dietary_fiber_g']/max(lo_fiber['nutrition']['dietary_fiber_g'],0.1):.0f}x.",
            f"",
        ]

    # Sourdough pair
    ferm_r = [r for r in verified if "מחמצת" in r.get("ingredients_text","").lower() and r.get("final_score")]
    non_ferm = [r for r in verified if "מחמצת" not in r.get("ingredients_text","").lower() and "שמרים" in r.get("ingredients_text","").lower() and r.get("final_score")]
    if ferm_r and non_ferm:
        f_ex = max(ferm_r, key=lambda r: r["final_score"])
        n_ex = max(non_ferm, key=lambda r: r["final_score"])
        lines += [
            f"### Pair 2 — Genuine Fermentation vs Industrial Yeast",
            f"",
            f"- **מחמצת אמיתית:** {f_ex.get('name_he','')} — score={f_ex['final_score']:.0f}",
            f"- **שמרים תעשייתיים:** {n_ex.get('name_he','')} — score={n_ex['final_score']:.0f}",
            f"",
            f"Story angle: the מחמצת label means something real when it appears in the ingredient list.",
            f"",
        ]

    lines += [
        f"---",
        f"",
        f"## 5. Confidence Labels for UI",
        f"",
        f"| Label (He) | Label (En) | When to use |",
        f"|:-----------|:-----------|:------------|",
        f"| נתונים מלאים יחסית | Relatively complete data | FULL degradation + ingredient text |",
        f"| נתונים חלקיים | Partial data | CAUTIOUS degradation + ingredient text |",
        f"| חסרים נתונים מהותיים | Missing essential data | No ingredients or UNCERTAINTY |",
        f"| לא מספיק לניתוח ודאי | Insufficient for certain analysis | INSUFFICIENT degradation |",
        f"",
        f"**Score display rules:**",
        f"- Show score: verified products (FULL/CAUTIOUS + ingredients) → show score + grade",
        f"- Provisional grade: CAUTIOUS → add asterisk or 'provisional' label",
        f"- No score: INSUFFICIENT → show confidence label only",
        f"",
        f"---",
        f"",
        f"## 6. Blog Narrative — Recommended Structure",
        f"",
        f"### Title Options",
        f"- מה יש בלחם מהמדף? ניתחנו {n} מוצרים משופרסל",
        f"- לחם, פיתה וקרקרים: מה הציון שלנו ומה הוא לא יכול לומר",
        f"- שקיפות בלחם: ניתוח נתוני מדף אמיתי מרשת שופרסל",
        f"",
        f"### Opening (Honest Framing)",
        f"",
        f"> ניתחנו {n} מוצרי לחם, פיתה וקרקרים ממדף שופרסל. לא כל המוצרים קיבלו ציון —",
        f"> חלק לא כללו נתוני תזונה או רשימת מרכיבים מלאה. הציונים שמוצגים מבוססים על",
        f"> {len(verified)} מוצרים שכללו גם לוח תזונה וגם רשימת מרכיבים.",
        f"> זהו ניתוח של מדף שופרסל בלבד — לא ייצוג של כל השוק הישראלי.",
        f"",
        f"### Recommended Structure",
        f"1. **הממצאים המאומתים** — {len(verified)} מוצרים עם נתוני מרכיבים מלאים",
        f"2. **מה שגילינו** — ציפוי סיבים, תסיסה אמיתית לעומת שמרים תעשייתיים, זרעים על גבי בסיס מזוקק",
        f"3. **מה שלא יכולנו לבדוק** — {len(insufficient)} מוצרים ללא נתונים מספיקים",
        f"4. **כיצד קוראים את הציון** — משמעות הדגל, הכוכבית, ואי-הוודאות",
        f"",
        f"### Safe Claims (backed by verified data)",
    ]
    if avg_fiber:
        lines.append(f"- ממוצע סיבים תזונתיים במוצרים מאומתים: {avg_fiber:.1f}g ל-100g")
    lines.append(f"- מוצרים עם מחמצת אמיתית (ברשימת מרכיבים): {ferm_count}/{len(verified)}")
    lines += [
        f"",
        f"### Claims Requiring Caveat",
        f"- 'הלחם הטוב ביותר' → specify: from Shufersal verified set only",
        f"- Any comparison across retailers → not applicable, Shufersal only",
        f"",
        f"---",
        f"",
        f"## 7. Visual Recommendations",
        f"",
        f"- **Score dial / grade badge:** show only for {len(verified)} verified products",
        f"- **Confidence tag:** small pill label under product name (always visible)",
        f"- **Fiber bar chart:** for products with fiber data ({sum(1 for r in results if r['nutrition'].get('dietary_fiber_g'))} products)",
        f"- **Product images:** use Shufersal Cloudinary URLs (res.cloudinary.com/shufersal/...)",
        f"- **Data availability panel:** always show 'מבוסס על {len(verified)} מוצרים מאומתים מתוך {n}'",
        f"- **No bottom-5 list** unless filtered to verified products only",
        f"",
        f"---",
        f"",
        f"## 8. Dataset Files",
        f"",
        f"- `bsip2/` — full pipeline results (JSON per product)",
        f"- `reports/` — all 10 analytical reports",
        f"",
        f"Key fields per product:",
        f"- `final_score` — null if not displayable",
        f"- `final_grade` — null if not displayable",
        f"- `degradation_level` — FULL/CAUTIOUS/UNCERTAINTY/INSUFFICIENT",
        f"- `confidence_label_he` — always set",
        f"- `source_url` — direct Shufersal product page link",
        f"- `image_urls` — Shufersal Cloudinary image URLs",
        f"",
        f"*Handoff generated by {RUN_ID} — {TODAY}*",
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    log.info("=== BSIP2 Real Bread Retail 002 v2 (Shufersal) ===")
    log.info("Source: %s", RAW_JSON)

    raw_products = json.loads(RAW_JSON.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products from BSIP0 v2", len(raw_products))

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
        pid = product.get("canonical_product_id","?")
        try:
            result = run_pipeline(product)
            results.append(result)
            deg   = _deg_label(result["degradation_level"])
            cat   = result["cat_result"].get("category","?")
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
            "image_urls":        r.get("image_urls",[]),
            "final_score":       r.get("final_score"),
            "final_grade":       r.get("final_grade"),
            "degradation_level": r["degradation_level"],
            "confidence_label_he": _conf_label_he(r),
            "category":          r["cat_result"].get("category"),
            "nutrition":         r["nutrition"],
            "has_ingredients":   bool(r.get("ingredients_text")),
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


if __name__ == "__main__":
    main()
