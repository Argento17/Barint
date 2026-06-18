
import json, os, pathlib, sys, subprocess
ROOT = pathlib.Path(r"C:/Bari")
SRC = ROOT / "03_operations/bsip2/proto_v0/src"
sys.path.insert(0, str(SRC))

def purge():
    for m in list(sys.modules):
        f=getattr(sys.modules[m],"__file__",None)
        if f and pathlib.Path(f).resolve().parent==SRC.resolve():
            del sys.modules[m]

def setf(extra=None):
    base={"BARI_RECAL_P0":"off","BARI_GRAD_SODIUM_V1":"off","BARI_SODIUM_SHELF_RELATIVE_V1":"off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off","BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off",
            "BARI_TASK144_FIXES":"off","BARI_TASK250_CONF":"off","BARI_GLASSBOX_D5D6":"off",
            "BARI_GLASSBOX_W15":"off","BARI_GLASSBOX_W2":"off","BARI_GLASSBOX_W4":"on",
            "BARI_SHELF_RELATIVE_V1":"off"}
    if extra: base.update(extra)
    for k,v in base.items(): os.environ[k]=v
    purge()

def score(doc):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    s=extract_signals(doc); c=classify_category(doc)
    n=infer_nova(doc,s["L3_inferred_classifications"]); e=assign_evaluation_scope(doc,c["category"])
    return score_product(doc,s,c,n,e)

def diff_traces(bsip1, traces, extra=None, shelf_setup=None):
    setf(extra)
    if shelf_setup: shelf_setup()
    mm=[]; n=0
    for tp in sorted(traces.rglob("bsip2_trace.json")):
        t=json.loads(tp.read_text(encoding="utf-8")); pid=tp.parent.name
        dp=bsip1 / f"{pid}.json"
        if not dp.exists():
            bc=str(t.get("barcode") or "")
            cands=list(bsip1.glob(f"*{bc}*.json")) if bc else []
            dp=cands[0] if cands else dp
        if not dp.exists(): continue
        r=score(json.loads(dp.read_text(encoding="utf-8"))); n+=1
        if r.get("final_score_estimate")!=t.get("final_score_estimate") or r.get("grade_estimate")!=t.get("grade_estimate"):
            mm.append((pid, t.get("final_score_estimate"), r.get("final_score_estimate"), t.get("grade_estimate"), r.get("grade_estimate")))
    return n, mm

def guard_g1():
    print("=== G1 frozen milk (BARI_SHELF_RELATIVE_V1=on) ===")
    n,mm=diff_traces(ROOT/"03_operations/bsip1/run_milk_002/output",
        ROOT/"02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products",
        {"BARI_SHELF_RELATIVE_V1":"on"})
    print(f"Command: re-score run_005_headpin with BARI_SHELF_RELATIVE_V1=on")
    print(f"Result: checked={n}/20 mismatches={len(mm)}")
    return len(mm)==0 and n==20

def guard_g2():
    print("=== G2 published byte-identical (BARI_SHELF_RELATIVE_V1=off) ===")
    corpora=[
      ("milk", ROOT/"03_operations/bsip1/run_milk_002/output",
       ROOT/"02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products", {}),
      ("brined", ROOT/"03_operations/bsip1/run_brined_cheeses_002/output",
       ROOT/"02_products/brined_cheeses/bsip2_outputs/run_brined_005/products",
       {"BARI_RECAL_P0":"on","BARI_GRAD_SODIUM_V1":"on","BARI_SODIUM_SHELF_RELATIVE_V1":"on","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"on"}),
    ]
    def brined_shelf():
        from input_loader import load_batch
        from score_engine import compute_shelf_sodium_stats, set_shelf_sodium_stats
        prods=list(load_batch(ROOT/"03_operations/bsip1/run_brined_cheeses_002/output"))
        set_shelf_sodium_stats(*compute_shelf_sodium_stats(prods))
    total_mm=0; total_n=0
    for name, b, t, flags in corpora:
        shelf = brined_shelf if name=="brined" else None
        n,mm=diff_traces(b,t,flags,shelf)
        print(f" {name}: checked={n} mismatches={len(mm)}")
        total_n+=n; total_mm+=len(mm)
    print(f"Aggregate: checked={total_n} mismatches={total_mm}")
    return total_mm==0

def guard_g3():
    print("=== G3 engine invariants ===")
    cmd=[sys.executable, str(ROOT/"03_operations/shadow/engine_invariants.py")]
    print("Command:", " ".join(cmd))
    r=subprocess.run(cmd, capture_output=True, text=True)
    tail=chr(10).join(r.stdout.strip().splitlines()[-8:])
    print(tail)
    ok = r.returncode==0 and '"cases": 342' in r.stdout and '"failures": 0' in r.stdout
    print("342 PASS" if ok else "FAIL")
    return ok

def guard_g4():
    print("=== G4 EV-056 path intact ===")
    flags={"BARI_RECAL_P0":"on","BARI_GRAD_SODIUM_V1":"on","BARI_SODIUM_SHELF_RELATIVE_V1":"on","BARI_SHELF_RELATIVE_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"on"}
    def setup():
        from input_loader import load_batch
        from score_engine import compute_shelf_sodium_stats, set_shelf_sodium_stats
        prods=list(load_batch(ROOT/"03_operations/bsip1/run_brined_cheeses_002/output"))
        set_shelf_sodium_stats(*compute_shelf_sodium_stats(prods))
    n,mm=diff_traces(ROOT/"03_operations/bsip1/run_brined_cheeses_002/output",
        ROOT/"02_products/brined_cheeses/bsip2_outputs/run_brined_005/products", flags, setup)
    from score_engine import clear_shelf_sodium_stats; clear_shelf_sodium_stats()
    print(f"Command: brined corpus GRAD+SHELF_SODIUM on, SHELF_RELATIVE off")
    print(f"Result: checked={n} mismatches={len(mm)}")
    return len(mm)==0 and n==48

def guard_g5():
    print("=== G5 monotonicity (one_sided_high) ===")
    setf({"BARI_SHELF_RELATIVE_V1":"on"})
    from score_engine import set_shelf_stats, shelf_relative_differentiator, clear_shelf_stats
    set_shelf_stats("sugars_g",20.0,5.0,"iqr",n=30)
    bands=[(0,4,0),(5,9,2),(10,19,4),(20,None,6)]; prev=-1; inv=[]
    for v in range(51):
        p,_=shelf_relative_differentiator(float(v),"sugars_g",frozenset(["biscuit"]),"biscuit",bands,0.5,direction="one_sided_high")
        if p<prev: inv.append((v,prev,p))
        prev=p
    clear_shelf_stats()
    print(f"inversions={len(inv)}")
    return len(inv)==0

def guard_g6():
    print("=== G6 non-scope = zero (flag ON, empty scope) ===")
    setf({"BARI_SHELF_RELATIVE_V1":"on"})
    from score_engine import set_shelf_stats, clear_shelf_stats
    set_shelf_stats("sugars_g",25.0,5.0,"iqr",n=30)
    nz=0
    for d in [ROOT/"03_operations/bsip1/run_cereals_008/output", ROOT/"03_operations/bsip1/run_001/output", ROOT/"02_products/bread_retail_001/bsip1"]:
        if not d.exists(): continue
        for fp in list(d.glob("*.json"))[:40]:
            r=score(json.loads(fp.read_text(encoding="utf-8")))
            for p in (r.get("penalties_applied") or []):
                if "SHELF_REL" in (p.get("rule") or "") and p.get("amount",0)!=0: nz+=1
    clear_shelf_stats()
    print(f"nonzero_shelf_rel_penalties={nz}")
    return nz==0

if __name__=="__main__":
    results={"G1":guard_g1(),"G2":guard_g2(),"G3":guard_g3(),"G4":guard_g4(),"G5":guard_g5(),"G6":guard_g6()}
    print("=== SUMMARY ===")
    for k,v in results.items(): print(k, "PASS" if v else "FAIL")
    sys.exit(0 if all(results.values()) else 1)
