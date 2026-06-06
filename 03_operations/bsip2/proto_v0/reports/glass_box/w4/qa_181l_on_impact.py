"""
TASK-181L (QA) — Glass Box W4 REWORK ON score-impact analysis (post medium-band split).

Read-only. Runs the engine OFF and ON across the 4 scored corpora, broken down by the
NEW uncertainty_materiality field (material / non_material / None[=high|low band]) and
confidence band. Produces the before/after vs the 181H baseline (17-down / 3-up).

Confirms:
  - medium-non-material products no longer move grade (and ideally not score);
  - material + low products still move (the defensible movers);
  - frozen invariants hold (milk top 85/A, snack ceiling 70/B, no snack A).

Does NOT flip the flag, rescore, or touch published data.
Output -> reports/glass_box/w4/qa_181l_on_impact.json
"""
import os, sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))

OUT = pathlib.Path(__file__).parent / "qa_181l_on_impact.json"

CORPORA = {
    "hummus":      r"C:\Bari\02_products\hummus\canonical_bsip1",
    "maadanim":    r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",
    "snack_bars":  r"C:\Bari\03_operations\bsip1\run_001\output",
    "golden_milk": r"C:\Bari\03_operations\bsip1\run_milk_002\output",
}
_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]


def _score_corpus(source, w4_on):
    os.environ["BARI_GLASSBOX_W4"]   = "on" if w4_on else "off"
    os.environ["BARI_GLASSBOX_D5D6"] = "off"
    os.environ["BARI_GLASSBOX_W2"]   = "off"
    os.environ["BARI_GLASSBOX_W15"]  = "off"
    os.environ["BARI_RECAL_P0"]      = "off"
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
    for product in products:
        pid = product.get("canonical_product_id", "?")
        try:
            sig  = extract_signals(product)
            cat  = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev   = assign_evaluation_scope(product, cat["category"])
            out[pid] = score_product(product, sig, cat, nova, ev)
        except Exception as e:
            out[pid] = {"_error": repr(e)}
    return out


def _mat_key(sig, band):
    """material / non_material for medium band; for high/low report the band itself."""
    if band == "medium":
        return sig.get("uncertainty_materiality") or "medium_unknown"
    return band  # high | low


def main():
    GRADE_ORD = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, None: 0}
    report = {"corpora": {}, "grade_changes": [], "frozen_check": {}}

    g_score_moves = g_grade_moves = 0
    dir_grade = {"up": 0, "down": 0}
    # buckets keyed by materiality class
    mat_score = {}   # cls -> [moves, total]
    mat_grade = {}   # cls -> moves
    band_grade = {"high": 0, "medium": 0, "low": 0, "none": 0}

    def _bump(d, k, n=1):
        d[k] = d.get(k, 0) + n

    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            report["corpora"][name] = "MISSING_SOURCE"; continue
        off = _score_corpus(src, False)
        on  = _score_corpus(src, True)
        c = {"n": len(on), "score_moves": 0, "grade_moves": 0, "max_abs_delta": 0.0,
             "moves_by_materiality": {}, "signal_by_materiality": {}}
        for pid, r in on.items():
            o = off.get(pid, {})
            so = o.get("final_score_estimate"); sn = r.get("final_score_estimate")
            go = o.get("grade_estimate");       gn = r.get("grade_estimate")
            sig = r.get("d3_processing_signal") or {}
            band = sig.get("confidence", "none")
            cls = _mat_key(sig, band) if sig else "none"
            mat_score.setdefault(cls, [0, 0]); mat_grade.setdefault(cls, 0)
            if sig:
                mat_score[cls][1] += 1
                _bump(c["signal_by_materiality"], cls)
            if so is not None and sn is not None and so != sn:
                c["score_moves"] += 1; g_score_moves += 1
                d = round(sn - so, 1)
                c["max_abs_delta"] = max(c["max_abs_delta"], abs(d))
                mat_score[cls][0] += 1
                _bump(c["moves_by_materiality"], cls)
            if go != gn:
                c["grade_moves"] += 1; g_grade_moves += 1
                mat_grade[cls] += 1
                band_grade[band] = band_grade.get(band, 0) + 1
                direction = "up" if GRADE_ORD.get(gn, 0) > GRADE_ORD.get(go, 0) else "down"
                dir_grade[direction] += 1
                report["grade_changes"].append({
                    "corpus": name, "pid": pid, "grade_off": go, "grade_on": gn,
                    "direction": direction, "score_off": so, "score_on": sn,
                    "delta": round((sn or 0) - (so or 0), 2),
                    "nova_class": sig.get("nova_class"), "confidence_band": band,
                    "uncertainty_materiality": sig.get("uncertainty_materiality"),
                    "modifier": sig.get("modifier"),
                    "low_conf_nova": r.get("d3_low_confidence_nova"),
                    "nonmaterial_gap": r.get("d3_nonmaterial_gap"),
                })
        report["corpora"][name] = c

    report["totals"] = {
        "score_moves": g_score_moves, "grade_moves": g_grade_moves,
        "grade_dir": dir_grade,
        "grade_moves_by_band": band_grade,
        "score_moves_by_materiality": {k: v[0] for k, v in mat_score.items()},
        "signal_by_materiality": {k: v[1] for k, v in mat_score.items()},
        "grade_moves_by_materiality": mat_grade,
    }

    # frozen-invariant checks
    fc = {}
    milk_on = _score_corpus(CORPORA["golden_milk"], True)
    fc["milk_top3_ON"] = sorted(
        [(p, r.get("final_score_estimate"), r.get("grade_estimate"))
         for p, r in milk_on.items() if r.get("final_score_estimate") is not None],
        key=lambda t: (t[1] or 0), reverse=True)[:3]
    snack_on = _score_corpus(CORPORA["snack_bars"], True)
    snack_ranked = sorted(
        [(p, r.get("final_score_estimate"), r.get("grade_estimate"))
         for p, r in snack_on.items() if r.get("final_score_estimate") is not None],
        key=lambda t: (t[1] or 0), reverse=True)[:5]
    fc["snack_top5_ON"] = snack_ranked
    fc["snack_any_A_ON"] = any(g == "A" for _, _, g in snack_ranked)
    report["frozen_check"] = fc

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["totals"], ensure_ascii=False, indent=2))
    print("\nGRADE CHANGES:", len(report["grade_changes"]))
    for gc in report["grade_changes"]:
        print(f"  {gc['corpus']:11s} {gc['pid']:30s} {gc['grade_off']}->{gc['grade_on']} "
              f"({gc['direction']:4s}) {gc['score_off']}->{gc['score_on']} "
              f"nova={gc['nova_class']} band={gc['confidence_band']} "
              f"mat={gc['uncertainty_materiality']} lowconf={gc['low_conf_nova']}")
    print("\nFROZEN milk top3 ON:", fc["milk_top3_ON"])
    print("FROZEN snack top5 ON:", fc["snack_top5_ON"], "any A:", fc["snack_any_A_ON"])
    print("\nwritten:", OUT)


if __name__ == "__main__":
    main()
