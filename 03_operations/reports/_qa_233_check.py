import json, sys, re, io
sys.path.insert(0, r'c:/Bari/integrations/clients')
import hebrew_readability as hr

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'c:/Bari/bari-web/src/data/comparisons/'
FILES = ['frozen_vegetables_frontend_v1','salty_snacks_frontend_v4','yogurts_frontend_v3',
         'snacks_frontend_v2','butter_frontend_v2','cereals_frontend_v2','bread_frontend_v2']

# consumer-facing string fields to scan
def consumer_strings(p):
    out = []
    def add(field, val):
        if isinstance(val, str) and val.strip():
            out.append((field, val))
    add('insightLine', p.get('insightLine'))
    add('rowVerdict', p.get('rowVerdict'))
    add('confidence_label_he', p.get('confidence_label_he'))
    add('confidence_tooltip_he', p.get('confidence_tooltip_he'))
    add('confidence_sub_reason', p.get('confidence_sub_reason'))
    exp = p.get('expansion')
    if isinstance(exp, dict):
        for k in ['bottomLine','comparisonContext','servingNote','confidenceLabel','dataNote','signals']:
            v = exp.get(k)
            if isinstance(v, str): add('expansion.'+k, v)
            elif isinstance(v, list):
                for i,it in enumerate(v):
                    if isinstance(it,str): add(f'expansion.{k}[{i}]', it)
                    elif isinstance(it,dict):
                        for kk,vv in it.items():
                            if isinstance(vv,str): add(f'expansion.{k}[{i}].{kk}', vv)
        # nutrition/ingredients are facts but scan anyway for grade literals
        nut = exp.get('nutrition')
        if isinstance(nut, list):
            for i,it in enumerate(nut):
                if isinstance(it,dict):
                    for kk,vv in it.items():
                        if isinstance(vv,str): add(f'expansion.nutrition[{i}].{kk}', vv)
    return out

# slash-grade literal regex NN/X
GRADE_LIT = re.compile(r'\b\d{1,3}(?:\.\d+)?\s*/\s*[A-Eא-ה]\b')
# bare decimal that the gate flags as score_mechanic
BARE_DEC = re.compile(r'\b\d{2,3}\.\d+\b')

total_strings = 0
not_clean = []
grade_lits = []
bare_dec_only = []  # strings whose only score_mechanic leak is a bare decimal (false positive)
framework_leaks = []
recommendation_leaks = []

for f in FILES:
    d = json.load(open(BASE+f+'.json', encoding='utf-8'))
    prods = d.get('products', [])
    for p in prods:
        pid = p.get('id')
        for field, s in consumer_strings(p):
            total_strings += 1
            r = hr.analyze(s)
            if not r.is_clean:
                kinds = {}
                for l in r.leaks:
                    kinds.setdefault(l.kind, []).append(l.term)
                not_clean.append((f, pid, field, kinds, s))
                # categorize
                if GRADE_LIT.search(s):
                    grade_lits.append((f, pid, field, s))
                # score_mechanic leaks
                sm = kinds.get('score_mechanic', [])
                if sm:
                    real_grade = [t for t in sm if '/' in t]
                    if not real_grade and all(BARE_DEC.fullmatch(t) for t in sm):
                        bare_dec_only.append((f, pid, field, sm, s))
                if 'framework' in kinds:
                    framework_leaks.append((f, pid, field, kinds['framework'], s))
                if 'recommendation' in kinds:
                    recommendation_leaks.append((f, pid, field, kinds['recommendation'], s))

print("=== LEAK / is_clean SWEEP ===")
print("total consumer strings scanned:", total_strings)
print("strings failing is_clean:", len(not_clean))
print("NN/X grade-literal hits:", len(grade_lits))
print("FRAMEWORK leaks:", len(framework_leaks))
print("RECOMMENDATION leaks:", len(recommendation_leaks))
print()
print("--- GRADE LITERAL (NN/X) hits ---")
for f,pid,field,s in grade_lits:
    print(f"  [{f}] {pid} {field}: {s[:90]}")
print()
print("--- FRAMEWORK leaks ---")
for f,pid,field,terms,s in framework_leaks:
    print(f"  [{f}] {pid} {field}: terms={terms} :: {s[:90]}")
print()
print("--- RECOMMENDATION leaks ---")
for f,pid,field,terms,s in recommendation_leaks:
    print(f"  [{f}] {pid} {field}: terms={terms} :: {s[:90]}")
print()
print("--- score_mechanic that are BARE DECIMALS ONLY (false-positive class) ---")
print("count:", len(bare_dec_only))
for f,pid,field,sm,s in bare_dec_only[:60]:
    print(f"  [{f}] {pid} {field}: {sm} :: {s[:80]}")
print()
# Any not_clean that is NOT explained by bare-decimal and NOT grade-literal?
explained_ids = set(id((f,pid,field,s)) for f,pid,field,s in grade_lits)
print("--- not_clean strings that are neither NN/X nor bare-decimal-only nor framework/recommendation ---")
bd_keys = set((f,pid,field,s) for f,pid,field,sm,s in bare_dec_only)
gl_keys = set((f,pid,field,s) for f,pid,field,s in grade_lits)
fw_keys = set((f,pid,field,s) for f,pid,field,t,s in framework_leaks)
rc_keys = set((f,pid,field,s) for f,pid,field,t,s in recommendation_leaks)
other = []
for f,pid,field,kinds,s in not_clean:
    key=(f,pid,field,s)
    if key in bd_keys or key in gl_keys or key in fw_keys or key in rc_keys:
        continue
    other.append((f,pid,field,kinds,s))
print("count:", len(other))
for f,pid,field,kinds,s in other:
    print(f"  [{f}] {pid} {field}: {kinds} :: {s[:90]}")
