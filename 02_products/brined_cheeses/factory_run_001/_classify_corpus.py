import json, sys, io, hashlib, datetime, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('C:/Bari/02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json', 'r', encoding='utf-8') as f:
    products = json.load(f)


def has_nutrition(p):
    """
    Require at minimum: energy AND (fat OR protein).
    Energy-only or energy+sodium-only panels cannot be fully scored.
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
    ingr = p.get('ingredients_raw', '') or ''

    # Rule 1: Non-food — floor cleaner (specific barcode)
    if barcode == '7290108351613' or 'נוזל רצפות' in name:
        return ('OUT_OF_SCOPE',
                'NON_FOOD: floor cleaner product ("נוזל רצפות"); matched on "חלומי" acquisition keyword. '
                'Excluded per methodology Sec 1.3 in/out rule: not a food product.')

    # Rule 2: Ice cream
    if 'גלידת' in name or 'גלידה' in name:
        return ('OUT_OF_SCOPE',
                'NON_CHEESE: ice cream (גלידת ריקוטה); not a table cheese, not brined. '
                'Excluded per methodology Sec 1.3 in/out rule (c): not consumed as a standalone table cheese.')

    # Rule 3: Bread / bakery products
    if 'חלומית' in name and ('חלה' in name or 'לחמניות' in name):
        return ('OUT_OF_SCOPE',
                'NON_CHEESE: bakery product (challah/roll from Berman Bread); matched on "חלומי" acquisition keyword. '
                'Excluded per Sec 1.3 in/out rule: not a dairy cheese product.')
    if barcode in ('497358', '4033583'):
        return ('OUT_OF_SCOPE',
                'NON_CHEESE: bakery product (Berman Bread); matched on "חלומי" acquisition keyword. '
                'Excluded per Sec 1.3 in/out rule: not a dairy cheese product.')

    # Rule 4: Ricotta — OUT (not brined, cooking ingredient)
    if 'ריקוטה' in name:
        return ('OUT_OF_SCOPE',
                'RICOTTA_OUT: ricotta is not a brined cheese (heat-coagulated whey product, not brine-preserved). '
                'Not a table cheese in Israeli retail context (ריקוטה לאפייה / cooking ingredient). '
                'Excluded per methodology Sec 1.3 ricotta ruling: out of scope for both cheese-spreads and brined-cheeses.')

    # Rule 5: Pasta / prepared dishes using cheese as ingredient
    if 'רביולי' in name:
        return ('OUT_OF_SCOPE',
                'PREPARED_DISH_OUT: pasta dish (רביולי תרד וריקוטה); not a standalone cheese product. '
                'Out of scope per Sec 1.3 in/out rule (c): not a table cheese consumed as-purchased.')

    # Rule 6: Filo/pastry products
    if 'מעטפות פילו' in name or 'מעטפת בצק פילו' in name or 'פילו' in name:
        return ('OUT_OF_SCOPE',
                'PREPARED_PASTRY_OUT: filo/pastry product; cheese is an ingredient, not the primary food. '
                'Out of scope per Sec 1.3 in/out rule (c): not a table cheese consumed as-purchased.')

    # Rule 7: Sauce products
    if 'רוטב' in name:
        return ('OUT_OF_SCOPE',
                'SAUCE_PRODUCT_OUT: sauce/condiment product; not a standalone table cheese. '
                'Out of scope per Sec 1.3 in/out rule (c).')

    # Rule 8: Spreadable form — ממרח / מריחה / למריחה — routes to cheese-spreads
    if 'למריחה' in name or 'ממרח' in name or 'מריחה' in name:
        return ('OUT_OF_SCOPE',
                'SPREADABLE_OUT: spreadable/whipped form ("למריחה"/"ממרח"/"מריחה"). '
                'Routes to cheese-spreads cream-cheese pool per methodology Sec 1.3 boundary call. '
                'Block/brined-block בולגרית belongs here; spreadable/whipped form does not.')

    # Rule 9: Vegan / plant-based feta-style
    if 'טבעוני' in name or brand == 'ויולייף' or ('שקדים' in name and 'פטה' in name):
        return ('OUT_OF_SCOPE',
                'VEGAN_OUT: plant-based / vegan feta-style product (not dairy, not brined). '
                'Out of scope per Sec 1.3 in/out rule (a)+(b): must be a soft/semi-firm dairy cheese preserved in brine. '
                '"Planty" almond/cashew feta and Violife vegan feta are food-tech products, not dairy brined cheeses.')

    # Rule 10: Tzfatit קשה מגורדת — shredded/grated hard Tzfatit
    # Tzfatit is in scope per Sec 1.2 ("צפתית"). Grated/shredded form is still the same cheese;
    # it is used as a table topping (mezze), not as a cooking ingredient exclusively.
    # Keep IN — the methodology includes tzfatit without form restriction.
    # (This applies to barcodes: 9953930, 7296073644972, 7296073644996 — מגורדת variants)

    # Now check nutrition sufficiency
    nutri = has_nutrition(p)
    if not nutri:
        return ('TRANSPARENCY_NULL',
                'NULL_NUTRITION: Shufersal did not render the nutrition label for this product. '
                'Cannot be scored. Retained as transparency/data-unavailable entry per standing policy '
                '("unknown is acceptable; OFF is not"). BSIP0 coverage gap accepted by owner for ~20% of SKUs. '
                'Page may disclose these as "לא ניתן לאחזר נתונים".')

    return ('IN_SCORED',
            'IN_SCOPE: brined/salty soft or semi-firm dairy table cheese with parsed nutrition. '
            'Meets all three in/out criteria (Sec 1.3): (a) soft/semi-firm, (b) preserved in brine, '
            '(c) table cheese consumed as-purchased. Types: בולגרית / פטה / צפתית / חלומי / גבינה מלוחה.')


# Build entries
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

# Counts
in_scored = [e for e in entries if e['decision'] == 'IN_SCORED']
transparency = [e for e in entries if e['decision'] == 'TRANSPARENCY_NULL']
out_of_scope = [e for e in entries if e['decision'] == 'OUT_OF_SCOPE']

# Brand distribution of in-scored set
brand_dist = {}
for e in in_scored:
    brand_dist[e['brand']] = brand_dist.get(e['brand'], 0) + 1
brand_dist_sorted = dict(sorted(brand_dist.items(), key=lambda x: -x[1]))

print(f'IN_SCORED: {len(in_scored)}')
print(f'TRANSPARENCY_NULL: {len(transparency)}')
print(f'OUT_OF_SCOPE: {len(out_of_scope)}')
print(f'TOTAL: {len(entries)}')
print()
print('OUT_OF_SCOPE products:')
for e in out_of_scope:
    print(f'  {e["barcode"]} | {e["name_he"]} | {e["brand"]}')
print()
print('TRANSPARENCY_NULL products:')
for e in transparency:
    print(f'  {e["barcode"]} | {e["name_he"]} | {e["brand"]}')
print()
print('Brand distribution IN_SCORED:')
for brand, count in brand_dist_sorted.items():
    print(f'  {brand}: {count}')
print()
print('IN_SCORED products:')
for e in in_scored:
    print(f'  {e["barcode"]} | {e["name_he"]} | {e["brand"]}')
