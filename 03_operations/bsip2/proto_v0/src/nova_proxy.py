"""
BSIP2 Prototype v0 — NOVA Proxy Classifier
Infers NOVA level from ingredient signals. Not a validated classifier.
Confidence is explicit. Every inference is traceable.
"""
import os
import re as _re

# TASK-169 P0 (R4) — plain-dairy NOVA-3→2 demotion guard, gated by BARI_RECAL_P0.
# DEFAULT OFF → classifier byte-identical. See recalibration_p0_design_v1.md R4.
RECAL_P0_ON = os.environ.get("BARI_RECAL_P0", "off").lower() == "on"

# R4 v1.1 (TASK-169A) — flavored/seasoned-variant markers that disqualify the plain-dairy
# NOVA-3→2 demotion. Imported from constants so the list is single-sourced.
try:
    from constants import FLAVORED_VARIANT_MARKERS_HE
except Exception:  # pragma: no cover — defensive for alternate import paths
    FLAVORED_VARIANT_MARKERS_HE = ()

# Additive categories that mark genuine ultra-processing; presence of ANY blocks the
# R4 demotion (product stays NOVA 3). Benign culinary/culturing/fortification additions
# (salt, cultures, rennet, calcium, vitamins) emit no additive_category marker.
NOVA_DEMOTE_BLOCKING_ADDITIVE_CATS = {
    "thickener", "stabilizer", "emulsifier", "humectant", "flavor_enhancer", "color",
}

# NOVA 4 requires evidence of industrial formulation:
# flavor enhancers, artificial colors, multiple additive systems, glucose syrups
NOVA4_STRONG_SIGNALS = [
    "flavor_enhancer",   # חומרי טעם וריח — strongest signal
    "color",             # צבע מאכל
]

# Additional NOVA 4 signals from additive categories
NOVA4_MODERATE_SIGNALS = [
    "humectant",         # e.g., גליצרין, סורביטול
    "emulsifier",        # מתחלב (multiple = stronger signal)
]

# NOVA 3 signals: processed but not ultra-processed
NOVA3_SIGNALS = [
    "preservative",
    "antioxidant",
    "acidity_regulator",
    "leavening_agent",
]

# Whole grain presence reduces NOVA level estimate
# Fermentation presence reduces NOVA level estimate
# Single ingredient is almost always NOVA 1

# EV-009 / EV-010: Extruded/shaped grain products are NOVA 3 (milling-disrupted matrix).
# "פתיתים אפויים" = Osem-style baked shaped pasta-cereal (extrusion + shaping + bake).
# This is the minimal name-detection component of EV-010 (extrusion_matrix_penalty).
# Gated to the specific product name prefix — does NOT apply to "פתיתים אורגנים" (rolled grain flakes).
# Backed by: Nutrition Agent ruling 2026-06-05 (TASK-140 QA-CER-W1); EV-009 (extruded shapes = disrupted);
# EV-010 (should_affect_score_now: true; risk-of-misuse: refined-grain extrusion penalized, whole-grain puffed exempt).
EXTRUDED_SHAPE_NAME_SIGNALS: list[str] = [
    "פתיתים אפויים",   # baked pasta-shaped flakes (Osem type: קוסקוס/כוכבים/טבעות/אורז)
]

# ---------------------------------------------------------------------------
# TASK-216 — Industrial extrusion NOVA 4 signal (EV-043)
# ---------------------------------------------------------------------------
# Industrial high-temperature extrusion (direct expansion) is an irreversible
# physical process that disrupts the grain matrix, gelatinizes starch, and
# fundamentally restructures the food beyond what any minimal-process product
# exhibits. It is invisible to additive-count classifiers yet marks a NOVA 4
# production method per the NOVA framework (Monteiro et al.).
#
# Signal A — Ingredient text "מורחב" (extruded grain):
#   Hebrew ingredient declarations mark extruded grain as "תירס מורחב",
#   "חיטה מורחבת", "אורז מורחב", etc.  The token "מורחב" / "מורחבת" is
#   unambiguous: it means expanded/extruded by high-temperature direct-expansion.
#   It does NOT appear in plain rice cakes (אורז, חיטה מלאה) or crackers.
#   False-positive risk: effectively zero — no Israeli retail snack uses "מורחב"
#   for anything other than puffed/extruded grain.
#
# Signal B — BSIP1 sub_pool=puffed + grain primary ingredient:
#   The BSIP1 enricher assigns sub_pool="puffed" to products whose category
#   or name cues confirm industrial puffing (Bisli, Bamba variants, ניבים,
#   corn puffs, cheese puffs).  Plain rice cakes receive sub_pool="rice_cakes"
#   by design.  When sub_pool=puffed AND the primary ingredient is a grain
#   (corn, wheat flour, potato, rice in extruded form) → NOVA 4.
#   False-positive risk: very low.  The only puffed product that could be
#   legitimately NOVA 2 is a single-grain puffed rice — but those get
#   sub_pool="rice_cakes" from the enricher.  Any product reaching this path
#   with sub_pool=puffed is an industrially recombined extruded snack.
#
# Guard — rice_cakes sub_pool is hard-excluded from both signals.
# Guard — whole-grain puffed rice cakes (פצפוצי אורז/חיטה מלאה) have
#   sub_pool="rice_cakes", ingredient "אורז"/"חיטה מלאה", NO "מורחב" →
#   neither signal fires → NOVA 1/2 preserved.
#
# Scope: approved for salty-snacks rescore (run_salty_snacks_002).
# Full engine promotion (all categories) requires Product Agent D7 co-sign.
# Evidence reference: EV-043 (pending evidence registry entry, TASK-216).
# ---------------------------------------------------------------------------

# Signal A: explicit extrusion marker in ingredient text
EXTRUSION_INGREDIENT_MARKERS: list[str] = [
    "מורחב",    # extruded grain — e.g. "תירס מורחב" (extruded corn, Bamba-type)
    "מורחבת",   # feminine form — e.g. "חיטה מורחבת" (extruded wheat)
]

# Signal B: BSIP1 sub_pool values that confirm industrial puffing/extrusion
INDUSTRIAL_PUFFED_SUBPOOLS: list[str] = [
    "puffed",
]

# Grain-type primary ingredients that, when combined with sub_pool=puffed,
# confirm industrial extrusion (rather than e.g. a baked cheese cracker
# that might also land in puffed).
GRAIN_PRIMARY_INGREDIENTS_HE: list[str] = [
    "תירס",         # corn
    "קמח תירס",     # corn flour
    "קמח חיטה",     # wheat flour
    "קמח",          # flour (generic — covers chickpea/lentil flour puffs)
    "תפוחי אדמה",   # potato (for potato puffs)
    "אורז",         # rice (when puffed sub_pool, not rice_cakes)
]

# Products in these sub_pools are never reclassified by the extrusion signal,
# regardless of ingredient text.  Protects plain rice cakes and rye crispbreads.
EXTRUSION_SIGNAL_EXCLUDED_SUBPOOLS: list[str] = [
    "rice_cakes",
    "pretzels",
    "baked",
    "popcorn",   # popcorn = hot-air or oil-popped whole kernel, not industrial extrusion
]

# BSIP2-HC-001 sub-rule B (TASK-REDLABEL-001) — Phosphate emulsifying salt markers.
# Compiled at module level for performance. Matches E339, E450, E451, E452 (all sodium/
# potassium/calcium phosphates used as emulsifying salts in processed cheese) and
# their Hebrew equivalents.  E331 (sodium citrate) is excluded: it acts as an
# acidity_regulator in many products, not specifically as an emulsifying salt.
PHOSPHATE_EMULSIFYING_SALT_RE = _re.compile(
    r"E-?339|E-?450|E-?451|E-?452|"
    r"נתרן\s+פוספט|דיסודיום\s+פוספט|טריסודיום\s+פוספט|סודיום\s+פוספט",
    _re.IGNORECASE,
)


def infer_nova(product: dict, l3_signals: dict) -> dict:
    """
    Infer NOVA proxy level (1-4) from L3 ingredient signals.
    Returns dict with nova_level, nova_confidence, and full trace.
    """
    # TASK-144 Fix1/EV-026 — prefer the sanitized ingredient count (OCR/nutrition-panel/
    # disclaimer bleed removed in signal_extractor). Falls back to the raw product list
    # for any legacy caller that does not supply the sanitized count, so behaviour is
    # unchanged where the field is absent.
    ingredients = product.get("ingredients_list") or []
    if l3_signals.get("sanitized_ingredient_count") is not None:
        ing_count = l3_signals["sanitized_ingredient_count"]
    else:
        ing_count = len(ingredients)
    additive_cats = set(l3_signals.get("additive_categories") or [])
    has_flavor_enhancer = l3_signals.get("has_flavor_enhancer", False)
    has_color = l3_signals.get("has_artificial_color", False)
    has_sweetener = l3_signals.get("sweetener_detected", False)
    has_whole_grain = l3_signals.get("has_whole_grain", False)
    has_fermentation = l3_signals.get("has_fermentation", False)
    additive_count = l3_signals.get("additive_marker_count", 0)
    added_sugar_ct = l3_signals.get("added_sugar_sources_count", 0)
    ing_quality = product.get("ingredient_text_quality", "unknown")

    evidence_for = []
    evidence_against = []
    confidence_penalties = []

    # ---------------------------------------------------------------------------
    # NOVA 1 check: single ingredient, no additives
    # ---------------------------------------------------------------------------
    # EV-030 guard: the single-ingredient fast-path must not fire when ingredient data is
    # degraded. Three degradation signals are checked:
    #   (a) explicit quality flag (corrupted/missing/malformed)
    #   (b) "ingredients_list" in missing_fields — BSIP1 failed to parse a real list
    #   (c) ingredients_raw_provenance.source == "bsip1_text_fallback" — list reconstructed
    #       from page marketing text, not a real ingredient declaration
    # When any signal fires, fall through to the main classifier with a confidence penalty
    # so the NOVA estimate reflects the actual uncertainty rather than a false 0.90.
    _mf = product.get("missing_fields") or []
    _prov_source = (product.get("ingredients_raw_provenance") or {}).get("source", "")
    _ingredient_data_degraded = (
        ing_quality in ("missing", "corrupted", "malformed")
        or "ingredients_list" in _mf
        or _prov_source == "bsip1_text_fallback"
    )
    if ing_count == 1 and additive_count == 0 and not has_sweetener and not _ingredient_data_degraded:
        return {
            "nova_level": 1,
            "nova_confidence": 0.90,
            "nova_confidence_band": "high",
            "nova_evidence_for": ["single_ingredient", "no_additives_detected"],
            "nova_evidence_against": [],
            "nova_uncertainty_notes": ["Single ingredient is strong NOVA 1 signal; undetected additives could change this"],
        }
    if _ingredient_data_degraded:
        confidence_penalties.append(
            f"EV-030: ingredient_data_degraded (quality={ing_quality}, "
            f"ingredients_list_missing={'ingredients_list' in _mf}, "
            f"provenance={_prov_source or 'unknown'}): NOVA 1 fast-path suppressed"
        )

    # ---------------------------------------------------------------------------
    # BSIP2-HC-002 (TASK-REDLABEL-001) — Dairy NOVA 1 fast-path for short-ingredient
    # hard/semi-hard cheese (milk + salt + rennet + cultures only).
    # ---------------------------------------------------------------------------
    # Per Monteiro NOVA framework: a cheese produced from pasteurised milk, salt,
    # rennet, and lactic cultures is minimally processed (NOVA 1).  The engine's
    # default classifier has no path to NOVA 1 for multi-ingredient products — the
    # single-ingredient fast-path (ing_count == 1) exits early, but all 2–5 ingredient
    # dairy products fall through to the score-based classifier which bottoms out at
    # NOVA 2.  The BSIP1 enricher correctly classifies these as NOVA 1 based on label
    # reading.
    #
    # Activation conditions (ALL must hold):
    #   (a) RECAL_P0_ON — gated with the same flag as R4 (TASK-169 lineage)
    #   (b) product_type_dairy — dairy base confirmed by signal_extractor
    #   (c) ing_count ≤ 6 — short ingredient list; culinary staples only
    #   (d) no NOVA-relevant additives — specifically: no thickener, stabilizer,
    #       emulsifier, humectant, flavor_enhancer, or flavor_enhancer category;
    #       and no artificial color (has_artificial_color == False).
    #       Benign / NOVA-1-compatible categories allowed: "acidity_regulator"
    #       (citric acid is naturally present in milk / used in cheesemaking),
    #       "color" when natural (has_artificial_color == False, e.g. beta-carotene).
    #   (e) added_sugar_ct == 0 and not has_sweetener — no sugar/sweetener
    #   (f) not has_flavor_enhancer — no NOVA 4 signals
    #   (g) not _ingredient_data_degraded — ingredient evidence is trustworthy
    #
    # Evidence: NOVA framework (Monteiro et al. 2018, §4 NOVA 1 definition);
    # Cheese Council compositional guides; Bari signal corpus audit 2026-06-08
    # (55/67 BSIP1 hard-cheese files show NOVA 1 with ≤5 culinary ingredients;
    # citric acid / acidity_regulator is a natural cheesemaking aid, not an
    # industrial additive; natural colorants are pigments, not processing markers).
    # ---------------------------------------------------------------------------

    # Categories that are benign / compatible with NOVA 1 dairy cheese production:
    #   - "acidity_regulator": citric acid / lactic acid — natural fermentation byproducts
    #   - "color" when not artificial: annatto, beta-carotene — whole-food pigments
    # Categories that are NOT benign (block HC-002 → fall through to main classifier):
    _HC002_BLOCKING_CATS = {"thickener", "stabilizer", "emulsifier", "humectant",
                             "flavor_enhancer", "preservative", "sweetener"}
    _has_artificial_color_early = l3_signals.get("has_artificial_color", False)
    _product_type_dairy_early = l3_signals.get("product_type_dairy", False)

    # Compute blocking additive load for HC-002 (excludes benign cats)
    _hc002_blocking_cats_present = set(additive_cats) & _HC002_BLOCKING_CATS
    _hc002_artificial_color_block = has_color and _has_artificial_color_early

    if (RECAL_P0_ON
            and _product_type_dairy_early
            and ing_count <= 6
            and not _hc002_blocking_cats_present
            and not _hc002_artificial_color_block
            and added_sugar_ct == 0
            and not has_sweetener
            and not has_flavor_enhancer
            and not _ingredient_data_degraded):
        _benign_note = []
        if "acidity_regulator" in additive_cats:
            _benign_note.append("acidity_regulator (citric/lactic acid: natural cheesemaking)")
        if has_color and not _has_artificial_color_early:
            _benign_note.append("natural colorant (beta-carotene/annatto: not an industrial additive)")
        _benign_str = ("; benign additives present: " + ", ".join(_benign_note)) if _benign_note else ""
        return {
            "nova_level": 1,
            "nova_r4_demotion_applied": False,
            "nova_confidence": 0.85,
            "nova_confidence_band": "high",
            "nova4_signal_score": 0,
            "nova_evidence_for": [],
            "nova_evidence_against": [],
            "nova_uncertainty_notes": [
                "BSIP2-HC-002: short-ingredient dairy NOVA 1 rule — milk/salt/rennet/cultures "
                "are minimally processed per NOVA framework (Monteiro et al.); no industrial "
                f"additive markers, no sweetener, ≤6 ingredients, dairy matrix confirmed{_benign_str}; "
                "gated by BARI_RECAL_P0 (TASK-REDLABEL-001)",
                "NOVA inference is a proxy; validated NOVA classification requires expert ingredient analysis",
            ],
        }

    # ---------------------------------------------------------------------------
    # NOVA 4 assessment: ultra-processed
    # ---------------------------------------------------------------------------
    nova4_score = 0

    if has_flavor_enhancer:
        nova4_score += 3
        evidence_for.append("flavor_enhancer_detected (חומרי טעם וריח)")
    if has_color:
        nova4_score += 2
        evidence_for.append("artificial_color_detected (צבע מאכל)")
    if has_sweetener:
        nova4_score += 2
        evidence_for.append("sweetener_detected")
    if added_sugar_ct >= 3:
        nova4_score += 2
        evidence_for.append(f"multiple_added_sugar_sources: {added_sugar_ct}")
    if "emulsifier" in additive_cats and "humectant" in additive_cats:
        nova4_score += 1
        evidence_for.append("emulsifier+humectant combination")
    if additive_count >= 4:
        nova4_score += 1
        evidence_for.append(f"high_additive_category_count: {additive_count}")
    if ing_count > 15:
        nova4_score += 1
        evidence_for.append(f"very_long_ingredient_list: {ing_count}")

    # Signals that argue against NOVA 4
    if has_whole_grain:
        nova4_score -= 1
        evidence_against.append("whole_grain_present (consistent with NOVA 2-3)")
    if has_fermentation:
        nova4_score -= 1
        evidence_against.append("fermentation_markers (consistent with NOVA 1-2)")

    # ---------------------------------------------------------------------------
    # EV-043 (TASK-216): Industrial extrusion signal — NOVA 4 assertion
    # ---------------------------------------------------------------------------
    # Two complementary signals, evaluated before the score-based classifier.
    # Signal A: explicit "מורחב"/"מורחבת" token in ingredient text.
    # Signal B: BSIP1 sub_pool=puffed + grain-type primary ingredient.
    # Both are hard-excluded for sub_pools that are never industrial extrusion.
    # ---------------------------------------------------------------------------
    _sub_pool = (product.get("sub_pool") or "").lower().strip()
    _excluded_by_subpool = _sub_pool in EXTRUSION_SIGNAL_EXCLUDED_SUBPOOLS

    _extrusion_signal_fired = False
    _extrusion_signal_source = ""

    if not _excluded_by_subpool:
        # Signal A: ingredient text contains an explicit extrusion marker
        _ingredients_text = " ".join(str(i) for i in ingredients)
        _signal_a = any(marker in _ingredients_text for marker in EXTRUSION_INGREDIENT_MARKERS)
        if _signal_a:
            _extrusion_signal_fired = True
            _matched_marker = next(m for m in EXTRUSION_INGREDIENT_MARKERS if m in _ingredients_text)
            _extrusion_signal_source = (
                f"EV-043 Signal-A: extrusion_ingredient_marker='{_matched_marker}' found in "
                f"ingredient text — high-temperature direct-expansion confirmed from label declaration; "
                f"NOVA 4 per NOVA framework (Monteiro); approved for salty-snacks rescore TASK-216"
            )

        # Signal B: BSIP1 sub_pool=puffed + grain-type primary ingredient
        if not _extrusion_signal_fired and _sub_pool in INDUSTRIAL_PUFFED_SUBPOOLS:
            _first_ingredient = str(ingredients[0]).strip() if ingredients else ""
            _signal_b = any(grain in _first_ingredient for grain in GRAIN_PRIMARY_INGREDIENTS_HE)
            if _signal_b:
                _extrusion_signal_fired = True
                _extrusion_signal_source = (
                    f"EV-043 Signal-B: sub_pool=puffed + grain_primary_ingredient='{_first_ingredient}' "
                    f"— BSIP1 enricher confirmed industrial puffing category; grain base + industrial "
                    f"direct-expansion = NOVA 4; approved for salty-snacks rescore TASK-216"
                )

    if _extrusion_signal_fired:
        evidence_for.append(_extrusion_signal_source)
        _extrusion_conf = round(max(0.20, 0.80 - (0.20 if _ingredient_data_degraded else 0.0)), 2)
        return {
            "nova_level": 4,
            "nova_confidence": _extrusion_conf,
            "nova_confidence_band": "high" if _extrusion_conf >= 0.75 else "medium",
            "nova_evidence_for": evidence_for,
            "nova_evidence_against": evidence_against,
            "nova_uncertainty_notes": confidence_penalties + [
                "EV-043 extrusion signal: industrial high-temperature direct-expansion is a "
                "structural NOVA 4 process regardless of additive count; "
                "signal approved for salty-snacks rescore (TASK-216); "
                "full engine promotion requires Product Agent D7 co-sign",
                "NOVA inference is a proxy; validated NOVA classification requires expert ingredient analysis",
            ],
        }

    # ---------------------------------------------------------------------------
    # BSIP2-HC-001 — Processed dairy (גבינה מותכת / מעובדת) → NOVA 4
    # ---------------------------------------------------------------------------
    # Two sub-rules for processed/reconstituted dairy products.
    #
    # Sub-rule A (original): Modified starch (E1442, E1422, E1440 etc.) in a dairy
    # matrix with ≥2 additive categories.  Modified starch cannot exist in a natural
    # or artisan cheese; its presence requires industrial recombination of the
    # protein/fat matrix.
    #
    # Sub-rule B (TASK-REDLABEL-001, 2026-06-08): Phosphate emulsifying salts
    # (E339, E450, E451, E452) in a dairy/cheese matrix.  Emulsifying salts are the
    # defining ingredient of processed cheese — they melt and reconstitute the casein
    # matrix into a uniform product (Codex CXS 283-1978).  They are NEVER present in
    # natural or artisan cheese; their presence unconditionally signals NOVA 4.
    #
    # Critical distinction from carrageenan (E407): carrageenan stabilises fat-reduced
    # cheeses without reconstituting the protein matrix.  Fat-reduced yellow cheese
    # with carrageenan but no phosphate salts is NOVA 3 (processed), not NOVA 4.
    # Sub-rule B therefore uses phosphate salt detection only, NOT tax_emulsifier_concern.
    #
    # Scope extension: product_type_dairy checks "חלב"/"גבינת" in the first 3 ingredients
    # but misses "גבינה" (absolute form) as first ingredient in processed cheese ("גבינה
    # טבעית 60%").  HC-001 adds a separate "cheese_base" check on the first ingredient.
    #
    # The fermentation signal reflects the cheese BASE, not the reconstituted product.
    # Evidence: Monteiro NOVA 4 framework; Codex CXS 283-1978;
    # Bari corpus audit 2026-06-08 (3 processed cheeses misclassified as NOVA 3).
    # ---------------------------------------------------------------------------

    _tax_modified_starch = l3_signals.get("tax_modified_starch", False)
    _sprint1_count_for_nova = l3_signals.get("sprint1_additive_count", 0)
    _product_type_dairy = l3_signals.get("product_type_dairy", False)

    # For HC-001: use the full ingredient text (list joined OR raw text) so the
    # phosphate salt detector fires even when ingredients_list is null/absent in BSIP1.
    _ing_text_for_hc001 = (
        " ".join(str(i) for i in ingredients)
        if ingredients
        else (product.get("ingredients_text_he") or "")
    )
    _first_ing_for_hc001 = str(ingredients[0]).lower() if ingredients else _ing_text_for_hc001[:30].lower()
    # Extended dairy/cheese matrix detection
    _is_cheese_base_matrix = (
        _product_type_dairy
        or "גבינה" in _first_ing_for_hc001
        or "גבינה" in (product.get("ingredients_text_he") or "")[:30].lower()
    )

    _has_phosphate_salt = bool(PHOSPHATE_EMULSIFYING_SALT_RE.search(_ing_text_for_hc001))

    # Sub-rule A: modified starch in dairy (original, unconditional — matches prior behavior).
    # Uses _product_type_dairy only (original scope, unchanged for flag-OFF safety).
    _hc001_a = _tax_modified_starch and _sprint1_count_for_nova >= 2 and _product_type_dairy
    # Sub-rule B: phosphate emulsifying salt in cheese matrix (TASK-REDLABEL-001, new).
    # Gated by RECAL_P0_ON so flag-OFF behavior is byte-identical to the baseline.
    # Uses _is_cheese_base_matrix (extended scope: catches "גבינה טבעית" first-ingredient).
    _hc001_b = (RECAL_P0_ON and _has_phosphate_salt and _is_cheese_base_matrix)

    if _hc001_a or _hc001_b:
        _hc001_rule = "A (modified_starch)" if _hc001_a else "B (phosphate_emulsifying_salt)"
        _hc001_signal = (
            "tax_modified_starch=True"
            if _hc001_a
            else "phosphate_emulsifying_salt detected (E339/E450/E451/E452 or נתרן פוספט)"
        )
        evidence_for.append(
            f"BSIP2-HC-001 sub-rule {_hc001_rule}: {_hc001_signal} + dairy/cheese matrix "
            "→ NOVA 4; industrial reconstitution of protein/fat matrix confirmed "
            "(processed cheese archetype); fermentation reflects cheese base input, "
            "not reconstituted product; NOVA 4 per Monteiro (TASK-REDLABEL-001)"
        )
        return {
            "nova_level": 4,
            "nova_r4_demotion_applied": False,
            "nova_confidence": 0.82,
            "nova_confidence_band": "high",
            "nova_evidence_for": evidence_for,
            "nova_evidence_against": evidence_against,
            "nova_uncertainty_notes": confidence_penalties + [
                f"BSIP2-HC-001 sub-rule {_hc001_rule}: processed/reconstituted dairy rule; "
                "fermentation evidence from cheese base does not override this classification",
                "NOVA inference is a proxy; validated NOVA classification requires "
                "expert ingredient analysis",
            ],
        }

    # EV-009 / EV-010: extruded-shape early detection.
    # If the product name matches an extruded/shaped cereal pattern, assert NOVA 3 immediately.
    # Runs before the full score-based classifier so a product with a missing ingredient list
    # (empty ingredient signals → nova4_score≈0 → would land at NOVA 2 by default) is still
    # correctly placed at NOVA 3 based on its production method.
    _product_name_he = (product.get("canonical_name_he") or product.get("product_name_he") or "").strip()
    _is_extruded_shape = any(sig in _product_name_he for sig in EXTRUDED_SHAPE_NAME_SIGNALS)
    if _is_extruded_shape:
        evidence_for.append(
            "EV-010: extruded_shape_name_signal fired ('פתיתים אפויים') — "
            "industrial extrusion + shaping + bake = NOVA 3 per EV-009 disrupted-grain classification; "
            "Nutrition ruling 2026-06-05"
        )
        return {
            "nova_level": 3,
            "nova_confidence": round(max(0.20, 0.55 - (0.25 if _ingredient_data_degraded else 0.0)), 2),
            "nova_confidence_band": "medium" if not _ingredient_data_degraded else "low",
            "nova_evidence_for": evidence_for,
            "nova_evidence_against": evidence_against,
            "nova_uncertainty_notes": confidence_penalties + [
                "EV-010 name-detection: 'פתיתים אפויים' confirms extrusion/shaping; "
                "EV-010 full scoring signal pending D7 co-sign (follow-up scope)",
                "NOVA inference is a proxy; validated NOVA classification requires expert ingredient analysis",
            ],
        }

    # ---------------------------------------------------------------------------
    # Classify by score
    # ---------------------------------------------------------------------------
    if nova4_score >= 4:
        level = 4
        base_conf = 0.80
    elif nova4_score >= 2:
        # Could be NOVA 3 or 4 — check for NOVA 3 signals
        nova3_cats = additive_cats & set(NOVA3_SIGNALS)
        if nova4_score >= 3:
            level = 4
            base_conf = 0.65
        else:
            level = 3
            base_conf = 0.60
    elif additive_count >= 1 or added_sugar_ct >= 1 or ing_count > 5:
        # Some processing signals but not ultra-processed
        level = 3
        base_conf = 0.55
        evidence_for.append(f"additive_categories: {additive_count}, added_sugars: {added_sugar_ct}")
    else:
        # Minimal processing signals
        level = 2
        base_conf = 0.50
        evidence_for.append("minimal_additives_and_processing_signals")

    # ---------------------------------------------------------------------------
    # Confidence adjustments
    # ---------------------------------------------------------------------------
    if ing_quality in ("corrupted", "missing", "malformed"):
        base_conf -= 0.20
        confidence_penalties.append(f"ingredient_quality={ing_quality}: confidence reduced")
    if _prov_source == "bsip1_text_fallback":
        base_conf -= 0.25
        confidence_penalties.append("provenance=bsip1_text_fallback: ingredient list reconstructed from page text, not label; NOVA inference unreliable")
    if ing_count == 0:
        base_conf -= 0.30
        confidence_penalties.append("no_ingredient_list: NOVA inference unreliable")

    nova_confidence = max(0.20, min(0.95, base_conf))

    # R4 — NOVA-3→2 demotion guard for PLAIN DAIRY (TASK-169, EV-024/026 lineage).
    # Demote a tentative 3 back to 2 ONLY when the product is a plain dairy base with no
    # flavor/sweetener/added-sugar and no genuine ultra-processing additive marker
    # (thickener/gum/emulsifier/humectant/flavor/color). Never promotes a 4. Gated.
    nova_demotion_applied = False
    product_type_dairy = l3_signals.get("product_type_dairy", False)
    if RECAL_P0_ON and level == 3 and product_type_dairy:
        # R4 v1.1 — a declared flavoring (even a whole-food one: garlic/dill/herbs/…) makes
        # this a FLAVORED VARIANT and forfeits the plain-dairy retention. This only blocks a
        # demotion (keeps tentative NOVA 3 at 3); it never promotes and never demotes new.
        name = (product.get("canonical_name_he") or product.get("product_name_he") or "")
        hay = name + " " + " ".join(str(i) for i in ingredients)
        has_flavor_variant = any(m in hay for m in FLAVORED_VARIANT_MARKERS_HE)
        is_plain = (added_sugar_ct == 0 and not has_sweetener
                    and not has_flavor_enhancer and not has_color
                    and not has_flavor_variant)
        # BSIP2-HC-002 (TASK-REDLABEL-001) — natural colorant exclusion from R4 blocking.
        # The "color" additive_cat fires for BOTH natural pigments (annatto, beta-carotene,
        # turmeric) AND synthetic dyes.  Natural colorants are NOT markers of ultra-processing
        # (NOVA framework: the relevant criterion is industrial additives absent from home
        # cooking, not natural pigments).  When the ONLY color signal is a natural colorant
        # (has_artificial_color == False), remove "color" from the blocking set so that R4
        # can demote a plain dairy from NOVA 3 to NOVA 2.  Synthetic dyes (has_artificial_color
        # == True) continue to block demotion as before.
        has_artificial_color_r4 = l3_signals.get("has_artificial_color", has_color)
        if "color" in additive_cats and not has_artificial_color_r4:
            # natural colorant only — strip from blocking (does not indicate ultra-processing)
            blocking_cats = set(additive_cats) - {"color"}
        else:
            blocking_cats = set(additive_cats)
        blocking = blocking_cats & set(NOVA_DEMOTE_BLOCKING_ADDITIVE_CATS)
        if is_plain and not blocking:
            level = 2
            nova_demotion_applied = True
            _nat_color_note = (
                " (natural colorant excluded from blocking: annatto/β-carotene are not "
                "ultra-processing markers per NOVA framework — BSIP2-HC-002)"
                if ("color" in additive_cats and not has_artificial_color_r4) else ""
            )
            evidence_against.append(
                "R4 plain-dairy demotion 3→2: dairy base, no flavor/sweetener/added-sugar, "
                "no flavored-variant marker, no ultra-processing additive marker "
                "(salt/culture/rennet/calcium/vitamins only)" + _nat_color_note)
        elif has_flavor_variant:
            evidence_for.append(
                "R4 v1.1: flavored/seasoned dairy variant → NOVA-2 retention forfeited (stays 3)")

    if nova_confidence >= 0.75:
        band = "high"
    elif nova_confidence >= 0.50:
        band = "medium"
    else:
        band = "low"

    return {
        "nova_level": level,
        "nova_r4_demotion_applied": nova_demotion_applied,
        "nova_confidence": round(nova_confidence, 2),
        "nova_confidence_band": band,
        "nova4_signal_score": nova4_score,
        "nova_evidence_for": evidence_for,
        "nova_evidence_against": evidence_against,
        "nova_uncertainty_notes": confidence_penalties + [
            "NOVA inference is a proxy; validated NOVA classification requires expert ingredient analysis",
            "Hebrew ingredient text keyword matching has limited coverage for novel additive names",
        ],
    }
