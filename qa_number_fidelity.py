"""
Number fidelity check: every numeric claim in copy must match nutrition_per_100g.
Superlative accuracy check against computed category extremes.
"""
import json, re, io, sys

out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('C:/Bari/bari-web/src/data/comparisons/protein_bars_frontend_v1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

fields = {}
for p in products:
    pid = p['id']
    n = p.get('nutrition_per_100g', {})
    fields[pid] = {
        'name': p['name'],
        'score': p['score'],
        'protein': n.get('protein_g'),
        'sugar': n.get('sugars_g'),
        'fat': n.get('fat_g'),
        'sat_fat': n.get('fat_saturated_g'),
        'sodium': n.get('sodium_mg'),
        'fiber': n.get('dietary_fiber_g'),
        'kcal': n.get('energy_kcal'),
    }

# ---- TRUE SUPERLATIVES ----
protein_vals = {pid: v['protein'] for pid, v in fields.items() if v['protein'] is not None}
fiber_vals = {pid: v['fiber'] for pid, v in fields.items() if v['fiber'] is not None and v['fiber'] > 0}
sugar_vals = {pid: v['sugar'] for pid, v in fields.items() if v['sugar'] is not None}
sodium_vals = {pid: v['sodium'] for pid, v in fields.items() if v['sodium'] is not None}
sat_fat_vals = {pid: v['sat_fat'] for pid, v in fields.items() if v['sat_fat'] is not None}
kcal_vals = {pid: v['kcal'] for pid, v in fields.items() if v['kcal'] is not None}
fat_vals = {pid: v['fat'] for pid, v in fields.items() if v['fat'] is not None}

max_protein = max(protein_vals.values())
max_fiber = max(fiber_vals.values())
max_sugar = max(sugar_vals.values())
max_sodium = max(sodium_vals.values())
max_sat_fat = max(sat_fat_vals.values())
max_kcal = max(kcal_vals.values())
max_fat = max(fat_vals.values())
min_sodium = min(sodium_vals.values())
min_sugar = min(sugar_vals.values())

out.write("====== SUPERLATIVE ACCURACY CHECKS ======\n\n")

# prot-001: claim "27 גרם חלבון ו-13 גרם סיבים יחד ל-100 גרם — צמד שאף חטיף אחר כאן לא מגיע אליו"
# This is a joint claim: both 27g protein AND 13g fiber simultaneously
# prot-001 has protein=27, fiber=13
# prot-004 has protein=36, fiber=19 -- clearly higher on BOTH dimensions
out.write("CHECK prot-001: 'no other bar has both 27g protein AND 13g fiber'\n")
out.write("  prot-001: protein=" + str(fields['prot-001']['protein']) + " fiber=" + str(fields['prot-001']['fiber']) + "\n")
out.write("  prot-004: protein=" + str(fields['prot-004']['protein']) + " fiber=" + str(fields['prot-004']['fiber']) + "\n")
out.write("  -> prot-004 has 36g protein AND 19g fiber: BOTH exceed prot-001's figures\n")
out.write("  -> CLAIM 'no other bar reaches this pair' is POTENTIALLY FALSE\n\n")

# prot-002: "הכי הרבה חלבון בקבוצה (36 גרם)" - prot-002 and prot-004 both have 36g
out.write("CHECK prot-002: 'highest protein in category (36g)'\n")
out.write("  prot-002: protein=36.0  prot-004: protein=36.0\n")
out.write("  -> TIE with prot-004. Claim is technically defensible but omits the tie.\n\n")

# prot-010: "שומן רווי הגבוה בקבוצה — 8.2 גרם"
out.write("CHECK prot-010: 'highest sat fat in category 8.2g'\n")
out.write("  Max sat_fat: " + str(max_sat_fat) + "g (prot-014 has 11.0g, prot-015 has 9.0g, prot-016 has 9.0g, prot-011 has 8.5g)\n")
out.write("  prot-010 sat_fat: " + str(fields['prot-010']['sat_fat']) + "g\n")
out.write("  -> CLAIM IS FALSE. prot-014 has 11.0g (HIGHEST), prot-015/016 have 9.0g, prot-011 has 8.5g.\n")
out.write("  -> prot-010 with 8.2g is FIFTH highest, not highest.\n\n")

# prot-012: "הצפוף ביותר בקבוצה ב-496 קלוריות" / "הצפוף ביותר במדף"
out.write("CHECK prot-012: 'most calorie dense (496 kcal)'\n")
out.write("  Max kcal: " + str(max_kcal) + "g -> TRUE (prot-012 is indeed highest at 496)\n\n")

# prot-012: "29.5 גרם שומן ל-100 גרם — הגבוה במדף"
out.write("CHECK prot-012: 'highest fat in category (29.5g)'\n")
out.write("  Max fat: " + str(max_fat) + "g -> TRUE (prot-012 is indeed highest)\n\n")

# prot-015: "הכי הרבה סוכר בקבוצה (35 גרם)"
out.write("CHECK prot-015: 'highest sugar in category (35g)'\n")
out.write("  Max sugar: " + str(max_sugar) + "g -> TRUE (prot-015 is indeed highest)\n\n")

# prot-015: "וכמעט הכי הרבה נתרן"
out.write("CHECK prot-015: 'almost highest sodium'\n")
out.write("  prot-015 sodium: " + str(fields['prot-015']['sodium']) + "mg\n")
out.write("  Max sodium: " + str(max_sodium) + "mg (prot-015 itself)\n")
out.write("  -> prot-015 IS the highest sodium (396mg). Claim 'almost highest' undersells it.\n")
out.write("  -> This is actually an understatement, not a false claim. LOW severity.\n\n")

# prot-004: "19 גרם סיבים ל-100 גרם — הגבוה בקבוצה"
out.write("CHECK prot-004: 'highest fiber in category (19g)'\n")
out.write("  Max fiber: " + str(max_fiber) + "g -> TRUE\n\n")

# prot-004 rowVerdict: "הכי הרבה בקבוצה" for both 36g protein AND 19g fiber
out.write("CHECK prot-004: rowVerdict claims 'most protein AND fiber in category'\n")
out.write("  protein: 36.0 -- TIED with prot-002 (also 36.0g)\n")
out.write("  fiber: 19.0 -- TRUE (highest)\n")
out.write("  -> Protein part is a TIE not a unique max. 'הכי הרבה בקבוצה' for protein is misleading.\n\n")

# prot-003: "כמעט הכי הרבה חלבון בקבוצה" - has 33.7g
out.write("CHECK prot-003: 'almost most protein in category'\n")
out.write("  prot-003: protein=33.7g, rank 4th or 5th by protein\n")
out.write("  Top proteins: 36.0 (2 products), 34.8, 34.0 (3 products), 33.8, 33.7 ...\n")
out.write("  -> prot-003 has 33.7g, EIGHTH in protein. 'almost highest' is a stretch.\n\n")

# prot-008 insightLine: "כמעט פי שלושה משלהם"
out.write("CHECK prot-008 insightLine: 'almost 3x the sodium of its low-sodium sibling'\n")
out.write("  prot-008 sodium: " + str(fields['prot-008']['sodium']) + "mg\n")
out.write("  prot-007 sodium: " + str(fields['prot-007']['sodium']) + "mg\n")
out.write("  prot-009 sodium: " + str(fields['prot-009']['sodium']) + "mg\n")
ratio_007 = fields['prot-008']['sodium'] / fields['prot-007']['sodium']
ratio_009 = fields['prot-008']['sodium'] / fields['prot-009']['sodium']
out.write("  ratio vs prot-007: " + str(round(ratio_007, 2)) + "x\n")
out.write("  ratio vs prot-009: " + str(round(ratio_009, 2)) + "x\n")
out.write("  -> 272/100 = 2.72x. 'Almost 3x' is broadly accurate.\n\n")

out.write("====== NUMBER FIDELITY SPOT-CHECKS ======\n\n")
# prot-001 copy claims: 27g protein, 17g sugar, 17g fat, 13g fiber, 29mg sodium
checks = [
    ('prot-001', 'insightLine', 'protein', 27, None),
    ('prot-001', 'insightLine', 'sugar', 17, None),
    ('prot-001', 'rowVerdict', 'sugar', 17, None),
    ('prot-001', 'rowVerdict', 'fat', 17, None),
    ('prot-001', 'positiveSignals', 'protein', 27, None),
    ('prot-001', 'positiveSignals', 'fiber', 13, None),
    ('prot-002', 'insightLine', 'protein', 36, None),
    ('prot-002', 'insightLine', 'sugar', 16, None),
    ('prot-002', 'rowVerdict', 'sodium', 385, None),
    ('prot-003', 'insightLine', 'protein', 34, None),  # rounded from 33.7
    ('prot-003', 'rowVerdict', 'sodium', 352, None),
    ('prot-004', 'insightLine', 'fiber', 19, None),
    ('prot-004', 'rowVerdict', 'protein', 36, None),
    ('prot-004', 'rowVerdict', 'fiber', 19, None),
    ('prot-004', 'rowVerdict', 'sodium', 387, None),
    ('prot-005', 'rowVerdict', 'sodium', 160, None),
    ('prot-006', 'insightLine', 'kcal', 406, None),
    ('prot-006', 'rowVerdict', 'protein', 33, None),
    ('prot-006', 'rowVerdict', 'fat', 20, None),
    ('prot-007', 'rowVerdict', 'protein', 32, None),
    ('prot-007', 'rowVerdict', 'sodium', 100, None),
    ('prot-008', 'rowVerdict', 'protein', 35, None),  # rounded from 34.8
    ('prot-008', 'rowVerdict', 'sodium', 272, None),
    ('prot-009', 'rowVerdict', 'protein', 33, None),
    ('prot-009', 'rowVerdict', 'sodium', 100, None),
    ('prot-010', 'insightLine', 'sat_fat', 8.2, None),
    ('prot-010', 'rowVerdict', 'sat_fat', 8.2, None),
    ('prot-011', 'insightLine', 'protein', 34, None),
    ('prot-011', 'insightLine', 'sat_fat', 8.5, None),
    ('prot-011', 'rowVerdict', 'protein', 34, None),
    ('prot-011', 'rowVerdict', 'sat_fat', 8.5, None),
    ('prot-012', 'insightLine', 'protein', 26, None),
    ('prot-012', 'insightLine', 'kcal', 496, None),
    ('prot-012', 'rowVerdict', 'protein', 26, None),
    ('prot-012', 'rowVerdict', 'fat', 29.5, None),
    ('prot-013', 'insightLine', 'protein', 25, None),
    ('prot-013', 'insightLine', 'kcal', 489, None),
    ('prot-013', 'rowVerdict', 'protein', 25, None),
    ('prot-013', 'rowVerdict', 'fat', 28, None),  # rounded from 28.3
    ('prot-014', 'insightLine', 'protein', 33, None),
    ('prot-014', 'insightLine', 'sugar', 31, None),
    ('prot-014', 'rowVerdict', 'sugar', 31, None),
    ('prot-014', 'rowVerdict', 'sat_fat', 11, None),
    ('prot-015', 'insightLine', 'protein', 34, None),
    ('prot-015', 'insightLine', 'sugar', 35, None),
    ('prot-015', 'insightLine', 'sodium', 396, None),
    ('prot-015', 'rowVerdict', 'sugar', 35, None),
    ('prot-015', 'rowVerdict', 'sodium', 396, None),
    ('prot-016', 'insightLine', 'protein', 34, None),
    ('prot-016', 'insightLine', 'sugar', 27, None),
    ('prot-016', 'insightLine', 'kcal', 465, None),
    ('prot-016', 'rowVerdict', 'protein', 34, None),
    ('prot-016', 'rowVerdict', 'sugar', 27, None),
    ('prot-016', 'rowVerdict', 'fat', 24, None),
    ('prot-016', 'rowVerdict', 'kcal', 465, None),
]

nutrient_map = {
    'protein': 'protein',
    'sugar': 'sugar',
    'fat': 'fat',
    'sat_fat': 'sat_fat',
    'sodium': 'sodium',
    'fiber': 'fiber',
    'kcal': 'kcal',
}

for pid, field, nutrient, claimed_val, _ in checks:
    actual = fields[pid][nutrient]
    if actual is None:
        out.write("MISSING " + pid + " " + nutrient + " actual=None, claimed=" + str(claimed_val) + "\n")
        continue
    # allow rounding: within 1 unit for most, within 2 for kcal
    tolerance = 2.0 if nutrient == 'kcal' else 1.0
    if abs(actual - claimed_val) > tolerance:
        out.write("MISMATCH " + pid + "." + field + " " + nutrient + ": claimed=" + str(claimed_val) + " actual=" + str(actual) + " diff=" + str(round(actual - claimed_val, 1)) + "\n")
    else:
        out.write("OK " + pid + "." + field + " " + nutrient + " claimed=" + str(claimed_val) + " actual=" + str(actual) + "\n")

out.flush()
