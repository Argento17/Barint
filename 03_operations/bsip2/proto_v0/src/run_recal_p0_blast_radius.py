"""
TASK-169A — BSIP2 P0 Recalibration blast-radius MODEL (NOT shipped).

Scores each corpus through the standard pipeline TWICE on the SAME engine, toggling only
BARI_RECAL_P0 (off → on). Flag OFF must be byte-identical to the published 0.4.1 baseline
(the safety contract); flag ON records the intended recalibration diffs.

Writes a scratch modeling output dir under 02_products/_recal_p0_model/ — it does NOT
overwrite any published run dir. Read-only against the frozen corpora.

Corpora:
  affected : cheese (run_cheese_003), hummus (canonical_bsip1 = run_hummus_002 lineage)
  frozen   : milk (run_milk_002 -> run_004_recalibrated), yogurt (run_yogurt_003)
             (bread retail_003 + snack_bars handled separately — bespoke loaders)
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

# Each entry: load_batch-compatible BSIP1 output dir.
CORPORA = {
    # affected (recal targets)
    "cheese":     (r"C:\Bari\03_operations\bsip1\run_cheese_003\output", "affected"),
    "hummus":     (r"C:\Bari\02_products\hummus\canonical_bsip1",        "affected"),
    # frozen invariants
    "milk":       (r"C:\Bari\03_operations\bsip1\run_milk_002\output",   "frozen"),
    "yogurt":     (r"C:\Bari\03_operations\bsip1\run_yogurt_003\output", "frozen"),
    "snack_bars": (r"C:\Bari\03_operations\bsip1\run_001\output",        "frozen"),
}

OUT_ROOT = pathlib.Path(r"C:\Bari\02_products\_recal_p0_model")

_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]


def _run(source, recal_on, task144_on=False):
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    os.environ["BARI_TASK144_FIXES"] = "on" if task144_on else "off"
    for m in _MODULES:
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
            res[pid] = {
                "name": product.get("canonical_name_he", ""),
                "score": r.get("final_score_estimate"),
                "grade": r.get("grade_estimate"),
                "ds": r.get("data_sufficiency"),
                "cat": cat["category"],
                "subtype": cat.get("category_subtype"),
                "nova": nova.get("nova_level"),
                "nova_r4": nova.get("nova_r4_demotion_applied"),
                "ferm_bonus": r.get("fermentation_bonus_applied"),
                "ferm_note": r.get("fermentation_bonus_note"),
                "veg_spread": r.get("recal_p0_veg_spread"),
                "dims": r.get("dimension_scores"),
            }
        except Exception as e:
            res[pid] = {"name": product.get("canonical_name_he", ""), "error": str(e)}
    return res


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    summary = {}
    for cat, (src, klass) in CORPORA.items():
        if not pathlib.Path(src).exists():
            summary[cat] = {"missing_source": src, "class": klass}
            continue
        base = _run(src, recal_on=False)
        recal = _run(src, recal_on=True)

        # OFF byte-identical guard: compare flag-OFF run to itself? No — we record OFF as
        # the baseline and the diffs are OFF->ON. The OFF==published check is done
        # separately against the published traces in verify_off_identical.py for cheese.
        changes = []
        off_errors = sum(1 for p in base.values() if p.get("error"))
        for pid, p in recal.items():
            b = base.get(pid, {})
            if p.get("error") or b.get("error"):
                continue
            moved = (b.get("score") != p.get("score")) or (b.get("grade") != p.get("grade"))
            if moved:
                delta = None
                if isinstance(b.get("score"), (int, float)) and isinstance(p.get("score"), (int, float)):
                    delta = round(p["score"] - b["score"], 1)
                changes.append({
                    "pid": pid, "name": p["name"], "cat": p.get("cat"),
                    "subtype": p.get("subtype"),
                    "old_score": b.get("score"), "old_grade": b.get("grade"),
                    "new_score": p.get("score"), "new_grade": p.get("grade"),
                    "delta": delta,
                    "grade_change": b.get("grade") != p.get("grade"),
                    "nova_off": b.get("nova"), "nova_on": p.get("nova"),
                    "nova_r4": p.get("nova_r4"),
                    "ferm_on": p.get("ferm_bonus"), "ferm_note_on": p.get("ferm_note"),
                    "veg_spread": p.get("veg_spread"),
                })
        changes.sort(key=lambda c: (c["delta"] if c["delta"] is not None else -999), reverse=True)
        summary[cat] = {
            "class": klass,
            "source": src,
            "corpus": len(recal),
            "off_errors": off_errors,
            "score_changes": len(changes),
            "grade_changes": sum(1 for c in changes if c["grade_change"]),
            "changes": changes,
        }
        # persist full OFF/ON tables for the report
        (OUT_ROOT / f"{cat}_off.json").write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT_ROOT / f"{cat}_on.json").write_text(json.dumps(recal, ensure_ascii=False, indent=2), encoding="utf-8")

    (OUT_ROOT / "blast_radius_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    for cat, s in summary.items():
        if "missing_source" in s:
            print(f"{cat:11s} MISSING: {s['missing_source']}")
            continue
        print(f"{cat:11s} [{s['class']:8s}] corpus={s['corpus']:3d} "
              f"off_err={s['off_errors']:2d} score_changes={s['score_changes']:3d} "
              f"grade_changes={s['grade_changes']:2d}")
    print("written:", OUT_ROOT / "blast_radius_summary.json")


if __name__ == "__main__":
    main()
