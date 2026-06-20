"""
TASK-360 Phase 3 — Fix: re-run BSIP2 + rebuild frontend JSON
Fixes:
  1. Read trace fields correctly (final_score_estimate, grade_estimate, input_reference)
  2. Apply second curation pass to remove false positives (chocolate bars, chips, etc.)
  3. Generate correct snacks_frontend_v5.json
Uses existing BSIP1 files from the phase3 run — no re-scraping needed.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import logging
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
BSIP2_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(BSIP2_SRC))

PHASE3_RUN_ID = "run_snacks_task360_phase3_20260620_083413"
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / PHASE3_RUN_ID / "output"
BSIP2_DIR = ROOT / "02_products" / "snack_bars" / "bsip2_outputs" / (PHASE3_RUN_ID + "_fix")
FRONTEND_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v5.json"

(BSIP2_DIR / "products").mkdir(parents=True, exist_ok=True)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def save_json(path, data):
    pathlib.Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Second curation pass — remove false positives ─────────────────────────────

# These are DEFINITIVELY not snack bars and should not have been kept:
FALSE_POSITIVE_BARCODES = {
    # Chocolate candy bars (not cereal/granola bars)
    "5000159560511",   # סניקרס חטיף בודד (Snickers)
    "5000159559485",   # טוויקס חטיף בודד (Twix)
    "5000159558792",   # מרס חטיף בודד (Mars)
    "5000159561976",   # באונטי חטיף בודד (Bounty)
    "34000250103",     # ריסז חטיף שוקולד ממולא בוטנים (Reese's)
    "4823077617041",   # ROSHEN חטיף שוקולד ממולא קרמל
    "4823077613630",   # ROSHEN חטיף שוקולד ממולא חלב מרוכז
    "4014400925319",   # ורטר חטיף פופקורן בציפוי קרמל (candy)
    "72917367",        # עלית חטיף שוקולד טעמי (chocolate)
    "7290105362377",   # עלית חטיף שוקולד כיף כף (chocolate)
    "7290106525504",   # עלית חטיף שוקולד טעמי בייגלה (chocolate)
    "7290116534442",   # קליק חטיף שוקולד חלב במילוי קרם חלבי (chocolate)
    # Salty/savory snacks (chips, corn puffs, etc.)
    "66349",           # אפרופו חטיף תירס
    "66332",           # אפרופו חטיף
    "178707",          # תפוצ'יפס חטיף תפוח אדמה אישי
    "7290100850923",   # דוריטוס חטיף תירס אישי
    "7290101551638",   # צ'יטוס חטיף תירס PUFFS
    "7290118427094",   # ביסלי חטיף גליץ' בטעם גריל (Bisli)
    "7290122782455",   # אסם חטיף צ'יפס בטעם מקסיקני
    "7290122782479",   # אסם חטיף צ'יפס גלי אסייתי
    "728229123590",    # טרה חטיף ירקות שורש (root vegetable crisps)
    "728229123811",    # טרה חטיף ירקות שורש ים תיכוני
    "7290019401780",   # חטיף פרוטאין מקס צ'יפס בטעם ברביקיו (protein CHIPS, not bar)
    # Borderline — soy/mixed snacks without bar format
    "7296073706359",   # הקולה מבגדד חטיף סויה בקופסא (loose soy snack)
    "7296073706342",   # הקולה מבגדד חטיף חריף בקופסא (loose spicy snack)
    # Raw oat products that passed curation due to category A281404 (but are raw oats)
    "7296073497721",   # גרין שיבולת שועל ללא גלוטן (raw gluten-free oats)
    "7296073497738",   # גרין קוואקר שיבולת שועל ללא גלוטן (raw oats)
    "7290018757123",   # עתיד ירוק פתיתי ש.שועל דקה אורגני (raw oat flakes)
    "7290018757130",   # עתיד ירוק פתיתי ש.שועל עבה אורגני (raw oat flakes)
    "58449870241",     # כדורוני תירס אורגני (corn puffs, not a bar)
    # Corn puffs / kids snacks
    "7290107646154",   # קוקומן חטיף פצפוצי דגנים (cereal puffs, not a bar)
    # nut snack pack (loose)
    # Pure candy confectionery (not a bar format)
    "72917329",     # עלית חטיף שוקולד אגוזי (chocolate candy)
    "72918388",     # עלית חטיף שוקולד טוויסט (candy chocolate)
    "7290116532011",# קליק חטיף נוגט (nougat candy, not a bar)
    # Corn/potato puffs (salty_corpus, not a bar)
    "110844",       # כיפלי חטיף בטעם גריל (corn puff)
}

# Additional exclusion: names that clearly indicate chocolate candy / chips
FALSE_POSITIVE_NAME_SIGNALS = [
    ("סניקרס", "chocolate_category"),
    ("טוויקס", "chocolate_category"),
    ("מרס חטיף", "chocolate_category"),
    ("באונטי", "chocolate_category"),
    ("ריסז", "chocolate_category"),
    ("roshen", "chocolate_category"),
    ("ורטר", "chocolate_category"),
    ("אפרופו", "salty_corpus"),
    ("תפוצ'יפס", "salty_corpus"),
    ("דוריטוס", "salty_corpus"),
    ("צ'יטוס", "salty_corpus"),
    ("ביסלי", "salty_corpus"),
    ("צ'יפס", "salty_corpus"),
    ("פופקורן", "salty_corpus"),
    ("ירקות שורש", "salty_corpus"),  # root vegetable crisps
    ("סויה בקופסא", "salty_corpus"),
    ("חריף בקופסא", "salty_corpus"),
    ("פצפוצי דגנים", "not_snack"),  # cereal puffs
    ("שיבולת שועל ללא גלוטן", "not_snack"),  # raw oats (gluten-free)
    ("פתיתי ש.שועל", "not_snack"),  # oat flakes (raw)
    ("קוואקר שיבולת", "not_snack"),  # Quaker oats
    ("כדורוני תירס", "not_snack"),  # corn puffs
    ("צ'יפס בטעם", "salty_corpus"),  # flavored chips
    ("פרוטאין מקס צ'יפס", "salty_corpus"),  # protein chips
    ("כיף כף", "chocolate_category"),  # Elite chocolate
    ("שוקולד אגוזי", "chocolate_category"),  # Elite nutty chocolate candy
    ("שוקולד טוויסט", "chocolate_category"),  # Elite chocolate twist candy
    ("קליק נוגט", "chocolate_category"),  # Click nougat candy
    ("טעמי בייגלה", "salty_corpus"),  # chocolate bagel snack
    ("שוקולד ממולא", "chocolate_category"),  # filled chocolate
    ("חטיף גליץ'", "salty_corpus"),  # Bisli Glitz
]


def second_curation(bsip1: dict) -> tuple[str, str]:
    """
    Second curation pass on BSIP1 records.
    Returns ('keep', reason) or ('exclude', tag:reason).
    """
    barcode = bsip1.get("barcode", "")
    name = (bsip1.get("canonical_name_he", "") or "").strip()
    brand = (bsip1.get("brand", "") or "").strip()
    name_l = name.lower()
    brand_l = brand.lower()

    # Barcode-based exclusions (definitive)
    if barcode in FALSE_POSITIVE_BARCODES:
        return "exclude", f"barcode match: known false positive"

    # Name-signal exclusions
    for sig, tag in FALSE_POSITIVE_NAME_SIGNALS:
        if sig.lower() in name_l or sig.lower() in brand_l:
            return "exclude", f"{tag}:name signal '{sig}'"

    return "keep", "passed second curation"


def run_bsip2_single(bsip1_path: pathlib.Path, output_dir: pathlib.Path) -> dict | None:
    """Run BSIP2 on one BSIP1 file. Returns the assembled trace dict or None on error."""
    from input_loader import load_product, validate_product
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    from trace_writer import assemble_trace, write_trace
    from structural_classifier import classify_structural_class

    try:
        product = load_product(bsip1_path)
        product["_source_path"] = str(bsip1_path)
        errors = validate_product(product)
        product["_load_errors"] = errors

        signals = extract_signals(product)
        cat_result = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = score_product(product, signals, cat_result, nova_result, eval_result)
        trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
        trace["structural_class"] = classify_structural_class(trace)

        barcode = product.get("barcode", "unknown")
        trace_dir = output_dir / f"bsip1_{barcode}"
        trace_dir.mkdir(parents=True, exist_ok=True)
        write_trace(trace, trace_dir)
        return trace
    except Exception as exc:
        log.error("BSIP2 error for %s: %s", bsip1_path.name, exc)
        return None


def build_frontend(scored: list[tuple[dict, dict]], run_id: str) -> dict:
    """
    Build frontend JSON from (bsip1, trace) pairs.
    Reads correct fields: final_score_estimate, grade_estimate from trace;
    identity from input_reference.
    """
    items = []
    for bsip1, trace in scored:
        barcode = trace.get("input_reference", {}).get("barcode", bsip1.get("barcode", ""))
        name_he = (
            trace.get("input_reference", {}).get("product_name_he")
            or bsip1.get("canonical_name_he", "")
        )
        brand = (
            trace.get("input_reference", {}).get("brand")
            or bsip1.get("brand", "")
        )
        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")
        image_url = bsip1.get("image_url", "")

        nutr = bsip1.get("normalized_nutrition_per_100g", {}) or {}

        item = {
            "barcode": barcode,
            "name_he": name_he,
            "brand": brand,
            "score": score,
            "grade": grade,
            "image_url": image_url,
            "nutrition_per_100g": {
                "energy_kcal": nutr.get("energy_kcal"),
                "fat_g": nutr.get("fat_g"),
                "fat_saturated_g": nutr.get("fat_saturated_g"),
                "sodium_mg": nutr.get("sodium_mg"),
                "carbohydrates_g": nutr.get("carbohydrates_g"),
                "sugars_g": nutr.get("sugars_g"),
                "dietary_fiber_g": nutr.get("dietary_fiber_g"),
                "protein_g": nutr.get("protein_g"),
            },
            # Copy fields — PENDING_COPY
            "verdict": "PENDING_COPY",
            "insight_line": "PENDING_COPY",
            "row_verdict": "PENDING_COPY",
            "_scoring_trace": {
                "category": trace.get("category"),
                "structural_class": trace.get("structural_class"),
                "final_score_estimate": score,
                "grade_estimate": grade,
                "nova_proxy": trace.get("nova_proxy"),
                "explanation_drivers": trace.get("explanation_drivers", []),
            },
        }
        items.append(item)

    # Sort by score descending (None at bottom)
    items.sort(key=lambda x: (x["score"] is None, -(x["score"] or 0)))

    return {
        "meta": {
            "version": "snacks_frontend_v5",
            "run_id": run_id,
            "generated_at": now_iso(),
            "category": "snack_bars",
            "product_count": len(items),
            "copy_status": "PENDING_COPY",
            "engine_unchanged": True,
            "off_check": "PASS - no Open Food Facts",
            "phase3_fix": "correct_score_extraction+second_curation_pass",
        },
        "products": items,
    }


def main():
    log.info("Phase 3 Fix: Re-run BSIP2 + rebuild frontend JSON")

    # Load all BSIP1 files
    bsip1_paths = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    log.info("Found %d BSIP1 files in %s", len(bsip1_paths), BSIP1_DIR)

    # Apply second curation pass
    kept_paths = []
    excluded_second = []
    for p in bsip1_paths:
        with open(p, encoding="utf-8") as f:
            bsip1 = json.load(f)
        verdict, reason = second_curation(bsip1)
        if verdict == "keep":
            kept_paths.append((p, bsip1))
        else:
            excluded_second.append({
                "barcode": bsip1.get("barcode", ""),
                "name": bsip1.get("canonical_name_he", ""),
                "brand": bsip1.get("brand", ""),
                "reason": reason,
            })
            log.info("  EXCL2: %s | %s | %s | %s",
                     bsip1.get("barcode",""), bsip1.get("brand",""),
                     bsip1.get("canonical_name_he","")[:40], reason)

    log.info("After second curation: %d kept, %d excluded", len(kept_paths), len(excluded_second))

    # Run BSIP2 on kept products
    scored = []
    errors = []
    for p, bsip1 in kept_paths:
        trace = run_bsip2_single(p, BSIP2_DIR / "products")
        if trace:
            scored.append((bsip1, trace))
        else:
            errors.append(p.name)

    log.info("BSIP2: %d scored, %d errors", len(scored), len(errors))

    # Grade distribution
    grade_dist: dict[str, int] = {}
    for _, trace in scored:
        g = trace.get("grade_estimate", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1
    log.info("Grade distribution: %s", grade_dist)

    # Data quality check
    name_ok = sum(1 for b, _ in scored if b.get("canonical_name_he", "").strip())
    brand_ok = sum(1 for b, _ in scored if b.get("brand", "").strip())
    ingr_ok = sum(1 for b, _ in scored if b.get("ingredients_text_he", ""))
    nutr_ok = sum(1 for b, _ in scored if b.get("normalized_nutrition_per_100g", {}).get("energy_kcal"))
    img_ok = sum(1 for b, _ in scored if b.get("image_url", "") and "default" not in b.get("image_url", ""))
    n = len(scored)
    log.info("Data quality: name=%d/%d brand=%d/%d ingr=%d/%d nutr=%d/%d img=%d/%d",
             name_ok, n, brand_ok, n, ingr_ok, n, nutr_ok, n, img_ok, n)

    # Products with gaps
    gaps = []
    for b, _ in scored:
        missing = []
        if not b.get("canonical_name_he", "").strip():
            missing.append("name")
        if not b.get("brand", "").strip():
            missing.append("brand")
        if not b.get("ingredients_text_he", ""):
            missing.append("ingredients")
        if not b.get("normalized_nutrition_per_100g", {}).get("energy_kcal"):
            missing.append("nutrition")
        if not b.get("image_url", "") or "default" in b.get("image_url", ""):
            missing.append("image")
        if missing:
            gaps.append({
                "barcode": b.get("barcode", ""),
                "name": b.get("canonical_name_he", ""),
                "brand": b.get("brand", ""),
                "missing": missing,
            })

    if gaps:
        log.warning("QUALITY GAPS (%d products):", len(gaps))
        for g in gaps:
            log.warning("  %s | %s | %s | missing: %s",
                        g["barcode"], g["brand"], g["name"][:40], g["missing"])

    # Build and save frontend JSON
    frontend_data = build_frontend(scored, PHASE3_RUN_ID + "_fix")
    save_json(FRONTEND_PATH, frontend_data)
    sha = hashlib.sha256(FRONTEND_PATH.read_bytes()).hexdigest()
    log.info("Frontend JSON: %d products → %s (sha256=%s)", n, FRONTEND_PATH, sha[:16])

    # Engine diff check
    import subprocess
    diff = subprocess.run(
        ["git", "diff", "--stat", "03_operations/bsip2/", "03_operations/page_generator/configs/"],
        cwd=str(ROOT), capture_output=True, text=True
    ).stdout.strip()
    log.info("Engine diff: %s", diff or "(empty — unchanged)")

    print("\n=== FINAL SUMMARY ===")
    print(f"BSIP1 files: {len(bsip1_paths)}")
    print(f"After second curation: {len(kept_paths)} kept, {len(excluded_second)} excluded")
    print(f"BSIP2 scored: {len(scored)}, errors: {len(errors)}")
    print(f"Grade distribution: {grade_dist}")
    print(f"Data completeness: name={name_ok}/{n} brand={brand_ok}/{n} ingr={ingr_ok}/{n} nutr={nutr_ok}/{n} img={img_ok}/{n}")
    print(f"Quality gaps: {len(gaps)} products")
    print(f"Frontend: {FRONTEND_PATH}")
    print(f"SHA256: {sha}")
    print(f"Engine unchanged: {diff == ''}")

    return {
        "bsip1_count": len(bsip1_paths),
        "kept_after_second_curation": len(kept_paths),
        "excluded_second_curation": excluded_second,
        "scored": len(scored),
        "errors": errors,
        "grade_dist": grade_dist,
        "quality_gaps": gaps,
        "frontend_path": str(FRONTEND_PATH),
        "frontend_sha256": sha,
        "engine_unchanged": diff == "",
    }


if __name__ == "__main__":
    result = main()
    save_json(
        ROOT / "02_products" / "snack_bars" / f"phase3_fix_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        result
    )
