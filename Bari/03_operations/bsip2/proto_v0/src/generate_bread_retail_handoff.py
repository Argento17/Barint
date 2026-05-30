"""
BSIP2 Real Bread Retail — Website Handoff Generator
run_id: real_bread_retail_001

Addresses all 7 pre-handoff issues:
  1. Separate real analysis from data availability
  2. Export clean JSON/CSV for Cursor
  3. Add Hebrew confidence labels for UI
  4. Fix score report: internal score ≠ consumer-visible score
  5. Remove data-gap products from consumer examples
  6. Build verified / plausible / gap tiers
  7. Generate real_bread_retail_website_handoff.md

Consumer visibility rules:
  FULL + has_ingredients     → נתונים מלאים יחסית  — show score + grade
  CAUTIOUS + has_ingredients → נתונים חלקיים       — show score + provisional grade
  FULL/CAUTIOUS + no_ing     → חסרים נתונים מהותיים — nutrition only, no score
  UNCERTAINTY any            → חסרים נתונים מהותיים — no score
  INSUFFICIENT any           → לא מספיק לניתוח ודאי — no score, data-gap note
"""

from __future__ import annotations
import sys, json, csv, pathlib, logging, datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

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

BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\bread_retail\bsip1")
REPORT_DIR = pathlib.Path(r"C:\Bari\02_products\bread_retail\reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TODAY  = datetime.date.today().isoformat()
RUN_ID = "real_bread_retail_001"

# ---------------------------------------------------------------------------
# Consumer visibility tiers
# ---------------------------------------------------------------------------
def _has_he_text(text: str) -> bool:
    return bool(text) and any('א' <= c <= 'ת' for c in text)

def _confidence_label(degradation: str, has_ingredients: bool) -> tuple[str, str]:
    """Returns (label_he, label_en)"""
    if degradation == "FULL" and has_ingredients:
        return ("נתונים מלאים יחסית", "Relatively complete data")
    if degradation == "CAUTIOUS" and has_ingredients:
        return ("נתונים חלקיים", "Partial data")
    if degradation in ("FULL", "CAUTIOUS") and not has_ingredients:
        return ("חסרים נתונים מהותיים", "Missing essential data")
    if degradation == "UNCERTAINTY":
        return ("חסרים נתונים מהותיים", "Missing essential data")
    return ("לא מספיק לניתוח ודאי", "Insufficient for certain analysis")

def _consumer_score_visible(degradation: str, has_ingredients: bool) -> bool:
    return degradation in ("FULL", "CAUTIOUS") and has_ingredients

def _consumer_grade_visible(degradation: str, has_ingredients: bool) -> bool:
    return degradation == "FULL" and has_ingredients

def _consumer_grade_provisional(degradation: str, has_ingredients: bool) -> bool:
    return degradation == "CAUTIOUS" and has_ingredients

def _tier(degradation: str, has_ingredients: bool) -> str:
    if _consumer_score_visible(degradation, has_ingredients):
        return "verified"
    if degradation in ("FULL", "CAUTIOUS"):
        return "nutrition_only"
    if degradation == "UNCERTAINTY":
        return "uncertain"
    return "data_gap"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def _run_pipeline(product: dict) -> dict:
    prod = {k: v for k, v in product.items() if not k.startswith("_")}

    signals      = extract_signals(prod)
    cat_result   = classify_category(prod)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(prod, l3)
    eval_result  = assign_evaluation_scope(prod, cat_result["category"])
    score_result = score_product(prod, signals, cat_result, nova_result, eval_result)

    base_conf    = compute_confidence(prod, signals, cat_result, nova_result)
    interp_conf  = compute_interpretation_confidence(base_conf, cat_result, prod, signals)
    score_result = apply_confidence_ceiling(score_result, interp_conf)

    bakery_result = run_bakery_semantics(prod, cat_result["category"], l3)
    trace         = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
    trace["bakery_semantics"] = bakery_result
    trace["structural_class"] = classify_structural_class(trace, bakery_result)
    synth_result  = run_synthesis(trace)

    final_score = synth_result.get("synthesis_score") or score_result.get("final_score_estimate")
    final_grade = score_to_grade(final_score) if final_score is not None else None

    failures         = classify_failures(prod, signals, cat_result, nova_result, score_result, interp_conf)
    degradation_level = determine_degradation_level(interp_conf, score_result, failures)
    degraded_output   = build_degraded_output(prod, score_result, cat_result, interp_conf, failures, degradation_level)

    nn  = prod.get("normalized_nutrition_per_100g") or {}
    ing = prod.get("ingredients_text_he") or prod.get("ingredients_raw") or ""
    has_ing = bool(ing.strip())
    has_he  = _has_he_text(ing)

    confidence_label_he, confidence_label_en = _confidence_label(degradation_level, has_ing)
    tier = _tier(degradation_level, has_ing)

    # Semantic flags
    ing_lower = ing.lower()
    name_lower = (prod.get("canonical_name_he") or "").lower()
    ferm_kw = ["מחמצת", "sourdough", "חיידקים", "תרבויות", "חומצה לקטית", "fermented"]
    seed_kw = ["שומשום", "פשתן", "גרעיני", "זרעי", "צ'יה", "chia", "sesame", "flax", "poppy"]
    fiber_matrix_kw = ["אינולין", "inulin", "psyllium", "ציקוריה", "chicory", "סיבי תאית", "cellulose"]
    wg_kw = ["קמח מלא", "שיפון מלא", "חיטה מלאה", "wholegrain", "whole grain", "whole wheat", "whole rye"]

    fermentation_flag = any(k in ing_lower or k in name_lower for k in ferm_kw)
    seed_signal       = any(k in ing_lower or k in name_lower for k in seed_kw)
    fiber_matrix      = any(k in ing_lower for k in fiber_matrix_kw)
    whole_grain       = any(k in ing_lower for k in wg_kw)
    fiber_laundering  = fiber_matrix and not whole_grain and (nn.get("dietary_fiber_g") or 0) >= 6

    # Ingredient count
    import re
    ing_count = len([p for p in re.split(r"[,;،]", ing) if p.strip()]) if ing else 0

    # Consumer-facing score/grade
    score_visible  = _consumer_score_visible(degradation_level, has_ing)
    grade_visible  = _consumer_grade_visible(degradation_level, has_ing)
    grade_prov     = _consumer_grade_provisional(degradation_level, has_ing)

    return {
        # Identity
        "product_id":        product.get("canonical_product_id"),
        "barcode":           product.get("barcode"),
        "name_he":           product.get("canonical_name_he") or "",
        "brand":             product.get("brand") or "",
        "source_url":        product.get("source_url") or "",
        "source_retailers":  product.get("source_retailers") or [],

        # Routing
        "category":          cat_result.get("category"),
        "category_confidence": round(cat_result.get("category_confidence", 0), 2),
        "anchor_override":   cat_result.get("anchor_override", False),

        # Internal pipeline scores (not all consumer-visible)
        "internal_score":    round(final_score, 1) if final_score is not None else None,
        "internal_grade":    final_grade,
        "degradation_level": degradation_level,
        "confidence_band":   interp_conf.get("interpretation_confidence_band"),
        "confidence_score":  interp_conf.get("interpretation_confidence_score"),

        # Consumer-visible output
        "consumer_score_visible":  score_visible,
        "consumer_grade_visible":  grade_visible,
        "consumer_grade_provisional": grade_prov,
        "consumer_score":    round(final_score, 1) if score_visible and final_score else None,
        "consumer_grade":    final_grade if (grade_visible or grade_prov) else None,
        "confidence_label_he": confidence_label_he,
        "confidence_label_en": confidence_label_en,
        "tier":              tier,

        # Nutrition (per 100g)
        "kcal_100g":         nn.get("energy_kcal"),
        "fat_g":             nn.get("fat_g"),
        "fat_saturated_g":   nn.get("fat_saturated_g"),
        "carbohydrates_g":   nn.get("carbohydrates_g"),
        "sugars_g":          nn.get("sugars_g"),
        "fiber_g":           nn.get("dietary_fiber_g"),
        "protein_g":         nn.get("protein_g"),
        "sodium_mg":         nn.get("sodium_mg"),

        # Ingredient data
        "has_ingredient_text": has_ing,
        "has_hebrew_ingredients": has_he,
        "ingredient_count":  ing_count,
        "ingredients_text_he": ing if has_ing else "",

        # Semantic flags
        "fermentation_flag":  fermentation_flag,
        "seed_signal":        seed_signal,
        "fiber_laundering_flag": fiber_laundering,
        "whole_grain_flag":   whole_grain,

        # Deductions from calibration patch
        "calibration_deductions": [
            r.get("factor", "") for r in interp_conf.get("additional_reductions", [])
        ],
        "interpretation_cautions": interp_conf.get("interpretation_cautions", []),
    }


# ---------------------------------------------------------------------------
# Website dataset export (JSON + CSV)
# ---------------------------------------------------------------------------
_CSV_FIELDS = [
    "product_id", "barcode", "name_he", "brand", "source_url",
    "category", "category_confidence", "tier",
    "consumer_score", "consumer_grade", "consumer_grade_provisional",
    "consumer_score_visible", "consumer_grade_visible",
    "confidence_label_he", "confidence_label_en",
    "internal_score", "internal_grade",
    "degradation_level", "confidence_band",
    "kcal_100g", "fat_g", "fat_saturated_g", "carbohydrates_g",
    "sugars_g", "fiber_g", "protein_g", "sodium_mg",
    "has_ingredient_text", "has_hebrew_ingredients", "ingredient_count",
    "fermentation_flag", "seed_signal", "fiber_laundering_flag", "whole_grain_flag",
    "anchor_override",
]

def export_website_dataset(results: list[dict]) -> tuple[pathlib.Path, pathlib.Path]:
    # JSON
    json_path = REPORT_DIR / "real_bread_retail_001_website_dataset.json"
    export = [{f: r.get(f) for f in _CSV_FIELDS} for r in results]
    json_path.write_text(
        json.dumps({"run_id": RUN_ID, "generated": TODAY, "n": len(export),
                    "products": export}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # CSV
    csv_path = REPORT_DIR / "real_bread_retail_001_website_dataset.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        for row in export:
            writer.writerow(row)

    return json_path, csv_path


# ---------------------------------------------------------------------------
# Fixed score report (replaces the original)
# ---------------------------------------------------------------------------
def report_score_fixed(results: list[dict]) -> str:
    n = len(results)
    verified   = [r for r in results if r["tier"] == "verified"]
    nutr_only  = [r for r in results if r["tier"] == "nutrition_only"]
    uncertain  = [r for r in results if r["tier"] == "uncertain"]
    data_gap   = [r for r in results if r["tier"] == "data_gap"]

    scored = [r for r in verified if r["internal_score"] is not None]
    scores = [r["internal_score"] for r in scored]

    lines = [
        f"# Real Bread Retail Corpus — Score Distribution (Corrected)",
        f"",
        f"Run: `{RUN_ID}` | Generated: {TODAY} | n={n} total products",
        f"",
        f"## ⚠ Data Tier Separation",
        f"",
        f"The pipeline computes an internal score for every product regardless of data quality.",
        f"**Consumer-visible scores apply only to products with verified ingredient data.**",
        f"",
        f"| Tier | Products | Description | Score shown? |",
        f"|:-----|:---------|:------------|:-------------|",
        f"| Verified | {len(verified)} | Full/Cautious degradation + ingredient text | ✓ Yes |",
        f"| Nutrition-only | {len(nutr_only)} | Nutrition complete, ingredients missing | ✗ No |",
        f"| Uncertain | {len(uncertain)} | Incomplete on multiple fields | ✗ No |",
        f"| Data gap | {len(data_gap)} | INSUFFICIENT — not enough for analysis | ✗ No |",
        f"",
        f"---",
        f"",
        f"## Verified Products — Score Distribution ({len(verified)} products)",
        f"",
        f"These are the only products that can safely be featured in consumer content.",
        f"",
    ]

    if scored:
        grade_counts = {}
        for r in scored:
            g = r["internal_grade"] or "?"
            grade_counts[g] = grade_counts.get(g, 0) + 1
        lines += [
            f"**Score range:** {min(scores):.0f}–{max(scores):.0f}",
            f"**Mean:** {sum(scores)/len(scores):.1f}",
            f"",
            f"| Grade | Count | Shown as |",
            f"|:------|:------|:---------|",
        ]
        for g in ["A", "B", "C", "D", "E"]:
            cnt = grade_counts.get(g, 0)
            if cnt:
                prov = sum(1 for r in scored if r["internal_grade"] == g
                           and r["consumer_grade_provisional"])
                full = cnt - prov
                shown = []
                if full:  shown.append(f"{full} confirmed")
                if prov:  shown.append(f"{prov} provisional")
                lines.append(f"| {g} | {cnt} | {', '.join(shown)} |")
        lines.append("")

    lines += [
        f"### Verified Products — Ranked",
        f"",
    ]
    for i, r in enumerate(sorted(verified, key=lambda x: x["internal_score"] or 0, reverse=True), 1):
        name  = r["name_he"][:38]
        brand = r["brand"][:14]
        score = r["internal_score"]
        grade = r["internal_grade"]
        prov  = " (provisional)" if r["consumer_grade_provisional"] else ""
        fiber = r.get("fiber_g")
        fiber_s = f"  fiber={fiber:.1f}g" if fiber else ""
        ferm  = " ⚗ fermentation" if r["fermentation_flag"] else ""
        lines.append(f"{i}. **{name}** ({brand}) — score={score:.0f} grade={grade}{prov}{fiber_s}{ferm}")

    lines += [
        f"",
        f"---",
        f"",
        f"## Nutrition-Only Products ({len(nutr_only)} products)",
        f"",
        f"These products have usable nutrition tables but NO ingredient text.",
        f"The internal pipeline score may look reasonable, but it cannot be verified",
        f"against ingredient signals. **Do not feature these with scores in consumer content.**",
        f"",
        f"The internal scores for these products range widely and likely overstate certainty.",
        f"",
    ]
    nutr_sorted = sorted(nutr_only, key=lambda x: x["internal_score"] or 0, reverse=True)
    for r in nutr_sorted[:8]:
        name = r["name_he"] or r.get("barcode", "")
        score = r["internal_score"]
        band  = r["confidence_band"]
        lines.append(f"- **{name}** — internal score={score:.0f} | band={band} | ⚠ no ingredient verification")

    lines += [
        f"",
        f"---",
        f"",
        f"## Data Gap Products ({len(data_gap)} products)",
        f"",
        f"These are INSUFFICIENT degradation products. They are NOT 'bad products' —",
        f"they are products with insufficient data in Open Food Facts for the pipeline",
        f"to produce a reliable output. Many may be good products in reality.",
        f"",
        f"**Do not feature these in 'worst products' lists.** They represent data gaps, not product quality.",
        f"",
    ]
    for r in data_gap[:10]:
        name = (r["name_he"] or r.get("barcode", ""))[:38]
        deductions = "; ".join(d.split(":")[0] for d in r["calibration_deductions"][:2])
        lines.append(f"- **{name}** — {deductions or 'insufficient_context'}")

    lines += ["", f"*Generated by {RUN_ID} — Corrected score report*"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Verified insights report
# ---------------------------------------------------------------------------
def report_verified_insights(results: list[dict]) -> str:
    verified  = [r for r in results if r["tier"] == "verified"]
    nutr_only = [r for r in results if r["tier"] == "nutrition_only"]
    data_gap  = [r for r in results if r["tier"] == "data_gap"]
    n = len(results)

    lines = [
        f"# Real Bread Retail — Verified Insights Only",
        f"",
        f"Run: `{RUN_ID}` | Generated: {TODAY}",
        f"",
        f"This report separates what we can reliably say (verified) from what we",
        f"can only suggest (plausible) and what we cannot assess (data gap).",
        f"",
        f"---",
        f"",
        f"## A. Verified Findings (ingredient data confirmed)",
        f"",
        f"**Basis:** {len(verified)} products with Hebrew ingredient text + FULL/CAUTIOUS degradation.",
        f"These findings are backed by full signal extraction on real ingredient lists.",
        f"",
    ]

    # Fermentation
    ferm_v = [r for r in verified if r["fermentation_flag"]]
    lines += [
        f"### Fermentation / Sourdough",
        f"",
        f"{len(ferm_v)}/{len(verified)} verified products show fermentation signals.",
    ]
    for r in ferm_v:
        score = r["internal_score"]
        fiber = r.get("fiber_g")
        grade = r["internal_grade"]
        label = r["confidence_label_he"]
        lines.append(
            f"- **{r['name_he']}** ({r['brand']}) — score={score:.0f} grade={grade}"
            f" — fiber={fiber:.1f}g" if fiber else
            f"- **{r['name_he']}** ({r['brand']}) — score={score:.0f} grade={grade}"
        )
        lines.append(f"  _{label}_")

    # Seeds
    seed_v = [r for r in verified if r["seed_signal"]]
    lines += [
        f"",
        f"### Seed Signals",
        f"",
        f"{len(seed_v)}/{len(verified)} verified products contain seed signals in ingredient text.",
    ]
    for r in seed_v:
        lines.append(f"- **{r['name_he']}** ({r['brand']}) — {r['confidence_label_he']}")

    # Fiber
    fiber_verified = [(r, r["fiber_g"]) for r in verified if r["fiber_g"] is not None]
    fiber_verified.sort(key=lambda x: -x[1])
    lines += [
        f"",
        f"### Fiber in Verified Products",
        f"",
        f"Fiber data confirmed from label nutrition tables (not ingredient text).",
        f"",
    ]
    for r, fib in fiber_verified:
        lines.append(
            f"- **{r['name_he']}** — {fib:.1f}g fiber/100g | "
            f"score={r['internal_score']:.0f} | {r['confidence_label_he']}"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## B. Plausible but Unverified Patterns",
        f"",
        f"**Basis:** {len(nutr_only)} products with complete nutrition tables but NO ingredient text.",
        f"Pipeline scores look meaningful but cannot be verified against actual ingredients.",
        f"Mention in analysis only with explicit caveat.",
        f"",
        f"High-scoring nutrition-only products (internal score, not consumer-displayed):",
        f"",
    ]
    nutr_sorted = sorted(nutr_only, key=lambda x: x["internal_score"] or 0, reverse=True)
    for r in nutr_sorted[:6]:
        score = r["internal_score"]
        fiber = r.get("fiber_g")
        fiber_s = f"  fiber={fiber:.1f}g" if fiber else ""
        lines.append(
            f"- **{r['name_he'] or r['barcode']}** ({r['brand']}) — "
            f"internal score={score:.0f}{fiber_s} — ⚠ no ingredient verification"
        )
    lines += [
        f"",
        f"Key caveat: these products may genuinely score as shown, but without ingredient",
        f"signals we cannot confirm fermentation, fiber type, additive profile, or matrix.",
        f"",
        f"---",
        f"",
        f"## C. Data Gaps",
        f"",
        f"**{len(data_gap)}/{n} products** returned INSUFFICIENT degradation. These are not",
        f"confirmed-bad products — they are OFF records with inadequate data for analysis.",
        f"",
        f"Primary causes:",
    ]
    causes = {"insufficient_context (no Hebrew name)": 0, "ingredients_missing": 0, "nutrition_incomplete": 0}
    for r in data_gap:
        deductions = " ".join(r["calibration_deductions"])
        if "product_name_empty" in deductions or "product_name_very_short" in deductions:
            causes["insufficient_context (no Hebrew name)"] += 1
        elif not r["has_ingredient_text"]:
            causes["ingredients_missing"] += 1
        else:
            causes["nutrition_incomplete"] += 1
    for cause, cnt in causes.items():
        if cnt:
            lines.append(f"- {cause}: {cnt} products")

    lines += [
        f"",
        f"**Conclusion:** The 100-product target required by the sprint spec is unachievable",
        f"from publicly accessible Israeli retail data. This is the honest result.",
        f"",
        f"*Generated by {RUN_ID}*"
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Website handoff file
# ---------------------------------------------------------------------------
def report_website_handoff(results: list[dict]) -> str:
    verified   = sorted([r for r in results if r["tier"] == "verified"],
                        key=lambda x: x["internal_score"] or 0, reverse=True)
    nutr_only  = sorted([r for r in results if r["tier"] == "nutrition_only"],
                        key=lambda x: x["internal_score"] or 0, reverse=True)
    n = len(results)
    n_v = len(verified)

    top_verified = verified[:3]

    lines = [
        f"# Website Handoff — Real Bread Retail 001",
        f"",
        f"Generated: {TODAY} | Run: `{RUN_ID}`",
        f"",
        f"This document is for Cursor/website team.",
        f"All analysis, copy, and caveats are here.",
        f"Do not use the raw score_distribution or batch_summary reports for consumer-facing content.",
        f"",
        f"---",
        f"",
        f"## 1. Data Transparency (mandatory framing — include in all consumer content)",
        f"",
        f"**What to say:**",
        f"",
        f"> ניתחנו מוצרי לחם ישראלים מסופרמרקטים ישראליים על בסיס נתונים ממסד הנתונים הפתוח",
        f"> Open Food Facts. מסד נתונים זה כולל נתוני תזונה ורשימות מרכיבים שנלקחו ממדבקות",
        f"> מוצרים אמיתיים. מידע על {n_v} מוצרים היה מלא מספיק לניתוח אמין.",
        f"> שאר המוצרים חסרו נתוני מרכיבים ולא ייוצגו בדירוג.",
        f"",
        f"**English equivalent:**",
        f"",
        f"> We analyzed Israeli retail bread products using data from Open Food Facts,",
        f"> a public database of real product label data. {n_v} products had sufficient",
        f"> data for reliable scoring. The remaining products are listed with a data-availability",
        f"> note — they are not confirmed poor products.",
        f"",
        f"**What NOT to say:**",
        f"- Do not say 'we analyzed {n} Israeli bread products' as if all {n} are fully scored",
        f"- Do not rank products without ingredient data against products with ingredient data",
        f"- Do not feature 'bottom products' that are there due to data gaps, not product quality",
        f"",
        f"---",
        f"",
        f"## 2. Key Stats — Safe to Publish",
        f"",
    ]

    # Fiber stats from verified
    fiber_vals = [r["fiber_g"] for r in verified if r["fiber_g"] is not None]
    avg_fiber  = sum(fiber_vals)/len(fiber_vals) if fiber_vals else None
    grade_dist = {}
    for r in verified:
        g = r["internal_grade"] or "?"
        grade_dist[g] = grade_dist.get(g, 0) + 1
    ferm_count = sum(1 for r in verified if r["fermentation_flag"])

    lines += [
        f"Based on {n_v} products with verified ingredient data:",
        f"",
        f"- **Average fiber:** {avg_fiber:.1f}g per 100g" if avg_fiber else "- Fiber data partially available",
        f"- **Grade distribution:**",
    ]
    for g in ["A", "B", "C", "D"]:
        cnt = grade_dist.get(g, 0)
        if cnt:
            lines.append(f"  - Grade {g}: {cnt} product{'s' if cnt > 1 else ''}")
    lines += [
        f"- **Fermentation signals detected:** {ferm_count}/{n_v} products",
        f"",
        f"---",
        f"",
        f"## 3. Product Examples — Safe to Feature",
        f"",
        f"### ✓ Tier 1 — Full Analysis (show score + grade as confirmed)",
        f"",
    ]
    full_tier = [r for r in verified if r["consumer_grade_visible"]]
    if full_tier:
        for r in full_tier:
            lines += [
                f"**{r['name_he']}** ({r['brand']})",
                f"- Score: {r['internal_score']:.0f} | Grade: {r['internal_grade']} | {r['confidence_label_he']}",
                f"- Fiber: {r['fiber_g']:.1f}g/100g" if r['fiber_g'] else "- Fiber: not recorded",
                f"- Fermentation: {'✓' if r['fermentation_flag'] else '✗'}",
                f"- Seeds: {'✓' if r['seed_signal'] else '✗'}",
                f"- Category: {r['category']}",
                f"- Source: {r['source_url']}",
                f"",
            ]
    else:
        lines += ["No products qualify for full confirmed grade display.", ""]

    lines += [
        f"### ~ Tier 2 — Partial Analysis (show score + provisional grade)",
        f"",
    ]
    cautious_tier = [r for r in verified if r["consumer_grade_provisional"]]
    for r in cautious_tier:
        fiber_s = f"{r['fiber_g']:.1f}g fiber" if r["fiber_g"] else "fiber not recorded"
        ferm_s  = "fermentation ✓" if r["fermentation_flag"] else ""
        notes   = " | ".join(filter(None, [fiber_s, ferm_s]))
        lines += [
            f"**{r['name_he']}** ({r['brand']}) — score={r['internal_score']:.0f} grade={r['internal_grade']}*",
            f"_{r['confidence_label_he']}_ — {notes}",
            f"",
        ]

    lines += [
        f"*Asterisk or label indicates provisional grade.*",
        f"",
        f"---",
        f"",
        f"## 4. Comparison Pairs — Recommended",
        f"",
        f"These pairs are interesting for the article because they contrast real verified products.",
        f"",
    ]

    # Pair 1: highest vs lowest verified fiber
    if len(fiber_vals) >= 2:
        hi = max(verified, key=lambda r: r["fiber_g"] or 0)
        lo = min(verified, key=lambda r: r["fiber_g"] or 0)
        lines += [
            f"### Pair 1 — Fiber Extremes (both verified)",
            f"",
            f"- **High fiber:** {hi['name_he']} ({hi['brand']}) — {hi['fiber_g']:.1f}g/100g — score={hi['internal_score']:.0f}",
            f"- **Low fiber:** {lo['name_he']} ({lo['brand']}) — {lo['fiber_g']:.1f}g — score={lo['internal_score']:.0f}",
            f"",
            f"Story angle: same product category (bread), fiber differs {hi['fiber_g'] - lo['fiber_g']:.0f}x.",
            f"",
        ]

    # Pair 2: fermentation vs not
    ferm_prods = [r for r in verified if r["fermentation_flag"]]
    no_ferm    = [r for r in verified if not r["fermentation_flag"] and r["fiber_g"]]
    if ferm_prods and no_ferm:
        f1 = ferm_prods[0]
        f2 = max(no_ferm, key=lambda r: r["internal_score"] or 0)
        lines += [
            f"### Pair 2 — Fermentation vs Industrial",
            f"",
            f"- **Fermented:** {f1['name_he']} ({f1['brand']}) — score={f1['internal_score']:.0f} grade={f1['internal_grade']}",
            f"- **Industrial:** {f2['name_he']} ({f2['brand']}) — score={f2['internal_score']:.0f} grade={f2['internal_grade']}",
            f"",
            f"Story angle: fermentation claim is a real signal, not just marketing — compare ingredient lists.",
            f"",
        ]

    # Pair 3: plausible vs verified
    if nutr_only and verified:
        n1 = nutr_only[0]
        v1 = verified[0]
        lines += [
            f"### Pair 3 — Verified vs Nutrition-Only (for transparency narrative)",
            f"",
            f"- **Verified:** {v1['name_he']} ({v1['brand']}) — score={v1['internal_score']:.0f} | has ingredients | grade={v1['internal_grade']}",
            f"- **Nutrition-only:** {n1['name_he'] or n1['barcode']} ({n1['brand']}) — internal score={n1['internal_score']:.0f} | no ingredients | grade NOT shown",
            f"",
            f"Story angle: transparency in data matters — same analysis, but only one product can",
            f"earn a confirmed grade because its ingredients are publicly available.",
            f"",
        ]

    lines += [
        f"---",
        f"",
        f"## 5. Confidence Language for UI",
        f"",
        f"Use these exact labels in the product UI. Do not invent alternatives.",
        f"",
        f"| Label (He) | Label (En) | When to use |",
        f"|:-----------|:-----------|:------------|",
        f"| נתונים מלאים יחסית | Relatively complete data | FULL degradation + ingredient text present |",
        f"| נתונים חלקיים | Partial data | CAUTIOUS degradation + ingredient text |",
        f"| חסרים נתונים מהותיים | Missing essential data | Nutrition only, no ingredients; or UNCERTAINTY |",
        f"| לא מספיק לניתוח ודאי | Insufficient for certain analysis | INSUFFICIENT degradation |",
        f"",
        f"**Score display rules:**",
        f"- Score visible: FULL or CAUTIOUS + has ingredient text → show",
        f"- Grade confirmed: FULL + has ingredient text → show without asterisk",
        f"- Grade provisional: CAUTIOUS + has ingredient text → show with asterisk or 'provisional' label",
        f"- No score: everything else → show confidence label only",
        f"",
        f"---",
        f"",
        f"## 6. Recommended Blog Narrative",
        f"",
        f"### Title options",
        f"- מה באמת יש בלחם שלכם? ניתחנו מוצרי לחם ישראלים",
        f"- הלחם הטוב ביותר שמצאנו — ומה שהיינו רוצים לדעת",
        f"- שקיפות בלחם: מה הציון שלנו אומר ומה הוא לא יכול לומר",
        f"",
        f"### Opening (honest framing)",
        f"",
        f"> ניתחנו מוצרי לחם ישראלים שנמכרים בסופרמרקטים. לא כל המוצרים קיבלו ציון —",
        f"> חלק לא כללו מספיק נתונים לניתוח אמין. הציונים שמוצגים כאן מבוססים על",
        f"> {n_v} מוצרים שכללו גם רשימת מרכיבים וגם נתוני תזונה מלאים.",
        f"",
        f"### Recommended structure",
        f"",
        f"1. **הממצאים המאומתים** — {n_v} מוצרים עם נתוני מרכיבים מלאים",
        f"2. **מה שגילינו** — ציפוי סיבים, תסיסה אמיתית לעומת מלאכותית, זרעים על גבי בסיס מזוקק",
        f"3. **מה שלא יכולנו לבדוק** — מוצרים ללא רשימת מרכיבים",
        f"4. **כיצד קוראים את הציון** — מה המשמעות של כוכבית",
        f"",
        f"### Safe claims (backed by verified data)",
        f"",
    ]
    if ferm_prods:
        lines.append(f"- לחם מחמצת אמיתי (עם מרכיב 'מחמצת' ברשימה) נמצא ב-{len(ferm_prods)} מוצרים מתוך {n_v} מאומתים")
    if fiber_vals:
        lines.append(f"- ממוצע סיבים תזונתיים במוצרים מאומתים: {avg_fiber:.1f} גרם ל-100 גרם")
    high_fiber = [r for r in verified if (r["fiber_g"] or 0) >= 8]
    if high_fiber:
        lines.append(f"- {len(high_fiber)} מוצרים מאומתים עם סיבים ≥8g/100g — לחם סיבים גבוה בפועל")

    lines += [
        f"",
        f"### Claims that require caveat",
        f"",
        f"- 'הלחם עם הציון הגבוה ביותר' → specify it's from the verified set only",
        f"- Any fiber laundering claim → only from verified products with ingredient text",
        f"- Comparison to synthetic corpus → note synthetic was designed for stress testing, not market rep.",
        f"",
        f"---",
        f"",
        f"## 7. Visual Recommendations",
        f"",
        f"- **Score dial / grade badge:** show only for verified ({n_v}) products",
        f"- **Confidence tag:** small pill label under product name for all products",
        f"- **Fiber bar chart:** show for products with fiber data ({sum(1 for r in results if r['fiber_g'])} products)",
        f"- **Ingredient text indicator:** icon showing whether ingredient list was available",
        f"- **Data availability panel:** always visible — 'מבוסס על {n_v} מוצרים מאומתים מתוך {n}'",
        f"- **Grade with asterisk:** use ✱ or 'משוקלל חלקית' for CAUTIOUS-tier grades",
        f"- **No bottom-5 list** unless filtered to verified products only",
        f"",
        f"---",
        f"",
        f"## 8. Dataset Files for Cursor",
        f"",
        f"- `real_bread_retail_001_website_dataset.json` — full product dataset with all fields",
        f"- `real_bread_retail_001_website_dataset.csv` — same, CSV format",
        f"",
        f"Key fields to use in UI:",
        f"- `consumer_score` — null if not displayable",
        f"- `consumer_grade` — null if not displayable",
        f"- `consumer_grade_provisional` — true if grade is provisional",
        f"- `confidence_label_he` — always set, use in UI",
        f"- `tier` — verified / nutrition_only / uncertain / data_gap",
        f"- `has_ingredient_text` — boolean filter",
        f"",
        f"*Handoff generated by generate_bread_retail_handoff.py — {TODAY}*"
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    log.info("=== BSIP2 Bread Retail Website Handoff Generator ===")

    files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    if not files:
        log.error("No products found in %s", BSIP1_DIR)
        return

    log.info("Loading and running pipeline on %d products...", len(files))
    results = []
    for f in files:
        try:
            product = json.loads(f.read_text(encoding="utf-8"))
            product["_source_path"] = str(f)
            result = _run_pipeline(product)
            results.append(result)
            log.info("  %-12s %-30s → tier=%-12s deg=%-14s score=%s",
                     str(product.get("barcode", ""))[-12:],
                     (product.get("canonical_name_he") or "")[:28],
                     result["tier"],
                     result["degradation_level"],
                     f"{result['internal_score']:.0f}" if result["internal_score"] else "—")
        except Exception as e:
            log.error("Error on %s: %s", f.name, e)
            import traceback; traceback.print_exc()

    log.info("Processed: %d | verified=%d | nutrition_only=%d | uncertain=%d | data_gap=%d",
             len(results),
             sum(1 for r in results if r["tier"] == "verified"),
             sum(1 for r in results if r["tier"] == "nutrition_only"),
             sum(1 for r in results if r["tier"] == "uncertain"),
             sum(1 for r in results if r["tier"] == "data_gap"))

    # Export website datasets
    json_path, csv_path = export_website_dataset(results)
    log.info("Dataset JSON: %s", json_path)
    log.info("Dataset CSV:  %s", csv_path)

    # Reports
    reports = [
        ("real_bread_retail_001_score_distribution_corrected.md", report_score_fixed),
        ("real_bread_retail_001_verified_insights.md",            report_verified_insights),
        ("real_bread_retail_website_handoff.md",                  report_website_handoff),
    ]
    for filename, fn in reports:
        path = REPORT_DIR / filename
        try:
            content = fn(results)
            path.write_text(content, encoding="utf-8")
            log.info("Report: %s", path)
        except Exception as e:
            log.error("Failed %s: %s", filename, e)
            import traceback; traceback.print_exc()

    print(f"\nHandoff complete. Files in: {REPORT_DIR}")
    print(f"  Verified (consumer-displayable): {sum(1 for r in results if r['tier'] == 'verified')}")
    print(f"  Nutrition-only: {sum(1 for r in results if r['tier'] == 'nutrition_only')}")
    print(f"  Data gaps (not for consumer content): {sum(1 for r in results if r['tier'] == 'data_gap')}")


if __name__ == "__main__":
    main()
