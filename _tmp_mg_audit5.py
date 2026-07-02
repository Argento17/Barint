import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mg_results = [r for r in data['results'] if r.get('engine_active') == 'magnesium']
solgar = next(r for r in mg_results if r['barcode'] == '0033984005181')

# The bsip0s_label for Solgar has only ONE active: calcium citrate 200mg, slug=vitamin_d3
# The engine was dispatched under engine_active='magnesium'
# The engine scored on 200mg citrate (but that's CALCIUM, not MAGNESIUM)
# The Mg content is 100mg in the full panel, not 200mg
#
# HOWEVER: The engine with fairy_dust at 200mg citrate STILL fires fairy_dust
# because 200mg citrate * 16.2% = 32mg elemental < fairy_floor
# So the CONCLUSION (fairy_dust cap -> 49/D) is likely correct for the Mg dose.
# But the INPUT was wrong (200mg Ca-citrate vs 100mg Mg-citrate).
#
# For 100mg Mg-citrate: 100 * 16.2% = 16.2mg elemental -> even more fairy_dust.
# The conclusion (D) is still correct, but the reasoning chain has a data error.
#
# KEY: The page COPY says "מגנזיום ציטראט 200 מ"ג" but actual Mg is 100mg.
# This is a factual error in consumer-facing copy.

print('=== SOLGAR: WHAT THE PAGE COPY SAYS vs WHAT THE LABEL SAYS ===')
print()
print('Page says: "מגנזיום ציטראט 200 מ\"ג" (magnesium citrate 200mg)')
print('Corpus panel shows: magnesium = 100mg (active_slug was misrouted to vitamin_d3)')
print('The 200mg figure is CALCIUM citrate, not magnesium citrate')
print()
print('IMPACT:')
print('  Page insightLine: "מגנזיום ציטראט 200 מ\"ג בתוך מולטי Ca/Mg/D" -- cites wrong Mg dose')
print('  Page expansion.ingredients: lists 200mg for magnesium -- wrong (actual = 100mg)')
print('  Scoring: engine scored on 200mg (Ca-citrate misrouted) -> still fairy_dust')
print('  Corrected: 100mg Mg-citrate -> 16.2mg elemental -> even more deeply fairy_dust')
print('  Conclusion (D grade) is still defensible, but the stated dose is wrong')
print()

# NT LC: form_raw = hydroxide but form = oxide (engine mapped hydroxide->oxide)
# Page calls it "magnesium hydroxide" but engine uses form_score=45 (oxide level)
# The NT LC insightLine says: "מגנזיום מים ים המלח עם B6 ו-E — 450 מ\"ג, ספיגה דומה לאוקסיד"
# This is honest: acknowledges hydroxide has oxide-level absorption
print('=== NT LC FORM MAPPING ===')
nt = next(r for r in mg_results if r['barcode'] == '7290010207640')
print('form_raw:', nt['panel']['actives'][0]['form_raw'])
print('form (scored as):', nt['panel']['actives'][0]['form'])
print('form_score:', nt['engine_output']['sub_scores']['form'])
print('Page says "ספיגה דומה לאוקסיד" -> accurate disclosure of hydroxide=oxide scoring')
print()

# Check if Altman Balance (אלטמן מגנזיום באלאנס): page says "oxide 450mg"
# but is it actually a different form?
bal = next(r for r in mg_results if r['barcode'] == '7290019444206')
print('=== ALTMAN BALANCE FORM ===')
print('Panel actives:', json.dumps(bal['panel']['actives'], ensure_ascii=False))
print('Form score:', bal['engine_output']['sub_scores']['form'])
print()

# Check Magnox B6: sub_therapeutic dose, 61.4/C
# Page says "432mg oxide" -- form_score = 45 (oxide)
# 432 * 60.3% = 260mg elemental
# Dose = 75.0, reason = sub_therapeutic (not in_range, not fairy_dust)
# What's the sub_therapeutic threshold vs in_range threshold?
magnox = next(r for r in mg_results if r['barcode'] == '7290017847122')
print('=== MAGNOX DOSE TRACE ===')
print('Panel amount:', magnox['panel']['actives'][0]['amount'], 'mg')
print('Dose trace:', magnox['trace']['sub_scores']['dose'])
print('Score:', magnox['engine_output']['score'])
print('432mg oxide * 60.3% =', 432*0.603, 'mg elemental')

# UP 450mg oxide -> dose=77.5, sub_therapeutic
# 520mg oxide -> dose=92, in_range (passes!)
# 432mg oxide -> dose=75, sub_therapeutic
# So somewhere between 432mg and 520mg oxide there's a threshold
# 432 * 0.603 = 260mg elemental -> sub_therapeutic
# 520 * 0.603 = 313.5mg elemental -> in_range
print()
print('THRESHOLD ANALYSIS:')
print('432mg oxide = 260mg elemental -> sub_therapeutic (dose=75)')
print('450mg oxide = 271mg elemental -> sub_therapeutic (dose=77.5)')
print('520mg oxide = 313mg elemental -> in_range (dose=92)')
print('Threshold likely ~300mg elemental for in_range')
