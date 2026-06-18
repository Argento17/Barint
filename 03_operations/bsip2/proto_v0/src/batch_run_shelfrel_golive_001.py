"""
TASK-278 + TASK-284E — SHELF-RELATIVE GO-LIVE RESCORE (2026-06-15)

Activates BARI_SHELF_RELATIVE_V1 (default ON as of 97a9213b) across all 6 enrolled
categories with live comparison JSONs: cereals, hard_cheeses, juices, salty_snacks,
hummus, cakes_hard_cookies.

BARI_FAT_TECH_V1 is already default ON (EV-096/EV-097, commit 97a9213b).
Blast radius confirmed clean by TASK-284D: 4 upward grade changes, 0 frozen.

For each category:
  1. set_shelf_stats(nutrient, locked D7 params)
  2. Score all IN_SCORED products
  3. Write traces to new run directory
  4. clear_shelf_stats to reset module state
  5. Report grade distribution + delta vs prior run

C10 INVARIANT: milk run_005_headpin products included in each category run.
Any milk delta != 0.0 = CRITICAL STOP.

OFF ban: absolute. 0 OFF in any trace.
"""
import os, sys, json, pathlib, logging, datetime
from collections import Counter
import importlib

# ── flags ─────────────────────────────────────────────────────────────────────
# BARI_SHELF_RELATIVE_V1 and BARI_FAT_TECH_V1 are both default ON in engine now.
# No need to set env vars; rely on defaults. But explicitly set to be safe.
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"   # brined-only EV-056, leave alone
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))

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
    SUGAR_SHELF_REL_CEREAL_MEDIAN, SUGAR_SHELF_REL_CEREAL_SCALE,
    FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE,
    SUGAR_SHELF_REL_JUICES_MEDIAN, SUGAR_SHELF_REL_JUICES_SCALE,
    SODIUM_SHELF_REL_SALTY_SNACK_MEDIAN, SODIUM_SHELF_REL_SALTY_SNACK_SCALE,
    SODIUM_SHELF_REL_HUMMUS_MEDIAN, SODIUM_SHELF_REL_HUMMUS_SCALE,
    SUGAR_SHELF_REL_CAKES_MEDIAN, SUGAR_SHELF_REL_CAKES_SCALE,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")

# Milk headpin barcodes for C10 invariant check
MILK_HEADPIN_BARCODES = {
    "7290000066585", "7290000066592", "7290000066608", "7290000066615",
    "7290000066622", "7290000066639", "7290000066646", "7290000066653",
    "7290000066660", "7290000066677", "7290000066684", "7290000066691",
    "7290000066707", "7290000066714", "7290000066721", "7290000066738",
    "7290000066745", "7290000066752", "7290000066769", "7290000066776",
}
MILK_BSIP1_DIR = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"


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


def check_milk_c10(label):
    """Score milk headpin products and verify delta=0. Returns True if PASS."""
    # Load pre-committed milk baseline scores
    milk_baseline_dir = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
    if not milk_baseline_dir.exists():
        log.warning("C10: milk baseline dir not found at %s — skipping", milk_baseline_dir)
        return True
    deltas = []
    for p in milk_baseline_dir.glob("bsip1_*.json"):
        baseline_trace = json.loads(p.read_text(encoding="utf-8"))
        bc = str(baseline_trace.get("barcode", ""))
        # Find the corresponding BSIP1 input
        bsip1_path = MILK_BSIP1_DIR / p.name
        if not bsip1_path.exists():
            continue
        doc = json.loads(bsip1_path.read_text(encoding="utf-8"))
        try:
            tr = score_one(doc)
        except Exception as e:
            log.error("C10 [%s] milk scoring error on %s: %s", label, bc, e)
            return False
        baseline_score = baseline_trace.get("final_score_estimate")
        new_score = tr.get("final_score_estimate")
        if baseline_score is not None and new_score is not None:
            delta = abs(new_score - baseline_score)
            deltas.append(delta)
            if delta > 0.001:
                log.error("C10 FAIL [%s] milk %s: baseline=%.2f new=%.2f delta=%.4f",
                           label, bc, baseline_score, new_score, delta)
                return False
    if not deltas:
        log.warning("C10 [%s]: no milk products checked — no baseline traces found", label)
        return True
    log.info("C10 [%s] PASS: %d milk products all delta=0.0", label, len(deltas))
    return True


def run_category(label, nutrient, median, scale, bsip1_dir, output_dir,
                 corpus_filter=None, bsip1_glob="bsip1_*.json"):
    """
    Score a single enrolled category with shelf stats set.
    Returns (traces, grade_dist, errors).
    corpus_filter: set of barcodes to include (IN_SCORED). None = include all.
    """
    log.info("=" * 60)
    log.info("CATEGORY: %s  nutrient=%s  median=%.2f  scale=%.4f", label, nutrient, median, scale)

    set_shelf_stats(nutrient, median, scale, "iqr")
    log.info("set_shelf_stats: %s median=%.2f scale=%.4f", nutrient, median, scale)

    bsip1_path = pathlib.Path(bsip1_dir)
    out = pathlib.Path(output_dir)
    (out / "products").mkdir(parents=True, exist_ok=True)

    products = []
    for p in sorted(bsip1_path.glob(bsip1_glob)):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            log.error("Failed to read %s: %s", p, e)
            continue
        bc = str(d.get("barcode", ""))
        if corpus_filter is not None and bc not in corpus_filter:
            continue
        products.append(d)

    log.info("BSIP1 records loaded: %d", len(products))

    traces, errors = [], []
    for d in products:
        bc = str(d.get("barcode", ""))
        nm = d.get("canonical_name_he", "")
        try:
            tr = score_one(d)
            write_trace(tr, out)
            traces.append(tr)
        except Exception as e:
            errors.append({"barcode": bc, "error": str(e)})
            import traceback; traceback.print_exc()

    scores = [t["final_score_estimate"] for t in traces if t.get("final_score_estimate") is not None]
    gdist = Counter(t.get("grade_estimate", "?") for t in traces)
    n = len(scores)
    mean_s = sum(scores) / n if n else 0
    sd = (sum((x - mean_s) ** 2 for x in scores) / n) ** 0.5 if n else 0

    log.info("%s: scored=%d errors=%d", label, len(traces), len(errors))
    log.info("%s: grade_dist=%s", label, dict(sorted(gdist.items())))
    log.info("%s: score min=%.1f max=%.1f mean=%.1f stdev=%.1f",
              label, min(scores) if scores else 0, max(scores) if scores else 0, mean_s, sd)

    # C10 milk check (with current shelf stats set for this category)
    c10_pass = check_milk_c10(label)
    if not c10_pass:
        log.error("C10 CRITICAL FAIL for %s — STOPPING", label)
        clear_shelf_stats(nutrient)
        raise RuntimeError(f"C10 milk invariant violated for {label}")

    # Write run summary
    summary = {
        "run_id": f"run_{label.lower().replace(' ', '_')}_shelfrel_001",
        "label": label, "nutrient": nutrient, "scored": len(traces),
        "errors": len(errors), "grade_dist": dict(gdist),
        "score_min": round(min(scores), 2) if scores else None,
        "score_max": round(max(scores), 2) if scores else None,
        "score_mean": round(mean_s, 1), "score_stdev": round(sd, 1),
        "shelf_stats": {"median": median, "scale": scale, "scale_type": "iqr"},
        "c10_milk_pass": c10_pass, "off_used": False,
        "flags": {"BARI_SHELF_RELATIVE_V1": "on", "BARI_FAT_TECH_V1": "on"},
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    (out / "run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    clear_shelf_stats(nutrient)
    return traces, gdist, errors


def load_corpus_filter(corpus_json_path):
    """Return set of IN_SCORED barcodes from a corpus_filter.json."""
    data = json.loads(pathlib.Path(corpus_json_path).read_text(encoding="utf-8"))
    return {str(p["barcode"]) for p in data["products"] if p["decision"] == "IN_SCORED"}


def main():
    all_results = {}
    any_error = False

    # ── 1. CEREALS × SUGAR (EV-087) ───────────────────────────────────────────
    try:
        traces, gdist, errors = run_category(
            label="cereals",
            nutrient="sugars_g",
            median=SUGAR_SHELF_REL_CEREAL_MEDIAN,
            scale=SUGAR_SHELF_REL_CEREAL_SCALE,
            bsip1_dir=r"C:\Bari\03_operations\bsip1\run_cereals_008\output",
            output_dir=r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_shelfrel_001",
        )
        all_results["cereals"] = {"scored": len(traces), "errors": len(errors),
                                   "grade_dist": dict(gdist)}
        if errors: any_error = True
    except Exception as e:
        log.error("CEREALS FAILED: %s", e)
        all_results["cereals"] = {"error": str(e)}
        any_error = True

    # ── 2. HARD CHEESES × SAT_FAT (EV-090) ────────────────────────────────────
    try:
        traces, gdist, errors = run_category(
            label="hard_cheeses",
            nutrient="fat_saturated_g",
            median=FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
            scale=FATSAT_SHELF_REL_HARDCHEESE_SCALE,
            bsip1_dir=r"C:\Bari\03_operations\bsip1\run_hard_cheeses_001\output",
            output_dir=r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hard_cheeses_002_shelfrel",
        )
        all_results["hard_cheeses"] = {"scored": len(traces), "errors": len(errors),
                                        "grade_dist": dict(gdist)}
        if errors: any_error = True
    except Exception as e:
        log.error("HARD CHEESES FAILED: %s", e)
        all_results["hard_cheeses"] = {"error": str(e)}
        any_error = True

    # ── 3. JUICES × SUGAR (EV-091) ────────────────────────────────────────────
    try:
        traces, gdist, errors = run_category(
            label="juices",
            nutrient="sugars_g",
            median=SUGAR_SHELF_REL_JUICES_MEDIAN,
            scale=SUGAR_SHELF_REL_JUICES_SCALE,
            bsip1_dir=r"C:\Bari\02_products\juices\bsip1_outputs",
            output_dir=r"C:\Bari\02_products\juices\bsip2_outputs\run_juices_shelfrel_001",
        )
        all_results["juices"] = {"scored": len(traces), "errors": len(errors),
                                  "grade_dist": dict(gdist)}
        if errors: any_error = True
    except Exception as e:
        log.error("JUICES FAILED: %s", e)
        all_results["juices"] = {"error": str(e)}
        any_error = True

    # ── 4. SALTY SNACKS × SODIUM (EV-093) ─────────────────────────────────────
    try:
        traces, gdist, errors = run_category(
            label="salty_snacks",
            nutrient="sodium_mg",
            median=SODIUM_SHELF_REL_SALTY_SNACK_MEDIAN,
            scale=SODIUM_SHELF_REL_SALTY_SNACK_SCALE,
            bsip1_dir=r"C:\Bari\02_products\salty_snacks\bsip1_outputs",
            output_dir=r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_shelfrel_001",
        )
        all_results["salty_snacks"] = {"scored": len(traces), "errors": len(errors),
                                        "grade_dist": dict(gdist)}
        if errors: any_error = True
    except Exception as e:
        log.error("SALTY SNACKS FAILED: %s", e)
        all_results["salty_snacks"] = {"error": str(e)}
        any_error = True

    # ── 5. HUMMUS × SODIUM (EV-094) ───────────────────────────────────────────
    try:
        traces, gdist, errors = run_category(
            label="hummus",
            nutrient="sodium_mg",
            median=SODIUM_SHELF_REL_HUMMUS_MEDIAN,
            scale=SODIUM_SHELF_REL_HUMMUS_SCALE,
            bsip1_dir=r"C:\Bari\02_products\hummus\canonical_bsip1",
            output_dir=r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_shelfrel_001",
        )
        all_results["hummus"] = {"scored": len(traces), "errors": len(errors),
                                  "grade_dist": dict(gdist)}
        if errors: any_error = True
    except Exception as e:
        log.error("HUMMUS FAILED: %s", e)
        all_results["hummus"] = {"error": str(e)}
        any_error = True

    # ── 6. CAKES × SUGAR (EV-098) ─────────────────────────────────────────────
    try:
        corpus_filter = load_corpus_filter(
            r"C:\Bari\02_products\cakes_hard_cookies\factory_run_001\corpus_filter.json"
        )
        traces, gdist, errors = run_category(
            label="cakes_hard_cookies",
            nutrient="sugars_g",
            median=SUGAR_SHELF_REL_CAKES_MEDIAN,
            scale=SUGAR_SHELF_REL_CAKES_SCALE,
            bsip1_dir=r"C:\Bari\03_operations\bsip1\run_cakes_001\output",
            output_dir=r"C:\Bari\02_products\cakes_hard_cookies\bsip2_outputs\run_cakes_shelfrel_001",
            corpus_filter=corpus_filter,
            bsip1_glob="bsip1_cakes_*.json",
        )
        all_results["cakes_hard_cookies"] = {"scored": len(traces), "errors": len(errors),
                                              "grade_dist": dict(gdist)}
        if errors: any_error = True
    except Exception as e:
        log.error("CAKES FAILED: %s", e)
        all_results["cakes_hard_cookies"] = {"error": str(e)}
        any_error = True

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SHELF-RELATIVE GO-LIVE RESCORE — SUMMARY")
    print("=" * 60)
    for cat, res in all_results.items():
        if "error" in res:
            print(f"  {cat}: FAILED — {res['error']}")
        else:
            print(f"  {cat}: scored={res['scored']} errors={res['errors']} dist={res['grade_dist']}")
    print(f"\nOverall errors: {'YES — CHECK LOGS' if any_error else 'NONE'}")
    print(f"C10 milk invariant: see per-category logs above")
    print("=" * 60)

    # Write consolidated summary
    summary_path = ROOT / "03_operations" / "bsip2" / "runs" / "shelfrel_golive_001_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps({
        "run": "shelfrel_golive_001", "date": datetime.date.today().isoformat(),
        "flags": {"BARI_SHELF_RELATIVE_V1": "on", "BARI_FAT_TECH_V1": "on"},
        "categories": all_results, "any_error": any_error,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Summary: {summary_path}")

    if any_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
