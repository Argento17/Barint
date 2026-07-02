import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mg_results = [r for r in data['results'] if r.get('engine_active') == 'magnesium']
solgar = next(r for r in mg_results if r['barcode'] == '0033984005181')

print('=== SOLGAR Ca+Mg+D FULL PANEL ===')
print('Barcode:', solgar['barcode'])
print('Name:', solgar['name_he'])
print('Panel actives:')
for a in solgar['panel']['actives']:
    print('  ingredient:', a['ingredient'])
    print('  amount:', a['amount'], 'mg, form:', a['form'])
    print('  active_slug:', a['active_slug'])
    print()

print('bsip0s_label actives (what engine scored):')
for a in solgar['bsip0s_label']['actives']:
    print('  display_name:', a['display_name'])
    print('  quantity:', a['quantity'], 'mg, form:', a['form'])
    print('  active_slug:', a['active_slug'])
    print()

print('Engine dose sub-score:', solgar['engine_output']['sub_scores']['dose'])
print('Engine score:', solgar['engine_output']['score'])
print()

# Check the Mg specific active in bsip0s
mg_active = next((a for a in solgar['bsip0s_label']['actives'] if a['active_slug'] == 'magnesium'), None)
if mg_active:
    print('ENGINE scored on: Mg', mg_active['quantity'], 'mg', mg_active['form'])
else:
    print('No Mg active in bsip0s_label -- check first active only')
    print('First active:', solgar['bsip0s_label']['actives'][0])

print()
# Check: does the page say 200mg or 100mg for Solgar?
print('PAGE SAYS (from magnesium-page-data.ts inspection):')
print('  ingredients: "סידן (calcium citrate), מגנזיום (magnesium citrate) 200 מג, ויטמין D3"')
print('  rowVerdict includes: "מגנזיום ציטראט 200 מג בלבד"')
print('  insightLine: "מגנזיום ציטראט 200 מג"')
print()
print('If corpus panel shows Mg = 100mg but page says 200mg -> DATA ERROR')
print('If corpus panel shows Mg = 200mg -> consistent')
