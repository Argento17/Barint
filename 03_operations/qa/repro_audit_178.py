"""
TASK-178 read-only repro audit.
Re-runs HEAD BSIP2 pipeline against the same BSIP1 source used by a published run,
compares final_score_estimate / grade_estimate against the published trace.
WRITES NOTHING to product dirs. Prints a delta table + reproduction rate.
"""
import sys, json, pathlib, argparse, io, contextlib

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class


def run_pipeline(product):
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def load_published(products_dir):
    pub = {}
    for d in pathlib.Path(products_dir).iterdir():
        tf = d / "bsip2_trace.json"
        if tf.exists():
            t = json.load(open(tf, encoding="utf-8"))
            pid = t.get("input_reference", {}).get("canonical_product_id") or d.name
            pub[d.name] = t
    return pub


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bsip1", required=True)
    ap.add_argument("--published", required=True)
    ap.add_argument("--label", required=True)
    args = ap.parse_args()

    pub = load_published(args.published)
    # suppress engine logging noise
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        products = load_batch(pathlib.Path(args.bsip1))
        head = {}
        for p in products:
            pid = p.get("canonical_product_id", "unknown")
            try:
                head[pid] = run_pipeline(p)
            except Exception as e:
                head[pid] = {"_error": str(e)}

    rows = []
    matched = 0
    grade_aff = 0
    cosmetic = 0
    for dname, pt in sorted(pub.items()):
        pid = pt.get("input_reference", {}).get("canonical_product_id") or dname
        ht = head.get(pid)
        ps = pt.get("final_score_estimate")
        pg = pt.get("grade_estimate")
        if ht is None:
            rows.append((dname, ps, pg, "NO_HEAD", "-", "-", "MISSING"))
            continue
        if "_error" in ht:
            rows.append((dname, ps, pg, "ERR", "-", "-", ht["_error"][:30]))
            continue
        hs = ht.get("final_score_estimate")
        hg = ht.get("grade_estimate")
        if ps is None and hs is None:
            verdict = "MATCH(null)"; matched += 1
            delta = "-"
        elif ps is None or hs is None:
            verdict = "NULL_FLIP"; delta = "n/a"
        else:
            delta = round(hs - ps, 1)
            if abs(delta) < 0.05 and pg == hg:
                verdict = "MATCH"; matched += 1
            elif pg != hg:
                verdict = "GRADE_FLIP"; grade_aff += 1
            elif abs(delta) >= 2:
                verdict = "DRIFT>=2"; grade_aff += 1
            else:
                verdict = "cosmetic"; cosmetic += 1
        rows.append((dname, ps, pg, hs, hg, delta, verdict))

    print(f"\n=== {args.label}: HEAD vs published ===")
    print(f"products published: {len(pub)}   reproduced exactly: {matched}/{len(pub)}")
    print(f"grade-affecting deltas: {grade_aff}   cosmetic (<2pt, same grade): {cosmetic}")
    print(f"\n{'product':40} {'pub_s':>6} {'pg':>3} {'head_s':>7} {'hg':>3} {'delta':>7}  verdict")
    for r in rows:
        name = r[0][:40]
        print(f"{name:40} {str(r[1]):>6} {str(r[2]):>3} {str(r[3]):>7} {str(r[4]):>3} {str(r[5]):>7}  {r[6]}")


if __name__ == "__main__":
    main()
