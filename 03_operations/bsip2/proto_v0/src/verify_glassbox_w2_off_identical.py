"""
TASK-179S — Glass Box W2 D4 byte-identical OFF verifier.

Mirrors the BARI_GLASSBOX_W15 discipline (verify_glassbox_w15_off_identical.py):
with BARI_GLASSBOX_W2=off the FULL score_product() result dict for every product
in the test corpus must be byte-identical to the pre-change baseline.

score_product() is the single function modified by the W2 change, so an
OFF-identical result guarantees every downstream consumer is unaffected.

Three modes:
  python verify_glassbox_w2_off_identical.py snapshot   # capture baseline (run BEFORE editing)
  python verify_glassbox_w2_off_identical.py check      # re-run with flag OFF, diff vs baseline
  python verify_glassbox_w2_off_identical.py on_pilot   # run with flag ON, report d4_additives

Baseline persisted to: reports/glass_box/w2/_off_baseline.json
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

BASELINE = (pathlib.Path(__file__).parent.parent
            / "reports" / "glass_box" / "w2" / "_off_baseline.json")

# Test corpus: hummus and maadanim (pilot categories with ingredient text).
# Frozen corpora (snack_bars, golden_milk) included as no-change safeguard —
# these must always show 0 diffs regardless of any flag state.
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


def _score_corpus(source, w2_on, w15_on=False, glassbox_d5d6_on=False):
    """Score all products in a corpus with the given flag settings."""
    os.environ["BARI_GLASSBOX_W2"]    = "on" if w2_on else "off"
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
    """Stable JSON for deep comparison. W2 OFF must not add/remove/change any key."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)


def snapshot():
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    snap = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            snap[name] = {"_missing_source": src}
            continue
        res = _score_corpus(src, w2_on=False)
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
        res = _score_corpus(src, w2_on=False)
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
    print("W2 FLAG-OFF BYTE-IDENTICAL:", "PASS (0-diff)" if total_diffs == 0 else f"FAIL ({total_diffs} diffs)")
    if total_diffs != 0:
        sys.exit(1)
    return per_corpus, total_diffs


def on_pilot():
    """ON pilot — report d4_additives for each product that has them."""
    summary = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            summary[name] = "MISSING_SOURCE"
            continue
        res_off = _score_corpus(src, w2_on=False)
        res_on  = _score_corpus(src, w2_on=True)
        products_with_findings = []
        products_clean = []
        for pid, r in res_on.items():
            d4 = r.get("d4_additives", [])
            off_score = res_off.get(pid, {}).get("final_score_estimate")
            on_score  = r.get("final_score_estimate")
            off_grade = res_off.get(pid, {}).get("grade_estimate")
            on_grade  = r.get("grade_estimate")
            # Guard: score and grade must not change
            score_changed = (off_score != on_score)
            grade_changed = (off_grade != on_grade)
            entry = {
                "pid": pid,
                "d4_additives": d4,
                "score_off": off_score, "score_on": on_score,
                "grade_off": off_grade, "grade_on": on_grade,
                "score_changed": score_changed,
                "grade_changed": grade_changed,
            }
            if d4:
                products_with_findings.append(entry)
            else:
                products_clean.append(pid)

        tier_counts = {}
        for p in products_with_findings:
            for f in p["d4_additives"]:
                t = f["tier"]
                tier_counts[t] = tier_counts.get(t, 0) + 1

        score_changes = [p for p in products_with_findings if p["score_changed"]]
        grade_changes = [p for p in products_with_findings if p["grade_changed"]]

        summary[name] = {
            "n_total": len(res_on),
            "n_with_findings": len(products_with_findings),
            "n_clean": len(products_clean),
            "tier_distribution": tier_counts,
            "score_changes_MUST_BE_0": len(score_changes),
            "grade_changes_MUST_BE_0": len(grade_changes),
            "products_with_findings": products_with_findings[:10],
        }
        print(f"ON pilot {name:12s} n={len(res_on):4d}"
              f" with_findings={len(products_with_findings)}"
              f" tiers={tier_counts}"
              f" score_changes={len(score_changes)}"
              f" grade_changes={len(grade_changes)}")

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
