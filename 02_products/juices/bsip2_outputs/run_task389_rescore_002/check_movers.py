# -*- coding: utf-8 -*-
import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

data = json.loads(open(r'C:\Bari\bari-web\src\data\comparisons\juices_frontend_v3.json', encoding='utf-8').read())
mover_bcs = {'7290000136523', '7290019056720', '7290019056737'}
for p in data['products']:
    bc = p.get('barcode','')
    if bc not in mover_bcs:
        continue
    print(f"barcode={bc}  id={p.get('id')}  score={p.get('score')}  grade={p.get('grade')}  name={p.get('name','')[:40]}")
    for k, v in p.items():
        if k not in ('id', 'name', 'barcode', 'imageUrl', 'retailers', 'subPool') and v is not None:
            print(f"  {k}: {v}")
    print()
