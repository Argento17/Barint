"""
TASK-169A — Safety-contract verifier: with BARI_RECAL_P0 OFF, re-scoring the cheese_003
corpus must reproduce the PUBLISHED run_cheese_003 traces byte-for-byte (final score,
grade, every dimension). Any mismatch breaks the rollback guarantee.
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_003\output")
PUB = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_003\products")

os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_TASK144_FIXES"] = "off"

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product


def published_trace(pid):
    d = PUB / pid / "bsip2_trace.json"
    if d.exists():
        return json.load(open(d, encoding="utf-8"))
    return None


def main():
    mism = []
    n = 0
    for product in load_batch(SRC):
        pid = product.get("canonical_product_id", "?")
        pub = published_trace(pid)
        if pub is None:
            continue
        n += 1
        sig = extract_signals(product)
        cat = classify_category(product)
        nova = infer_nova(product, sig["L3_inferred_classifications"])
        ev = assign_evaluation_scope(product, cat["category"])
        r = score_product(product, sig, cat, nova, ev)
        cur_score = r.get("final_score_estimate")
        pub_score = pub.get("final_score_estimate")
        cur_dims = r.get("dimension_scores") or {}
        pub_dims = pub.get("dimension_scores") or {}
        dim_mismatch = {k: (pub_dims.get(k), cur_dims.get(k))
                        for k in cur_dims if pub_dims.get(k) != cur_dims.get(k)}
        if cur_score != pub_score or r.get("grade_estimate") != pub.get("grade_estimate") or dim_mismatch:
            mism.append({"pid": pid, "name": product.get("canonical_name_he", ""),
                         "pub": f"{pub_score}/{pub.get('grade_estimate')}",
                         "cur": f"{cur_score}/{r.get('grade_estimate')}",
                         "dim_mismatch": dim_mismatch})
    print(f"compared={n}  mismatches={len(mism)}")
    for m in mism[:30]:
        print(" MISMATCH", m["pid"], m["pub"], "->", m["cur"], m["dim_mismatch"])
    print("OFF byte-identical:" , "PASS" if not mism else "FAIL")


if __name__ == "__main__":
    main()
