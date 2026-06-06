# TASK-176 MODEL v2 — NOT LIVE. Three candidate rules compared on real published numbers.
# DISPLAY-ONLY; never mutates engine scores or live files.
import json, csv, os
from collections import defaultdict
LIVE = r'C:\Bari\bari-web\src\data\comparisons\cheese_frontend_v2.json'
OUT  = r'C:\Bari\02_products\cheese_spreads\_model_task176'
d=json.load(open(LIVE,encoding='utf-8'))
clusters=defaultdict(dict)
def walk(o):
    if isinstance(o,dict):
        if str(o.get('id','')).startswith('che-') and 'score' in o and o.get('_cluster'):
            nut=o.get('expansion',{}).get('nutrition',{}) or {}
            clusters[o['_cluster']][o['id']]={'id':o['id'],'score':o['score'],'grade':o.get('grade'),
                'aCapped':o.get('_aCappedToB'),'fat':nut.get('fat'),'satFat':nut.get('satFat'),'protein':nut.get('protein')}
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
clusters={k:list(v.values()) for k,v in clusters.items()}

def grade(s): return 'S' if s>=90 else 'A' if s>=80 else 'B' if s>=65 else 'C' if s>=50 else 'D' if s>=35 else 'E'

# M1: clamp to MIN of all strictly-lower-fat siblings (too aggressive - shown for contrast)
def M1(rows):
    by=defaultdict(list)
    for r in rows:
        if r['fat'] is not None: by[r['fat']].append(r)
    out={}; run=10**9
    for f in sorted(by):
        for r in by[f]: out[r['id']]=min(r['score'],run)
        run=min(run,min(x['score'] for x in by[f]))
    return out

# M3: NEAREST-LOWER-FAT TIE-BREAK (recommended). A higher-fat product may not display a score
# strictly ABOVE the MAX score of the immediately-lower fat tier (the best leaner sibling). I.e.
# the leanest-best in a fat tier sets the ceiling for the next-fatter tier. Higher fat can MATCH
# but not BEAT the best lower-fat option. Only ever lowers; clamps to the *best* lower sibling
# (so a single weak low-fat outlier does NOT drag the fatter tier down).
def M3(rows):
    by=defaultdict(list)
    for r in rows:
        if r['fat'] is not None: by[r['fat']].append(r)
    fats=sorted(by); out={}; ceil=10**9
    for f in fats:
        tier_best=max(x['score'] for x in by[f])
        for r in by[f]: out[r['id']]=min(r['score'],ceil)
        ceil=min(ceil,tier_best)   # next-fatter tier capped at this tier's BEST
    return out

for name,fn in [('M1_min',M1),('M3_nearest_best',M3)]:
    print('############',name,'############')
    tot=0
    for c in ['cottage','white-cheese-quark']:
        rows=clusters[c]; cap=fn(rows)
        print(f"--- {c} ---")
        for r in sorted(rows,key=lambda x:(x['fat'] or 99,-x['score'])):
            m=cap.get(r['id'],r['score']); delta=m-r['score']
            if delta: tot+=1
            g=grade(m); 
            if r['aCapped'] and g=='A': g='B'
            mark=' <==' if delta else ''
            print(f"  fat={str(r['fat']):4s} prot={str(r['protein']):5s} {r['score']}/{r['grade']} -> {m}/{g} ({delta:+d}){mark}")
    print('changed:',tot,'\n')

# M4: BOUNDED near-equal fat tie-break. For each higher-fat product H, look at every strictly
# lower-fat sibling L. If H.score > L.score but the gap is within NOISE (<= N points), the two are
# "effectively equal on quality" and fat should break the tie -> clamp H to L.score-1 (display only).
# If H beats L by MORE than N, H is genuinely better (cleaner label) and is left alone.
# N=2 per comparison governance "<=2 pts = noise".
def M4(rows, N=2):
    out={r['id']:r['score'] for r in rows if r['fat'] is not None}
    fat_of={r['id']:r['fat'] for r in rows if r['fat'] is not None}
    base={r['id']:r['score'] for r in rows if r['fat'] is not None}
    for h in [r for r in rows if r['fat'] is not None]:
        worst_needed=h['score']
        for l in [r for r in rows if r['fat'] is not None and r['fat']<h['fat']]:
            if h['score']>l['score'] and (h['score']-l['score'])<=N:
                worst_needed=min(worst_needed, l['score']-1)
        out[h['id']]=worst_needed
    return out

print('############ M4_bounded_tiebreak (N=2) ############')
for c in ['cottage','white-cheese-quark']:
    rows=clusters[c]; cap=M4(rows)
    print(f"--- {c} ---")
    for r in sorted(rows,key=lambda x:(x['fat'] or 99,-x['score'])):
        m=cap.get(r['id'],r['score']); delta=m-r['score']
        g=grade(m)
        if r['aCapped'] and g=='A': g='B'
        mark=' <==' if delta else ''
        print(f"  fat={str(r['fat']):4s} prot={str(r['protein']):5s} {r['score']}/{r['grade']} -> {m}/{g} ({delta:+d}){mark}")
