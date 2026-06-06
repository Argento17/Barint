"""
TASK-169E — snack-bars frozen-category recal confirm wave.

Rescores the frozen snack-bars corpus (BSIP1 run_001/output, n=53) twice on the SAME
HEAD engine, toggling only BARI_RECAL_P0 (off -> on), into a NEW run id dir. Does NOT
touch any published run dir or the live frontend JSON.

Deliverables computed here:
  1. before/after diff: HEAD-OFF (== published BSIP2 baseline) -> HEAD-ON (recal)
  2. flag-OFF rollback identity: run OFF twice, must be byte-identical (N/N)
  3. HEAD-vs-published drift: HEAD-OFF vs sealed proto_v0 traces (2026-05-17)
  4. config hash + run record

Run-only; pure read against frozen corpus + published traces.
"""
import os, sys, json, glob, hashlib, pathlib, datetime

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))

CORPUS = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
PUBLISHED_TRACES = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs\products")
PRODUCTION_BASELINE = pathlib.Path(r"C:\Bari\03_operations\bsip2\sprint1\outputs\production_snack_bars.json")

RUN_ID = "run_snackbars_006_recal_p0"
OUT_ROOT = pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs") / RUN_ID

_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]

_HASH_FILES = ["score_engine.py", "constants.py", "nova_proxy.py", "signal_extractor.py",
               "router_v2.py", "evaluation_scope.py", "input_loader.py",
               "structural_classifier.py", "trace_writer.py"]


def config_hash():
    h = hashlib.sha256()
    for f in sorted(_HASH_FILES):
        h.update(f.encode())
        h.update((SRC / f).read_bytes())
    return h.hexdigest()[:16]


def run(recal_on):
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    os.environ["BARI_TASK144_FIXES"] = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)
    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    res = {}
    for product in load_batch(CORPUS):
        pid = product.get("canonical_product_id", "?")
        sig = extract_signals(product)
        cat = classify_category(product)
        nova = infer_nova(product, sig["L3_inferred_classifications"])
        ev = assign_evaluation_scope(product, cat["category"])
        r = score_product(product, sig, cat, nova, ev)
        res[pid] = {
            "name": product.get("canonical_name_he", ""),
            "score": r.get("final_score_estimate"),
            "grade": r.get("grade_estimate"),
            "ds": r.get("data_sufficiency"),
            "cat": cat["category"],
            "subtype": cat.get("category_subtype"),
            "nova": nova.get("nova_level"),
            "ferm_bonus": r.get("fermentation_bonus_applied"),
            "dims": r.get("dimension_scores"),
        }
    return res


def load_published():
    out = {}
    for d in sorted(glob.glob(str(PUBLISHED_TRACES / "*"))):
        f = pathlib.Path(d) / "bsip2_trace.json"
        if not f.exists():
            continue
        t = json.loads(f.read_text(encoding="utf-8"))
        out[pathlib.Path(d).name] = {
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "ds": t.get("data_sufficiency"),
        }
    return out


def load_production_baseline():
    d = json.loads(PRODUCTION_BASELINE.read_text(encoding="utf-8"))
    return {p["pid"]: {"score": p["score"], "grade": p["grade"]} for p in d}


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    cfg = config_hash()

    off1 = run(False)
    off2 = run(False)            # rollback identity proof
    on = run(True)
    published = load_published()
    prod_base = load_production_baseline()

    # --- rollback identity: OFF == OFF byte-identical
    rollback_match = sum(1 for pid in off1 if off1[pid] == off2.get(pid))
    rollback_total = len(off1)

    # --- recal diff: OFF -> ON
    recal_score_moves, recal_grade_moves = [], []
    for pid, p in on.items():
        b = off1.get(pid, {})
        if p["score"] != b.get("score") or p["grade"] != b.get("grade"):
            mv = {"pid": pid, "name": p["name"],
                  "off_score": b.get("score"), "off_grade": b.get("grade"),
                  "on_score": p["score"], "on_grade": p["grade"],
                  "grade_move": b.get("grade") != p["grade"]}
            recal_score_moves.append(mv)
            if mv["grade_move"]:
                recal_grade_moves.append(mv)

    # --- HEAD-vs-published drift (sealed proto_v0 traces, 2026-05-17)
    drift_match, drift_total, drift_rows = 0, 0, []
    for pid, pub in published.items():
        drift_total += 1
        h = off1.get(pid, {})
        same = (round(float(h.get("score")), 1) == round(float(pub["score"]), 1)
                and h.get("grade") == pub["grade"]) if h else False
        if same:
            drift_match += 1
        else:
            drift_rows.append({"pid": pid, "published": [pub["score"], pub["grade"]],
                               "head_off": [h.get("score"), h.get("grade")]})

    # --- HEAD-OFF vs live production baseline (sprint1 = behind live page)
    pb_match, pb_total, pb_rows = 0, 0, []
    for pid, pb in prod_base.items():
        pb_total += 1
        h = off1.get(pid, {})
        if h and h["score"] == pb["score"] and h["grade"] == pb["grade"]:
            pb_match += 1
        else:
            pb_rows.append({"pid": pid, "production": [pb["score"], pb["grade"]],
                            "head_off": [h.get("score"), h.get("grade")]})

    # --- frozen invariant checks
    snk001 = on.get("bsip1_7290011498870", {})
    a_or_above = [pid for pid, p in on.items()
                  if isinstance(p["score"], (int, float)) and p["score"] >= 80]

    summary = {
        "run_id": RUN_ID,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "engine_config_hash": cfg,
        "flag": "BARI_RECAL_P0",
        "corpus": str(CORPUS),
        "corpus_n": len(on),
        "rollback_off_identical": f"{rollback_match}/{rollback_total}",
        "recal_score_moves": len(recal_score_moves),
        "recal_grade_moves": len(recal_grade_moves),
        "recal_grade_move_list": recal_grade_moves,
        "recal_score_move_list": recal_score_moves,
        "frozen_invariant": {
            "snk001_pid": "bsip1_7290011498870",
            "snk001_on": [snk001.get("score"), snk001.get("grade")],
            "snk001_held_70B": snk001.get("score") == 70 and snk001.get("grade") == "B",
            "products_at_or_above_A(>=80)": a_or_above,
            "no_A_held": len(a_or_above) == 0,
        },
        "head_vs_published_proto_v0_2026_05_17": f"{drift_match}/{drift_total}",
        "head_vs_published_drift_rows": drift_rows,
        "head_off_vs_live_production_baseline": f"{pb_match}/{pb_total}",
        "head_off_vs_production_drift_rows": pb_rows,
    }

    (OUT_ROOT / "off.json").write_text(json.dumps(off1, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "on.json").write_text(json.dumps(on, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "run_record.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("recal_score_move_list",)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
