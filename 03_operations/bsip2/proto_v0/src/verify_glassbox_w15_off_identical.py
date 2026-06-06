"""
TASK-179P — Glass Box W1.5 DIAAS byte-identical OFF verifier.

Mirrors the BARI_GLASSBOX_D5D6 discipline (verify_glassbox_off_identical.py):
with BARI_GLASSBOX_W15=off the FULL score_product() result dict for every product
in the test corpus must be byte-identical to the pre-change baseline.

score_product() is the single function modified by the W1.5 change, so an
OFF-identical result guarantees every downstream consumer is unaffected.

Two modes:
  python verify_glassbox_w15_off_identical.py snapshot   # capture baseline
  python verify_glassbox_w15_off_identical.py check      # re-run with flag OFF, diff vs baseline
  python verify_glassbox_w15_off_identical.py on_pilot   # run with flag ON, report credits/gaps

Baseline persisted to: reports/glass_box/w15/_off_baseline.json
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

BASELINE = (pathlib.Path(__file__).parent.parent
            / "reports" / "glass_box" / "w15" / "_off_baseline.json")

# Test corpus: hummus and maadanim have ingredient text (required for DIAAS detection).
# These are NOT frozen invariants (milk/snack/bread), so they are safe to use as a
# test set. The frozen corpora are included as a no-change safeguard.
CORPORA = {
    "hummus":       r"C:\Bari\02_products\hummus\canonical_bsip1",
    "maadanim":     r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",
    "snack_bars":   r"C:\Bari\03_operations\bsip1\run_001\output",     # frozen — must show 0 diffs
    "golden_milk":  r"C:\Bari\03_operations\bsip1\run_milk_002\output", # frozen — must show 0 diffs
}

_MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "trace_writer",
    "router_v2", "evaluation_scope", "input_loader", "constants",
    "structural_classifier",
]


def _score_corpus(source, w15_on, glassbox_d5d6_on=False):
    """Score all products in a corpus with the given flag settings."""
    os.environ["BARI_GLASSBOX_W15"]   = "on" if w15_on else "off"
    os.environ["BARI_GLASSBOX_D5D6"]  = "on" if glassbox_d5d6_on else "off"
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
    """Stable JSON for deep comparison. W15 OFF must not add/remove/change any key."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)


def snapshot():
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    snap = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            snap[name] = {"_missing_source": src}
            continue
        res = _score_corpus(src, w15_on=False)
        snap[name] = {pid: _canon(r) for pid, r in res.items()}
        print(f"snapshot {name:12s} n={len(res)}")
    BASELINE.write_text(json.dumps(snap, ensure_ascii=False, indent=0), encoding="utf-8")
    print("baseline written:", BASELINE)


def check():
    """OFF check — must be 0 diffs vs baseline."""
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
        res = _score_corpus(src, w15_on=False)
        cur = {pid: _canon(r) for pid, r in res.items()}
        b = base.get(name, {})
        diffs = []
        all_pids = set(b) | set(cur)
        for pid in all_pids:
            if b.get(pid) != cur.get(pid):
                diffs.append(pid)
        per_corpus[name] = {"n": len(cur), "diffs": len(diffs), "examples": diffs[:5]}
        total_diffs += len(diffs)
        print(f"check {name:12s} n={len(cur):4d} diffs={len(diffs)}")
    print()
    print("W15 FLAG-OFF BYTE-IDENTICAL:", "PASS (0-diff)" if total_diffs == 0 else f"FAIL ({total_diffs} diffs)")
    if total_diffs != 0:
        sys.exit(1)
    return per_corpus, total_diffs


def on_pilot():
    """ON pilot — report which products receive Rule A credit or Rule B flag."""
    summary = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            summary[name] = "MISSING_SOURCE"
            continue
        res_off = _score_corpus(src, w15_on=False)
        res_on  = _score_corpus(src, w15_on=True)
        rule_a_products = []
        rule_b_products = []
        for pid, r in res_on.items():
            if r.get("diaas_d2_credit_applied", 0) > 0:
                off_prq = res_off.get(pid, {}).get("dimension_scores", {}).get("protein_quality")
                on_prq  = r.get("dimension_scores", {}).get("protein_quality")
                off_grade = res_off.get(pid, {}).get("grade_estimate")
                on_grade  = r.get("grade_estimate")
                rule_a_products.append({
                    "pid": pid,
                    "source": r.get("diaas_w15_signal", {}).get("rule_a_source"),
                    "prq_off": off_prq, "prq_on": on_prq,
                    "grade_off": off_grade, "grade_on": on_grade,
                })
            if r.get("diaas_d5_protein_disclosure_gap"):
                rule_b_products.append({
                    "pid": pid,
                    "reason": r.get("diaas_w15_signal", {}).get("rule_b_reason"),
                })
        summary[name] = {
            "n_total": len(res_on),
            "rule_a_count": len(rule_a_products),
            "rule_b_count": len(rule_b_products),
            "rule_a_products": rule_a_products[:20],
            "rule_b_products": rule_b_products[:20],
        }
        print(f"ON pilot {name:12s} n={len(res_on):4d}"
              f" rule_A={len(rule_a_products)} rule_B={len(rule_b_products)}")

    out_path = BASELINE.parent / "_on_pilot_summary.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nON pilot summary written: {out_path}")
    return summary


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "snapshot":
        snapshot()
    elif mode == "on_pilot":
        on_pilot()
    else:
        check()
