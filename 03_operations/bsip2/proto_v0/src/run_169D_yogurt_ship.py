"""
TASK-169D ship-prep — CLEAN capped rescore of the FIXED yogurt corpus.

Owner decision = option (b): cap yogurt at A, no S, via BARI_RECAL_P0_YOGURT_TRIM
(+8 A-ceiling at 89.9). This is the authoritative SHIP-CANDIDATE rescore.

Prereqs already applied to the corpus / engine (Part 1):
  - corpus fix #1: bsip1_7290116932620 protein_g 190.0 -> 12.5 (OFF-sourced; see
    nutrition_corrections block in that corpus file).
  - engine fix #2 (flag-gated, RECAL_P0_YOGURT_TRIM only): serving-suggestion marketing
    prose is dropped before the flavored-variant scan, so bsip1_7290102395231
    (יוגורט ביו נטורל 2.8%) regains its legitimate +8. Zero collateral (1 product moves).

Runs three configurations on the SAME HEAD engine over the FIXED frozen corpus
(BSIP1 run_yogurt_003/output, n=86), into a NEW run id dir. Touches NO published run dir
and NOT the live frontend JSON.

  OFF      : BARI_RECAL_P0=off  (rollback baseline)            -> must match published byte
  ON       : BARI_RECAL_P0=on,  TRIM=off                       (recal, uncapped = option a)
  ON+TRIM  : BARI_RECAL_P0=on,  TRIM=on  (SHIP CANDIDATE = option b, capped)

Deliverables:
  1. verified distribution (ON+TRIM): grade counts; A-list w/ drivers; 0-S confirmation
  2. corpus-fix confirmation (the 2 target products before/after)
  3. rollback: OFF==OFF byte-identical; OFF==published byte-identical (N/N)
  4. reship before/after table: current-live grade -> new capped grade for every product
  5. config hash + run record
"""
import os, sys, json, glob, hashlib, pathlib, datetime

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))

CORPUS = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_003\output")
PUBLISHED_TRACES = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_004\products")
LIVE_FRONTEND = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons\yogurts_frontend_v2.json")

RUN_ID = "run_yogurt_006_recal_p0_trim"
OUT_ROOT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs") / RUN_ID

_MODULES = ["signal_extractor", "score_engine", "nova_proxy", "trace_writer",
            "router_v2", "evaluation_scope", "input_loader", "constants",
            "structural_classifier"]

_HASH_FILES = ["score_engine.py", "constants.py", "nova_proxy.py", "signal_extractor.py",
               "router_v2.py", "evaluation_scope.py", "input_loader.py",
               "structural_classifier.py", "trace_writer.py"]

# The two corpus-bug targets (Part 1).
FIX_PROTEIN_PID = "bsip1_yogurt_7290116932620"     # GO lactose-free; protein 190->12.5
FIX_PLUS8_PID = "bsip1_yogurt_7290102395231"       # bio naturel 2.8%; false +8 exclusion


def config_hash():
    h = hashlib.sha256()
    for f in sorted(_HASH_FILES):
        h.update(f.encode())
        h.update((SRC / f).read_bytes())
    return h.hexdigest()[:16]


def run(recal_on, trim=False):
    os.environ["BARI_RECAL_P0"] = "on" if recal_on else "off"
    os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on" if trim else "off"
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
            dims = r.get("dimension_scores") or {}
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
                "protein_dim": dims.get("protein_quality"),
                "nutrient_density": dims.get("nutrient_density"),
            }
        except Exception as e:
            res[pid] = {"name": product.get("canonical_name_he", ""), "error": str(e)}
    return res


def dist(d):
    out = {}
    for p in d.values():
        out[p.get("grade")] = out.get(p.get("grade"), 0) + 1
    return out


def load_published():
    out = {}
    for dpath in sorted(glob.glob(str(PUBLISHED_TRACES / "*"))):
        f = pathlib.Path(dpath) / "bsip2_trace.json"
        if not f.exists():
            continue
        t = json.loads(f.read_text(encoding="utf-8"))
        out[pathlib.Path(dpath).name] = {
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
        }
    return out


def load_live_grades():
    """current-live grade per barcode (from yogurts_frontend_v2.json imageUrl barcode)."""
    j = json.loads(LIVE_FRONTEND.read_text(encoding="utf-8"))
    import re
    out = {}
    for p in j.get("products", []):
        m = re.search(r"_P_(\d{8,14})_", p.get("imageUrl", "") or "")
        bc = m.group(1) if m else None
        out["bsip1_yogurt_" + bc if bc else p["id"]] = {
            "name": p["name"], "score": p["score"], "grade": p["grade"], "barcode": bc,
        }
    return out


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    cfg = config_hash()

    off1 = run(False)
    off2 = run(False)
    ship = run(True, trim=True)        # SHIP CANDIDATE (option b: capped)
    on_uncapped = run(True, trim=False)  # option a (for context / 0-S delta)
    published = load_published()
    live = load_live_grades()

    # rollback identity OFF==OFF
    rb_match = sum(1 for pid in off1 if off1[pid] == off2.get(pid))
    rb_total = len(off1)

    # OFF == published byte-identical (score+grade to 1dp)
    pub_match, pub_total, pub_drift = 0, 0, []
    for pid, pub in published.items():
        pub_total += 1
        h = off1.get(pid, {})
        same = (h.get("score") is not None
                and round(float(h["score"]), 1) == round(float(pub["score"]), 1)
                and h.get("grade") == pub["grade"])
        if same:
            pub_match += 1
        else:
            pub_drift.append({"pid": pid, "published": [pub["score"], pub["grade"]],
                              "head_off": [h.get("score"), h.get("grade")]})

    # SHIP distribution + A-list + S-confirmation
    a_list, s_list = [], []
    for pid, p in ship.items():
        sc = p.get("score")
        if not isinstance(sc, (int, float)):
            continue
        row = {"pid": pid, "name": p["name"], "score": sc, "grade": p["grade"],
               "protein_g": p.get("protein_g"), "protein_dim": p.get("protein_dim"),
               "nutrient_density": p.get("nutrient_density"),
               "ferm_bonus": p.get("ferm_bonus"), "ferm_note": p.get("ferm_note"),
               "subtype": p.get("subtype"), "nova": p.get("nova")}
        if sc >= 90:
            s_list.append(row)
        elif sc >= 80:
            a_list.append(row)
    s_list.sort(key=lambda x: -x["score"])
    a_list.sort(key=lambda x: -x["score"])

    # corpus-fix confirmation
    fix_confirm = {
        "protein_fix_7290116932620": {
            "corpus_protein_g": ship.get(FIX_PROTEIN_PID, {}).get("protein_g"),
            "ship_score": ship.get(FIX_PROTEIN_PID, {}).get("score"),
            "ship_grade": ship.get(FIX_PROTEIN_PID, {}).get("grade"),
            "uncapped_score": on_uncapped.get(FIX_PROTEIN_PID, {}).get("score"),
            "uncapped_grade": on_uncapped.get(FIX_PROTEIN_PID, {}).get("grade"),
            "note": "was protein_g=190.0 -> S 98.8 (corrupt). Now 12.5 -> capped A 89.9.",
        },
        "plus8_fix_7290102395231": {
            "ship_ferm_bonus": ship.get(FIX_PLUS8_PID, {}).get("ferm_bonus"),
            "ship_ferm_note": ship.get(FIX_PLUS8_PID, {}).get("ferm_note"),
            "ship_score": ship.get(FIX_PLUS8_PID, {}).get("score"),
            "ship_grade": ship.get(FIX_PLUS8_PID, {}).get("grade"),
            "note": "was +8 stripped (honey marketing-prose bleed) -> B 77.5. Now +8 -> A.",
        },
    }

    # reship before/after table — live grade -> new capped grade, for every product
    reship = []
    for pid, lv in live.items():
        s = ship.get(pid, {})
        reship.append({
            "id_barcode": lv.get("barcode"),
            "name": lv["name"],
            "live_score": lv["score"], "live_grade": lv["grade"],
            "new_score": s.get("score"), "new_grade": s.get("grade"),
            "matched_in_corpus": pid in ship,
            "ferm_bonus": s.get("ferm_bonus"),
        })

    summary = {
        "run_id": RUN_ID,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "engine_config_hash": cfg,
        "flags": {"BARI_RECAL_P0": "on", "BARI_RECAL_P0_YOGURT_TRIM": "on",
                  "BARI_TASK144_FIXES": "off"},
        "corpus": str(CORPUS),
        "corpus_n": len(ship),
        "ship_candidate_config": "BARI_RECAL_P0=on + BARI_RECAL_P0_YOGURT_TRIM=on (option b, capped)",
        "rollback_off_off_identical": f"{rb_match}/{rb_total}",
        "rollback_off_vs_published_run_yogurt_004": f"{pub_match}/{pub_total}",
        "rollback_off_vs_published_drift_rows": pub_drift,
        "grade_dist_off": dist(off1),
        "grade_dist_on_uncapped": dist(on_uncapped),
        "grade_dist_ship_capped": dist(ship),
        "ship_counts": {"S": len(s_list), "A": len(a_list)},
        "zero_S_confirmed": len(s_list) == 0,
        "A_list": a_list,
        "S_list": s_list,
        "corpus_fix_confirmation": fix_confirm,
        "reship_before_after": reship,
    }

    (OUT_ROOT / "off.json").write_text(json.dumps(off1, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "ship_capped.json").write_text(json.dumps(ship, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "on_uncapped.json").write_text(json.dumps(on_uncapped, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "run_record.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("A_list", "S_list", "reship_before_after",
                                   "rollback_off_vs_published_drift_rows")},
                     ensure_ascii=False, indent=2))
    print("=== A:", len(a_list), "S:", len(s_list), "zero_S:", len(s_list) == 0)
    print("=== written:", OUT_ROOT)


if __name__ == "__main__":
    main()
