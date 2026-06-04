"""
TASK-181H (QA) — Glass Box W4 ON score-impact analysis.

Read-only. Runs the engine OFF and ON across the 4 available scored corpora,
emits the full delta distribution, the complete grade-change list (per product,
old->new, confidence band, NOVA class, score delta), and the frozen-invariant
check (milk top 85/A on golden_milk; snack ceiling on snack_bars; bread n/a here).

Does NOT touch published frontend JSON. Output -> reports/glass_box/w4/qa_181h_on_impact.json
This mirrors the verifier's _score_corpus discipline (flags pinned explicitly).
"""
import os, sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))

OUT = pathlib.Path(__file__).parent / "qa_181h_on_impact.json"

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

def main():
    report = {"corpora": {}, "grade_changes": [], "frozen_check": {}}
    # global delta buckets
    g_score_moves = 0
    g_grade_moves = 0
    delta_hist = {}  # rounded delta -> count
    band_score = {"high": [0,0], "medium": [0,0], "low": [0,0], "none":[0,0]}  # [moves, total_with_signal]
    band_grade = {"high": 0, "medium": 0, "low": 0, "none":0}
    dir_grade = {"up": 0, "down": 0}  # up = less punitive (higher grade)
    GRADE_ORD = {"A":5,"B":4,"C":3,"D":2,"E":1,None:0}

    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            report["corpora"][name] = "MISSING_SOURCE"; continue
        off = _score_corpus(src, False)
        on  = _score_corpus(src, True)
        c = {"n": len(on), "score_moves": 0, "grade_moves": 0,
             "max_abs_delta": 0.0, "moves_by_band": {}, "with_signal": 0}
        for pid, r in on.items():
            o = off.get(pid, {})
            so = o.get("final_score_estimate"); sn = r.get("final_score_estimate")
            go = o.get("grade_estimate");       gn = r.get("grade_estimate")
            sig = r.get("d3_processing_signal") or {}
            band = sig.get("confidence", "none")
            if sig: c["with_signal"] += 1; band_score[band][1]+=1
            else: band_score["none"][1]+=1
            if so is not None and sn is not None and so != sn:
                c["score_moves"] += 1; g_score_moves += 1
                d = round(sn - so, 1)
                delta_hist[d] = delta_hist.get(d, 0) + 1
                c["max_abs_delta"] = max(c["max_abs_delta"], abs(d))
                band_score[band][0]+=1
                c["moves_by_band"][band] = c["moves_by_band"].get(band,0)+1
            if go != gn:
                c["grade_moves"] += 1; g_grade_moves += 1
                band_grade[band] += 1
                direction = "up" if GRADE_ORD.get(gn,0) > GRADE_ORD.get(go,0) else "down"
                dir_grade[direction] += 1
                report["grade_changes"].append({
                    "corpus": name, "pid": pid,
                    "grade_off": go, "grade_on": gn, "direction": direction,
                    "score_off": so, "score_on": sn,
                    "delta": round((sn or 0)-(so or 0),2),
                    "nova_class": sig.get("nova_class"),
                    "confidence_band": band,
                    "modifier": sig.get("modifier"),
                    "low_conf_nova": r.get("d3_low_confidence_nova"),
                })
        report["corpora"][name] = c

    report["totals"] = {
        "score_moves": g_score_moves, "grade_moves": g_grade_moves,
        "grade_dir": dir_grade,
        "grade_moves_by_band": band_grade,
        "score_moves_by_band": {b: band_score[b][0] for b in band_score},
        "products_with_signal_by_band": {b: band_score[b][1] for b in band_score},
        "delta_histogram": {str(k): delta_hist[k] for k in sorted(delta_hist)},
    }

    # Frozen-invariant checks
    # milk top: golden_milk highest ON score/grade
    fc = {}
    milk_on = _score_corpus(CORPORA["golden_milk"], True)
    milk_ranked = sorted(
        [(p, r.get("final_score_estimate"), r.get("grade_estimate"))
         for p,r in milk_on.items() if r.get("final_score_estimate") is not None],
        key=lambda t: (t[1] or 0), reverse=True)[:3]
    fc["milk_top3_ON"] = milk_ranked
    snack_on = _score_corpus(CORPORA["snack_bars"], True)
    snack_ranked = sorted(
        [(p, r.get("final_score_estimate"), r.get("grade_estimate"))
         for p,r in snack_on.items() if r.get("final_score_estimate") is not None],
        key=lambda t: (t[1] or 0), reverse=True)[:5]
    fc["snack_top5_ON"] = snack_ranked
    fc["snack_any_A_ON"] = any(g=="A" for _,_,g in snack_ranked)
    report["frozen_check"] = fc

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["totals"], ensure_ascii=False, indent=2))
    print("\nGRADE CHANGES:", len(report["grade_changes"]))
    for gc in report["grade_changes"]:
        print(f"  {gc['corpus']:11s} {gc['pid']:28s} {gc['grade_off']}->{gc['grade_on']} "
              f"({gc['direction']:4s}) score {gc['score_off']}->{gc['score_on']} "
              f"nova={gc['nova_class']} band={gc['confidence_band']} lowconf={gc['low_conf_nova']}")
    print("\nFROZEN milk top3 ON:", fc["milk_top3_ON"])
    print("FROZEN snack top5 ON:", fc["snack_top5_ON"], "any A:", fc["snack_any_A_ON"])
    print("\nwritten:", OUT)

if __name__ == "__main__":
    main()
