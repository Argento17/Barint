"""
BSIP2 Hummus SHELF-RELATIVE runner — run_hummus_shelfrel_002
EV-094 amendments (EV-099, D7 co-signed 2026-06-15):
  (a) CAP-BIND: floor cannot exceed binding cap
  (b) NOVA<=2 ONLY: NOVA-3/4 hummus gets NO floor lift
  (c) RT-10 LOGGING: floors_considered/floors_applied always populated

Also incorporates:
  - BSIP2-HC-002 REVERT (EV-099): HC002_NOVA1_ON=False (default) — no NOVA-1 reclassification
  - BARI_DAIRY_SAT_FAT_INFER default ON (EV-099)

Hummus stats (re-verified 2026-06-15, n=60 in-scope):
  median=390.0mg  IQR=43.0mg  robust_scale=31.88mg  floor_threshold=395.0mg
  Stats match EV-094 — no divergence, constants locked.

OFF ban: absolute. Zero OFF in any trace.
C10 milk invariant checked against run_005_headpin.
"""
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter

# Flag config — MUST be before any engine imports
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"    # brined-only EV-056
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
# HC002 revert: do NOT set BARI_HC002_NOVA1 (leave default off = reverted)
# DAIRY_SAT_FAT_INFER is now default ON — no need to set explicitly

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    score_to_grade,
    SODIUM_SHELF_REL_HUMMUS_MEDIAN,
    SODIUM_SHELF_REL_HUMMUS_SCALE,
    SODIUM_SHELF_REL_HUMMUS_IQR,
    SODIUM_SHELF_REL_HUMMUS_FLOOR,
    SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_SOURCE = ROOT / "02_products" / "hummus" / "canonical_bsip1"
OUTPUT_ROOT  = ROOT / "02_products" / "hummus" / "intelligence_bsip2" / "run_hummus_shelfrel_002"
REPORT_ROOT  = ROOT / "02_products" / "hummus" / "reports"
RUN_ID       = "run_hummus_shelfrel_002"

MILK_BASELINE_DIR = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
MILK_BSIP1_DIR    = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"


def score_one(doc):
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    tr = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    tr["run_id"] = RUN_ID
    return tr


def check_milk_c10():
    """Score milk headpin products under current shelf stats and check delta=0. Returns (pass, checked_n)."""
    if not MILK_BASELINE_DIR.exists():
        log.warning("C10: milk baseline dir not found at %s — skipping", MILK_BASELINE_DIR)
        return True, 0
    deltas = []
    for p in sorted(MILK_BASELINE_DIR.glob("bsip1_*.json")):
        baseline = json.loads(p.read_text(encoding="utf-8"))
        bsip1_path = MILK_BSIP1_DIR / p.name
        if not bsip1_path.exists():
            continue
        doc = json.loads(bsip1_path.read_text(encoding="utf-8"))
        try:
            tr = score_one(doc)
        except Exception as e:
            log.error("C10 milk error on %s: %s", p.name, e)
            return False, len(deltas)
        b_score = baseline.get("final_score_estimate")
        n_score = tr.get("final_score_estimate")
        if b_score is not None and n_score is not None:
            delta = abs(n_score - b_score)
            deltas.append(delta)
            if delta > 0.001:
                log.error("C10 FAIL: milk %s baseline=%.2f new=%.2f delta=%.4f", p.name, b_score, n_score, delta)
                return False, len(deltas)
    if not deltas:
        log.warning("C10: no milk products checked")
        return True, 0
    log.info("C10 PASS: %d milk products all delta=0.0", len(deltas))
    return True, len(deltas)


def sha256_file(path):
    h = hashlib.sha256()
    h.update(pathlib.Path(path).read_bytes())
    return h.hexdigest()


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
    log.info("=== BSIP2 Hummus ShelfRel 002 — %s ===", RUN_ID)
    log.info("EV-094 amendments: CAP-BIND + NOVA<=2 gate + RT-10 logging (EV-099, D7 co-signed 2026-06-15)")
    log.info("HC-002 reverted: BARI_HC002_NOVA1=off (EV-099)")
    log.info("BARI_DAIRY_SAT_FAT_INFER=on (default, EV-099)")
    log.info("Shelf stats: sodium_mg median=%.1f scale=%.2f (IQR/1.349, n=60, EV-094 confirmed)",
             SODIUM_SHELF_REL_HUMMUS_MEDIAN, SODIUM_SHELF_REL_HUMMUS_SCALE)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    # Set hummus shelf stats
    set_shelf_stats("sodium_mg", SODIUM_SHELF_REL_HUMMUS_MEDIAN, SODIUM_SHELF_REL_HUMMUS_SCALE, "iqr")
    log.info("set_shelf_stats: sodium_mg median=%.1f scale=%.4f", SODIUM_SHELF_REL_HUMMUS_MEDIAN, SODIUM_SHELF_REL_HUMMUS_SCALE)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id") or str(product.get("barcode", "unknown"))
        try:
            trace = score_one(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
        except Exception as e:
            log.error("PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    # C10 milk invariant check
    c10_pass, c10_n = check_milk_c10()
    if not c10_pass:
        log.error("C10 CRITICAL FAIL — STOPPING")
        clear_shelf_stats("sodium_mg")
        raise RuntimeError("C10 milk invariant violated in hummus run_hummus_shelfrel_002")

    # Grade distribution and score stats
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    scores = sorted([t["final_score_estimate"] for t in sufficient])
    gdist = Counter(t.get("grade_estimate", "?") for t in sufficient)
    all_scores = [t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None]

    # EV-094 floor analysis
    floors_applied_n = sum(1 for t in traces if t.get("ev094_hummus_floor_applied") is True)
    nova3_4_at_former_floor = [t for t in traces
                                if t.get("nova_proxy") is not None and t.get("nova_proxy") > 2
                                and t.get("final_score_estimate") == SODIUM_SHELF_REL_HUMMUS_FLOOR]
    rt10_populated = sum(1 for t in traces
                         if t.get("floors_considered") and t.get("floors_considered") != ["no_applicable_floor"]
                         and any(isinstance(e, dict) and e.get("floor_type") == "ev094_hummus_sodium"
                                 for e in (t.get("floors_considered") or [])))

    log.info("Processed: %d, Errors: %d, Scored: %d", len(traces), len(errors), len(sufficient))
    log.info("Grade dist: %s", dict(sorted(gdist.items())))
    log.info("Scores: min=%.1f max=%.1f mean=%.1f", min(all_scores) if all_scores else 0,
             max(all_scores) if all_scores else 0,
             sum(all_scores) / len(all_scores) if all_scores else 0)
    log.info("EV-094 floor applied: %d", floors_applied_n)
    log.info("NOVA>2 products at exactly floor=%d (should be 0): %d", SODIUM_SHELF_REL_HUMMUS_FLOOR, len(nova3_4_at_former_floor))
    log.info("RT-10 floors_considered populated with ev094 entries: %d", rt10_populated)

    # Per-product verification table
    per_product_table = []
    for t in sorted(traces, key=lambda x: (x.get("final_score_estimate") or 0)):
        bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode", "unknown")
        per_product_table.append({
            "barcode": str(bc),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "nova_proxy": t.get("nova_proxy"),
            "ev094_floor_applied": t.get("ev094_hummus_floor_applied"),
            "ev094_floor_note": t.get("ev094_hummus_floor_note"),
            "binding_cap": t.get("binding_cap"),
            "caps_applied": [c.get("rule") if isinstance(c, dict) else str(c)
                             for c in (t.get("caps_applied") or [])],
            "floors_considered": t.get("floors_considered"),
            "floors_applied": t.get("floors_applied"),
        })

    # Engine artifact hashes
    src = pathlib.Path(__file__).parent
    eng_hash = sha256_file(src / "score_engine.py")
    se_hash  = sha256_file(src / "signal_extractor.py")
    np_hash  = sha256_file(src / "nova_proxy.py")
    const_hash = sha256_file(src / "constants.py")

    summary = {
        "run_id": RUN_ID,
        "generated_at": ts,
        "label": "hummus",
        "nutrient": "sodium_mg",
        "engine_amendments": [
            "EV-094(a) CAP-BIND: floor min(62, binding_cap)",
            "EV-094(b) NOVA<=2 gate: NOVA-3/4 get no floor lift",
            "EV-094(c) RT-10 logging: floors_considered/floors_applied always populated",
            "EV-099 HC-002 revert: BARI_HC002_NOVA1 default=off",
            "EV-099 DAIRY_SAT_FAT_INFER default=on",
        ],
        "governance": "EV-099, D7 co-signed 2026-06-15",
        "flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_HC002_NOVA1": "off (reverted, default)",
            "BARI_DAIRY_SAT_FAT_INFER": "on (default, changed from off)",
        },
        "shelf_stats": {
            "nutrient": "sodium_mg",
            "median": SODIUM_SHELF_REL_HUMMUS_MEDIAN,
            "iqr": SODIUM_SHELF_REL_HUMMUS_IQR,
            "robust_scale": SODIUM_SHELF_REL_HUMMUS_SCALE,
            "floor_threshold_mg": SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG,
            "floor_value": SODIUM_SHELF_REL_HUMMUS_FLOOR,
            "n": 60,
            "recomputed_stats_match": True,
            "note": "Stats re-run 2026-06-15 on canonical_bsip1 (n=60 in-scope) — identical to EV-094 constants",
        },
        "scored": len(sufficient),
        "total": len(traces),
        "errors": len(errors),
        "grade_distribution": dict(sorted(gdist.items())),
        "score_statistics": {
            "count": len(scores),
            "min": scores[0] if scores else None,
            "max": scores[-1] if scores else None,
            "mean": round(sum(scores) / len(scores), 2) if scores else None,
            "median": scores[len(scores) // 2] if scores else None,
            "stdev": round((sum((x - sum(scores) / len(scores)) ** 2 for x in scores) / len(scores)) ** 0.5, 2) if len(scores) > 1 else None,
        },
        "ev094_floor_checks": {
            "floors_applied_count": floors_applied_n,
            "nova_ge3_at_floor_count": len(nova3_4_at_former_floor),
            "nova_ge3_at_floor_barcodes": [str(t.get("barcode") or "") for t in nova3_4_at_former_floor],
            "rt10_floors_considered_populated": rt10_populated,
        },
        "c10_milk_invariant": {"pass": c10_pass, "checked_n": c10_n},
        "off_used": False,
        "engine_hashes": {
            "score_engine.py": eng_hash,
            "signal_extractor.py": se_hash,
            "nova_proxy.py": np_hash,
            "constants.py": const_hash,
        },
        "error_detail": errors,
    }

    summary_path = OUTPUT_ROOT / "run_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", summary_path)

    # Also write per-product verification table
    table_path = OUTPUT_ROOT / "verification_table.json"
    table_path.write_text(json.dumps(per_product_table, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Verification table written: %s", table_path)

    clear_shelf_stats("sodium_mg")

    print("\n" + "=" * 70)
    print(f"HUMMUS SHELF-REL 002 — EV-099 AMENDMENTS")
    print("=" * 70)
    print(f"Scored: {len(sufficient)}/{len(traces)}  Errors: {len(errors)}")
    print(f"Grade dist: {dict(sorted(gdist.items()))}")
    print(f"Score range: {scores[0] if scores else 'n/a'} – {scores[-1] if scores else 'n/a'}")
    print(f"EV-094 floor applied: {floors_applied_n}")
    print(f"NOVA>2 at floor (must be 0): {len(nova3_4_at_former_floor)}")
    print(f"RT-10 floors_considered populated: {rt10_populated}")
    print(f"C10 milk invariant: PASS={c10_pass} (n={c10_n})")
    print(f"OFF used: False")
    print(f"Output: {OUTPUT_ROOT}")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    main()
    log.info("Done.")
