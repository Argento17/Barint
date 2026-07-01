#!/usr/bin/env python3
"""Surgically patch score+grade in a DEPLOYED frontend JSON from a freshly-generated
(trace-derived) generate_page output, preserving all authored copy/assembly.
Reports grade changes, new products, dropped products. Does NOT author copy.
Usage: surgical_repro_patch.py --deployed <path> --generated <path> [--apply]"""
import argparse, json, sys

def products(obj):
    """Return the list holding product dicts (barcode+score/grade), and a ref to mutate."""
    found=[]
    def rec(o):
        if isinstance(o,list):
            if o and isinstance(o[0],dict) and any(('barcode' in x or 'id' in x) and ('score' in x or 'grade' in x) for x in o):
                found.append(o)
            for v in o: rec(v)
        elif isinstance(o,dict):
            for v in o.values(): rec(v)
    rec(obj)
    return found

def index(obj):
    out={}
    for lst in products(obj):
        for p in lst:
            bc=str(p.get('barcode') or p.get('id'))
            out[bc]=p
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--deployed',required=True)
    ap.add_argument('--generated',required=True)
    ap.add_argument('--apply',action='store_true')
    a=ap.parse_args()
    dep=json.load(open(a.deployed,encoding='utf-8'))
    gen=json.load(open(a.generated,encoding='utf-8'))
    di=index(dep); gi=index(gen)
    common=set(di)&set(gi)
    gradech=[]; scorech=0
    for bc in common:
        dp=di[bc]; gp=gi[bc]
        ds,dg=dp.get('score'),dp.get('grade'); gs,gg=gp.get('score'),gp.get('grade')
        if dg!=gg: gradech.append((bc,dg,gg))
        try:
            if abs(float(ds)-float(gs))>=0.05: scorech+=1
        except: pass
        if a.apply:
            dp['score']=gs; dp['grade']=gg
    newp=sorted(set(gi)-set(di)); dropp=sorted(set(di)-set(gi))
    print(f"common={len(common)} score_patched={scorech} grade_changes={len(gradech)} new={len(newp)} dropped={len(dropp)}")
    for bc,dg,gg in gradech: print(f"  GRADE {bc}: {dg} -> {gg}")
    if newp: print(f"  NEW (need copy): {', '.join(newp)}")
    if dropp: print(f"  DROPPED (in deployed, not in corpus): {', '.join(dropp)}")
    if a.apply:
        json.dump(dep,open(a.deployed,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
        print("APPLIED (scores+grades patched; copy preserved)")

if __name__=='__main__': main()
