"""
TASK-181G — Glass Box W4 D3 de-moralization byte-identical OFF verifier.

Mirrors the BARI_GLASSBOX_W2 discipline (verify_glassbox_w2_off_identical.py):
with BARI_GLASSBOX_W4=off the FULL score_product() result dict for every product
in the test corpus must be byte-identical to the pre-change baseline.

score_product() is the single entry point modified by the W4 change, so an
OFF-identical result guarantees every downstream consumer is unaffected.

Three modes:
  python verify_glassbox_w4_off_identical.py snapshot   # capture baseline (run BEFORE editing)
  python verify_glassbox_w4_off_identical.py check      # re-run with flag OFF, diff vs baseline
  python verify_glassbox_w4_off_identical.py on_smoke   # run with flag ON, report d3_processing_signal

Baseline persisted to: reports/glass_box/w4/_off_baseline.json

NOTE: this verifier explicitly sets BARI_GLASSBOX_W4 in every scoring run so the
OFF/ON state is controlled here, not inherited from the ambient environment. The
W2/W15/D5D6 flags are pinned OFF so the W4 OFF baseline equals the W2 baseline.
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

BASELINE = (pathlib.Path(__file__).parent.parent
            / "reports" / "glass_box" / "w4" / "_off_baseline.json")

# Same corpora as the W2 verifier. hummus + maadanim are the pilot (have ingredient
# text); snack_bars + golden_milk are FROZEN and must always show 0 diffs.
CORPORA = {
    "hummus":      r"C:\Bari\02_products\hummus\canonical_bsip1",
    "maadanim":    r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",
    "snack_bars":  r"C:\Bari\03_operations\bsip1\run_001\output",       # frozen — must show 0 diffs
    "golden_milk": r"C:\Bari\03_operations\bsip1\run_milk_002\output",  # frozen — must show 0 diffs
}

_MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "trace_writer",
    "router_v2", "evaluation_scope", "input_loader", "constants",
    "structural_classifier",
]


def _score_corpus(source, w4_on, d5d6_on=False, w2_on=False, w15_on=False):
    os.environ["BARI_GLASSBOX_W4"]    = "on" if w4_on else "off"
    os.environ["BARI_GLASSBOX_D5D6"]  = "on" if d5d6_on else "off"
    os.environ["BARI_GLASSBOX_W2"]    = "on" if w2_on else "off"
    os.environ["BARI_GLASSBOX_W15"]   = "on" if w15_on else "off"
    os.environ["BARI_RECAL_P0"]       = "off"
    os.environ["BARI_TASK144_FIXES"]  = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)
    import io
    import contextlib
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
            r    = score_product(product, sig, cat, nova, ev)
            out[pid] = r
        except Exception as e:
            out[pid] = {"_error": repr(e)}
    return out


def _canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)


def snapshot():
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    snap = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            snap[name] = {"_missing_source": src}
            continue
        res = _score_corpus(src, w4_on=False)
        snap[name] = {pid: _canon(r) for pid, r in res.items()}
        print(f"snapshot {name:12s} n={len(res)}")
    BASELINE.write_text(json.dumps(snap, ensure_ascii=False, indent=0), encoding="utf-8")
    print("baseline written:", BASELINE)


def check():
    if not BASELINE.exists():
        print("NO BASELINE — run `snapshot` first (before editing the engine).")
        sys.exit(2)
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    total_diffs = 0
    per_corpus = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            per_corpus[name] = "MISSING_SOURCE"
            continue
        res = _score_corpus(src, w4_on=False)
        cur = {pid: _canon(r) for pid, r in res.items()}
        b = base.get(name, {})
        diffs = [pid for pid in (set(b) | set(cur)) if b.get(pid) != cur.get(pid)]
        per_corpus[name] = {"n": len(cur), "diffs": len(diffs), "examples": diffs[:5]}
        total_diffs += len(diffs)
        print(f"check {name:12s} n={len(cur):4d} diffs={len(diffs)}")
    print()
    print("W4 FLAG-OFF BYTE-IDENTICAL:", "PASS (0-diff)" if total_diffs == 0 else f"FAIL ({total_diffs} diffs)")
    if total_diffs != 0:
        sys.exit(1)
    return per_corpus, total_diffs


def on_smoke():
    """ON smoke — report d3_processing_signal coverage + confidence distribution.
    NOT a score-impact analysis (that is QA's job, TASK-181H). This only confirms
    the struct emits, note_he wires, and the OFF→ON delta is bounded to D3."""
    summary = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            summary[name] = "MISSING_SOURCE"
            continue
        res_off = _score_corpus(src, w4_on=False)
        res_on  = _score_corpus(src, w4_on=True)
        conf_dist = {"high": 0, "medium": 0, "low": 0}
        note_dist = {"A": 0, "B": 0, "C": 0, "none": 0}
        n_signal = 0
        n_low_routed = 0
        score_moves = 0
        grade_moves = 0
        examples = []
        for pid, r in res_on.items():
            sig = r.get("d3_processing_signal")
            if sig:
                n_signal += 1
                conf_dist[sig["confidence"]] = conf_dist.get(sig["confidence"], 0) + 1
                nh = sig.get("note_he")
                from score_engine import (W4_NOTE_HE_A, W4_NOTE_HE_B, W4_NOTE_HE_C)
                if nh == W4_NOTE_HE_A:
                    note_dist["A"] += 1
                elif nh == W4_NOTE_HE_B:
                    note_dist["B"] += 1
                elif nh == W4_NOTE_HE_C:
                    note_dist["C"] += 1
                else:
                    note_dist["none"] += 1
            if r.get("d3_low_confidence_nova"):
                n_low_routed += 1
            off = res_off.get(pid, {})
            if off.get("final_score_estimate") != r.get("final_score_estimate"):
                score_moves += 1
            if off.get("grade_estimate") != r.get("grade_estimate"):
                grade_moves += 1
            if sig and len(examples) < 4:
                examples.append({"pid": pid, "nova": sig["nova_class"],
                                 "confidence": sig["confidence"],
                                 "modifier": sig["modifier"],
                                 "score_off": off.get("final_score_estimate"),
                                 "score_on": r.get("final_score_estimate"),
                                 "grade_off": off.get("grade_estimate"),
                                 "grade_on": r.get("grade_estimate")})
        summary[name] = {
            "n_total": len(res_on), "n_with_signal": n_signal,
            "confidence_distribution": conf_dist, "note_he_distribution": note_dist,
            "n_low_confidence_nova_routed": n_low_routed,
            "off_to_on_score_moves": score_moves, "off_to_on_grade_moves": grade_moves,
            "examples": examples,
        }
        print(f"ON smoke {name:12s} n={len(res_on):4d} signal={n_signal} "
              f"conf={conf_dist} notes={note_dist} low_routed={n_low_routed} "
              f"score_moves={score_moves} grade_moves={grade_moves}")
    out_path = BASELINE.parent / "_on_smoke_summary.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nON smoke summary written: {out_path}")
    return summary


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "snapshot":
        snapshot()
    elif mode == "on_smoke":
        on_smoke()
    else:
        check()
