"""
task378_bread_sugar_reparse.py — TASK-378 Phase 1: Bread Sugar Re-Parse

STAGING ONLY — does NOT promote, deploy, or modify published scores.

ROOT CAUSE (confirmed):
  The bread BSIP0 scraper (shufersal_probe_v3.py, May 2026) used a
  NUTR_LABEL_MAP dict with "פחמימות": "carbs" before "סוכרים": "sugar".
  On Shufersal, the "of which sugars" sub-row label is
  "סוכרים מתוך פחמימות" — which contains "פחמימות" as a substring.
  The break-on-first-match loop fired "פחמימות" (carbs) instead of
  "סוכרים" (sugar) → sugar value was LOST, carbs was briefly
  overwritten then corrected by the real carbs row.
  Result: 30/31 curated bread products have sugars_g = null.
  The engine treats null sugar as sugar=0 → free perfect glycemic score.

  The SHARED parser (bsip0_nutrition.py classify_nutr_label) already
  handles this correctly (sugar check before carbs check, confirmed in tests).
  The fix is to re-scrape the 30 affected products using the shared parser.

THIS SCRIPT:
1. Re-fetches each product page from Shufersal using the shared parser
2. Extracts actual sugars_g from the live page
3. Builds an in-memory sugar_patch dict: barcode → sugars_g
4. Runs BSIP2 re-scoring in staging with the patched sugar values
5. Emits a per-product comparison table: current vs staged score/grade
6. Does NOT write to BSIP1 files, does NOT promote, does NOT touch website

OUTPUTS (staging only):
  C:/Bari/02_products/bread/staging/run_378_sugar_patch.json
  C:/Bari/02_products/bread/staging/run_378_staging_scores.json

Run:  python task378_bread_sugar_reparse.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import hashlib
import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path("C:/Bari")
STAGING_DIR = ROOT / "02_products/bread/staging"
STAGING_DIR.mkdir(parents=True, exist_ok=True)

BSIP0_RAW = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
BSIP1_DIR = ROOT / "03_operations/bsip1/run_bread_conform_001/output"
RUN_RECORD = ROOT / "02_products/bread/bsip2_outputs/run_bread_conform_001/run_record.json"
BSIP2_SRC = ROOT / "03_operations/bsip2/proto_v0/src"

SRC_FLAGS = {
    "BARI_RECAL_P0":                   "on",
    "BARI_SHELF_RELATIVE_V1":          "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1":   "off",
    "BARI_FAT_TECH_V1":                "on",
    "BARI_GRAD_SODIUM_V1":             "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1":  "off",
    "BARI_REDLABEL_V1":                "off",
    "BARI_SODIUM_CEREAL":              "off",
    # TASK-250 confidence reduction - match the published run state
    "BARI_TASK250_CONF":               "off",
}

# Apply flags before engine import
for k, v in SRC_FLAGS.items():
    os.environ[k] = v

sys.path.insert(0, str(BSIP2_SRC))

# ── Shufersal fetch helpers ───────────────────────────────────────────────────
BASE = "https://www.shufersal.co.il"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}
FETCH_DELAY = 1.2

sys.path.insert(0, str(ROOT / "03_operations/bsip0/scrape/_shared"))
from bsip0_nutrition import (    # noqa: E402
    extract_nutrition_raw,
    parse_nutrition_rows,
    classify_nutr_label,
)


def _get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def fetch_sugar_for_barcode(barcode: str) -> dict:
    """Fetch the Shufersal PDP for a barcode and extract sugars_g via the shared parser.

    Returns dict with keys: barcode, sugar_raw, sugars_g, source_url, fetch_status,
    fetch_note, panel_html_snippet.
    """
    url = f"{BASE}/online/he/p/P_{barcode.upper()}"
    r = _get(url)
    if not r or r.status_code != 200:
        return {
            "barcode": barcode, "sugar_raw": None, "sugars_g": None,
            "source_url": url, "fetch_status": "failed",
            "fetch_note": f"HTTP {r.status_code if r else 'timeout'}",
            "panel_html_snippet": "",
        }

    soup = BeautifulSoup(r.text, "html.parser")

    # Use the shared shared parser — the FIXED path
    raw = extract_nutrition_raw(soup)
    rows = raw["rows"]
    parsed = parse_nutrition_rows(rows)

    sugar_raw = parsed.get("sugar")
    sugars_g = None
    if sugar_raw is not None:
        try:
            # Parse value (handles "פחות מ 0.5")
            num_match = re.search(r"(\d+(?:[.,]\d+)?)", str(sugar_raw).replace(",", "."))
            if num_match:
                sugars_g = float(num_match.group(1))
        except (ValueError, TypeError):
            pass

    # HTML snippet for audit
    nutr_divs = soup.find_all("div", class_="nutritionList")
    html_snippet = str(nutr_divs[0])[:800] if nutr_divs else ""

    # Find what label text appeared for sugar (for audit)
    sugar_label_found = None
    for row in rows:
        field = classify_nutr_label(row.get("label", ""))
        if field == "sugar":
            sugar_label_found = row.get("label")
            break

    return {
        "barcode": barcode,
        "sugar_raw": sugar_raw,
        "sugars_g": sugars_g,
        "source_url": r.url,
        "fetch_status": "ok" if sugar_raw is not None else "no_sugar_row",
        "fetch_note": f"sugar label='{sugar_label_found}'" if sugar_label_found else "no sugar row in panel",
        "panel_html_snippet": html_snippet,
        "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
        "selection_basis": raw.get("selection", {}).get("selected_basis", ""),
    }


# ── Load published run data ───────────────────────────────────────────────────
def load_run_record() -> dict:
    with open(RUN_RECORD, encoding="utf-8") as f:
        return json.load(f)


def load_bsip1(barcode: str) -> dict | None:
    """Load the BSIP1 file for a barcode."""
    # Files are named bsip1_{barcode}.json
    path = BSIP1_DIR / f"bsip1_{barcode}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── BSIP2 staging re-score ────────────────────────────────────────────────────
def rescore_with_sugar(bsip1: dict, sugars_g: float | None) -> dict:
    """Re-run BSIP2 scoring with the patched sugars_g value.

    Creates a deep copy of the BSIP1 product, injects sugars_g, runs the
    engine in staging, and returns the result dict with score/grade.
    Returns None if engine fails.
    """
    import copy
    import importlib

    # Fresh import so flags are current
    for mod_name in ["score_engine", "signal_extractor", "nova_proxy", "trace_writer",
                      "router_v2", "evaluation_scope", "input_loader", "constants",
                      "structural_classifier", "bakery_semantics", "score_synthesis",
                      "interpretation_confidence", "failure_taxonomy", "graceful_degradation"]:
        if mod_name in sys.modules:
            importlib.reload(sys.modules[mod_name])

    from input_loader import validate_product
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product, compute_confidence
    from trace_writer import assemble_trace
    from bakery_semantics import run_bakery_semantics
    from structural_classifier import classify_structural_class
    from score_synthesis import run_synthesis
    from interpretation_confidence import compute_interpretation_confidence, apply_confidence_ceiling
    from failure_taxonomy import classify_failures, summarize_failures
    from graceful_degradation import determine_degradation_level
    from constants import score_to_grade

    product = copy.deepcopy(bsip1)
    # Inject the new sugar value
    product["normalized_nutrition_per_100g"]["sugars_g"] = sugars_g

    try:
        load_errors = validate_product(product)
        product["_load_errors"] = load_errors

        prod = {k: v for k, v in product.items() if not k.startswith("_")}

        signals = extract_signals(prod)
        cat_result = classify_category(prod)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(prod, l3)
        eval_result = assign_evaluation_scope(prod, cat_result["category"])
        score_result = score_product(prod, signals, cat_result, nova_result, eval_result)

        base_conf = compute_confidence(prod, signals, cat_result, nova_result)
        interp_conf = compute_interpretation_confidence(base_conf, cat_result, prod, signals)
        score_result = apply_confidence_ceiling(score_result, interp_conf)

        bakery_result = run_bakery_semantics(prod, cat_result.get("category"), l3)
        trace = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
        trace["bakery_semantics"] = bakery_result
        trace["structural_class"] = classify_structural_class(trace, bakery_result)
        synth_result = run_synthesis(trace)

        final_score = synth_result.get("synthesis_score") or score_result.get("final_score_estimate")
        final_grade = score_to_grade(final_score) if final_score is not None else None

        return {
            "score": round(final_score, 1) if final_score is not None else None,
            "grade": final_grade,
            "glycemic_quality": trace.get("dimension_scores", {}).get("glycemic_quality"),
            "glycemic_note": trace.get("dimension_notes", {}).get("glycemic_quality"),
            "sugar_penalty_applied": sugars_g is not None and sugars_g > 0,
            "caps_fired": [c["rule"] for c in score_result.get("caps_considered", []) if c.get("fired")],
        }
    except Exception as e:
        return {"error": str(e), "score": None, "grade": None}


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("TASK-378 Phase 1: Bread Sugar Re-Parse (STAGING)")
    print("=" * 70)
    print(f"  Run ID: task378_bread_sugar_reparse")
    print(f"  Date: {datetime.date.today().isoformat()}")
    print(f"  Staging only — nothing promoted, 0 published scores changed")
    print()

    run_record = load_run_record()
    products = run_record["results"]
    print(f"Published run: {run_record['run_id']} | {len(products)} curated products")
    print()

    # ── Step 1: Re-fetch sugar for each product ────────────────────────────────
    print("Step 1: Fetch sugar values from Shufersal (using shared parser)")
    print("-" * 70)

    sugar_patches = []
    fetch_results = []

    for i, p in enumerate(products):
        barcode = p["barcode"]
        name = p["name"][:35]
        current_score = p["score"]
        current_grade = p["grade"]

        # Skip the one product that already has sugar (challah 1902325, sugar=4)
        if barcode == "1902325":
            bsip1 = load_bsip1(barcode)
            existing_sugar = bsip1["normalized_nutrition_per_100g"]["sugars_g"] if bsip1 else None
            fetch_results.append({
                "barcode": barcode, "name": name,
                "sugar_raw": str(existing_sugar) if existing_sugar is not None else "4",
                "sugars_g": existing_sugar or 4.0,
                "fetch_status": "already_present",
                "fetch_note": "sugar=4.0 already in BSIP1 (challah, was correctly parsed)",
                "source_url": "",
                "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
                "selection_basis": "per_100g",
            })
            print(f"  [{i+1:02d}/{len(products)}] {name:<36} SKIP (sugar=4.0 already captured)")
            continue

        print(f"  [{i+1:02d}/{len(products)}] {name:<36} fetching...", end="", flush=True)
        result = fetch_sugar_for_barcode(barcode)
        result["name"] = name
        result["current_score"] = current_score
        result["current_grade"] = current_grade
        fetch_results.append(result)

        status = result["fetch_status"]
        sugar_val = result["sugars_g"]
        note = result.get("fetch_note", "")
        print(f" [{status}] sugars_g={sugar_val} | {note}")

        if status == "ok" and sugar_val is not None:
            sugar_patches.append({"barcode": barcode, "sugars_g": sugar_val, "sugar_raw": result["sugar_raw"]})

        if i < len(products) - 1:
            time.sleep(FETCH_DELAY)

    print()
    print(f"Fetched: {len(fetch_results)} | Sugar recovered: {len(sugar_patches)}")
    print()

    # ── Step 2: Build sugar patch dict ────────────────────────────────────────
    sugar_by_barcode: dict[str, float | None] = {}
    for r in fetch_results:
        sugar_by_barcode[r["barcode"]] = r.get("sugars_g")
    # Always include challah
    sugar_by_barcode["1902325"] = 4.0

    # Save patch file
    patch_file = STAGING_DIR / "run_378_sugar_patch.json"
    patch_record = {
        "run_id": "task378_bread_sugar_reparse",
        "task": "TASK-378",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "staging_only": True,
        "promoted": False,
        "published_run_id": run_record["run_id"],
        "fetch_results": fetch_results,
        "sugar_by_barcode": {k: v for k, v in sugar_by_barcode.items()},
        "recovery_count": sum(1 for v in sugar_by_barcode.values() if v is not None),
        "total_products": len(products),
    }
    patch_file.write_text(json.dumps(patch_record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Sugar patch saved: {patch_file}")
    print()

    # ── Step 3: Staging re-score ───────────────────────────────────────────────
    print("Step 2: Staging re-score with real sugar values")
    print("-" * 70)

    comparison_rows = []
    grade_movers = []

    for p in products:
        barcode = p["barcode"]
        name = p["name"]
        current_score = p["score"]
        current_grade = p["grade"]
        sugars_g = sugar_by_barcode.get(barcode)

        bsip1 = load_bsip1(barcode)
        if bsip1 is None:
            comparison_rows.append({
                "barcode": barcode, "name": name,
                "current_score": current_score, "current_grade": current_grade,
                "sugars_g": sugars_g,
                "staged_score": None, "staged_grade": None,
                "score_delta": None, "grade_moves": False,
                "note": "BSIP1 file not found",
            })
            continue

        if sugars_g is None:
            # Cannot re-score without sugar (fetch failed / panel absent)
            comparison_rows.append({
                "barcode": barcode, "name": name,
                "current_score": current_score, "current_grade": current_grade,
                "sugars_g": None,
                "staged_score": None, "staged_grade": None,
                "score_delta": None, "grade_moves": False,
                "note": "sugar fetch failed — not re-scored",
            })
            continue

        result = rescore_with_sugar(bsip1, sugars_g)
        staged_score = result.get("score")
        staged_grade = result.get("grade")
        score_delta = round(staged_score - current_score, 1) if staged_score is not None and current_score not in (None, 50) else None
        grade_moves = (staged_grade != current_grade) if (staged_grade and current_grade and current_grade != "insufficient_data") else False

        row = {
            "barcode": barcode, "name": name,
            "current_score": current_score, "current_grade": current_grade,
            "sugars_g": sugars_g,
            "staged_score": staged_score, "staged_grade": staged_grade,
            "score_delta": score_delta, "grade_moves": grade_moves,
            "glycemic_quality_staged": result.get("glycemic_quality"),
            "caps_fired": result.get("caps_fired", []),
            "note": result.get("error", ""),
        }
        comparison_rows.append(row)

        if grade_moves:
            grade_movers.append(row)

        arrow = "→" if not grade_moves else "★"
        delta_str = f"{score_delta:+.1f}" if score_delta is not None else "N/A"
        print(f"  {barcode:<16} {name:<36} {current_score}/{current_grade} → {staged_score}/{staged_grade} (Δ{delta_str}) sugar={sugars_g}g {arrow}")

    print()
    print("=" * 70)
    print("STAGING RESULT SUMMARY")
    print("=" * 70)

    rescored = [r for r in comparison_rows if r["staged_score"] is not None]
    not_rescored = [r for r in comparison_rows if r["staged_score"] is None]

    print(f"Products in corpus:          {len(products)}")
    print(f"Sugar recovered & re-scored: {len(rescored)}")
    print(f"Sugar fetch failed:          {len(not_rescored)}")
    print(f"Grade movers:                {len(grade_movers)}")
    print()

    if grade_movers:
        print("GRADE MOVERS:")
        for r in grade_movers:
            print(f"  {r['barcode']:<16} {r['name']:<36} {r['current_grade']} → {r['staged_grade']} (Δ{r['score_delta']:+.1f}) sugar={r['sugars_g']}g")

    print()
    print("0 published scores changed. Grade movers listed above require owner approval.")
    print()

    # Save staging scores
    staging_record = {
        "run_id": "task378_bread_sugar_reparse",
        "task": "TASK-378",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "staging_only": True,
        "promoted": False,
        "published_run_id": run_record["run_id"],
        "engine_flags": SRC_FLAGS,
        "summary": {
            "total_products": len(products),
            "sugar_recovered": len(rescored),
            "sugar_fetch_failed": len(not_rescored),
            "grade_movers": len(grade_movers),
            "published_scores_changed": 0,
        },
        "comparison": comparison_rows,
        "grade_movers": grade_movers,
    }

    staging_file = STAGING_DIR / "run_378_staging_scores.json"
    staging_file.write_text(json.dumps(staging_record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Staging scores saved: {staging_file}")

    return staging_record


if __name__ == "__main__":
    main()
