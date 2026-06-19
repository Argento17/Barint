# -*- coding: utf-8 -*-
"""
Hard Cheeses — BARI_REDLABEL_V1 fresh re-score.
Run ID: run_hc_redlabel_v2_001
Worktree: C:\\bari_hcredlabel  (branch: fan/hcredlabel)

Activates ALL four live flags:
  BARI_SHELF_RELATIVE_V1 = on   (EV-090: fat_sat shelf-relative for yellow/yellow_light/hard_grating)
  BARI_FAT_TECH_V1       = on   (existing fat-technology scoring)
  BARI_RECAL_P0          = on   (R1-R7 recalibration)
  BARI_REDLABEL_V1       = on   (NEW: graduated red-label, no binary ISRAELI_RED_LABELS_2_PLUS cliff)

The bogus run_hardcheese_redlabel_v1_001 is EXCLUDED from this lineage:
  - It never called set_shelf_stats() so fat_sat shelf-relative was inert,
    producing 37/67 insufficient_data outcomes. Those scores are invalid.

Corpus: 23 display barcodes from the live hard_cheeses_frontend_v2.json
  (28-product corpus after OFF exclusions, de-duplicated to 23 unique size-variants)
Source BSIP1: C:\\bari_hcredlabel\\02_products\\hard_cheeses\\bsip1_outputs
Output: C:\\bari_hcredlabel\\02_products\\hard_cheeses\\bsip2_outputs\\run_hc_redlabel_v2_001\\
"""
import os, sys

# Set ALL flags before any engine import so env is read at module load
os.environ["BARI_SHELF_RELATIVE_V1"]      = "on"
os.environ["BARI_FAT_TECH_V1"]            = "on"
os.environ["BARI_RECAL_P0"]               = "on"
os.environ["BARI_REDLABEL_V1"]            = "on"
# BARI_HC002_NOVA1: must match the live baseline (run_003_shelfrel).
# run_003 was generated 2026-06-15, BEFORE the EV-099 gate that requires explicit opt-in.
# At run_003 time HC-002 was active by default (nova_uncertainty_notes confirm it).
# Without this flag, products get NOVA 2 instead of NOVA 1 — a separate change
# unrelated to BARI_REDLABEL_V1, which would contaminate the before→after comparison.
os.environ["BARI_HC002_NOVA1"]             = "on"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"   # brined-only EV-056
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"]           = "off"
os.environ["BARI_GRAD_SODIUM_V1"]          = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json, pathlib, logging, datetime
from collections import Counter

SRC = pathlib.Path(__file__).parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from trace_writer import assemble_trace, write_trace
from constants import (
    score_to_grade,
    FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
    FATSAT_SHELF_REL_HARDCHEESE_SCALE,
)
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

WORKTREE = pathlib.Path(r"C:\bari_hcredlabel")
BSIP1_DIR = WORKTREE / "02_products" / "hard_cheeses" / "bsip1_outputs"
OUTPUT_DIR = WORKTREE / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hc_redlabel_v2_001"
FRONTEND_JSON = WORKTREE / "bari-web" / "src" / "data" / "comparisons" / "hard_cheeses_frontend_v2.json"

RUN_ID = "run_hc_redlabel_v2_001"

# The 23 barcodes currently displayed in hard_cheeses_frontend_v2.json
# (extracted from the live JSON; these are the exact display-eligible products)
DISPLAY_BARCODES_23 = {
    "7290108502725",  # Gouda Euro Cheese 400g
    "7290019635192",  # Gouda Goat slices
    "7290110324872",  # Galboa 5% slices
    "7290110323301",  # Tal Haemek Emmental 32%
    "7290116931524",  # Gouda Emek 200g
    "7290102396672",  # Naom 9% 360g
    "7290004122348",  # Emek 9% 200g
    "7290004137311",  # Emek 9% 400g
    "7290108501346",  # Gouda Euro Cheese grated 500g
    "7290117265888",  # Gouda Yochananof grated 400g
    "7290117265918",  # Gouda Yochananof sliced 400g
    "7290102397204",  # Naom 22% 200g
    "7290102394463",  # Naom 28% 500g
    "7290014760912",  # Gush Chalav 28% Mehadrin 400g
    "7290004125776",  # Emek 28% 400g
    "7290004122683",  # Emek fingers 172g
    "7290110320867",  # Emek grated 500g
    "7290000057088",  # Emek thin 200g
    "7290014763395",  # Emek 28% 600g
    "7290017065434",  # Dutch Gouda 30% 200g
    "8711528211138",  # Gouda Goat (imported)
    "7290108503999",  # Euro Cheese processed 13%
    "3073781199918",  # Babybel 5*20g
}

assert len(DISPLAY_BARCODES_23) == 23, f"Expected 23, got {len(DISPLAY_BARCODES_23)}"


def score_one(doc):
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    tr = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    return tr


def main():
    log.info("=== BSIP2 Hard Cheeses — %s ===", RUN_ID)
    log.info("Flags: BARI_SHELF_RELATIVE_V1=on BARI_FAT_TECH_V1=on BARI_RECAL_P0=on BARI_REDLABEL_V1=on BARI_HC002_NOVA1=on")
    log.info("Corpus: 23 display barcodes from live hard_cheeses_frontend_v2.json")
    log.info("fat_sat shelf stats: median=%.1f scale=%.4f (EV-090 locked params)",
             FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE)
    log.info("BARI_REDLABEL_V1: binary ISRAELI_RED_LABELS_2_PLUS cap REPLACED by "
             "REFORMULABLE_LABELS_2_PLUS (endemic sat_fat excluded); "
             "HIGH_SODIUM_700MG_PLUS cliff REPLACED by SODIUM_GENERAL_BANDS graduated penalty")

    # Purge and recreate output dir
    import shutil
    prod_dir = OUTPUT_DIR / "products"
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    prod_dir.mkdir(parents=True, exist_ok=True)

    # Set shelf stats for fat_sat (EV-090 locked params — same as run_003_shelfrel)
    set_shelf_stats(
        "fat_saturated_g",
        FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
        FATSAT_SHELF_REL_HARDCHEESE_SCALE,
        "iqr"
    )
    log.info("set_shelf_stats: fat_saturated_g median=%.1f scale=%.4f type=iqr",
             FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE)

    # Load BSIP1 records — filter to the 23 display barcodes
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    log.info("Total BSIP1 files found: %d", len(bsip1_files))

    products = []
    for p in bsip1_files:
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            log.error("Failed to read %s: %s", p, e)
            continue
        bc = str(doc.get("barcode", ""))
        if bc not in DISPLAY_BARCODES_23:
            continue
        products.append(doc)

    log.info("Products in display corpus: %d / 23 expected", len(products))
    if len(products) != 23:
        missing = DISPLAY_BARCODES_23 - {str(d.get("barcode")) for d in products}
        log.error("MISSING BARCODES: %s", missing)
        raise RuntimeError(f"Corpus mismatch: expected 23, found {len(products)}")

    traces, errors = [], []
    for doc in products:
        bc = str(doc.get("barcode", ""))
        nm = doc.get("canonical_name_he", "")
        try:
            tr = score_one(doc)
            write_trace(tr, OUTPUT_DIR)
            traces.append(tr)
        except Exception as e:
            log.error("PIPELINE ERROR [%s] %s: %s", bc, nm[:30], e)
            import traceback; traceback.print_exc()
            errors.append({"barcode": bc, "name": nm, "error": str(e)})

    clear_shelf_stats("fat_saturated_g")

    # Build per-product result table
    results = []
    for tr in traces:
        ref = tr.get("input_reference") or {}
        bc = ref.get("barcode") or tr.get("barcode") or ""
        results.append({
            "barcode": str(bc),
            "name":    ref.get("canonical_name_he") or ref.get("product_name_he") or "",
            "score":   tr.get("final_score_estimate"),
            "grade":   tr.get("grade_estimate"),
            "nova":    tr.get("nova_proxy"),
            "status":  tr.get("evaluation_status"),
            "caps_fired": [c["rule"] for c in (tr.get("caps_applied") or [])],
        })
    results.sort(key=lambda x: (x["score"] or 0), reverse=True)

    scores = [r["score"] for r in results if r["score"] is not None]
    grade_dist = dict(Counter(r["grade"] for r in results))
    n = len(scores)
    mean_s = sum(scores) / n if n else 0
    stdev_s = (sum((x - mean_s)**2 for x in scores) / n)**0.5 if n else 0

    log.info("=" * 60)
    log.info("RESULTS — %s", RUN_ID)
    log.info("scored=%d errors=%d", len(traces), len(errors))
    log.info("grade_dist=%s", dict(sorted(grade_dist.items())))
    log.info("score min=%.1f max=%.1f mean=%.1f stdev=%.1f",
             min(scores) if scores else 0, max(scores) if scores else 0, mean_s, stdev_s)
    log.info("")
    log.info("%-16s %-42s %6s %-2s  %s", "BARCODE", "NAME", "SCORE", "GR", "CAPS")
    for r in results:
        nm = r["name"][:41]
        caps_str = ",".join(r["caps_fired"]) if r["caps_fired"] else "-"
        log.info("%-16s %-42s %6.1f %-2s  %s", r["barcode"], nm, r["score"] or 0, r["grade"] or "?", caps_str)

    # Write run summary
    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_REDLABEL_V1": "on",
            "BARI_HC002_NOVA1": "on (matches run_003_shelfrel baseline; active before EV-099 gate 2026-06-16)",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GRAD_SODIUM_V1": "off",
        },
        "shelf_stats": {
            "nutrient": "fat_saturated_g",
            "median": FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
            "scale": FATSAT_SHELF_REL_HARDCHEESE_SCALE,
            "scale_type": "iqr",
            "source": "EV-090 locked params (constants.py FATSAT_SHELF_REL_HARDCHEESE_*)",
        },
        "corpus": {
            "source_dir": str(BSIP1_DIR),
            "display_count": 23,
            "scored_count": len(traces),
            "error_count": len(errors),
        },
        "prior_bogus_run": {
            "run_id": "run_hardcheese_redlabel_v1_001",
            "reason_invalid": "Never called set_shelf_stats(); fat_sat shelf-relative was inert; produced 37/67 insufficient_data. EXCLUDED from this lineage.",
        },
        "grade_distribution": dict(sorted(grade_dist.items())),
        "score_stats": {
            "min": round(min(scores), 1) if scores else None,
            "max": round(max(scores), 1) if scores else None,
            "mean": round(mean_s, 1),
            "stdev": round(stdev_s, 1),
        },
        "per_product": results,
        "errors": errors,
        "off_used": False,
        "c10_milk_invariant": "Not checked in this worktree run — no shared milk corpus at C:\\bari_hcredlabel paths. Scores are read from existing traces; milk delta check is irrelevant here since this run only affects hard_cheeses scoring.",
    }
    summary_path = OUTPUT_DIR / "run_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", summary_path)
    return results, grade_dist, errors


if __name__ == "__main__":
    main()
    log.info("Done.")
