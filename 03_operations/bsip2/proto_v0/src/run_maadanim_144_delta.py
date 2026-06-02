"""
TASK-144 — Controlled before/after delta for the maadanim corpus.

Runs the FULL maadanim BSIP1 corpus through the pipeline twice on the SAME (patched)
engine + SAME router, toggling only the three TASK-144 fixes via BARI_TASK144_FIXES:
  - baseline pass  (fixes OFF)  → isolates the pre-existing engine state
  - patched pass   (fixes ON)   → the new 0.4.1 result
This attributes score deltas cleanly to TASK-144 (NOT to any pre-existing router drift,
which is identical in both passes).

The patched pass ALSO writes the regenerated traces to the run output directory
(this is the deliverable). It does NOT touch any frontend JSON.
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_maadanim_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001")
GO_ID        = "bsip1_maadanim_7290110321031"


def _run_corpus(fixes_on: bool, write_traces: bool):
    os.environ["BARI_TASK144_FIXES"] = "on" if fixes_on else "off"
    # Fresh import so the module-level toggles re-read the env var.
    for m in ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
              "router_v2", "evaluation_scope", "input_loader", "constants",
              "structural_classifier"]:
        sys.modules.pop(m, None)
    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    from trace_writer import assemble_trace, write_trace
    from structural_classifier import classify_structural_class

    products = load_batch(BSIP1_SOURCE)
    results = {}
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            signals = extract_signals(product)
            cat_result = classify_category(product)
            l3 = signals["L3_inferred_classifications"]
            nova_result = infer_nova(product, l3)
            eval_result = assign_evaluation_scope(product, cat_result["category"])
            score_result = score_product(product, signals, cat_result, nova_result, eval_result)
            trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
            trace["structural_class"] = classify_structural_class(trace)
            if write_traces:
                write_trace(trace, OUTPUT_ROOT)
            results[pid] = {
                "name": product.get("canonical_name_he", ""),
                "score": trace.get("final_score_estimate"),
                "grade": trace.get("grade_estimate"),
                "nova": trace.get("nova_proxy"),
                "category": trace.get("category"),
                "data_sufficiency": trace.get("data_sufficiency"),
            }
        except Exception as e:
            results[pid] = {"name": product.get("canonical_name_he", ""), "error": str(e)}
    return results


def main():
    base = _run_corpus(fixes_on=False, write_traces=False)
    patched = _run_corpus(fixes_on=True, write_traces=True)

    changes = []
    for pid, p in patched.items():
        b = base.get(pid, {})
        if p.get("error") or b.get("error"):
            if p.get("error"):
                changes.append({"pid": pid, "name": p.get("name"), "error": p["error"]})
            continue
        if (b.get("score") != p.get("score")) or (b.get("grade") != p.get("grade")):
            changes.append({
                "pid": pid, "name": p.get("name"),
                "old_score": b.get("score"), "new_score": p.get("score"),
                "old_grade": b.get("grade"), "new_grade": p.get("grade"),
                "old_nova": b.get("nova"), "new_nova": p.get("nova"),
                "category": p.get("category"),
                "grade_change": b.get("grade") != p.get("grade"),
            })

    out = {
        "corpus_size": len(patched),
        "changed_count": len(changes),
        "grade_changes": sum(1 for c in changes if c.get("grade_change")),
        "go": {"pid": GO_ID, "base": base.get(GO_ID), "patched": patched.get(GO_ID)},
        "a_grades_patched": sorted(
            [(p["name"], p["score"]) for p in patched.values()
             if not p.get("error") and p.get("grade") in ("A", "S")],
            key=lambda x: -(x[1] or 0)),
        "changes": sorted(changes, key=lambda c: -((c.get("new_score") or 0) - (c.get("old_score") or 0))),
    }
    report_path = pathlib.Path(r"C:\Bari\02_products\maadanim") / "task144_delta_data.json"
    report_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in
                      ["corpus_size", "changed_count", "grade_changes", "go", "a_grades_patched"]},
                     ensure_ascii=False, indent=2))
    print("changes_written:", report_path)


if __name__ == "__main__":
    main()
