"""
BSIP2 Failure Taxonomy v1

Classifies BSIP2 pipeline outputs into discrete failure categories.
A single product can have multiple failure categories (overlapping).

Failure categories:
  1.  OCR_DEGRADATION           Corrupted/garbled ingredient or name text
  2.  SEMANTIC_AMBIGUITY        Product meaning genuinely unclear from signals
  3.  CATEGORY_LEAKAGE          Ingredient-context signals contaminate routing
  4.  MISSINGNESS               Critical fields absent (nutrition, ingredients, barcode)
  5.  RETAILER_INCONSISTENCY    Conflicting values across retailer sources
  6.  ONTOLOGY_GAP              Product type outside current archetype coverage
  7.  WEAK_SUPPRESSION          Guardrail fires incorrectly OR fails to fire when it should
  8.  CONFIDENCE_OVERSTATEMENT  High confidence_band despite poor input data quality
  9.  INGREDIENT_TRUNCATION     Ingredient list cut off; signals based on incomplete picture
  10. HYBRID_CONFLICT           Legitimate dual-category product; primary routing uncertain

Severity levels: CRITICAL / HIGH / MEDIUM / LOW
"""

from __future__ import annotations
from constants import KCAL_PLAUSIBLE_LOWER, KCAL_PLAUSIBLE_UPPER  # EV-047

FAILURE_CATEGORIES = {
    "OCR_DEGRADATION":          "Corrupted or garbled text prevents reliable signal extraction",
    "SEMANTIC_AMBIGUITY":       "Product semantics genuinely unclear from available signals",
    "CATEGORY_LEAKAGE":         "Ingredient text signals cross-contaminate category routing",
    "MISSINGNESS":              "Critical fields absent — scoring operates on incomplete information",
    "RETAILER_INCONSISTENCY":   "Conflicting values across retailer sources create uncertainty",
    "ONTOLOGY_GAP":             "Product type outside current archetype/category coverage",
    "WEAK_SUPPRESSION":         "Guardrail fires incorrectly or fails to fire when warranted",
    "CONFIDENCE_OVERSTATEMENT": "Confidence band higher than input data quality justifies",
    "INGREDIENT_TRUNCATION":    "Ingredient list appears cut off; downstream signals incomplete",
    "HYBRID_CONFLICT":          "Legitimate dual-category product; routing choice materially affects score",
}

SEVERITY_WEIGHTS = {
    "CRITICAL": 4,
    "HIGH":     3,
    "MEDIUM":   2,
    "LOW":      1,
}


def classify_failures(
    product: dict,
    signals: dict,
    cat_result: dict,
    nova_result: dict,
    score_result: dict,
    interpretation_conf: dict,
) -> list[dict]:
    """
    Classify all applicable failure categories for a product.
    Returns list of {category, severity, evidence, recommendation} dicts.
    """
    failures: list[dict] = []

    def add(category: str, severity: str, evidence: str, recommendation: str) -> None:
        failures.append({
            "category":       category,
            "severity":       severity,
            "evidence":       evidence,
            "recommendation": recommendation,
            "description":    FAILURE_CATEGORIES[category],
        })

    nn  = product.get("normalized_nutrition_per_100g") or {}
    l1  = signals.get("L1_observed_signals", {})
    ing_text    = product.get("ingredients_text_he") or ""
    ing_list    = product.get("ingredients_list") or []
    ing_quality = product.get("ingredient_text_quality", "clean")
    consistency = product.get("nutrition_consistency_status", "consistent")
    trust_level = product.get("canonical_trust_level", "unknown")
    conf_band   = interpretation_conf.get("interpretation_confidence_band", "high")
    base_band   = interpretation_conf.get("base_confidence_band", "high")

    # ── 1. OCR_DEGRADATION ────────────────────────────────────────────────────
    if ing_quality == "corrupted":
        add("OCR_DEGRADATION", "HIGH",
            "ingredient_text_quality=corrupted — text contains garbled or unreadable sequences",
            "Re-scrape product page or source ingredient data from alternative channel")
    elif ing_quality == "malformed":
        add("OCR_DEGRADATION", "MEDIUM",
            "ingredient_text_quality=malformed — text structure is inconsistent",
            "Manual review of ingredient text before re-processing")

    # Heuristic: very short ingredient text relative to list length suggests OCR truncation
    if ing_list and len(ing_text) < len(ing_list) * 4:
        add("OCR_DEGRADATION", "MEDIUM",
            f"ingredient_text={len(ing_text)} chars but {len(ing_list)} items listed — text likely truncated by OCR",
            "Cross-reference against physical product label or alternative retailer scrape")

    # ── 2. SEMANTIC_AMBIGUITY ─────────────────────────────────────────────────
    cat_conf = cat_result.get("category_confidence", 1.0)
    if cat_conf < 0.50:
        add("SEMANTIC_AMBIGUITY", "HIGH",
            f"category_confidence={cat_conf:.2f} — routing is unreliable below 0.50",
            "Inspect product name and ingredient signals; consider adding a hard anchor for this product class")
    elif cat_conf < 0.65:
        add("SEMANTIC_AMBIGUITY", "MEDIUM",
            f"category_confidence={cat_conf:.2f} — routing is uncertain",
            "Review routing signal log for competing signals; consider dedicated anchor term")

    # ── 3. CATEGORY_LEAKAGE ───────────────────────────────────────────────────
    suppressed = cat_result.get("routing_suppressed_signals", [])
    if len(suppressed) >= 3:
        add("CATEGORY_LEAKAGE", "MEDIUM",
            f"{len(suppressed)} signals suppressed: {suppressed[:4]}",
            "Review signal scope assignments; context_gated signals may need tighter gate conditions")
    elif len(suppressed) >= 1:
        add("CATEGORY_LEAKAGE", "LOW",
            f"{len(suppressed)} signal(s) suppressed: {suppressed[:2]}",
            "Monitor for signal leakage in this product class")

    # If anchor did NOT fire but competing signals are high
    if not cat_result.get("anchor_override") and cat_conf < 0.75:
        scores = cat_result.get("raw_category_scores", {})
        top2 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
        if len(top2) == 2 and top2[1][1] > 0.3 * top2[0][1]:
            pass  # already caught by SEMANTIC_AMBIGUITY above

    # ── 4. MISSINGNESS ────────────────────────────────────────────────────────
    missing_nutrition = [f for f in ["energy_kcal", "protein_g", "fat_g", "carbohydrates_g", "dietary_fiber_g", "sodium_mg"]
                         if nn.get(f) is None]
    if len(missing_nutrition) >= 4:
        add("MISSINGNESS", "CRITICAL",
            f"Missing critical nutrition fields: {missing_nutrition}",
            "Product cannot be reliably scored — flag for data collection priority")
    elif len(missing_nutrition) >= 2:
        add("MISSINGNESS", "HIGH",
            f"Missing nutrition fields: {missing_nutrition}",
            "Scoring operates in degraded mode; affected dimensions use neutral fallback")
    elif len(missing_nutrition) == 1:
        add("MISSINGNESS", "LOW",
            f"Missing nutrition field: {missing_nutrition[0]}",
            "Minor gap; affected dimension uses neutral 50")

    if not product.get("barcode"):
        add("MISSINGNESS", "MEDIUM",
            "barcode=null — product identity relies on name+brand matching only",
            "Source barcode from packaging or alternative retailer")

    if not ing_list and not ing_text:
        add("MISSINGNESS", "HIGH",
            "No ingredient data available — signal extraction runs on nutrition only",
            "Ingredient data required for NOVA, additive, fiber source, and fermentation signals")

    # ── 5. RETAILER_INCONSISTENCY ─────────────────────────────────────────────
    if consistency in ("suspicious", "cross_retailer_conflict"):
        add("RETAILER_INCONSISTENCY", "HIGH",
            f"nutrition_consistency_status={consistency}",
            "Cross-reference with physical product; flag for BSIP1 re-enrichment")
    elif consistency == "warnings":
        add("RETAILER_INCONSISTENCY", "MEDIUM",
            "nutrition_consistency_status=warnings — cross-retailer disagreement detected",
            "Review specific disagreeing fields in BSIP1 conflicts_summary")

    # Impossible values (direct data inconsistency)
    checks = l1.get("consistency_checks", {})
    if checks.get("sugar_le_carbs") is False:
        add("RETAILER_INCONSISTENCY", "CRITICAL",
            f"sugar={nn.get('sugars_g')}g > carbohydrates={nn.get('carbohydrates_g')}g — physically impossible",
            "Data entry error — nutrition panel must be re-sourced before scoring is valid")
    if checks.get("satfat_le_fat") is False:
        add("RETAILER_INCONSISTENCY", "CRITICAL",
            f"sat_fat={nn.get('fat_saturated_g')}g > fat={nn.get('fat_g')}g — physically impossible",
            "Data entry error — fat values must be re-sourced")
    if checks.get("kcal_plausible") is False:
        add("RETAILER_INCONSISTENCY", "HIGH",
            f"energy_kcal={nn.get('energy_kcal')} outside plausible range ({KCAL_PLAUSIBLE_LOWER}-{KCAL_PLAUSIBLE_UPPER} kcal/100g)",
            "Verify per-100g basis; possible per-serving confusion")  # EV-047: upper raised 700→800

    # ── 6. ONTOLOGY_GAP ───────────────────────────────────────────────────────
    primary_cat = cat_result.get("category", "default")
    if primary_cat == "default":
        add("ONTOLOGY_GAP", "HIGH",
            "Routed to 'default' — product type not recognized by any category anchor or signal",
            "Evaluate if a new category or hard anchor is needed; do not score without explicit category")

    # Check if bakery product is not covered by current archetypes
    robustness_meta = product.get("_robustness_meta", {})
    if robustness_meta.get("noise_profile") == "ontology_gap":
        add("ONTOLOGY_GAP", "HIGH",
            "Product explicitly tagged as outside current ontology coverage",
            "New archetype or category definition required")

    # ── 7. WEAK_SUPPRESSION ───────────────────────────────────────────────────
    caps_applied = score_result.get("caps_applied", [])
    penalties_applied = score_result.get("penalties_applied", [])
    nova_level = nova_result.get("nova_level", 1)
    final_score = score_result.get("final_score_estimate")

    # Suspiciously high score for NOVA 4
    if nova_level == 4 and final_score is not None and final_score > 60:
        add("WEAK_SUPPRESSION", "HIGH",
            f"NOVA 4 product scored {final_score:.1f} — NOVA_PROXY_4_ULTRA_PROCESSED cap(68) should bind",
            "Verify guardrail evaluation; check if cap coordination is working correctly")

    # No caps fired but product has 2+ red labels (cap should have fired)
    red_label_count = signals.get("L3_inferred_classifications", {}).get("red_label_count", 0)
    if red_label_count >= 2 and not caps_applied:
        add("WEAK_SUPPRESSION", "MEDIUM",
            f"2+ red labels ({red_label_count}) but no guardrail cap fired — ISRAELI_RED_LABELS_2_PLUS should fire",
            "Verify red_label detection in signal_extractor; check guardrail evaluation path")

    # Trans fat present but no veto
    trans = nn.get("fat_trans_g") or 0
    if trans > 1.0 and not score_result.get("trans_fat_veto_applied"):
        add("WEAK_SUPPRESSION", "CRITICAL",
            f"fat_trans_g={trans} > 1.0 but trans fat veto not applied",
            "Critical bug: veto logic must be reviewed immediately")

    # ── 8. CONFIDENCE_OVERSTATEMENT ───────────────────────────────────────────
    ic_score = interpretation_conf.get("interpretation_confidence_score", 100)
    ic_band  = interpretation_conf.get("interpretation_confidence_band", "high")

    # Base confidence high but interpretation_confidence much lower
    base_score_raw = interpretation_conf.get("base_confidence_score", 100)
    if base_score_raw >= 70 and ic_score < 50:
        add("CONFIDENCE_OVERSTATEMENT", "MEDIUM",
            f"base_confidence={base_score_raw:.0f} (band={base_band}) but interpretation_confidence={ic_score:.0f} ({ic_band}) "
            f"— router instability or ingredient quality not captured in base score",
            "Prefer interpretation_confidence_band over confidence_band for output display")

    # High confidence band despite critical missingness
    if ic_band in ("high", "very_high") and len(missing_nutrition) >= 3:
        add("CONFIDENCE_OVERSTATEMENT", "HIGH",
            f"confidence_band={ic_band} despite {len(missing_nutrition)} missing nutrition fields",
            "Confidence scoring must account for field-level missingness more aggressively")

    # ── 9. INGREDIENT_TRUNCATION ──────────────────────────────────────────────
    # Already partially handled in OCR_DEGRADATION; check for logical truncation
    if ing_list and ing_text and len(ing_list) >= 3:
        # If last item in text ends mid-word (no punctuation at end of meaningful item)
        last_ing = ing_text.strip()
        if last_ing and not last_ing[-1] in (".", ",", ")", "]", "\"", "'"):
            # Ends without closure — possible truncation
            if len(last_ing) > 30:  # long enough that truncation is meaningful
                add("INGREDIENT_TRUNCATION", "MEDIUM",
                    f"Ingredient text ends without closing punctuation — possible OCR or scraper truncation",
                    "Verify full ingredient list; truncated list may miss additives or key ingredients")

    # Very few items in list relative to ingredient text length
    if ing_text and len(ing_text) > 150 and len(ing_list) <= 3:
        add("INGREDIENT_TRUNCATION", "HIGH",
            f"Ingredient text is {len(ing_text)} chars but only {len(ing_list)} items parsed — parsing failure suspected",
            "Re-parse ingredient text with updated parser; manual validation required")

    # ── 10. HYBRID_CONFLICT ───────────────────────────────────────────────────
    if cat_result.get("is_hybrid"):
        top_cat = cat_result.get("category")
        sec_cat = cat_result.get("secondary_category")
        scores  = cat_result.get("raw_category_scores", {})
        top_s   = scores.get(top_cat, 0)
        sec_s   = scores.get(sec_cat, 0)
        delta   = top_s - sec_s
        add("HYBRID_CONFLICT", "MEDIUM",
            f"Hybrid routing: {top_cat}({top_s:.2f}) vs {sec_cat}({sec_s:.2f}), delta={delta:.2f}",
            f"Score produced under '{top_cat}' interpretation; verify which context better matches consumer intent")

    return failures


def summarize_failures(failures: list[dict]) -> dict:
    """Produce a compact summary of failure classifications."""
    if not failures:
        return {
            "failure_count":       0,
            "severity_breakdown":  {},
            "categories_fired":    [],
            "max_severity":        None,
            "composite_risk":      "none",
        }

    by_severity: dict[str, int] = {}
    categories: list[str] = []
    for f in failures:
        sev = f["severity"]
        by_severity[sev] = by_severity.get(sev, 0) + 1
        if f["category"] not in categories:
            categories.append(f["category"])

    max_weight = max(SEVERITY_WEIGHTS.get(f["severity"], 0) for f in failures)
    max_sev = {4: "CRITICAL", 3: "HIGH", 2: "MEDIUM", 1: "LOW"}.get(max_weight, "LOW")

    total_weight = sum(SEVERITY_WEIGHTS.get(f["severity"], 1) for f in failures)
    if total_weight >= 12 or max_weight == 4:
        risk = "critical"
    elif total_weight >= 7 or max_weight == 3:
        risk = "high"
    elif total_weight >= 4:
        risk = "medium"
    else:
        risk = "low"

    return {
        "failure_count":      len(failures),
        "severity_breakdown": by_severity,
        "categories_fired":   categories,
        "max_severity":       max_sev,
        "composite_risk":     risk,
    }
