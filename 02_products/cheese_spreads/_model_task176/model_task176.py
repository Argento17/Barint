# TASK-176 MODEL — NOT LIVE. Reads the LIVE cheese frontend JSON read-only and computes a
# what-if "fat-monotonic same-family display guard" (M1). DISPLAY-ONLY clamp, mirrors _aCappedToB.
# NEVER mutates any engine score or any live file. Pure arithmetic on already-published numbers.
import json, csv, os
LIVE = r'C:\Bari\bari-web\src\data\comparisons\cheese_frontend_v2.json'
OUT  = r'C:\Bari\02_products\cheese_spreads\_model_task176'

d=json.load(open(LIVE,encoding='utf-8'))
from collections import defaultdict
clusters=defaultdict(list)
def walk(o):
    if isinstance(o,dict):
        if str(o.get('id','')).startswith('che-') and 'score' in o and o.get('_cluster'):
            nut=o.get('expansion',{}).get('nutrition',{}) or {}
            clusters[o['_cluster']].append({'id':o['id'],'name':o.get('name',''),'score':o['score'],
                'grade':o.get('grade'),'aCapped':o.get('_aCappedToB'),
                'fat':nut.get('fat'),'satFat':nut.get('satFat'),'protein':nut.get('protein')})
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
# de-dup by id (the JSON repeats products in featured + table)
for c in clusters: 
    seen={}; 
    for r in clusters[c]: seen[r['id']]=r
    clusters[c]=list(seen.values())

# ---- M1: within a fat-ladder cluster, a higher-fat product's DISPLAYED score is clamped to
# the minimum displayed score of any strictly-lower-fat sibling. Lower fat = leaner = the better
# choice when a shopper sorts by fat; the guard only ever LOWERS a higher-fat product, never raises.
def m1(rows):
    by_fat=defaultdict(list)
    for r in rows:
        if r['fat'] is None: continue
        by_fat[r['fat']].append(r)
    fats=sorted(by_fat); running=10**9; out={}
    for f in fats:
        tier=by_fat[f]
        for r in tier: out[r['id']]=min(r['score'],running)
        running=min(running, min(x['score'] for x in tier))
    return out

def grade(s):
    return 'S' if s>=90 else 'A' if s>=80 else 'B' if s>=65 else 'C' if s>=50 else 'D' if s>=35 else 'E'

rows_out=[]
changed=0
for c in ['cottage','white-cheese-quark']:
    rows=clusters[c]
    capped=m1(rows)
    print(f"=== {c} (fat ASC) ===")
    print(f"{'fat':5s} {'satf':5s} {'prot':5s} {'live':7s} {'M1':7s} delta  id")
    for r in sorted(rows,key=lambda x:(x['fat'] if x['fat'] is not None else 99, -x['score'])):
        m=capped.get(r['id'],r['score'])
        # M1 display: if numeric already display-capped to B by sat-fat (aCapped), keep B; else regrade
        new_g = grade(m) if not r['aCapped'] else ('B' if grade(m)=='A' else grade(m))
        live_disp=f"{r['score']}/{r['grade']}"
        new_disp=f"{m}/{new_g}"
        delta=m-r['score']
        if delta!=0: changed+=1
        print(f"{str(r['fat']):5s} {str(r['satFat']):5s} {str(r['protein']):5s} {live_disp:7s} {new_disp:7s} {delta:+d}    {r['id']}")
        rows_out.append({'cluster':c,'id':r['id'],'fat':r['fat'],'satFat':r['satFat'],'protein':r['protein'],
            'live_score':r['score'],'live_grade':r['grade'],'M1_score':m,'M1_grade':new_g,'delta':delta})
    print()
print('Total products whose displayed score changes under M1:',changed)
with open(os.path.join(OUT,'cottage_white_before_after.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows_out[0].keys())); w.writeheader()
    for r in rows_out: w.writerow(r)
