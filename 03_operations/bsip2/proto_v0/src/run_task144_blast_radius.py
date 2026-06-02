"""
TASK-144 — Cross-category blast-radius check.

For each frozen/important category, runs its BSIP1 corpus through the pipeline twice on
the SAME patched engine, toggling only the TASK-144 fixes (BARI_TASK144_FIXES off/on).
Reports any product whose score or GRADE changed — these are the cross-category effects
of Fix1 (sanitizer, cross-category) and Fix2 (gated; should be inert outside dairy) and
Fix3 (dairy source typing). Does NOT write traces — read-only blast radius.
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

CATEGORIES = {
    "snack_bars":   r"C:\Bari\03_operations\bsip1\run_001\output",
    "cereals":      r"C:\Bari\03_operations\bsip1\run_cereals_001\output",
    "milk":         r"C:\Bari\03_operations\bsip1\run_milk_002\output",
    "cheese":       r"C:\Bari\03_operations\bsip1\run_cheese_001\output",
    "hummus":       r"C:\Bari\03_operations\bsip1\run_hummus_001\output",
    "yogurt":       r"C:\Bari\03_operations\bsip1\run_yogurt_003\output",
    "bread_light":  r"C:\Bari\03_operations\bsip1\run_bread_light_001\output",
}


def _run(source, fixes_on):
    os.environ["BARI_TASK144_FIXES"] = "on" if fixes_on else "off"
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
    res = {}
    for product in load_batch(pathlib.Path(source)):
        pid = product.get("canonical_product_id", "?")
        try:
            sig = extract_signals(product)
            cat = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(product, cat["category"])
            r = score_product(product, sig, cat, nova, ev)
            res[pid] = {"name": product.get("canonical_name_he", ""),
                        "score": r.get("final_score_estimate"),
                        "grade": r.get("grade_estimate"),
                        "ds": r.get("data_sufficiency"),
                        "cat": cat["category"]}
        except Exception as e:
            res[pid] = {"name": product.get("canonical_name_he", ""), "error": str(e)}
    return res


def main():
    summary = {}
    for cat, src in CATEGORIES.items():
        if not pathlib.Path(src).exists():
            summary[cat] = {"missing_source": src}
            continue
        base = _run(src, False)
        patched = _run(src, True)
        changes = []
        for pid, p in patched.items():
            b = base.get(pid, {})
            if p.get("error"):
                continue
            if b.get("score") != p.get("score") or b.get("grade") != p.get("grade"):
                changes.append({
                    "name": p["name"], "cat": p.get("cat"),
                    "old": f"{b.get('score')}/{b.get('grade')}",
                    "new": f"{p.get('score')}/{p.get('grade')}",
                    "grade_change": b.get("grade") != p.get("grade"),
                })
        gradech = [c for c in changes if c["grade_change"]]
        summary[cat] = {
            "corpus": len(patched),
            "score_changes": len(changes),
            "grade_changes": len(gradech),
            "grade_change_detail": gradech,
        }
    out = pathlib.Path(r"C:\Bari\02_products\maadanim\task144_blast_radius.json")
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    for cat, s in summary.items():
        if "missing_source" in s:
            print(f"{cat:12s} MISSING SOURCE")
        else:
            print(f"{cat:12s} corpus={s['corpus']:3d}  score_changes={s['score_changes']:3d}  grade_changes={s['grade_changes']}")
            for g in s["grade_change_detail"]:
                print(f"             GRADE: {g['old']} -> {g['new']}  [{g['cat']}] {g['name']}")
    print("written:", out)


if __name__ == "__main__":
    main()
