import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mg_results = [r for r in data['results'] if r.get('engine_active') == 'magnesium']
solgar = next(r for r in mg_results if r['barcode'] == '0033984005181')

print('=== SOLGAR FULL TRACE ===')
trace = solgar['trace']
print('active (engine input):', trace.get('active'))
print('on_label_claim:', trace.get('on_label_claim'))
print('bsip0s actives used:')
print(json.dumps(solgar['bsip0s_label']['actives'], ensure_ascii=False, indent=2))
print()
print('Engine sub_scores:', solgar['engine_output']['sub_scores'])
print('dose reason from trace:', trace['sub_scores']['dose'])
print()

# The corpus shows:
# bsip0s_label actives[0]: calcium (calcium citrate), 200mg, active_slug=vitamin_d3
# Panel shows Mg = 100mg
# The engine appears to have mapped ALL actives under vitamin_d3 slug (wrong!)
# This is a data pipeline error: engine_active=magnesium but bsip0s_label has active_slug=vitamin_d3
# The engine scored on 200mg of CALCIUM, not 100mg of MAGNESIUM
# Both the engine scoring and the page copy are working from wrong data

print('=== CRITICAL: Solgar active_slug audit ===')
print('engine_active in corpus:', solgar['engine_active'])
print('bsip0s_label all actives:')
for i, a in enumerate(solgar['bsip0s_label']['actives']):
    print(f'  [{i}] slug={a["active_slug"]} qty={a["quantity"]}mg form={a["form"]} name={a["display_name"]}')
print()
print('FINDING: All three actives (Ca, Mg, D3) have active_slug=vitamin_d3 in bsip0s_label')
print('The engine was dispatched under engine_active=magnesium')
print('But the scored active quantity appears to be 200mg (Ca-citrate) not 100mg (Mg-citrate)')
print()

# Check TRIOMAG - it says 200mg citrate blend but is that citrate, bisglycinate+taurate?
triomag = next(r for r in mg_results if r['barcode'] == '7290118816065')
print('=== TRIOMAG PANEL ===')
print(json.dumps(triomag['panel']['actives'], ensure_ascii=False, indent=2))
print()
print('bsip0s_label:')
print(json.dumps(triomag['bsip0s_label']['actives'], ensure_ascii=False, indent=2))

print()
# NT LC: 450mg hydroxide
nt = next(r for r in mg_results if r['barcode'] == '7290010207640')
print('=== NT LC PANEL ===')
print(json.dumps(nt['panel']['actives'], ensure_ascii=False, indent=2))
print('Form score:', nt['engine_output']['sub_scores']['form'])
print('Note: page says hydroxide (45 form score), same as oxide - correct? hydroxide ~= oxide for scoring')
