import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mg_results = [r for r in data['results'] if r.get('engine_active') == 'magnesium']

print('=== ALL Mg DOSE TRACES ===')
for r in mg_results:
    if r.get('outcome') == 'scored':
        bc = r['barcode']
        name = r['name_he'][:30]
        dose = r['trace']['sub_scores']['dose']
        panel_amt = r['panel']['actives'][0]['amount']
        panel_form = r['panel']['actives'][0].get('form', 'N/A')
        dv = dose['value']
        dr = dose['reason']
        print(f'{bc} | {name:30s} | {panel_amt:6.0f}mg {panel_form:15s} | dose_value={dv!s:5} reason={dr}')

print()
# Check Amorphicure
amorp = next(r for r in mg_results if r['barcode'] == '7290015429245')
print('Amorphicure dose trace:', amorp['trace']['sub_scores']['dose'])
print('160*0.288 =', 160*0.288)

print()
# Check TRIOMAG caps
triomag = next(r for r in mg_results if r['barcode'] == '7290118816065')
print('TRIOMAG dose trace:', triomag['trace']['sub_scores']['dose'])
print('TRIOMAG caps_fired:', triomag['engine_output']['caps_vetoes_fired'])

print()
# The bisglycinate WELL: 168mg bisglycinate -> E/34 (evidence cap)
# Page says "168mg bisglycinate with zinc and B6" -> evidence cap because claim is vague
well = next(r for r in mg_results if r['barcode'] == '7290018439043')
print('WELL dose trace:', well['trace']['sub_scores']['dose'])
print('WELL cap:', well['engine_output']['caps_vetoes_fired'])
print('168*0.141 =', 168*0.141, 'mg elemental bisglycinate')

print()
# The IMPORTANT finding: bisglycinate WELL has 168mg bisglycinate = 23.7mg elemental
# Yet it gets dose=sub_therapeutic? Or fairy_dust? Let's see
print('WELL score:', well['engine_output']['score'])
print('WELL grade:', well['engine_output']['grade'])
