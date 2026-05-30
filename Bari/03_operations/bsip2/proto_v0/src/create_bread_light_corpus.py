"""
BSIP2 Bread-Light Stress Test Corpus Generator

Creates 32 synthetic BSIP1-format product records across 6 groups:
  A — Simple baselines (clean reference anchors)
  B — Wholegrain halo (laundering via grain tokens + isolated fiber)
  C — Seed halo (surface seeding on refined matrix)
  D — Sourdough / fermentation spectrum (genuine → industrial fake)
  E — Engineered wellness bakery (protein / keto / fiber systems)
  F — Highly processed / kids (hyper-palatable, structural void)

Philosophy: include deceptive, mediocre, and structurally confusing products.
Not a "healthy products" corpus — ontology pressure corpus.

Output: C:\\Bari\\03_operations\\bsip1\\run_bread_light_001\\output\\
"""

import json
import re
import sys
import pathlib

OUTPUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_light_001\output")

# ---------------------------------------------------------------------------
# Signal lists (mirror signal_extractor.py for enrichment metadata)
# ---------------------------------------------------------------------------
_FERMENTATION_KW = ["מחמצת", "שמרים", "חומצה לקטית", "תרבויות", "חיידקים"]
_PROTEIN_ISO_KW  = ["חלבון מי גבינה", "חלבון אפונה", "חלבון סויה", "גלוטן חיטה",
                     "חלבון חלב", "קזאין", "אייזולאט"]
_MATRIX_KW       = ["אינולין", "psyllium", "psyllium husk", "סיבי תאית", "בטא-גלוקן",
                     "סיבי חיטה", "גואר", "קסנטן"]
_ADDITIVE_E_RE   = re.compile(r"E-\d{3}|E\d{3}")
_SWEETENER_KW    = ["אריתריטול", "סוכרלוזה", "E-955", "E955", "סטביה", "ממתיק"]
_ADDITIVE_CATS   = [
    (r"לציטין|E-322|E322|E-471|E471|E-476|E476", "emulsifier"),
    (r"E-450|E450|E-451|E451|E-500|E500|E-501|E501|חומר מתפיח", "leavening_agent"),
    (r"E-282|E282|E-211|E211|חומר שימור|שומר טריות", "preservative"),
    (r"E-621|E621|E-627|E627|E-631|E631", "flavor_enhancer"),
    (r"E-160|E160|E-100|E100|צבע מאכל|קרוטן", "color"),
    (r"E-412|E412|E-415|E415|E-410|E410|גואר|קסנטן|קרגינן", "stabilizer"),
    (r"E-300|E300|E-320|E320|E-321|E321|טוקופרול|מעכב חמצון", "antioxidant"),
    (r"E-920|E920|חומר הוספה לקמח", "flour_treatment"),
]


def _extract_enrichment(ing_text: str, ing_list: list[str]) -> dict:
    full = ing_text + " " + " ".join(ing_list)
    full_l = full.lower()

    fermentation = [k for k in _FERMENTATION_KW if k in full_l]
    protein_iso  = [k for k in _PROTEIN_ISO_KW  if k in full_l]
    matrix       = [k for k in _MATRIX_KW        if k in full_l]
    sweeteners   = [k for k in _SWEETENER_KW     if k in full_l]
    has_live     = any(w in full_l for w in ["תרבויות חיות", "חיידקים פרוביוטיים"])
    has_prebiotic = any(w in full_l for w in ["אינולין", "פרה-ביוטי", "psyllium"])
    has_prot_iso = bool(protein_iso)

    additive_cats: dict[str, bool] = {}
    for pattern, cat in _ADDITIVE_CATS:
        if re.search(pattern, full, re.IGNORECASE):
            additive_cats[cat] = True

    has_flavor_enh = additive_cats.get("flavor_enhancer", False)
    additive_count = len(additive_cats)

    return {
        "extracted_fermentation_markers": fermentation,
        "extracted_protein_markers":      protein_iso,
        "extracted_matrix_markers":       matrix,
        "extracted_sweeteners":           sweeteners,
        "extracted_additives":            sorted(additive_cats.keys()),
        "extracted_flavors":              [],
        "extracted_roasting_markers":     [],
        "enrichment_summary": {
            "ingredient_count_parsed":           len(ing_list),
            "additive_count":                    additive_count,
            "flavor_marker_count":               0,
            "sweetener_count":                   len(sweeteners),
            "protein_marker_count":              len(protein_iso),
            "matrix_marker_count":               len(matrix),
            "fermentation_marker_count":         len(fermentation),
            "roasting_marker_count":             0,
            "has_flavor_descriptor":             has_flavor_enh,
            "has_prebiotic_fiber":               has_prebiotic,
            "has_live_cultures":                 has_live,
            "has_protein_isolate_or_concentrate": has_prot_iso,
        },
    }


def _parse_ingredient_order(ing_text: str) -> list[dict]:
    parts = [p.strip() for p in re.split(r",|;", ing_text) if p.strip()]
    order = []
    for i, part in enumerate(parts, 1):
        pct = None
        m = re.search(r"\((\d+(?:\.\d+)?)\%\)", part)
        if m:
            pct = float(m.group(1))
        order.append({
            "position":             i,
            "text":                 part,
            "percentage_declared":  pct,
            "has_subgroup":         "(" in part and ")" in part and pct is None,
        })
    return order


def _make_product(
    barcode: str,
    name_he: str,
    brand: str,
    nn: dict,
    ing_text: str,
    claims: list[str],
    bread_subtype: str,
    group: str,
    design_note: str,
    allergens: list[str] | None = None,
) -> dict:
    ing_list = [p.strip() for p in re.split(r",|;", ing_text) if p.strip()]
    enrichment = _extract_enrichment(ing_text, ing_list)
    ingredient_order = _parse_ingredient_order(ing_text)

    pid = f"bsip1_bread_light_{barcode}"
    return {
        "schema_version":         "bsip1_v0_1",
        "file_type":              "product",
        "canonical_product_id":   pid,
        "barcode":                barcode,
        "canonical_name_he":      name_he,
        "canonical_name_en":      None,
        "brand":                  brand,
        "package_size_g":         None,
        "unit_count":             None,
        "unit_size_g":            None,
        "serving_size_g":         None,
        "country_of_origin":      None,
        "kosher_certification":   None,
        "image_url":              None,
        "source_retailers":       ["synthetic_bread_light_001"],
        "normalized_nutrition_per_100g": {
            **{k: None for k in ["energy_kcal","fat_g","fat_saturated_g","fat_trans_g",
                                   "sodium_mg","carbohydrates_g","sugars_g",
                                   "dietary_fiber_g","protein_g","cholesterol_mg"]},
            **nn,
        },
        "energy_source_unit":          "kcal",
        "ingredients_text_he":         ing_text,
        "ingredients_list":            ing_list,
        "ingredients_raw":             ing_text,
        "ingredients_raw_provenance": {
            "source": "synthetic_corpus",
            "bsip0_status": "synthetic",
            "populated_at": "bread_light_corpus_v1",
            "missing": False,
            "note": "Synthetic product designed for ontology stress testing",
        },
        "ingredient_order":       ingredient_order,
        "allergens_contains":     allergens or ["גלוטן"],
        "allergens_may_contain":  [],
        "claims":                 claims,
        "front_of_pack_claims":   claims,
        "confidence": {
            "identity_confidence":   "synthetic",
            "barcode_confidence":    "synthetic",
            "nutrition_confidence":  "synthetic_per_100g",
            "matched_by":            "synthetic_corpus",
            "observation_count":     1,
        },
        "barcode_validation_status":    "synthetic",
        "barcode_confidence_reason":    "Synthetic product for bread-light stress test corpus v1",
        "nutrition_basis_claimed":      "ל100 גרם",
        "nutrition_basis_detected":     "per_100g",
        "nutrition_consistency_status": "consistent",
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality":      "clean",
        "ingredient_warnings":          [],
        "canonical_trust_score":        0.75,
        "canonical_trust_level":        "medium",
        "canonical_risk_flags":         ["synthetic_product"],
        "conflicts_summary": {
            "count": 0, "has_unresolved": False,
            "fields_in_conflict": [], "identity_conflicts": [],
            "nutrition_conflicts": [], "ingredient_conflicts": [],
            "labeling_conflicts": [], "completeness_conflicts": [],
        },
        "missing_fields":    [],
        "inferred_fields":   [],
        "audit_ref":         f"synthetic_{pid}_audit.json",
        "bsip_bread_subtype": bread_subtype,
        "bsip_stress_group":  group,
        "bsip_design_note":   design_note,
        "enrichment_version": "bsip1_enrichment_v1",
        "enrichment_warnings": [],
        **enrichment,
    }


# ---------------------------------------------------------------------------
# Corpus definition — 32 products across 6 groups
# ---------------------------------------------------------------------------

CORPUS = [

    # ── GROUP A: Simple Baselines ──────────────────────────────────────────

    _make_product(
        barcode="9990001000001",
        name_he="קרקר מלוח פריך",
        brand="מיני גולד",
        nn=dict(energy_kcal=462, fat_g=19, fat_saturated_g=7, fat_trans_g=0.3,
                sodium_mg=640, carbohydrates_g=65, sugars_g=4, dietary_fiber_g=2, protein_g=7),
        ing_text="קמח חיטה, שמן דקל, מלח, סוכר, שמרים, לציטין סויה (E-322), E-471, נתרן ביקרבונט (E-500)",
        claims=[],
        bread_subtype="cracker_refined",
        group="A",
        design_note="Baseline refined cracker — Ritz-style. Refined flour first, palm oil, emulsifiers. "
                    "No nutritional pretense. NOVA 4. Structural void baseline.",
    ),
    _make_product(
        barcode="9990001000002",
        name_he="קרקר חיטה מלאה פשוט",
        brand="ויסה",
        nn=dict(energy_kcal=385, fat_g=4, fat_saturated_g=0.6, fat_trans_g=0.0,
                sodium_mg=320, carbohydrates_g=72, sugars_g=1, dietary_fiber_g=8, protein_g=11),
        ing_text="קמח חיטה מלאה (75%), קמח חיטה, מלח, שמרים, שמן זית (3%)",
        claims=["חיטה מלאה"],
        bread_subtype="cracker_wholegrain",
        group="A",
        design_note="Genuine whole wheat cracker baseline. Whole grain first (75%), minimal additives. "
                    "NOVA 3. Structural class B. Good reference point for grain integrity.",
    ),
    _make_product(
        barcode="9990001000003",
        name_he="לחמי קריספ שיפון פשוט",
        brand="וואסה",
        nn=dict(energy_kcal=352, fat_g=1.5, fat_saturated_g=0.2, fat_trans_g=0.0,
                sodium_mg=360, carbohydrates_g=71, sugars_g=1, dietary_fiber_g=10, protein_g=9),
        ing_text="קמח שיפון מלא (93%), מלח",
        claims=[],
        bread_subtype="rye_crispbread",
        group="A",
        design_note="Gold standard crispbread: 93% whole rye, salt only. NOVA 2. "
                    "Structural class A/B. Maximum grain integrity. Highest fiber from whole grain.",
    ),
    _make_product(
        barcode="9990001000004",
        name_he="עוגיות אורז ללא מלח",
        brand="בלה",
        nn=dict(energy_kcal=386, fat_g=2.5, fat_saturated_g=0.5, fat_trans_g=0.0,
                sodium_mg=5, carbohydrates_g=82, sugars_g=0, dietary_fiber_g=2, protein_g=7),
        ing_text="אורז מלא 100%",
        claims=["ללא מלח", "ללא גלוטן"],
        bread_subtype="rice_cake_plain",
        group="A",
        design_note="Plain rice cake — single ingredient. NOVA 2 but puffing process. "
                    "Structural class B (puffing fragments matrix). Low fiber despite whole grain. "
                    "Baseline for rice-format comparison.",
        allergens=["ללא גלוטן"],
    ),
    _make_product(
        barcode="9990001000005",
        name_he="לחם לבן פרוס פשוט",
        brand="אנגלו",
        nn=dict(energy_kcal=265, fat_g=3.5, fat_saturated_g=0.7, fat_trans_g=0.1,
                sodium_mg=420, carbohydrates_g=49, sugars_g=4, dietary_fiber_g=2, protein_g=8),
        ing_text="קמח חיטה, מים, סוכר, שמן צמחי, שמרים, מלח, E-471, E-481, חומר שימור E-282",
        claims=[],
        bread_subtype="white_bread_sliced",
        group="A",
        design_note="Industrial white bread baseline. Refined flour, added sugar, emulsifiers, preservative. "
                    "NOVA 4. Structural class D. No redeeming nutritional structure. Standard supermarket loaf.",
    ),

    # ── GROUP B: Wholegrain Halo ───────────────────────────────────────────

    _make_product(
        barcode="9990001000006",
        name_he='קרקרים "5 דגנים" ושיפון',
        brand="ריאל קרנץ'",
        nn=dict(energy_kcal=418, fat_g=6, fat_saturated_g=1.0, fat_trans_g=0.0,
                sodium_mg=580, carbohydrates_g=74, sugars_g=2, dietary_fiber_g=6, protein_g=10),
        ing_text="קמח חיטה, קמח שיפון, גרגרי שיפון (3%), שיבולת שועל, פלקס (2%), מלח, שמן סויה, לציטין (E-322), E-500",
        claims=["5 דגנים", "עשיר בסיבים", "מולטיגריין"],
        bread_subtype="multigrain_cracker",
        group="B",
        design_note="WHOLEGRAIN HALO — refined wheat flour listed first. '5 grain' grains are minor: "
                    "rye 3%, oats unlisted%, flax 2%. Fiber=6 is plausible but grain tokens, not whole-grain structure. "
                    "Classic marketing halo without structural commitment.",
    ),
    _make_product(
        barcode="9990001000007",
        name_he='קרקרים "מולטיגריין" עשיר בסיבים',
        brand="פייבר פלוס",
        nn=dict(energy_kcal=395, fat_g=5, fat_saturated_g=0.8, fat_trans_g=0.0,
                sodium_mg=490, carbohydrates_g=70, sugars_g=1, dietary_fiber_g=12, protein_g=9),
        ing_text="קמח חיטה, אינולין (10%), קמח שיבולת שועל, קמח שיפון (5%), מלח, שמן צמחי, E-450, E-500",
        claims=["12 גרם סיבים", "מולטיגריין", "עשיר בסיבים", "תומך בעיכול"],
        bread_subtype="fiber_enriched_cracker",
        group="B",
        design_note="FIBER LAUNDERING — 12g fiber from isolated inulin (10%). Refined flour first. "
                    "'Multigrain' from oat flour + rye flour (5%). All fiber can be attributed to extracted "
                    "chicory inulin, not structural grain. High fiber claim is technically accurate but structurally misleading.",
    ),
    _make_product(
        barcode="9990001000008",
        name_he='לחם "7 דגנים" תעשייתי',
        brand="כרמי",
        nn=dict(energy_kcal=258, fat_g=4, fat_saturated_g=0.8, fat_trans_g=0.0,
                sodium_mg=430, carbohydrates_g=47, sugars_g=4, dietary_fiber_g=4, protein_g=9),
        ing_text="קמח חיטה, קמח חיטה מלאה (25%), מים, גרגרי שבעה דגנים (4%), סוכר, שמן צמחי, שמרים, מלח, E-471, E-481, גלוטן חיטה, חומר שימור E-282, E-300",
        claims=["7 דגנים", "מחיטה מלאה", "טבעי"],
        bread_subtype="multigrain_bread_industrial",
        group="B",
        design_note="'7 GRAIN' HALO — refined wheat first, whole wheat only 25%, grain blend 4%. "
                    "Added vital gluten. Two preservatives (E-282 + E-300). "
                    "'מחיטה מלאה' claim on label legally valid but structurally misleading. "
                    "Maximum marketing halo with minimum structural commitment.",
    ),
    _make_product(
        barcode="9990001000009",
        name_he='לחם "100% חיטה מלאה" מעורב',
        brand="בית ברד",
        nn=dict(energy_kcal=255, fat_g=3, fat_saturated_g=0.5, fat_trans_g=0.0,
                sodium_mg=380, carbohydrates_g=47, sugars_g=1, dietary_fiber_g=5, protein_g=9),
        ing_text="קמח חיטה מלאה (50%), קמח חיטה (45%), מים, שמרים, מלח, שמן זית (2%), E-471",
        claims=["100% חיטה מלאה", "ללא חומרי שימור"],
        bread_subtype="wholegrain_bread_mixed",
        group="B",
        design_note="DECEPTIVE LABEL — front-of-pack says '100% whole wheat' but ingredient list is "
                    "50% whole wheat + 45% refined flour. First ingredient whole wheat gives legal cover. "
                    "Refined flour is almost equal. This is a structurally critical stress case: "
                    "fiber=5 is modest despite the claim.",
    ),
    _make_product(
        barcode="9990001000010",
        name_he='קרקר "בטא-גלוקן" תומך בלב',
        brand="ביו ויטל",
        nn=dict(energy_kcal=408, fat_g=7, fat_saturated_g=1.0, fat_trans_g=0.0,
                sodium_mg=510, carbohydrates_g=69, sugars_g=1, dietary_fiber_g=9, protein_g=10),
        ing_text="קמח שיבולת שועל (40%), קמח חיטה (35%), בטא-גלוקן שיבולת שועל (3%), אינולין (5%), מלח, שמן קנולה, לציטין (E-322), E-450",
        claims=["בטא-גלוקן", "מוריד כולסטרול", "סיבים גבוהים", "מאושר בריאות הלב"],
        bread_subtype="functional_cracker",
        group="B",
        design_note="FUNCTIONAL FIBER SYSTEM — real beta-glucan (3%) plus isolated inulin (5%). "
                    "Oat flour 40% + refined wheat 35%. Fiber=9 is a mix of genuine oat beta-glucan, "
                    "extracted concentrate, and inulin. Health claim requires distinguishing structural "
                    "beta-glucan from extracted inulin. Borderline legitimate.",
    ),
    _make_product(
        barcode="9990001000011",
        name_he='לחמי קריספ "14 גרם סיבים" תאית',
        brand="פיברנה",
        nn=dict(energy_kcal=365, fat_g=3, fat_saturated_g=0.5, fat_trans_g=0.0,
                sodium_mg=310, carbohydrates_g=67, sugars_g=0.5, dietary_fiber_g=14, protein_g=10),
        ing_text="קמח חיטה מלאה (60%), קמח חיטה (20%), סיבי תאית (8%), מלח, שמרים, שמן צמחי",
        claims=["14 גרם סיבים", "ללא סוכר", "מחיטה מלאה", "גבוה בסיבים"],
        bread_subtype="fiber_laundered_crispbread",
        group="B",
        design_note="FIBER LAUNDERING — 14g fiber headline. 8% is wood-pulp cellulose (סיבי תאית). "
                    "Whole wheat is 60% but refined wheat also present. Cellulose adds bulk without "
                    "nutritional structure or fermentability. Pure fiber inflation. This is a critical test case.",
    ),

    # ── GROUP C: Seed Halo ─────────────────────────────────────────────────

    _make_product(
        barcode="9990001000012",
        name_he='קרקרים "שבעת המינים" גרעינים',
        brand="שבעה מינים",
        nn=dict(energy_kcal=448, fat_g=14, fat_saturated_g=2.0, fat_trans_g=0.0,
                sodium_mg=590, carbohydrates_g=66, sugars_g=2, dietary_fiber_g=4, protein_g=9),
        ing_text="קמח חיטה, שמן סויה, מלח, גרגרי שיבולת שועל (4%), שומשום (3%), כוסמין (2%), זרעי פשתן (2%), זרעי חמנייה (2%), לציטין (E-322), E-471, E-500",
        claims=["שבעת המינים", "עשיר בגרעינים", "טבעי", "ארץ ישראל"],
        bread_subtype="seed_halo_cracker",
        group="C",
        design_note="SEED HALO — seeds total <15%, all in visually evocative packaging. "
                    "Refined wheat flour base. The '7 species' branding is cultural/religious marketing. "
                    "Seeds are cosmetic garnish, not structural components. Classic Israeli market deception.",
    ),
    _make_product(
        barcode="9990001000013",
        name_he="לחם גרעינים אמיתי",
        brand="גרעינים טבעיים",
        nn=dict(energy_kcal=298, fat_g=9, fat_saturated_g=1.2, fat_trans_g=0.0,
                sodium_mg=290, carbohydrates_g=42, sugars_g=1, dietary_fiber_g=7, protein_g=12),
        ing_text="קמח חיטה מלאה (55%), מים, שומשום (8%), זרעי חמנייה (7%), פשתן (5%), מלח, שמרים",
        claims=["עשיר בגרעינים", "ללא מוסיפים", "טבעי"],
        bread_subtype="genuine_seed_bread",
        group="C",
        design_note="GENUINE SEED BREAD — seeds ~20% structurally meaningful. Whole wheat base (55%). "
                    "No additives. Good product that LOOKS like seed-halo but ISN'T. "
                    "Key stress test: can the system distinguish 20% seeds from 3% seeds? "
                    "High protein (12g) from seed combination.",
    ),
    _make_product(
        barcode="9990001000014",
        name_he='קרקר "פשתן וצ\'יה" סופר-פוד',
        brand="סידס פלוס",
        nn=dict(energy_kcal=442, fat_g=13, fat_saturated_g=2.0, fat_trans_g=0.0,
                sodium_mg=570, carbohydrates_g=66, sugars_g=1, dietary_fiber_g=5, protein_g=8),
        ing_text="קמח חיטה (70%), שמן צמחי, זרעי פשתן (4%), זרעי צ'יה (3%), מלח, לציטין (E-322), E-471, E-500, טעם טבעי",
        claims=["אומגה 3", "פשתן וצ'יה", "סופר-פוד", "ברא-טבע"],
        bread_subtype="superfood_halo_cracker",
        group="C",
        design_note="SUPERFOOD SEED HALO — 'omega-3 from flax' marketing. Flax only 4%, chia only 3%. "
                    "Omega-3 contribution from 4% flax is ~160mg per 30g serving — marginal. "
                    "Refined flour 70% base with emulsifiers and artificial flavoring. "
                    "Premium pricing for negligible nutritional benefit from the headline seeds.",
    ),
    _make_product(
        barcode="9990001000015",
        name_he="לחמי קריספ שיפון וגרעינים נורדי",
        brand="נורדיק קריספ",
        nn=dict(energy_kcal=378, fat_g=11, fat_saturated_g=1.2, fat_trans_g=0.0,
                sodium_mg=290, carbohydrates_g=54, sugars_g=1, dietary_fiber_g=11, protein_g=13),
        ing_text="קמח שיפון מלא (65%), זרעי חמנייה (12%), זרעי פשתן (8%), זרעי שומשום (5%), מלח, שמרים",
        claims=["גרעינים מלאים", "עשיר בסיבים", "ללא תוספת סוכר"],
        bread_subtype="nordic_seed_crispbread",
        group="C",
        design_note="GENUINE NORDIC CRISPBREAD — seeds 25% structurally significant. Whole rye base (65%). "
                    "No additives. High fiber (11g) from real grain + seeds. High protein (13g). "
                    "This is a good product. Can the system reward it correctly vs the seed-halo products?",
    ),
    _make_product(
        barcode="9990001000016",
        name_he='קרקר "גרעינים זהובים" פרמיום',
        brand="ספיר",
        nn=dict(energy_kcal=450, fat_g=16, fat_saturated_g=2.5, fat_trans_g=0.0,
                sodium_mg=480, carbohydrates_g=66, sugars_g=5, dietary_fiber_g=3, protein_g=8),
        ing_text="קמח חיטה, שמן קנולה, זרעי שומשום מזהב (5%), מלח, דבש (2%), לציטין (E-322), E-471, E-481",
        claims=["גרעינים זהובים", "טבעי", "ללא GMO", "פרמיום"],
        bread_subtype="premium_seed_halo_cracker",
        group="C",
        design_note="PREMIUM SEED HALO — golden sesame visually dominant on packaging, only 5% by weight. "
                    "Honey at 2% adds naturalness halo. Refined base + canola oil + emulsifiers. "
                    "Premium price for cosmetic seeds. Classic upmarket deception pattern.",
    ),

    # ── GROUP D: Sourdough / Fermentation Spectrum ─────────────────────────

    _make_product(
        barcode="9990001000017",
        name_he="לחם מחמצת אמיתי ממחיטה מלאה",
        brand="מאפיית שמש",
        nn=dict(energy_kcal=248, fat_g=1.5, fat_saturated_g=0.2, fat_trans_g=0.0,
                sodium_mg=410, carbohydrates_g=48, sugars_g=0.5, dietary_fiber_g=5, protein_g=9),
        ing_text="קמח חיטה מלאה (60%), קמח חיטה (35%), מים, מחמצת חיה (15%), מלח",
        claims=["מחמצת אמיתית", "תסיסה ל-24 שעות", "ללא שמרים מסחריים", "עבודת יד"],
        bread_subtype="genuine_sourdough_bread",
        group="D",
        design_note="GENUINE SOURDOUGH — only leavening is live sourdough culture. No commercial yeast. "
                    "Whole wheat 60%. Long fermentation implied by process claim. "
                    "This is the gold standard sourdough. Can the system recognize it "
                    "vs industrial sourdough-style products?",
    ),
    _make_product(
        barcode="9990001000018",
        name_he="לחמי קריספ מחמצת שיפון מסורתי",
        brand="שיפון הצפון",
        nn=dict(energy_kcal=345, fat_g=1.0, fat_saturated_g=0.1, fat_trans_g=0.0,
                sodium_mg=380, carbohydrates_g=70, sugars_g=1, dietary_fiber_g=12, protein_g=8),
        ing_text="קמח שיפון מלא (90%), מחמצת שיפון (8%), מלח",
        claims=["מחמצת שיפון מסורתית", "ללא שמרים"],
        bread_subtype="sourdough_rye_crispbread",
        group="D",
        design_note="GENUINE SOURDOUGH CRISPBREAD — 90% whole rye + rye sourdough. Only 3 ingredients. "
                    "Highest fiber (12g) from structural grain. Authentic fermentation. "
                    "Fermentation protects the product — expect NOVA 2/3 routing. Strong structural class A/B.",
    ),
    _make_product(
        barcode="9990001000019",
        name_he='לחם "בסגנון מחמצת" תעשייתי',
        brand="בקרי",
        nn=dict(energy_kcal=262, fat_g=3, fat_saturated_g=0.6, fat_trans_g=0.0,
                sodium_mg=430, carbohydrates_g=49, sugars_g=2, dietary_fiber_g=2, protein_g=9),
        ing_text="קמח חיטה, מים, שמרים, מחמצת מגובשת (2%), מלח, גלוטן חיטה, E-471, E-481, חומר שימור E-282, חומצה לקטית",
        claims=["בטעם מחמצת", "בסגנון מסורתי", "מחמצת"],
        bread_subtype="industrial_sourdough_style",
        group="D",
        design_note="DECEPTIVE SOURDOUGH — 'מחמצת מגובשת' (dehydrated sourdough powder) at 2% is a "
                    "flavor ingredient, not a leavening system. Commercial yeast does the fermentation. "
                    "Lactic acid added chemically for sour taste. Two additives (E-471, E-481), preservative. "
                    "The sourdough claim is technically present but structurally meaningless.",
    ),
    _make_product(
        barcode="9990001000020",
        name_he='קרקר "מחמצת" בייצור מהיר',
        brand="קריספ מחמצת",
        nn=dict(energy_kcal=410, fat_g=8, fat_saturated_g=1.2, fat_trans_g=0.0,
                sodium_mg=510, carbohydrates_g=70, sugars_g=1, dietary_fiber_g=5, protein_g=9),
        ing_text="קמח חיטה (65%), קמח שיפון (20%), מחמצת (5%), מלח, שמן קנולה, E-450, E-500, חומצה לקטית",
        claims=["מחמצת", "תסיסה טבעית", "שיפון"],
        bread_subtype="quick_sourdough_cracker",
        group="D",
        design_note="MIXED FERMENTATION SIGNAL — 5% sourdough is real but chemical leaveners (E-450, E-500) "
                    "do the actual leavening work. Lactic acid added separately. The sourdough is a flavor "
                    "contributor, not a structural fermentation system. Routing should see: mחמצת present "
                    "but leavening_agent additives also present — ambiguous signal.",
    ),
    _make_product(
        barcode="9990001000021",
        name_he='לחם כפרי "מחמצת ושמרים"',
        brand="כפרי",
        nn=dict(energy_kcal=255, fat_g=4, fat_saturated_g=0.6, fat_trans_g=0.0,
                sodium_mg=390, carbohydrates_g=45, sugars_g=1, dietary_fiber_g=4, protein_g=9),
        ing_text="קמח חיטה מלאה (40%), קמח חיטה (50%), מים, שמרים (1.5%), מחמצת (8%), מלח, שמן זית (2%), E-471",
        claims=["מחמצת כפרית", "ביתי", "אמיתי", "כפרי"],
        bread_subtype="mixed_leaven_rustic_bread",
        group="D",
        design_note="MIXED LEAVENING SYSTEM — both sourdough (8%) and commercial yeast (1.5%). "
                    "'כפרי' (rustic/farmhouse) marketing. Refined wheat dominates (50% vs 40% whole). "
                    "Genuinely intermediate: sourdough is substantial but not sole leavening. "
                    "Fermentation semantics should distinguish this from pure sourdough.",
    ),

    # ── GROUP E: Engineered Wellness Bakery ────────────────────────────────

    _make_product(
        barcode="9990001000022",
        name_he='קרקר חלבון 30 "פרוטין קריספ"',
        brand="פרוטין קריספ",
        nn=dict(energy_kcal=395, fat_g=8, fat_saturated_g=1.0, fat_trans_g=0.0,
                sodium_mg=510, carbohydrates_g=42, sugars_g=0.5, dietary_fiber_g=5, protein_g=30),
        ing_text="קמח שיפון (35%), חלבון אפונה מבודד (20%), קמח חיטה (20%), גלוטן חיטה (10%), שמן קנולה, מלח, לציטין (E-322), E-471, E-450",
        claims=["30 גרם חלבון", "פחות פחמימות", "מושלם לאחר אימון", "צמחי"],
        bread_subtype="protein_engineered_cracker",
        group="E",
        design_note="ENGINEERED PROTEIN — pea protein isolate (20%) + vital wheat gluten (10%) creates "
                    "artificial protein density. The cracker matrix is a protein delivery vehicle with grain "
                    "as filler. Structural class E. The 30g protein is real but mechanistically assembled. "
                    "Tests whether the system penalizes protein engineering in bakery.",
    ),
    _make_product(
        barcode="9990001000023",
        name_he='לחם "קטו" דל פחמימות',
        brand="קטו בייק",
        nn=dict(energy_kcal=330, fat_g=27, fat_saturated_g=10, fat_trans_g=0.0,
                sodium_mg=380, carbohydrates_g=12, sugars_g=0.5, dietary_fiber_g=9, protein_g=11),
        ing_text="קמח שקדים (40%), psyllium husk (15%), ביצים, שמן קוקוס, אינולין (8%), אבקת אפייה, מלח, אריתריטול (5%), ממתיק: E-955",
        claims=["3 גרם פחמימות נטו", "ידידותי לקטו", "ללא גלוטן", "ללא דגנים"],
        bread_subtype="keto_bread",
        group="E",
        design_note="KETO BREAD SYSTEM — no cereal grains. Nut flour base (almond) + psyllium husk fiber + "
                    "inulin + erythritol + sucralose. Structurally mimics bread without grain matrix. "
                    "Fiber is 100% extracted. Sweetener present. Tests structural class interpretation "
                    "when the product lacks cereal backbone entirely.",
        allergens=["אגוזי עץ", "ביצים"],
    ),
    _make_product(
        barcode="9990001000024",
        name_he='לחמי קריספ חלבון ופשתן "17 גרם"',
        brand="פרוטין קריספ",
        nn=dict(energy_kcal=388, fat_g=7, fat_saturated_g=1.5, fat_trans_g=0.0,
                sodium_mg=410, carbohydrates_g=52, sugars_g=1, dietary_fiber_g=8, protein_g=17),
        ing_text="קמח שיפון מלא (45%), חלבון מי גבינה מרוכז (15%), קמח חיטה מלאה (20%), פשתן (8%), מלח, שמרים, לציטין (E-322)",
        claims=["17 גרם חלבון", "עשיר בפשתן", "ללא תוספת סוכר", "חיטה מלאה"],
        bread_subtype="protein_crispbread",
        group="E",
        design_note="ENGINEERED ON GENUINE BASE — good grain foundation (whole rye 45% + whole wheat 20%) "
                    "but whey protein concentrate (15%) added to boost protein. Hybrid between natural and "
                    "engineered. Flax (8%) is structurally significant. Tests whether the system "
                    "can credit the good base while flagging the protein engineering.",
    ),
    _make_product(
        barcode="9990001000025",
        name_he='לחם "ללא גלוטן" עמילן תפוחי אדמה',
        brand="גלוטן פרי",
        nn=dict(energy_kcal=272, fat_g=5, fat_saturated_g=1.0, fat_trans_g=0.0,
                sodium_mg=450, carbohydrates_g=52, sugars_g=3, dietary_fiber_g=2, protein_g=4),
        ing_text="עמילן תפוחי אדמה (35%), קמח אורז (25%), עמילן תירס (20%), שמן צמחי, מלח, שמרים, E-412 (גואר), E-415 (קסנטן), E-471, E-481, סוכר, חומר שימור E-282",
        claims=["ללא גלוטן", "מוסמך", "בריא"],
        bread_subtype="gluten_free_starch_bread",
        group="E",
        design_note="GLUTEN-FREE STRUCTURAL VOID — starch base (potato + corn + rice) with gum systems "
                    "(guar + xanthan) to simulate bread texture. Protein=4g, fiber=2g, preservative added. "
                    "'ללא גלוטן' claim on packaging implies health benefit it doesn't have. "
                    "Classic gluten-free trap: structurally poorer than standard refined bread.",
        allergens=["ללא גלוטן"],
    ),
    _make_product(
        barcode="9990001000026",
        name_he='קרקר "סיבים+" אינולין וסיליום',
        brand="ביו פייבר",
        nn=dict(energy_kcal=382, fat_g=6, fat_saturated_g=0.9, fat_trans_g=0.0,
                sodium_mg=480, carbohydrates_g=63, sugars_g=1, dietary_fiber_g=15, protein_g=9),
        ing_text="קמח חיטה (50%), אינולין מצ'יקורי (12%), קמח שיפון (15%), psyllium husk (5%), מלח, שמן קנולה, לציטין (E-322), E-450, E-500",
        claims=["15 גרם סיבים", "תומך בעיכול", "סיבים טבעיים", "צ'יקורי"],
        bread_subtype="fiber_system_cracker",
        group="E",
        design_note="FIBER SYSTEM — 15g fiber but: chicory inulin 12% + psyllium husk 5% = 17% extracted "
                    "fiber systems. Refined flour first. Rye only 15%. 'Naturally sourced' fiber is true "
                    "but non-structural. Tests fiber laundering detection at extreme fiber claims. "
                    "Most aggressive fiber engineering in corpus.",
    ),
    _make_product(
        barcode="9990001000027",
        name_he='לחם חלבון ואגוזים "נוטרישן"',
        brand="נוטרישן בייק",
        nn=dict(energy_kcal=365, fat_g=20, fat_saturated_g=3.0, fat_trans_g=0.0,
                sodium_mg=390, carbohydrates_g=22, sugars_g=1, dietary_fiber_g=6, protein_g=20),
        ing_text="קמח שקדים (25%), גלוטן חיטה (20%), קמח חיטה מלאה (15%), אגוזי מלך (10%), חלבון אפונה (10%), שמן זית, ביצים, מלח, E-450, שמרים",
        claims=["20 גרם חלבון", "אגוזים ושקדים", "ללא פחמימות ריקות", "מאוזן"],
        bread_subtype="protein_nut_bread",
        group="E",
        design_note="MULTI-ENGINEERED BAKERY — vital gluten (20%) + pea protein (10%) + almond flour (25%) "
                    "creates a protein-dense product (20g) with engineered fat profile. Real walnuts (10%). "
                    "Carbs=22g is genuinely low. This is a premium engineered system — "
                    "tests whether the system can recognize engineering even when some ingredients are real.",
        allergens=["גלוטן", "אגוזי עץ", "ביצים"],
    ),

    # ── GROUP F: Highly Processed / Kids ──────────────────────────────────

    _make_product(
        barcode="9990001000028",
        name_he='עוגיות אורז שוקולד "בלה שוקו"',
        brand="בלה",
        nn=dict(energy_kcal=398, fat_g=4, fat_saturated_g=2.0, fat_trans_g=0.0,
                sodium_mg=30, carbohydrates_g=83, sugars_g=12, dietary_fiber_g=2, protein_g=6),
        ing_text="אורז (85%), ציפוי שוקולד (15%): סוכר, חמאת קקאו, אבקת קקאו, לציטין סויה (E-322), ונילין",
        claims=["קל וקריספי", "בטעם שוקולד", "ללא גלוטן"],
        bread_subtype="chocolate_rice_cake",
        group="F",
        design_note="PUFFED + SWEETENED — simple rice cake baseline degraded by chocolate coating. "
                    "Sugar from coating pushes sugars to 12g. The rice base has nutritional value; "
                    "the coating subverts it. Tests how coating systems affect structural evaluation.",
        allergens=["ללא גלוטן"],
    ),
    _make_product(
        barcode="9990001000029",
        name_he='קרקרים מתוקים לילדים "גולדה קידס"',
        brand="גולדה קידס",
        nn=dict(energy_kcal=475, fat_g=22, fat_saturated_g=10, fat_trans_g=0.5,
                sodium_mg=680, carbohydrates_g=62, sugars_g=4, dietary_fiber_g=2, protein_g=7),
        ing_text="קמח חיטה, שמן דקל, עמילן תפוחי אדמה, מלח, אבקת גבינה (5%), חלב אבקה, E-621, צבע: E-160c, לציטין (E-322), E-471, E-481, ויטמין B1, ויטמין B2",
        claims=["בטעם גבינה", "מוסיף ויטמינים", "לילדים", "מבצע"],
        bread_subtype="kids_flavored_cracker",
        group="F",
        design_note="KIDS PRODUCT — palm oil, MSG (E-621), artificial color (E-160c), vitamin fortification "
                    "to mask nutritional poverty. Trans fat present (0.5g). High sat fat from palm. "
                    "Vitamin addition is compensation for nutritional stripping. "
                    "Tests HP reconstruction logic and fortification signal.",
    ),
    _make_product(
        barcode="9990001000030",
        name_he='פצפוצי דגנים "פצ\'פץ\'" בטעם דבש',
        brand="פצ'פץ'",
        nn=dict(energy_kcal=468, fat_g=15, fat_saturated_g=6, fat_trans_g=0.3,
                sodium_mg=520, carbohydrates_g=74, sugars_g=12, dietary_fiber_g=2, protein_g=6),
        ing_text="קמח תירס (70%), קמח חיטה (15%), סוכר, שמן דקל, דבש (2%), מלח, ארומה, לציטין (E-322), מעכב חמצון E-320, E-321, צבעי מאכל",
        claims=["דגנים טבעיים", "בטעם דבש", "ללא קולורנטים מלאכותיים"],
        bread_subtype="puffed_corn_snack",
        group="F",
        design_note="STRUCTURAL VOID — corn puff product. Honey at 2% is a flavor token justifying "
                    "'natural honey taste' marketing. BHA/BHT antioxidants (E-320/E-321) in cheap oil. "
                    "Trans fat from palm. 'ללא קולורנטים מלאכותיים' claim but has artificial flavoring. "
                    "Classic hyper-palatable corn snack in bakery format.",
    ),
    _make_product(
        barcode="9990001000031",
        name_he='לחמי קריספ "שום ועשבים" תעשייתי',
        brand="קריספי גארד",
        nn=dict(energy_kcal=445, fat_g=13, fat_saturated_g=2.0, fat_trans_g=0.0,
                sodium_mg=620, carbohydrates_g=68, sugars_g=2, dietary_fiber_g=3, protein_g=9),
        ing_text="קמח חיטה (65%), שמן קנולה (10%), אבקת גבינה (3%), ארומה שום (0.5%), E-621, E-627, E-631, מלח, לציטין (E-322), E-471, E-500",
        claims=["בטעם שום ועשבים", "קריספי לייט", "פרמיום"],
        bread_subtype="flavored_crispbread_industrial",
        group="F",
        design_note="UMAMI INDUSTRIAL SYSTEM — nucleotide flavor enhancers E-627 + E-631 with MSG (E-621). "
                    "These three together are the industrial umami trinity. Garlic content is 0.5% aroma, "
                    "not actual garlic. 'לייט' claim despite 445 kcal/100g and high fat. "
                    "Tests flavor enhancer detection and NOVA 4 classification.",
    ),
    _make_product(
        barcode="9990001000032",
        name_he='עוגיות אורז "חמאה" שמן דקל',
        brand="אורז לייט",
        nn=dict(energy_kcal=390, fat_g=8, fat_saturated_g=3.5, fat_trans_g=0.0,
                sodium_mg=420, carbohydrates_g=76, sugars_g=0.5, dietary_fiber_g=2, protein_g=6),
        ing_text="אורז (80%), שמן דקל (8%), ארומה חמאה, מלח, לציטין (E-322), E-471, מעכב חמצון E-320",
        claims=["קלוריות נמוכות", "ללא גלוטן", "בטעם חמאה"],
        bread_subtype="butter_rice_cake_industrial",
        group="F",
        design_note="RICE CAKE DEGRADED — plain rice cake baseline (A4) corrupted by palm oil addition, "
                    "butter flavoring (artificial), and BHA (E-320). 'Low calorie' claim misleading: "
                    "8% palm oil adds 72 kcal/100g vs plain version. "
                    "Tests whether the system detects palm oil + flavoring as a degradation signal.",
        allergens=["ללא גלוטן"],
    ),
]


# ---------------------------------------------------------------------------
# Write corpus to output directory
# ---------------------------------------------------------------------------

def write_corpus() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for product in CORPUS:
        barcode = product["barcode"]
        path = OUTPUT_DIR / f"bsip1_{barcode}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(product, f, ensure_ascii=False, indent=2)
        written += 1
        name_ascii = product['canonical_name_he'][:40].encode('utf-8').decode('utf-8')
        sys.stdout.buffer.write(f"  Written: {path.name}  [{product['bsip_stress_group']}] {name_ascii}\n".encode('utf-8'))

    print(f"\nCorpus complete: {written} products → {OUTPUT_DIR}")
    _write_manifest()


def _write_manifest() -> None:
    groups: dict[str, list] = {}
    for p in CORPUS:
        g = p["bsip_stress_group"]
        groups.setdefault(g, []).append(p)

    lines = ["# Bread-Light Corpus Manifest", "",
             f"**Version:** bread_light_v1  **Products:** {len(CORPUS)}", "",
             "| Group | Count | Purpose |",
             "|-------|-------|---------|",
             "| A | 5 | Simple baselines — clean reference anchors |",
             "| B | 6 | Wholegrain halo — grain tokens + isolated fiber |",
             "| C | 5 | Seed halo — surface seeding on refined matrix |",
             "| D | 5 | Sourdough spectrum — genuine → industrial fake |",
             "| E | 6 | Engineered wellness — protein / keto / fiber systems |",
             "| F | 5 | Highly processed / kids — hyper-palatable, structural void |",
             "", "## Products by Group", ""]

    group_labels = {
        "A": "Simple Baselines", "B": "Wholegrain Halo",
        "C": "Seed Halo", "D": "Sourdough/Fermentation",
        "E": "Engineered Wellness", "F": "Highly Processed/Kids"
    }
    for g, label in group_labels.items():
        lines.append(f"### Group {g} — {label}")
        for p in groups.get(g, []):
            lines.append(f"- **{p['canonical_name_he']}** ({p['brand']}): {p['bsip_design_note'][:80]}...")
        lines.append("")

    manifest_path = OUTPUT_DIR / "corpus_manifest.md"
    manifest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    write_corpus()
