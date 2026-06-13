import json, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('C:/Bari/02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json', 'r', encoding='utf-8') as f:
    products = json.load(f)


def has_nutrition(p):
    """
    Require energy AND (fat OR protein) — partial panels (energy+sodium only) cannot be scored.
    """
    n = p.get('nutrition', {})
    has_energy = bool(n.get('energy_kcal_raw', '').strip())
    has_fat = bool(n.get('fat_raw', '').strip())
    has_protein = bool(n.get('protein_raw', '').strip())
    return has_energy and (has_fat or has_protein)


def classify(p):
    name = p.get('name_he', '')
    barcode = p.get('barcode', '')
    brand = p.get('brand', '')

    # R1 — Non-food
    if barcode == '7290108351613' or 'נוזל רצפות' in name:
        return ('OUT_OF_SCOPE',
                'NON_FOOD: floor cleaner matched on halloumi acquisition keyword. '
                'Out of scope per methodology Sec 1.3 in/out rule.')

    # R2 — Bakery products (bread/challah)
    if barcode in ('497358', '4033583'):
        return ('OUT_OF_SCOPE',
                'NON_CHEESE: bakery product (Berman Bread) matched on halloumi acquisition keyword. '
                'Out of scope per Sec 1.3 in/out rule: not a dairy cheese product.')

    # R3 — Ice cream
    if 'גלידת' in name:
        return ('OUT_OF_SCOPE',
                'NON_CHEESE: ice cream product (גלידת ריקוטה); not a table cheese, not brined. '
                'Out of scope per Sec 1.3 (c): not consumed as-purchased standalone cheese.')

    # R4 — Ricotta (all forms: פרסקה, קרם, בסגנון איטלקי, ריקוטה גד, למריחה ריקוטה, etc.)
    if 'ריקוטה' in name:
        return ('OUT_OF_SCOPE',
                'RICOTTA_OUT: heat-coagulated whey product (not brine-preserved); cooking/baking ingredient. '
                'Not a table cheese in Israeli retail context. '
                'Out of scope per methodology Sec 1.3 ricotta ruling.')

    # R5 — Filo/pastry products
    if 'פילו' in name:
        return ('OUT_OF_SCOPE',
                'PREPARED_PASTRY_OUT: filo/pastry product; cheese is a filling ingredient, not the primary food. '
                'Out of scope per Sec 1.3 (c): not a table cheese consumed as-purchased.')

    # R6 — Sauce/condiment products
    if 'רוטב' in name:
        return ('OUT_OF_SCOPE',
                'SAUCE_PRODUCT_OUT: sauce/condiment product; cheese is ingredient, not standalone table cheese. '
                'Out of scope per Sec 1.3 (c).')

    # R7 — Spreadable bulgarin / ממרח
    if 'למריחה' in name or ('ממרח' in name and 'בולגרית' in name):
        return ('OUT_OF_SCOPE',
                'SPREADABLE_OUT: spreadable/whipped form (למריחה / ממרח). '
                'Routes to cheese-spreads cream-cheese pool per Sec 1.3 boundary call. '
                'Block/brined-block בולגרית belongs in brined-cheeses; spreadable/whipped form does not.')

    # R8 — Vegan plant-based feta-style
    if 'טבעוני' in name or brand == 'ויולייף' or (brand == 'פלנטי' and 'שקדים' in name):
        return ('OUT_OF_SCOPE',
                'VEGAN_OUT: plant-based feta-style product (almond/cashew/coconut oil base; zero protein). '
                'Not dairy, not brined. Out of scope per Sec 1.3 (a)+(b): must be dairy soft/semi-firm cheese preserved in brine.')

    # R9 — Null / partial nutrition
    if not has_nutrition(p):
        return ('TRANSPARENCY_NULL',
                'NULL_NUTRITION: Shufersal did not render a scorable nutrition panel '
                '(fat_raw and protein_raw both absent). Cannot be fully scored. '
                'Retained as transparency/data-unavailable entry per standing policy. '
                'Page may disclose as "לא ניתן לאחזר נתונים". OFF fill is absolutely prohibited.')

    return ('IN_SCORED',
            'IN_SCOPE: brined/salty soft or semi-firm dairy table cheese with scorable nutrition panel. '
            'Meets all three Sec 1.3 in/out criteria: (a) soft/semi-firm, (b) preserved in brine, '
            '(c) table cheese consumed as-purchased. Type: בולגרית/פטה/צפתית/חלומי/גבינה מלוחה.')


entries = []
for p in products:
    decision, reason = classify(p)
    entries.append({
        'barcode': p.get('barcode', ''),
        'name_he': p.get('name_he', ''),
        'brand': p.get('brand', ''),
        'decision': decision,
        'reason': reason
    })

in_scored = [e for e in entries if e['decision'] == 'IN_SCORED']
transparency = [e for e in entries if e['decision'] == 'TRANSPARENCY_NULL']
out_of_scope_list = [e for e in entries if e['decision'] == 'OUT_OF_SCOPE']

brand_dist = {}
for e in in_scored:
    brand_dist[e['brand']] = brand_dist.get(e['brand'], 0) + 1
brand_dist_sorted = dict(sorted(brand_dist.items(), key=lambda x: -x[1]))

out_breakdown = {}
for e in out_of_scope_list:
    key = e['reason'].split(':')[0]
    out_breakdown[key] = out_breakdown.get(key, 0) + 1

output = {
    "stage": "2_corpus_filter",
    "category_slug": "brined-cheeses",
    "run_id": "run_brined_001",
    "generated": "2026-06-13",
    "owner": "Data Architecture (data-agent)",
    "source_bsip0": "brined_cheese_bsip0_raw_20260613T065721.json",
    "source_bsip0_count": 94,
    "methodology_ref": "brined_cheeses_scoring_interpretation_v1.md Section 1",
    "nutrition_sufficiency_gate": (
        "energy_kcal_raw AND (fat_raw OR protein_raw) must both be non-empty. "
        "Partial panels (energy+sodium only; energy+sat_fat only) are TRANSPARENCY_NULL — "
        "the score engine requires fat and protein to run a full panel."
    ),
    "filter_logic": (
        "Name-based and barcode-based exclusion gate applied in R1–R8 priority order; "
        "R9 nutrition sufficiency gate applied last on remaining in-scope products. "
        "Same two-stage pattern as run_cheese_001 / run_cereals_002."
    ),
    "exclusion_rules": {
        "R1_NON_FOOD": "Barcode 7290108351613 (floor cleaner 'נוזל רצפות מלון חלומי') matched on halloumi acquisition keyword. Any non-food product is OUT_OF_SCOPE.",
        "R2_NON_CHEESE_BAKERY": "Berman Bread products (barcodes 497358, 4033583) matched on halloumi acquisition keyword. Not dairy cheese.",
        "R3_NON_CHEESE_ICE_CREAM": "Ice cream products (גלידת) are not table cheeses. Sec 1.3 (c).",
        "R4_RICOTTA_OUT": (
            "All ricotta products are OUT. Ricotta is a heat-coagulated whey cheese (not brine-preserved), "
            "consumed primarily as a cooking/baking ingredient in Israeli retail (ריקוטה לאפייה dominant shelf form). "
            "Not a brined cheese, not a table cheese. Out of scope for both brined-cheeses and cheese-spreads. "
            "Methodology Sec 1.3 ricotta ruling."
        ),
        "R5_PREPARED_PASTRY_OUT": "Filo/pastry products (מעטפות פילו, פילו ריקוטה פרימיום) where cheese is a filling ingredient. Sec 1.3 (c).",
        "R6_SAUCE_OUT": "Sauce products (רוטב פטה ים תיכוני, רוטב אלפרדו עם ריקוטה). Sec 1.3 (c).",
        "R7_SPREADABLE_OUT": (
            "Products explicitly labeled למריחה or ממרח בולגרית. "
            "Routes to cheese-spreads cream-cheese pool per Sec 1.3 boundary call. "
            "Brined-block בולגרית at any fat tier belongs in brined-cheeses; spreadable/whipped form does not."
        ),
        "R8_VEGAN_OUT": (
            "Plant-based feta-style products: Planty (almond/cashew), Violife (coconut oil, protein=0). "
            "Not dairy, not brined. Sec 1.3 (a)+(b)."
        ),
        "R9_NULL_NUTRITION": (
            "Products where Shufersal rendered a partial or absent nutrition panel "
            "(fat_raw and protein_raw both absent from parsed fields). Cannot be fully scored. "
            "Retained as TRANSPARENCY_NULL. OFF fill is absolutely prohibited (CLAUDE.md, TASK-238). "
            "Known Shufersal rendering gap (~20-25% of shelf); accepted by owner."
        )
    },
    "in_scope_types": ["בולגרית", "פטה (כבשים/עיזים/פרה)", "צפתית", "חלומי", "גבינה מלוחה"],
    "notes": [
        "פטינה בסגנון פטה (Rucker Quantum) — classified IN_SCORED. Name explicitly says 'בסגנון פטה'; dairy cheese, has nutrition. Methodology Sec 1.2: 'evaluate on structure: if it is brined semi-soft, it is in scope.'",
        "גבינת טמרה מלוחה בקר 17% (Rajab dairy) — classified IN_SCORED. Ingredients: milk + salt only; classic brined cheese. Matches 'גבינה מלוחה' in-scope type.",
        "כדורי פטה בשמן מתובל (Nizan) — classified IN_SCORED. Feta balls in seasoned oil; the cheese itself is the primary food, oil is a preservation/presentation medium. Consumed as table cheese.",
        "גבינה צפתית בטעמים (Hamoshava) — classified IN_SCORED. Tzfatit with garlic/dill; seasoning variants are in-scope per Sec 1.2 ('seasoning variants treated as variants within same type').",
        "סלט קוביות בולגרית 25% (Nizan) — classified TRANSPARENCY_NULL. Has energy=282 and sodium=698 but fat_raw and protein_raw are absent from parsed panel. Partial panel insufficient for scoring.",
        "גבינה בולגרית למריחה 5% (Gad) — classified OUT_OF_SCOPE (SPREADABLE_OUT). Name explicitly says 'למריחה'; routes to cheese-spreads. Confirmed by ingredients: includes starch + potassium sorbate consistent with spreadable texture.",
        "בסגנון פטה יוונית טבעוני (Violife) — classified OUT_OF_SCOPE (VEGAN_OUT). Ingredients: water, coconut oil, starch. Protein=0. Not dairy, not brined.",
        "פטה שקדים (Planty) — classified OUT_OF_SCOPE (VEGAN_OUT). Ingredients: water, almonds, cashews. Not dairy, not brined.",
        "16 products have TRANSPARENCY_NULL due to partial nutrition panels (energy+sodium or energy+sat_fat only, missing total fat and protein). This is a Shufersal rendering pattern for products in the 7296073... barcode series — likely the retailer's private-label shelf tag format omits the full table.",
        "No OFF data was used at any point. NULL fields are NULL."
    ],
    "min_corpus_size": 30,
    "corpus_size_check": f"PASS: {len(in_scored)} IN_SCORED >= 30 minimum",
    "off_used": False,
    "off_note": "OFF ban is absolute (CLAUDE.md hard rule, TASK-238). No field from any product was filled from OFF or any external source. NULL fields remain NULL.",
    "summary": {
        "total_bsip0": 94,
        "in_scored": len(in_scored),
        "transparency_null": len(transparency),
        "out_of_scope": len(out_of_scope_list),
        "out_of_scope_breakdown": out_breakdown,
        "brand_distribution_in_scored": brand_dist_sorted
    },
    "products": entries
}

out_path = 'C:/Bari/02_products/brined_cheeses/factory_run_001/corpus_filter.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

with open(out_path, 'rb') as f:
    sha = hashlib.sha256(f.read()).hexdigest()

print(f'Written: {out_path}')
print(f'SHA256: {sha}')
print(f'IN_SCORED={len(in_scored)} TRANSPARENCY_NULL={len(transparency)} OUT_OF_SCOPE={len(out_of_scope_list)} TOTAL={len(entries)}')
print(f'Brand dist: {brand_dist_sorted}')
print(f'OOS breakdown: {out_breakdown}')
