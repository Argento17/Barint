"""
TASK-397 Staging Re-scorer — Bread Fat-Sentinel (BARI_FAT_SENTINEL_V1=on)
Owner-approved 2026-06-25, Option B-Extended.

Scores the same 31 bread BSIP1 records as run_bread_conform_001, but with
BARI_FAT_SENTINEL_V1=on so ceiling-declared fat does NOT earn the R3 leanness
reward.

Output: staging/task397_rescore/  (never touches bsip2_outputs/run_bread_conform_001/)

Flags: same as batch_run_bread_conform_001 + BARI_FAT_SENTINEL_V1=on
"""
from __future__ import annotations
import sys, json, pathlib, datetime, os, hashlib

# ── flags MUST be set before score_engine is imported ──
STAGING_FLAGS = {
    "BARI_RECAL_P0":                  "on",
    "BARI_SHELF_RELATIVE_V1":         "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1":  "off",
    "BARI_FAT_TECH_V1":               "on",
    "BARI_GRAD_SODIUM_V1":            "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1":               "off",
    "BARI_SODIUM_CEREAL":             "off",
    # --- NEW flag ---
    "BARI_FAT_SENTINEL_V1":           "on",
}
for k, v in STAGING_FLAGS.items():
    os.environ[k] = v

sys.path.insert(0, str(pathlib.Path(__file__).parents[4] / "03_operations/bsip2/proto_v0/src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from input_loader   import load_product, validate_product
from signal_extractor import extract_signals
from router_v2      import classify_category
from nova_proxy     import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine   import score_product, compute_confidence
from trace_writer   import assemble_trace
from structural_classifier import classify_structural_class

BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_conform_001\output")
OUT_DIR    = pathlib.Path(__file__).parent / "products"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def score_one(product: dict) -> dict:
    prod     = {k: v for k, v in product.items() if not k.startswith("_")}
    signals  = extract_signals(prod)
    cat_res  = classify_category(prod)
    l3       = signals["L3_inferred_classifications"]
    nova_res = infer_nova(prod, l3)
    eval_res = assign_evaluation_scope(prod, cat_res["category"])
    sc_res   = score_product(prod, signals, cat_res, nova_res, eval_res)
    trace    = assemble_trace(prod, signals, cat_res, nova_res, eval_res, sc_res)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def sha256_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def main():
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    print(f"BSIP1 files: {len(bsip1_files)}")
    print(f"Flags: {STAGING_FLAGS}")
    print()

    scored, results = 0, []

    for fpath in bsip1_files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        product["_load_errors"] = validate_product(product)

        pid     = product.get("canonical_product_id", fpath.stem)
        barcode = str(product.get("barcode", ""))
        nn      = product.get("normalized_nutrition_per_100g", {}) or {}
        fat_sentinel = nn.get("fat_sentinel", False)

        try:
            trace = score_one(product)
        except Exception as e:
            print(f"  ERROR {pid}: {e}")
            results.append({"pid": pid, "barcode": barcode, "error": str(e)})
            continue

        pdir = OUT_DIR / str(pid)
        pdir.mkdir(parents=True, exist_ok=True)
        trace_path = pdir / "bsip2_trace.json"
        trace_path.write_text(
            json.dumps(trace, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        scored += 1

        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")
        fq    = trace.get("dimension_scores", {}).get("fat_quality")
        fq_note = trace.get("dimension_notes", {}).get("fat_quality", "")[:60]
        results.append({
            "pid": pid, "barcode": barcode,
            "name": product.get("canonical_name_he", "?"),
            "fat_sentinel": fat_sentinel,
            "fat_quality": fq,
            "score": score, "grade": grade,
            "fat_note": fq_note,
            "sha256": sha256_file(trace_path),
        })
        marker = "[SENTINEL]" if fat_sentinel else ""
        print(f"  {barcode} | score={score} | grade={grade} | fq={fq} | {marker}")

    print(f"\nScored: {scored}/{len(bsip1_files)}")

    run_record = {
        "run_id":       "task397_staging",
        "task":         "TASK-397",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip1_dir":    str(BSIP1_DIR),
        "out_dir":      str(OUT_DIR),
        "scored_count": scored,
        "flags":        STAGING_FLAGS,
        "results":      results,
    }
    rec_path = pathlib.Path(__file__).parent / "run_record.json"
    rec_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRun record: {rec_path}")


if __name__ == "__main__":
    main()
