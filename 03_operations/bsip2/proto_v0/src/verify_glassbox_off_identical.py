"""
TASK-179G — Glass Box D5/D6 byte-identical OFF verifier.

Mirrors the BARI_RECAL_P0 discipline (verify_recal_off_identical.py): with
BARI_GLASSBOX_D5D6=off the FULL score_product() result dict for every product in
the golden corpus + the three frozen corpora must be byte-identical to the
pre-change baseline.

score_product() is the single function modified by the Glass Box change, so an
OFF-identical result there guarantees every downstream consumer (bread synthesis,
trace writers, frontend packagers) is unaffected.

Two modes:
  python verify_glassbox_off_identical.py snapshot   # capture baseline (run BEFORE editing)
  python verify_glassbox_off_identical.py check       # re-run with flag OFF, diff vs baseline

Baseline persisted to: reports/glass_box/_off_baseline.json
"""
import os
import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

BASELINE = pathlib.Path(__file__).parent.parent / "reports" / "glass_box" / "_off_baseline.json"

# Standard-pipeline corpora (load_batch compatible). Golden anchors are real_product
# entries pointing at published traces; we re-derive their BSIP1 source where available.
# We score every corpus through the SAME standard pipeline used by the published runs.
CORPORA = {
    "golden_milk":  r"C:\Bari\03_operations\bsip1\run_milk_002\output",      # frozen: milk run_004 lineage
    "snack_bars":   r"C:\Bari\03_operations\bsip1\run_001\output",            # frozen: snk-001 ceiling
    "hummus":       r"C:\Bari\02_products\hummus\canonical_bsip1",            # pilot
    "maadanim":     r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",   # pilot
}

_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]


def _score_corpus(source, glassbox_on):
    os.environ["BARI_GLASSBOX_D5D6"] = "on" if glassbox_on else "off"
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
    for product in products:
        pid = product.get("canonical_product_id", "?")
        try:
            sig = extract_signals(product)
            cat = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(product, cat["category"])
            r = score_product(product, sig, cat, nova, ev)
            out[pid] = r
        except Exception as e:
            out[pid] = {"_error": repr(e)}
    return out


def _canon(obj):
    # Stable JSON for deep comparison. Glass Box OFF must not add/remove/change any key.
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)


def snapshot():
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    snap = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            snap[name] = {"_missing_source": src}
            continue
        res = _score_corpus(src, glassbox_on=False)
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
        res = _score_corpus(src, glassbox_on=False)
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
    print("FLAG-OFF BYTE-IDENTICAL:", "PASS (0-diff)" if total_diffs == 0 else f"FAIL ({total_diffs} diffs)")
    return per_corpus, total_diffs


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "snapshot":
        snapshot()
    else:
        check()
