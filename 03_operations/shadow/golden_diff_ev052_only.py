"""
Isolate EV-052 contribution to baseline movements.

Runs with the patched evaluation_scope.py (EV-052 active) but with
score_engine.py in its PRE-EV-053/054 state. To do this we temporarily
monkey-patch the engine's context_flag to be NEVER brined_food so that
only the 0.7 weight (already in the engine for brined_food) is tested,
and we compare against the baseline.

Actually: we do this differently. We just re-score the moved products
using the current engine and show their context_flag values. This tells
us whether the movements are purely due to EV-052 (context_flag firing
on products not in the baseline) rather than EV-053/054.
"""
import json
import os
import pathlib
import sys

_BASE_FLAGS = {
    "BARI_TASK144_FIXES":      "off",
    "BARI_RECAL_P0":           "off",
    "BARI_RECAL_P0_YOGURT_TRIM":"off",
    "BARI_GLASSBOX_D5D6":      "off",
    "BARI_GLASSBOX_W15":       "off",
    "BARI_GLASSBOX_W2":        "off",
    "BARI_GLASSBOX_W4":        "on",
    "BARI_SODIUM_CEREAL":      "off",
    "BARI_REDLABEL_V1":        "off",
    "BARI_TASK250_CONF":       "off",
}
for k, v in _BASE_FLAGS.items():
    os.environ[k] = v

_REPO = pathlib.Path(r"C:\Bari")
_SRC  = _REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
os.chdir(str(_SRC))

for _mod in list(sys.modules.keys()):
    try:
        f = getattr(sys.modules[_mod], "__file__", None)
        if f and pathlib.Path(f).resolve().parent == _SRC:
            del sys.modules[_mod]
    except Exception:
        pass

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from input_loader import load_batch

# The products that moved in the golden-diff run
MOVED_PIDS = {
    "maadanim": [
        "bsip1_maadanim_2385455", "bsip1_maadanim_554532", "bsip1_maadanim_6492616",
        "bsip1_maadanim_7290011499129", "bsip1_maadanim_7290011499327",
        "bsip1_maadanim_7290017065236", "bsip1_maadanim_7290017065663",
    ],
    "hard_cheeses": [
        "bsip1_hardcheese_7290000062488", "bsip1_hardcheese_7290000062518",
        "bsip1_hardcheese_7290000062563", "bsip1_hardcheese_7290000062570",
        "bsip1_hardcheese_7290000425009", "bsip1_hardcheese_7290000425016",
        "bsip1_hardcheese_7290000425023", "bsip1_hardcheese_7290010644743",
        "bsip1_hardcheese_7290010644750", "bsip1_hardcheese_7290010644767",
        "bsip1_hardcheese_7290010644774",
    ],
}

CORPUS_DIRS = {
    "maadanim":    _REPO / "03_operations" / "bsip1" / "run_maadanim_001" / "output",
    "hard_cheeses": _REPO / "03_operations" / "bsip1" / "run_hard_cheeses_001" / "output",
}

_BASELINE_PTR = _REPO / "03_operations" / "shadow" / "baselines" / "CURRENT.json"
_CURRENT      = json.loads(_BASELINE_PTR.read_text(encoding="utf-8"))
_BASELINE_PATH = pathlib.Path(_CURRENT["path"])
baseline       = json.loads(_BASELINE_PATH.read_text(encoding="utf-8"))

print("Diagnosing moved products — checking context_flag and score contribution of EV-052 vs EV-053/054\n")

for corpus_name, pids in MOVED_PIDS.items():
    src_dir = CORPUS_DIRS[corpus_name]
    if not src_dir.exists():
        print(f"[{corpus_name}] SOURCE DIR MISSING: {src_dir}")
        continue

    corpus_flags = baseline["corpora"].get(corpus_name, {}).get("flags", {})
    for k, v in _BASE_FLAGS.items():
        os.environ[k] = v
    for k, v in corpus_flags.items():
        os.environ[k] = v

    for _mod in list(sys.modules.keys()):
        try:
            f = getattr(sys.modules[_mod], "__file__", None)
            if f and pathlib.Path(f).resolve().parent == _SRC:
                del sys.modules[_mod]
        except Exception:
            pass

    from signal_extractor import extract_signals as _es
    from router_v2 import classify_category as _cc
    from nova_proxy import infer_nova as _in
    from evaluation_scope import assign_evaluation_scope as _ae
    from score_engine import score_product as _sp
    from input_loader import load_batch as _lb

    records = {
        prod.get("canonical_product_id"): prod
        for prod in _lb(str(src_dir))
    }

    frozen_prods = baseline["corpora"].get(corpus_name, {}).get("products", {})

    for pid in pids:
        prod = records.get(pid)
        if not prod:
            print(f"  [{corpus_name}] {pid}: NOT FOUND in source dir")
            continue

        sig  = _es(prod)
        cat  = _cc(prod)
        nova = _in(prod, sig["L3_inferred_classifications"])
        ev   = _ae(prod, cat["category"])

        ctx_flag = ev.get("context_flag")
        eval_status = ev.get("evaluation_status", "standard")

        result = _sp(prod, sig, cat, nova, ev)
        new_score = result.get("final_score_estimate")
        new_grade = result.get("grade_estimate")

        frozen = frozen_prods.get(pid, {})
        frz_score = frozen.get("score")
        frz_grade = frozen.get("grade")
        frz_eval  = frozen.get("eval_status", "standard")

        name = prod.get("canonical_name_he", "?")[:40]
        safe_name = name.encode('ascii', errors='replace').decode()

        print(f"  [{corpus_name}] {pid}")
        print(f"    Name: {safe_name}")
        print(f"    Baseline eval_status: {frz_eval}  ->  Current: {eval_status} / context_flag={ctx_flag}")
        print(f"    Score: {frz_score} -> {new_score}  Grade: {frz_grade} -> {new_grade}")
        # Check if ISRAELI_RED_LABELS_2_PLUS fired in baseline and now doesn't
        binding_cap = result.get("binding_cap")
        print(f"    Current binding_cap: {binding_cap}")
        print()

print("Diagnosis complete.")
print()
print("INTERPRETATION:")
print("If baseline eval_status=standard and current eval_status=context_limited (brined_food),")
print("the movement is caused by EV-052 (keyword extension) already firing on these products,")
print("NOT by EV-053/054. The baseline was captured before EV-052 was deployed.")
print("EV-053/054 then additionally lifts the 2-label cap and HP penalty on these products.")
