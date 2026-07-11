"""Measure served-product canonical-capture coverage from TASK-601 artifacts."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; MANIFEST=ROOT/'03_operations/bsip0/manifest/capture_manifest.json'; OUT=ROOT/'03_operations/reports/task601_bsip0_census.md'; FRONT=ROOT/'bari-web/src/data/comparisons'
def write_guard(p):
    if p.resolve()!=OUT.resolve(): raise AssertionError('write outside TASK-601 boundary')
def gtin(p):
    for k in ('gtin','barcode','ean','upc','product_code','product_id'):
        if p.get(k) is not None: return str(p[k])
    return None
def main():
    records=json.loads(MANIFEST.read_text(encoding='utf-8'))['records']; canon={str(x['gtin']) for x in records if x['canonical'] and x['gtin']}
    retailer=Counter(x['retailer'] for x in records); shelves=[]; total=has_=0
    for f in sorted(FRONT.glob('*_frontend_v*.json')):
        data=json.loads(f.read_text(encoding='utf-8')); products=data.get('products', data if isinstance(data,list) else []); h=sum(gtin(p) in canon for p in products); n=len(products)-h; total+=len(products); has_+=h; shelves.append((f.stem,len(products),h,n))
    canonical=sum(x['canonical'] for x in records); distinct=len(canon); flag_counts=Counter(); replay_rows=0
    base=ROOT/'03_operations/bsip0/manifest/replay_baseline.jsonl'
    for line in base.read_text(encoding='utf-8').splitlines():
        replay_rows+=1
        flag_counts.update(json.loads(line)['flags'])
    text=['# TASK-601 BSIP0 Capture Census','',f'- Total captures: {len(records)} (manifest records).','- Canonical captures: %d (manifest records).'%canonical,'- Duplicates superseded: %d (manifest records).'%(len(records)-canonical),f'- Distinct GTINs: {distinct} (canonical records with GTIN).','', '## Per-retailer capture breakdown','']+[f'- {k}: {v}/{len(records)} captures' for k,v in sorted(retailer.items())]+['','## Served-product coverage','', '| Shelf | Served products | HAS_CANONICAL_CAPTURE | NO_CAPTURE |','|---|---:|---:|---:|']+[f'| {a} | {b} | {c} | {d} |' for a,b,c,d in shelves]+['',f'Total served products: {total}; HAS_CANONICAL_CAPTURE: {has_}/{total}; NO_CAPTURE: {total-has_}/{total}.','', '## Replay distribution marker','',f'- Replay rows: {replay_rows} (canonical captures × 10 fields).','- Flagged rows: %d/%d; most_common flag: %s.'%(sum(flag_counts.values()), replay_rows, flag_counts.most_common(1) or [('none', 0)]),f'- Flag histogram: {dict(sorted(flag_counts.items()))}.','']
    write_guard(OUT); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text('\n'.join(text),encoding='utf-8'); print('\n'.join(text))
if __name__=='__main__': main()
