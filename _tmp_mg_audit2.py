import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mg_results = [r for r in data['results'] if r.get('engine_active') == 'magnesium']

print('=== BISGLYCINATE PANEL DATA ===')
for r in mg_results:
    if r.get('outcome') == 'scored':
        acts = r['panel']['actives']
        for a in acts:
            form_val = a.get('form') or ''
            if 'bisglycinate' in form_val.lower():
                bc = r['barcode']
                name = r['name_he'][:30]
                amt = a['amount']
                ing = a.get('ingredient','')
                print(f'{bc} | {name:30s} | {amt}mg bisglycinate | ing: {ing}')

print()
print('=== CITRATE PANEL DATA ===')
for r in mg_results:
    if r.get('outcome') == 'scored':
        acts = r['panel']['actives']
        for a in acts:
            form_val = a.get('form') or ''
            if 'citrate' in form_val.lower():
                bc = r['barcode']
                name = r['name_he'][:30]
                amt = a['amount']
                ing = a.get('ingredient','')
                print(f'{bc} | {name:30s} | {amt}mg citrate | ing: {ing}')

print()
print('=== MALATE PANEL DATA ===')
for r in mg_results:
    if r.get('outcome') == 'scored':
        acts = r['panel']['actives']
        for a in acts:
            form_val = a.get('form') or ''
            if 'malate' in form_val.lower():
                bc = r['barcode']
                name = r['name_he'][:30]
                amt = a['amount']
                ing = a.get('ingredient','')
                print(f'{bc} | {name:30s} | {amt}mg malate | ing: {ing}')

print()
# FINAL SCORING ARCHITECTURE REVIEW
# The oxide paradox: does the scoring ACTUALLY account for bioavailability?
print('=== SCORING ARCHITECTURE: FORM SCORES ===')
for r in mg_results:
    if r.get('outcome') == 'scored':
        bc = r['barcode']
        name = r['name_he'][:25]
        form_score = r['engine_output']['sub_scores']['form']
        dose_reason = r['trace']['sub_scores']['dose'].get('reason','?')
        acts = r['panel']['actives']
        form_val = acts[0].get('form') or 'unknown' if acts else 'unknown'
        score = r['engine_output']['score']
        grade = r['engine_output']['grade']
        print(f'{bc} | {name:25s} | form={form_val:15s} | form_score={form_score:4} | dose_reason={dose_reason:30s} | final={score}/{grade}')
