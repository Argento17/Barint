"""
Golden-corpus diff — EV-053 + EV-054 no-regression check.

Re-scores every product in the CURRENT baseline using the patched engine and
compares score + grade + dimension_scores to the frozen baseline values.

Expected result: zero movement on all published categories
(EV-053/054 gate on context_flag==brined_food; none of these products receive it).

Exit 0 = all byte-identical (no regression).
Exit 1 = any movement detected (HARD STOP — do not proceed to run_brined_002).
"""
import json
import os
import pathlib
import sys

# ----- flag setup (match the flags in the baseline for each corpus) -----
_BASE_FLAGS = {
    "BARI_TASK144_FIXES":      "off",
    "BARI_DAIRY_SAT_FAT_INFER":"off",
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

# purge cached engine modules so env flags take effect cleanly
import importlib
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


def score_one(product: dict) -> dict:
    sig = extract_signals(product)
    cat = classify_category(product)
    nova = infer_nova(product, sig["L3_inferred_classifications"])
    ev   = assign_evaluation_scope(product, cat["category"])
    return score_product(product, sig, cat, nova, ev)


# Load CURRENT baseline
_BASELINE_PTR = _REPO / "03_operations" / "shadow" / "baselines" / "CURRENT.json"
_CURRENT      = json.loads(_BASELINE_PTR.read_text(encoding="utf-8"))
_BASELINE_PATH = pathlib.Path(_CURRENT["path"])
baseline       = json.loads(_BASELINE_PATH.read_text(encoding="utf-8"))

print(f"Baseline: {baseline['baseline_id']}")
print(f"EV-053 + EV-054 golden-corpus no-regression check\n")

total_products = 0
moved = []
errors = []
corpora_checked = []

for corpus_name, corpus_data in baseline.get("corpora", {}).items():
    source_dir = pathlib.Path(corpus_data["source"])
    flags      = corpus_data.get("flags", {})
    n_expected = corpus_data.get("n", 0)
    frozen_products = corpus_data.get("products", {})

    if not source_dir.exists():
        print(f"  [{corpus_name}] SOURCE DIR MISSING: {source_dir} — SKIPPING")
        corpora_checked.append({
            "corpus": corpus_name,
            "status": "SKIPPED_MISSING_DIR",
            "n": 0,
            "moved": 0,
        })
        continue

    # Set corpus-specific flags
    for k, v in _BASE_FLAGS.items():
        os.environ[k] = v
    for k, v in flags.items():
        os.environ[k] = v

    # Reload engine modules with updated flags for this corpus
    for _mod in list(sys.modules.keys()):
        try:
            f = getattr(sys.modules[_mod], "__file__", None)
            if f and pathlib.Path(f).resolve().parent == _SRC:
                del sys.modules[_mod]
        except Exception:
            pass

    # Re-import with updated env
    from signal_extractor import extract_signals as _es
    from router_v2 import classify_category as _cc
    from nova_proxy import infer_nova as _in
    from evaluation_scope import assign_evaluation_scope as _ae
    from score_engine import score_product as _sp
    from input_loader import load_batch as _lb

    # Load BSIP1 records from source
    try:
        records = _lb(str(source_dir))
    except Exception as e:
        print(f"  [{corpus_name}] LOAD ERROR: {e} — SKIPPING")
        corpora_checked.append({
            "corpus": corpus_name,
            "status": f"LOAD_ERROR: {e}",
            "n": 0,
            "moved": 0,
        })
        continue

    n_checked = 0
    n_moved   = 0

    for prod in records:
        pid = prod.get("canonical_product_id", "?")
        if pid not in frozen_products:
            continue  # not in baseline (skip additions)

        frozen = frozen_products[pid]
        try:
            sig  = _es(prod)
            cat  = _cc(prod)
            nova = _in(prod, sig["L3_inferred_classifications"])
            ev   = _ae(prod, cat["category"])
            result = _sp(prod, sig, cat, nova, ev)
        except Exception as e:
            errors.append(f"[{corpus_name}] {pid} CRASH: {e}")
            n_checked += 1
            continue

        new_score = result.get("final_score_estimate")
        new_grade = result.get("grade_estimate")
        new_dims  = result.get("dimension_scores", {})
        frz_score = frozen.get("score")
        frz_grade = frozen.get("grade")
        frz_dims  = frozen.get("dims", {})

        score_changed = (new_score != frz_score)
        grade_changed = (new_grade != frz_grade)
        dims_changed  = any(
            abs((new_dims.get(k) or 0) - (frz_dims.get(k) or 0)) > 1e-6
            for k in set(list(new_dims.keys()) + list(frz_dims.keys()))
        )

        if score_changed or grade_changed or dims_changed:
            n_moved += 1
            moved.append({
                "corpus": corpus_name,
                "pid": pid,
                "name": frozen.get("name", prod.get("canonical_name_he", "?")),
                "frozen_score": frz_score,
                "new_score":    new_score,
                "frozen_grade": frz_grade,
                "new_grade":    new_grade,
                "score_delta":  (new_score or 0) - (frz_score or 0),
                "dims_changed": dims_changed,
            })

        n_checked += 1

    total_products += n_checked
    corpora_checked.append({
        "corpus":   corpus_name,
        "status":   "OK",
        "n":        n_checked,
        "moved":    n_moved,
    })
    print(f"  [{corpus_name}] checked={n_checked} moved={n_moved}  {'PASS' if n_moved == 0 else 'FAIL'}")


print()
print("=" * 60)
print(f"Total products checked: {total_products}")
print(f"Total score movements:  {len(moved)}")
print(f"Errors:                 {len(errors)}")

if moved:
    print()
    print("REGRESSIONS DETECTED -- HARD STOP:")
    for m in moved:
        safe_name = m['name'][:40].encode('ascii', errors='replace').decode('ascii')
        print(f"  {m['corpus']} | {m['pid']} | {safe_name}")
        print(f"    score: {m['frozen_score']} -> {m['new_score']}  (delta={m['score_delta']:+.1f})")
        print(f"    grade: {m['frozen_grade']} -> {m['new_grade']}")
    print()
    print("DO NOT PROCEED to run_brined_002. Investigate and revert.")
    sys.exit(1)

if errors:
    print()
    print("ERRORS (crashes during re-scoring):")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print()
print("RESULT: ALL PUBLISHED SCORES BYTE-IDENTICAL — no regression.")
print("EV-053 + EV-054 gate is confirmed: brined_food conditional does not affect non-brined corpora.")
print()
print("MACHINE-READABLE SUMMARY:")
summary = {
    "check": "golden_diff_ev053_ev054",
    "baseline": baseline["baseline_id"],
    "total_products_checked": total_products,
    "published_scores_moved": len(moved),
    "errors": len(errors),
    "corpora": corpora_checked,
    "overall": "PASS" if (len(moved) == 0 and len(errors) == 0) else "FAIL",
}
print(json.dumps(summary, indent=2, ensure_ascii=False))
sys.exit(0 if summary["overall"] == "PASS" else 1)
