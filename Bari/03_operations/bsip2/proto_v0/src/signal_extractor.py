"""
BSIP2 Prototype v0 — Signal Extractor
Extracts L1-L6 signals from a BSIP1 product without modifying it.
All inferences are labelled by taxonomy layer and carry explicit uncertainty.
"""
import re
from input_loader import get_nutrition, get_ingredients, get_ingredients_text, get_trust

# ---------------------------------------------------------------------------
# Hebrew ingredient keyword lists
# ---------------------------------------------------------------------------

# Added sugar markers (SC classification: SC-3 through SC-5 signals)
ADDED_SUGAR_MARKERS_HE = [
    "סוכר",             # sugar
    "סירופ גלוקוזה",    # glucose syrup
    "סירופ גלוקוז",     # glucose syrup (variant)
    "סירופ גלוקוז-פרוקטוז",  # glucose-fructose syrup
    "סירופ גלוקוזה-פרוקטוזה",
    "פרוקטוזה",         # fructose
    "דקסטרוזה",         # dextrose
    "מולסה",            # molasses
    "סירופ תמרים",      # date syrup (SC-4)
    "סירופ מייפל",      # maple syrup
    "סוכר קנים",        # cane sugar
    "סוכר חום",         # brown sugar
    "סירופ סוכר",       # sugar syrup
    "סירופ אגבה",       # agave syrup
    "מלטוז",            # maltose
    "לקטוז",            # lactose (not added, but sugar)
    "סירופ תירס",       # corn syrup
    "סירופ קרמל",       # caramel syrup
    "אינברטי",          # inverted sugar
    "ריבה",             # jam
    "רכז פרות",         # fruit concentrate (SC-4)
    "מיץ פרות מרוכז",   # concentrated fruit juice (SC-4)
    "דבש",              # honey
    "אגבה",             # agave
    "פרי",              # fruit (weaker signal)
]

ADDED_SUGAR_MARKERS_EN = ["glucose", "fructose", "dextrose", "maltose", "sucrose",
                          "syrup", "honey", "molasses"]

# Sweetener markers (non-nutritive)
SWEETENER_MARKERS_HE = [
    "אספרטם", "סוכרלוזה", "סוכרלוז", "אצסולפם",
    "סטביה", "נאוטאם", "אדוונטאם", "נאוהספרידין",
    "ממתיק",        # general sweetener
    "סוכרין",       # saccharin
    "ציקלמאט",      # cyclamate
    "סורביטול",     # sorbitol (sugar alcohol, mild sweetener)
    "מניטול",       # mannitol
    "קסיליטול",     # xylitol
    "אריתריטול",    # erythritol
    "מלטיטול",      # maltitol
    "איזומאלט",     # isomalt
]
SWEETENER_E_NUMBERS = [
    "E-420", "E-421", "E-950", "E-951", "E-952", "E-953",
    "E-954", "E-955", "E-960", "E-961", "E-962", "E-965",
    "E-966", "E-967", "E-968",
    "E420", "E421", "E950", "E951", "E952", "E953",
    "E954", "E955", "E960", "E961", "E965", "E966", "E967",
]

# Additive category markers (each detection = +1 additive marker)
ADDITIVE_MARKER_PATTERNS = [
    # Emulsifiers
    (r"מתחלב|לציטין|E-322|E322|E-471|E471|E-472|E472|E-476|E476|E-481|E481", "emulsifier"),
    # Stabilizers
    (r"מייצב|קרגינן|גואר|גומי|E-407|E407|E-410|E410|E-412|E412|E-415|E415|E-440|E440", "stabilizer"),
    # Thickeners
    (r"מסמיך|עמילן מוקשה|עמילן משונה|E-1400|E-1404|E-1410|E-1412|E-1414|E-1420|E-1422|E-1440|E-1442|E-1450", "thickener"),
    # Preservatives
    (r"חומר שימור|שומר טריות|E-200|E200|E-202|E202|E-210|E210|E-211|E211|E-220|E220|E-250|E250|E-252|E252", "preservative"),
    # Antioxidants
    (r"מעכב חמצון|טוקופרול|E-300|E300|E-301|E301|E-302|E302|E-306|E306|E-307|E307|E-308|E308|E-309|E309|E-310|E310|E-320|E320|E-321|E321", "antioxidant"),
    # Humectants
    (r"חומר הלחה|גליצרין|גליצרול|סורביטול|E-422|E422", "humectant"),
    # Acidity regulators
    (r"מווסת חומציות|חומצה ציטרית|חומצת לימון|E-330|E330|E-331|E331|E-332|E332|E-333|E333|E-334|E334", "acidity_regulator"),
    # Colors
    (r"צבע מאכל|E-1[0-9]{2}|E-[0-9]{3}(?= )|קרוטן|קרמל|כורכום|טרטרזין|אנתוציאנין", "color"),
    # Flavor enhancers / artificial flavors — strongest NOVA 4 signal
    (r"חומרי טעם וריח|טעמים מלאכותיים|ונילין|ואניל|E-621|E621|E-627|E627|E-631|E631|E-635|E635", "flavor_enhancer"),
    # Leavening agents (weaker signal)
    (r"חומר מתפיח|E-500|E500|E-501|E501|E-503|E503|E-450|E450|E-451|E451|E-452|E452|סודה", "leavening_agent"),
    # Flour treatment agents
    (r"E-300|E-920|E920|חומר הוספה לקמח", "flour_treatment"),
]

# Seed oil markers
SEED_OIL_MARKERS_HE = [
    "שמן חמניות",   # sunflower oil
    "שמן קנולה",    # canola oil
    "שמן תירס",     # corn oil
    "שמן סויה",     # soy oil
    "שמן צמחי",     # vegetable oil (often seed oil blend)
    "שמנים צמחיים", # vegetable oils
]

# Palm oil markers (flagged separately, not seed oil)
PALM_OIL_MARKERS_HE = [
    "שמן דקל", "שמן קוקוס", "שומן קוקוס", "שמן דקל אדום",
    "דקל",      # palm (when in fat context)
    "קוקוס",    # coconut (when in fat context)
]

# Whole grain markers
WHOLE_GRAIN_MARKERS_HE = [
    "דגנים מלאים", "חיטה מלאה", "שיבולת שועל מלאה",
    "אורז מלא", "קמח מלא", "קמח חיטה מלא", "שעורה מלאה",
    "גרגרים מלאים", "תירס מלא",
    # Bakery additions
    "שיפון מלא", "קמח שיפון מלא",   # whole rye flour (common in crispbread/sourdough)
    "כוסמין",                         # spelt (inherently whole grain in Israeli usage)
    "כוסמת",                          # buckwheat
]

# Fermentation markers
FERMENTATION_MARKERS_HE = [
    "תרבויות חיות", "תרביות חיות", "חיידקים פרוביוטיים",
    "לקטובציל", "בידפידוס", "חומצה לקטית", "חמץ",
    "מחמצת", "ספיח", "שמר",
]

# Protein isolate markers
PROTEIN_ISOLATE_MARKERS_HE = [
    "חלבון מי גבינה", "חלבון סויה", "חלבון חיטה",
    "חלבון אפונה", "חלבון ביצה", "חלבון קזאין",
    "אבקת חלב",   # milk powder — mixed signal
    "קזאין",
    "אייזולאט", "איזולאט",
]

# Fruit concentrate markers (SC-4: treated as added sugar)
FRUIT_CONCENTRATE_MARKERS_HE = [
    "רכז", "תרכיז", "מיץ מרוכז", "רכז פרות",
    "סירופ תמרים", "סירופ תפוחים", "סירופ ענבים",
]


def _search(text: str, patterns: list[str]) -> list[str]:
    """Return list of matched patterns (case-insensitive, multiline)."""
    found = []
    combined_text = text.lower()
    for p in patterns:
        if p.lower() in combined_text:
            found.append(p)
    return found


def _search_re(text: str, patterns: list[tuple]) -> dict[str, bool]:
    """Search regex patterns; return {category: True} for matched categories."""
    found = {}
    for pattern, category in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found[category] = True
    return found


def extract_signals(product: dict) -> dict:
    """
    Extract all signal layers for a product.
    Returns a structured dict with L1-L6 layers.
    All fields are explicit: None means absent, not zero.
    """
    nn = get_nutrition(product)
    ingredients = get_ingredients(product)
    ing_text = get_ingredients_text(product)
    trust_level, trust_score = get_trust(product)

    # -----------------------------------------------------------------------
    # L1: Observed facts (direct from BSIP1 — no inference)
    # -----------------------------------------------------------------------
    l1 = {
        "energy_kcal":      nn["energy_kcal"],
        "fat_g":            nn["fat_g"],
        "fat_saturated_g":  nn["fat_saturated_g"],
        "fat_trans_g":      nn["fat_trans_g"],
        "sodium_mg":        nn["sodium_mg"],
        "carbohydrates_g":  nn["carbohydrates_g"],
        "sugars_g":         nn["sugars_g"],
        "dietary_fiber_g":  nn["dietary_fiber_g"],
        "protein_g":        nn["protein_g"],
        "ingredient_count": len(ingredients),
        "ingredient_list":  ingredients,
        "ingredient_text_quality": product.get("ingredient_text_quality"),
        "bsip1_trust_level":  trust_level,
        "bsip1_trust_score":  trust_score,
        "bsip1_risk_flags":   product.get("canonical_risk_flags") or [],
        "nutrition_consistency_status": product.get("nutrition_consistency_status"),
        "nutrition_consistency_warnings": product.get("nutrition_consistency_warnings") or [],
        "missing_nutrition_fields": [
            f for f in ["energy_kcal","fat_g","fat_saturated_g","sodium_mg",
                        "carbohydrates_g","sugars_g","dietary_fiber_g","protein_g"]
            if nn.get(f) is None
        ],
    }

    # Data consistency checks
    kcal  = nn["energy_kcal"]
    sugar = nn["sugars_g"]
    carbs = nn["carbohydrates_g"]
    sat_f = nn["fat_saturated_g"]
    fat   = nn["fat_g"]

    l1["consistency_checks"] = {
        "sugar_le_carbs":  None if (sugar is None or carbs is None) else (sugar <= carbs),
        "satfat_le_fat":   None if (sat_f is None or fat is None)   else (sat_f <= fat),
        "kcal_plausible":  None if kcal is None else (20 <= kcal <= 700),
    }

    # -----------------------------------------------------------------------
    # L2: Derived metrics (deterministic math on L1, never re-inferred)
    # -----------------------------------------------------------------------
    fat_pct_kcal = (fat * 9 / kcal * 100) if (fat is not None and kcal and kcal > 0) else None
    sat_frac     = (sat_f / fat) if (sat_f is not None and fat and fat > 0) else None
    sugar_carb_r = (sugar / carbs) if (sugar is not None and carbs and carbs > 0) else None
    prot_per_kcal = (nn["protein_g"] / kcal) if (nn["protein_g"] is not None and kcal and kcal > 0) else None

    l2 = {
        "fat_pct_of_kcal":       round(fat_pct_kcal, 2) if fat_pct_kcal is not None else None,
        "saturated_fat_fraction": round(sat_frac, 3)     if sat_frac is not None else None,
        "sugar_to_carb_ratio":   round(sugar_carb_r, 3) if sugar_carb_r is not None else None,
        "protein_per_kcal":      round(prot_per_kcal, 4) if prot_per_kcal is not None else None,
        "derivation_notes": [
            "fat_pct_of_kcal = (fat_g * 9 / energy_kcal) * 100",
            "saturated_fat_fraction = fat_saturated_g / fat_g",
            "sugar_to_carb_ratio = sugars_g / carbohydrates_g",
            "protein_per_kcal = protein_g / energy_kcal",
        ],
    }

    # -----------------------------------------------------------------------
    # L3: Inferred classifications (judgment required, confidence explicit)
    # -----------------------------------------------------------------------
    full_text = ing_text + " " + " ".join(ingredients)

    # Sweetener detection
    sweetener_matches = _search(full_text, SWEETENER_MARKERS_HE)
    sweetener_e = [e for e in SWEETENER_E_NUMBERS if e.lower() in full_text.lower()]
    has_sweetener = bool(sweetener_matches or sweetener_e)

    # Additive marker detection
    additive_categories = _search_re(full_text, ADDITIVE_MARKER_PATTERNS)
    # flavor_enhancer is the strongest NOVA 4 signal
    has_flavor_enhancer = additive_categories.get("flavor_enhancer", False)
    has_color = additive_categories.get("color", False)
    additive_marker_count = len(additive_categories)
    additive_categories_list = sorted(additive_categories.keys())

    # Seed oil
    seed_oil_matches = _search(full_text, SEED_OIL_MARKERS_HE)
    has_seed_oil = bool(seed_oil_matches)

    # Palm oil
    palm_oil_matches = _search(full_text, PALM_OIL_MARKERS_HE)
    has_palm_oil = bool(palm_oil_matches)

    # Whole grain
    whole_grain_matches = _search(full_text, WHOLE_GRAIN_MARKERS_HE)
    has_whole_grain = bool(whole_grain_matches)

    # Protein source
    isolate_matches = _search(full_text, PROTEIN_ISOLATE_MARKERS_HE)
    if isolate_matches:
        protein_source = "mixed"   # likely mixed whole+isolate
        protein_source_basis = isolate_matches
    elif nn["protein_g"] and nn["protein_g"] > 0:
        protein_source = "whole_food"
        protein_source_basis = ["no isolate markers detected"]
    else:
        protein_source = "unknown"
        protein_source_basis = ["insufficient protein signal"]

    # Added sugar sources (for SC classification and MULTIPLE_ADDED_SUGAR_MARKERS)
    added_sugar_matches = [m for m in ADDED_SUGAR_MARKERS_HE
                          if m in full_text and m != "דבש"]  # honey is SC-2 adjacent
    added_sugar_count = len(added_sugar_matches)

    # Fruit concentrate (SC-4 signal)
    fruit_conc_matches = _search(full_text, FRUIT_CONCENTRATE_MARKERS_HE)
    has_fruit_concentrate = bool(fruit_conc_matches)

    # Fermentation
    ferm_matches = _search(full_text, FERMENTATION_MARKERS_HE)
    has_fermentation = bool(ferm_matches)

    # Trans fat flag
    # fat_trans_g == 0.5 exactly is the Israeli nutritional labeling convention for "< 1g"
    # (mandatory declaration threshold). Treat as a possible artifact, not a confirmed real signal.
    trans_fat_g = nn["fat_trans_g"]
    if trans_fat_g is not None and trans_fat_g > 1.0:
        trans_fat_status = "veto"
    elif trans_fat_g is not None and trans_fat_g > 0.5:
        trans_fat_status = "high_concern"
    elif trans_fat_g is not None and trans_fat_g == 0.5:
        trans_fat_status = "threshold_declaration"
    elif trans_fat_g is not None and trans_fat_g > 0.2:
        trans_fat_status = "present"
    else:
        trans_fat_status = "not_detected"
    trans_fat_threshold_artifact = (trans_fat_g == 0.5)

    # Israeli red labels (Israeli Ministry of Health thresholds)
    red_labels = []
    if sugar is not None and sugar > 17.5:
        red_labels.append("sugar")
    if sat_f is not None and sat_f > 5.0:
        red_labels.append("sat_fat")
    if nn["sodium_mg"] is not None and nn["sodium_mg"] > 600:
        red_labels.append("sodium")

    # Hyper-palatability patterns (raw compositional check; NOVA gate applied in score_engine)
    hp_fat_sugar_raw = (
        fat_pct_kcal is not None and fat_pct_kcal >= 30 and
        sugar is not None and sugar >= 20
    )
    hp_fat_sodium_raw = (
        fat_pct_kcal is not None and fat_pct_kcal >= 25 and
        nn["sodium_mg"] is not None and nn["sodium_mg"] >= 300
    )

    l3 = {
        "sweetener_detected":       has_sweetener,
        "sweetener_matches":        sweetener_matches + sweetener_e,
        "additive_marker_count":    additive_marker_count,
        "additive_categories":      additive_categories_list,
        "has_flavor_enhancer":      has_flavor_enhancer,
        "has_artificial_color":     has_color,
        "has_seed_oil":             has_seed_oil,
        "seed_oil_matches":         seed_oil_matches,
        "has_palm_oil":             has_palm_oil,
        "palm_oil_matches":         palm_oil_matches,
        "has_whole_grain":          has_whole_grain,
        "whole_grain_matches":      whole_grain_matches,
        "protein_source":           protein_source,
        "protein_source_basis":     protein_source_basis,
        "added_sugar_sources_count": added_sugar_count,
        "added_sugar_matches":      added_sugar_matches[:8],  # cap list for readability
        "has_fruit_concentrate":    has_fruit_concentrate,
        "has_fermentation":         has_fermentation,
        "trans_fat_status":         trans_fat_status,
        "trans_fat_threshold_declaration_possible": trans_fat_threshold_artifact,
        "red_labels":               red_labels,
        "red_label_count":          len(red_labels),
        "hp_fat_sugar_pattern_raw": hp_fat_sugar_raw,
        "hp_fat_sodium_pattern_raw": hp_fat_sodium_raw,
        "inference_confidence_notes": [
            "Ingredient analysis uses keyword matching on Hebrew text — may miss transliterations or abbreviations",
            "Sweetener detection relies on known Hebrew/E-number terms; novel sweeteners not in dictionary will be missed",
            "Additive count reflects distinct functional categories detected, not total additive instances",
        ],
    }

    # -----------------------------------------------------------------------
    # L4: Interpreted concerns (threshold-based guardrail decisions)
    # Populated by score_engine; listed here as placeholders for trace clarity
    # -----------------------------------------------------------------------
    l4 = {
        "note": "L4 interpreted concerns are evaluated in score_engine and written to caps_applied / penalties_applied",
        "pre_evaluation_flags": [],
    }
    if l1["consistency_checks"]["sugar_le_carbs"] is False:
        l4["pre_evaluation_flags"].append("SUGAR_EXCEEDS_CARBS: data integrity concern, score confidence reduced")
    if l1["consistency_checks"]["satfat_le_fat"] is False:
        l4["pre_evaluation_flags"].append("SATFAT_EXCEEDS_FAT: data integrity concern, score confidence reduced")
    if l1["consistency_checks"]["kcal_plausible"] is False:
        l4["pre_evaluation_flags"].append("KCAL_IMPLAUSIBLE: outside 20-700 range, confidence severely reduced")
    if product.get("nutrition_consistency_status") == "suspicious":
        l4["pre_evaluation_flags"].append("BSIP1_SUSPICIOUS_NUTRITION: product may have per-serving/per-100g confusion")
    if product.get("nutrition_consistency_status") == "warnings":
        l4["pre_evaluation_flags"].append("BSIP1_NUTRITION_WARNINGS: cross-retailer disagreement detected")

    # -----------------------------------------------------------------------
    # L5: Behavioral hypotheses embedded in the scoring model
    # -----------------------------------------------------------------------
    l5 = {
        "hypotheses_active": [
            "High added sugar (>17.5g) correlates with poorer glycemic outcomes at population level",
            "NOVA 4 ultra-processed foods associate with poorer health outcomes at population level (epidemiological evidence)",
            "HP patterns (fat+sugar, fat+sodium) may override satiety signaling",
            "Whole grain presence modulates glycemic response",
            "Low calorie density (within whole-food context) associates with lower energy intake",
        ],
        "hypothesis_limitations": [
            "Per-100g frame does not reflect actual consumption volume",
            "Individual product does not establish population-level risk",
            "HP patterns rely on compositional thresholds, not behavioral evidence for specific product",
        ],
    }

    # -----------------------------------------------------------------------
    # L6: Normative / policy decisions embedded in the scoring architecture
    # -----------------------------------------------------------------------
    l6 = {
        "policy_commitments": [
            "NOVA 1 single-ingredient whole foods receive minimum score of 75 (normative floor, not empirical)",
            "Sweetener presence caps score at 70 regardless of other signals (policy commitment: sweeteners ≠ quality improvement)",
            "Trans fat veto (score=0) is a hard safety commitment, not a continuous signal",
            "Israeli red labels are incorporated as regulatory signals (policy: regulatory alignment)",
            "Whole-food floors override architecture-mismatch caps (SRC-01 policy)",
        ],
        "architecture_version": "bsip2_concept_v1 + score_resolution_contract_SRC-v1",
    }

    return {
        "L1_observed_signals":        l1,
        "L2_derived_signals":         l2,
        "L3_inferred_classifications": l3,
        "L4_interpreted_concerns":    l4,
        "L5_behavioral_hypotheses":   l5,
        "L6_policy_decisions":        l6,
    }
