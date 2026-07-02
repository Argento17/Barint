import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Bari/02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mg_results = [r for r in data['results'] if r.get('engine_active') == 'magnesium']

# Altman Balance: panel shows Ashwagandha KSM-66 and Valerian
bal = next(r for r in mg_results if r['barcode'] == '7290019444206')
print('ALTMAN BALANCE full panel actives:')
for a in bal['panel']['actives']:
    print('  ' + a['ingredient'] + ' ' + str(a['amount']) + 'mg')

print()
print('PAGE expansion.ingredients says: "מגנזיום (from oxide), 450 מג לכמוסה"')
print('MISSING from page: ashwagandha KSM-66 50mg, valerian 50mg, vitamin B6 30mg')
print()

# Check UP vs Balance score breakdown
altman_up = next(r for r in mg_results if r['barcode'] == '7290013142894')
altman_bal = next(r for r in mg_results if r['barcode'] == '7290019444206')
print('=== UP vs BALANCE SCORE BREAKDOWN ===')
print('UP: evidence=' + str(altman_up['engine_output']['sub_scores']['evidence']) +
    ' dose=' + str(altman_up['engine_output']['sub_scores']['dose']) +
    ' form=' + str(altman_up['engine_output']['sub_scores']['form']) +
    ' honesty=' + str(altman_up['engine_output']['sub_scores']['honesty']) +
    ' -> ' + str(altman_up['engine_output']['score']) + '/' + altman_up['engine_output']['grade'])
print('Balance: evidence=' + str(altman_bal['engine_output']['sub_scores']['evidence']) +
    ' dose=' + str(altman_bal['engine_output']['sub_scores']['dose']) +
    ' form=' + str(altman_bal['engine_output']['sub_scores']['form']) +
    ' honesty=' + str(altman_bal['engine_output']['sub_scores']['honesty']) +
    ' -> ' + str(altman_bal['engine_output']['score']) + '/' + altman_bal['engine_output']['grade'])
print()
print('UP claim matched:', altman_up['trace']['claim_matched'])
print('Balance claim matched:', altman_bal['trace']['claim_matched'])
print()
print('UP evidence tier:', altman_up['trace']['sub_scores']['evidence'])
print('Balance evidence tier:', altman_bal['trace']['sub_scores']['evidence'])
print()

# The page insightLine for Balance says:
# "קומפלקס Balance — מגנזיום אוקסיד 450 מ"ג, ציון זהה לגרסה הבסיסית"
# But the score is 62, not the same as the basic version (UP=70)
# rowVerdict also says "זהה לגרסת 520 מ"ג מינוס 70"
# This makes sense: UP 450mg is higher because of better evidence score
# Balance 450mg has lower evidence score (different claim)
print('NOTE: page insightLine says "ציון זהה לגרסה הבסיסית" (same score as basic version)')
print('But UP=70, Balance=62 -- these are NOT the same score')
print('The insightLine comparison to "basic version" may be referring to the 450mg oxide formulation')
print('vs the 520mg oxide formulation -- but the 520mg versions score 66, not 62')
print('This comparative language in the insightLine is potentially misleading/inaccurate')
