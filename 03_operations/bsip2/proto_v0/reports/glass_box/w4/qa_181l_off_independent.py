"""
TASK-181L (QA) — INDEPENDENT OFF byte-identity re-verification.

Rather than trust the 181K-captured _off_baseline.json, this re-derives the TRUE
pre-W4 baseline directly from the parent commit (fc6f13a~1) of the W4-rework commit,
runs that engine over the 4 corpora, then runs the CURRENT engine with the W4 flag
OFF, and diffs the full score_product() result dict per product.

A 0-diff here proves the current (post-W4) engine's OFF path is byte-identical to the
genuine pre-W4 engine — not merely identical to a self-captured baseline.

Read-only. Does not flip the flag, rescore, or touch any published data.
"""
import os, sys, json, pathlib, tempfile, subprocess, importlib

PROTO = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0")
SRC = PROTO / "src"
PARENT_REV = "fc6f13a~1"  # commit before the W4-rework commit fc6f13a

CORPORA = {
    "hummus":      r"C:\Bari\02_products\hummus\canonical_bsip1",
    "maadanim":    r"C:\Bari\03_operations\bsip1\run_maadanim_001\output",
    "snack_bars":  r"C:\Bari\03_operations\bsip1\run_001\output",
    "golden_milk": r"C:\Bari\03_operations\bsip1\run_milk_002\output",
}
_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]


def _set_flags(w4_on):
    os.environ["BARI_GLASSBOX_W4"]   = "on" if w4_on else "off"
    os.environ["BARI_GLASSBOX_D5D6"] = "off"
    os.environ["BARI_GLASSBOX_W2"]   = "off"
    os.environ["BARI_GLASSBOX_W15"]  = "off"
    os.environ["BARI_RECAL_P0"]      = "off"
    os.environ["BARI_TASK144_FIXES"] = "off"


def _score_with_src(src_dir, source, w4_on):
    """Import engine modules from src_dir, score one corpus."""
    _set_flags(w4_on)
    for m in _MODULES:
        sys.modules.pop(m, None)
    sys.path.insert(0, str(src_dir))
    try:
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
    finally:
        if str(src_dir) in sys.path:
            sys.path.remove(str(src_dir))
        for m in _MODULES:
            sys.modules.pop(m, None)


def _canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, default=str)


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="preW4_"))
    # extract the pre-W4 engine; copy the rest of src so imports resolve
    import shutil
    for f in SRC.glob("*.py"):
        shutil.copy(f, tmp / f.name)
    pre_engine = subprocess.run(
        ["git", "show", f"{PARENT_REV}:03_operations/bsip2/proto_v0/src/score_engine.py"],
        cwd=r"C:\Bari", capture_output=True, text=True, encoding="utf-8")
    if pre_engine.returncode != 0:
        print("git show failed:", pre_engine.stderr); sys.exit(2)
    (tmp / "score_engine.py").write_text(pre_engine.stdout, encoding="utf-8")

    total = 0
    per = {}
    for name, src in CORPORA.items():
        if not pathlib.Path(src).exists():
            per[name] = "MISSING"; continue
        pre = _score_with_src(tmp, src, w4_on=False)        # genuine pre-W4 engine, OFF
        cur = _score_with_src(SRC, src, w4_on=False)        # current engine, flag OFF
        pc = {pid: _canon(r) for pid, r in pre.items()}
        cc = {pid: _canon(r) for pid, r in cur.items()}
        diffs = [pid for pid in (set(pc) | set(cc)) if pc.get(pid) != cc.get(pid)]
        per[name] = {"n": len(cc), "diffs": len(diffs), "examples": diffs[:5]}
        total += len(diffs)
        print(f"{name:12s} n={len(cc):4d} diffs={len(diffs)}")
    print()
    print("CURRENT-OFF == GENUINE PRE-W4 ENGINE:",
          "PASS (0-diff)" if total == 0 else f"FAIL ({total} diffs)")
    shutil.rmtree(tmp, ignore_errors=True)
    return total


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
