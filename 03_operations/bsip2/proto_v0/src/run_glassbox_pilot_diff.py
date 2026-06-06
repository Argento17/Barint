"""
TASK-179G — Glass Box D5/D6 ON-vs-OFF pilot diff (hummus + maadanim).

Scores both pilot corpora through the standard pipeline TWICE, toggling only
BARI_GLASSBOX_D5D6 (off -> on), and proves EVERY ON-vs-OFF delta is a DEMOTE or a
NULL — never a promotion (no score up, no grade improvement). Models
run_recal_p0_blast_radius.py. Read-only; writes scratch JSON under reports/glass_box/.
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

OUT = pathlib.Path(__file__).parent.parent / "reports" / "glass_box"
CORPORA = {
    "hummus":   r"C:\Bari\02_products\hummus\canonical_bsip1",
    "maadanim": r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",
}
_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]

_GRADE_RANK = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4, "S": 5,
               "insufficient_data": -1, "לא נוקד": -2, None: -3}


def _run(source, glass_on):
    os.environ["BARI_GLASSBOX_D5D6"] = "on" if glass_on else "off"
    os.environ["BARI_RECAL_P0"] = "off"
    os.environ["BARI_TASK144_FIXES"] = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)
    import io, contextlib
    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    out = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        products = list(load_batch(pathlib.Path(source)))
    for p in products:
        pid = p.get("canonical_product_id", "?")
        try:
            sig = extract_signals(p)
            cat = classify_category(p)
            nova = infer_nova(p, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(p, cat["category"])
            r = score_product(p, sig, cat, nova, ev)
            dp = r.get("glassbox_disclosure_profile") or {}
            cr = r.get("confidence_result") or {}
            out[pid] = {
                "name": p.get("canonical_name_he", ""),
                "score": r.get("final_score_estimate"),
                "grade": r.get("grade_estimate"),
                "conf": cr.get("confidence_score"),
                "gate": r.get("glassbox_d6_gate_state"),
                "d5_band": dp.get("d5_band"),
                "panel_present": dp.get("panel_present"),
                "endemic_flav": (dp.get("counts") or {}).get("endemic_flavoring"),
                "findings": [f.get("type") for f in dp.get("findings", [])],
                "closable_n": (dp.get("counts") or {}).get("closable_n"),
            }
        except Exception as e:
            out[pid] = {"name": p.get("canonical_name_he", ""), "_error": repr(e)}
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    grand = {}
    promotions = []
    for cat, src in CORPORA.items():
        off = _run(src, glass_on=False)
        on = _run(src, glass_on=True)
        demoted, withheld, unchanged, other = [], [], [], []
        for pid, o in on.items():
            b = off.get(pid, {})
            if o.get("_error") or b.get("_error"):
                other.append(pid); continue
            os_, ns = b.get("score"), o.get("score")
            og, ng = b.get("grade"), o.get("grade")
            rec = {"pid": pid, "name": o["name"], "off": f"{os_}/{og}",
                   "on": f"{ns}/{ng}", "off_conf": b.get("conf"), "on_conf": o.get("conf"),
                   "gate": o.get("gate"), "d5_band": o.get("d5_band"),
                   "findings": o.get("findings"), "endemic_flav": o.get("endemic_flav")}
            if ng == "לא נוקד" or ns is None and og != ng:
                withheld.append(rec)
            elif (os_, og) == (ns, ng):
                unchanged.append(pid)
            else:
                # changed but not withheld → must be a demote
                demoted.append(rec)
                # promotion guard: score up OR grade rank up = VIOLATION
                score_up = (isinstance(os_, (int, float)) and isinstance(ns, (int, float))
                            and ns > os_)
                grade_up = _GRADE_RANK.get(ng, -3) > _GRADE_RANK.get(og, -3)
                if score_up or grade_up:
                    promotions.append(rec)
        grand[cat] = {
            "n": len(on), "demoted": demoted, "withheld": withheld,
            "n_demoted": len(demoted), "n_withheld": len(withheld),
            "n_unchanged": len(unchanged), "n_other": len(other),
            "endemic_count": sum(1 for o in on.values() if o.get("endemic_flav")),
        }
        (OUT / f"_pilot_{cat}_off.json").write_text(
            json.dumps(off, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT / f"_pilot_{cat}_on.json").write_text(
            json.dumps(on, ensure_ascii=False, indent=2), encoding="utf-8")

    grand["_promotions_VIOLATION"] = promotions
    (OUT / "_pilot_summary.json").write_text(
        json.dumps(grand, ensure_ascii=False, indent=2), encoding="utf-8")

    for cat in CORPORA:
        s = grand[cat]
        print(f"{cat:9s} n={s['n']:3d} demoted={s['n_demoted']:3d} "
              f"withheld={s['n_withheld']:3d} unchanged={s['n_unchanged']:3d} "
              f"endemic_flavoring={s['endemic_count']:3d}")
    print("PROMOTIONS (must be 0):", len(promotions))
    print("written:", OUT / "_pilot_summary.json")


if __name__ == "__main__":
    main()
