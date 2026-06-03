"""
TASK-169D — yogurt frozen-category recal wave (rescore + decision package).

Rescores the frozen yogurt corpus (BSIP1 run_yogurt_003/output, n=86) on the SAME HEAD
engine, toggling only BARI_RECAL_P0 (off -> on), into a NEW run id dir. Does NOT touch any
published run dir or the live frontend JSON (yogurts_frontend_v2.json).

Deliverables computed here:
  1. before/after diff: HEAD-OFF (flag-OFF baseline) -> HEAD-ON (recal); A-list + S-list
  2. flag-OFF rollback identity: run OFF twice, must be byte-identical (N/N)
  3. HEAD-vs-published drift: HEAD-OFF vs sealed run_yogurt_004 traces (algo 0.4.1)
  4. culture-gate audit: which yogurts get the +8 and which do NOT (and why)
  5. R1-anchor top-trim model (option b): re-score ON but route yogurt-subtype products
     through PROTEIN_SCALE_TABLES["yogurt"] (the dedicated, currently-UNWIRED R1 yogurt
     anchor) instead of the dairy_protein scale; report S->A / A->B drops.
  6. config hash + run record

Run-only; pure read against frozen corpus + published traces.
"""
import os, sys, json, glob, hashlib, pathlib, datetime

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))

CORPUS = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_003\output")
PUBLISHED_TRACES = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_004\products")

RUN_ID = "run_yogurt_005_recal_p0"
OUT_ROOT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs") / RUN_ID

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


def grade_of(score):
    if score is None:
        return None
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 55: return "C"
    if score >= 40: return "D"
    return "E"


def run(recal_on, r1_trim=False):
    """r1_trim: option (b) — yogurt-subtype products route protein-mass terms through the
    yogurt anchor (PROTEIN_SCALE_TABLES["yogurt"]) via the flag-gated engine branch
    BARI_RECAL_P0_YOGURT_TRIM. Faithful through the full cap/penalty/floor pipeline."""
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on" if r1_trim else "off"
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
        try:
            sig = extract_signals(product)
            cat = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev = assign_evaluation_scope(product, cat["category"])
            r = score_product(product, sig, cat, nova, ev)
            nn = product.get("normalized_nutrition_per_100g") or {}
            res[pid] = {
                "name": product.get("canonical_name_he", ""),
                "score": r.get("final_score_estimate"),
                "grade": r.get("grade_estimate"),
                "ds": r.get("data_sufficiency"),
                "cat": cat["category"],
                "subtype": cat.get("category_subtype"),
                "nova": nova.get("nova_level"),
                "ferm_bonus": r.get("fermentation_bonus_applied"),
                "ferm_note": r.get("fermentation_bonus_note"),
                "protein_g": nn.get("protein_g"),
                "dims": r.get("dimension_scores"),
                "_raw": r,
                "_nn": nn,
            }
        except Exception as e:
            res[pid] = {"name": product.get("canonical_name_he", ""), "error": str(e)}
    return res


def slim(d):
    return {pid: {k: v for k, v in p.items() if k not in ("_raw", "_nn")}
            for pid, p in d.items()}


def is_yogurt_subtype(p):
    from constants import CULTURED_YOGURT_SUBTYPES
    return (p.get("cat") == "yogurt" or p.get("subtype") in CULTURED_YOGURT_SUBTYPES)


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    cfg = config_hash()

    off1 = run(False)
    off2 = run(False)            # rollback identity proof
    on = run(True)
    published = load_published()

    # --- rollback identity: OFF == OFF byte-identical (slim, drops raw objects)
    s_off1, s_off2 = slim(off1), slim(off2)
    rollback_match = sum(1 for pid in s_off1 if s_off1[pid] == s_off2.get(pid))
    rollback_total = len(s_off1)

    # --- recal diff: OFF -> ON
    grade_dist_off, grade_dist_on = {}, {}
    for p in off1.values():
        grade_dist_off[p.get("grade")] = grade_dist_off.get(p.get("grade"), 0) + 1
    for p in on.values():
        grade_dist_on[p.get("grade")] = grade_dist_on.get(p.get("grade"), 0) + 1

    a_list, s_list = [], []
    for pid, p in on.items():
        sc = p.get("score")
        if not isinstance(sc, (int, float)):
            continue
        b = off1.get(pid, {})
        dims = p.get("dims") or {}
        row = {
            "pid": pid, "name": p["name"],
            "off": [b.get("score"), b.get("grade")],
            "on_score": sc, "on_grade": p["grade"],
            "protein_g": p.get("protein_g"),
            "protein_dim": dims.get("protein_quality"),
            "nutrient_density": dims.get("nutrient_density"),
            "ferm_bonus": p.get("ferm_bonus"),
            "ferm_note": p.get("ferm_note"),
            "subtype": p.get("subtype"),
            "nova": p.get("nova"),
        }
        if sc >= 90:
            s_list.append(row)
        elif sc >= 80:
            a_list.append(row)
    s_list.sort(key=lambda x: -x["on_score"])
    a_list.sort(key=lambda x: -x["on_score"])

    # --- culture-gate audit: who got +8 and who did NOT
    got_bonus, no_bonus = [], []
    for pid, p in on.items():
        row = {"pid": pid, "name": p["name"], "subtype": p.get("subtype"),
               "nova": p.get("nova"), "ferm_note": p.get("ferm_note")}
        if p.get("ferm_bonus"):
            got_bonus.append(row)
        else:
            no_bonus.append(row)

    # --- R1-anchor top-trim (option b): yogurt-subtype products use yogurt protein scale.
    on_trim = run(True, r1_trim=True)
    trim = compare_trim(on, on_trim)

    # --- HEAD-vs-published drift (sealed run_yogurt_004 traces, algo 0.4.1)
    drift_match, drift_total, drift_rows = 0, 0, []
    for pid, pub in published.items():
        drift_total += 1
        h = off1.get(pid, {})
        same = (round(float(h.get("score")), 1) == round(float(pub["score"]), 1)
                and h.get("grade") == pub["grade"]) if h.get("score") is not None else False
        if same:
            drift_match += 1
        else:
            drift_rows.append({"pid": pid, "published": [pub["score"], pub["grade"]],
                               "head_off": [h.get("score"), h.get("grade")]})

    summary = {
        "run_id": RUN_ID,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "engine_config_hash": cfg,
        "flag": "BARI_RECAL_P0",
        "corpus": str(CORPUS),
        "corpus_n": len(on),
        "rollback_off_identical": f"{rollback_match}/{rollback_total}",
        "grade_dist_off": grade_dist_off,
        "grade_dist_on": grade_dist_on,
        "option_a_counts": {"S": len(s_list), "A": len(a_list)},
        "A_list": a_list,
        "S_list": s_list,
        "culture_gate": {
            "received_plus8": len(got_bonus),
            "did_not": len(no_bonus),
            "got_bonus": got_bonus,
            "no_bonus": no_bonus,
        },
        "option_b_r1_trim": trim,
        "head_vs_published_run_yogurt_004": f"{drift_match}/{drift_total}",
        "head_vs_published_drift_rows": drift_rows,
    }

    (OUT_ROOT / "off.json").write_text(json.dumps(slim(off1), ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "on.json").write_text(json.dumps(slim(on), ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "run_record.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("A_list", "S_list", "head_vs_published_drift_rows",
                                   "culture_gate", "option_b_r1_trim")},
                     ensure_ascii=False, indent=2))
    print("=== A list:", len(a_list), " S list:", len(s_list))
    print("=== bonus:", len(got_bonus), " no-bonus:", len(no_bonus))
    print("=== written:", OUT_ROOT)


def compare_trim(on, on_trim):
    """Option (b): full-engine re-score with the yogurt anchor wired. Reports the resulting
    S/A counts and every yogurt that drops a grade (S->A, A->B) vs option (a)."""
    counts_a = counts_s = 0
    drops, trim_rows = [], {}
    for pid, p in on_trim.items():
        sc = p.get("score")
        if not isinstance(sc, (int, float)):
            continue
        if sc >= 90: counts_s += 1
        elif sc >= 80: counts_a += 1
        a = on.get(pid, {})
        if not is_yogurt_subtype(p):
            continue
        row = {"name": p["name"], "protein_g": p.get("protein_g"),
               "a_score": a.get("score"), "a_grade": a.get("grade"),
               "b_score": sc, "b_grade": p.get("grade")}
        trim_rows[pid] = row
        if a.get("grade") != p.get("grade"):
            drops.append({**row, "pid": pid})
    drops.sort(key=lambda x: -(x["a_score"] or 0))
    return {"resulting_counts": {"S": counts_s, "A": counts_a},
            "grade_drops": drops, "all_yogurt_rows": trim_rows}


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


if __name__ == "__main__":
    main()
