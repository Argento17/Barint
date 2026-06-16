"""
pipeline_e2e.py — Generic EXECUTABLE end-to-end Spine pipeline (TASK-259 / P41 + P42).

THROWAWAY: runs on synthetic raw HTML fixtures only. Not a live category. Not yogurts.
Not cereals. All output goes to _e2e_out/ (scratch).

Chains (updated for P42 — copy stages added after generate_page):
  Stage 0: extract_bsip0        — parse raw HTML fixtures → BSIP0 JSON per product.
                                  Uses replay_parse._parse_product_from_html (the same
                                  offline BSIP0 parser replay_parse.py uses). No network.
                                  OFF ban: never falls back to Open Food Facts; missing
                                  field stays null.
  Stage 0.5: build_bsip1        — convert BSIP0 JSON → BSIP1 records (the shape the
                                  score stage reads). Calls bsip0_nutrition.parse_nutrition_numeric
                                  (canonical numeric path; single source of truth). Written
                                  as a minimal inline builder (bsip0_to_bsip1_builder) that
                                  is documented in the seam report below.
  Stage 1: [REMOVED]            — fixture_ingest is gone. The chain now starts at raw HTML.
  Stage 2: score_products       — call score_engine.score_product() for each BSIP1
                                  record; write bsip2_trace.json per product.
  Stage 3: generate_page        — call generate_page.py via subprocess with a config
                                  that points at the scratch dirs; produce a page JSON.
  Stage 4: gate_page            — call run_gates.py via subprocess; produce a gate
                                  report. Exit non-zero on hard failures.
  Stage 5: build_copy_inputs    — DETERMINISTIC. Reads page JSON + BSIP2 traces; writes
                                  fact_sheets.json (one fact sheet per product). Only
                                  verifiable facts from the trace. No copy written here.
  Stage 6: author_copy          — THE SEAM. Reads fact_sheets.json; writes authored.json.
                                  For this throwaway run: baseline_placeholder author
                                  (deterministic, rule-based). Production: swap in the
                                  Content Agent (LLM) — reads the same fact_sheets.json,
                                  writes the same authored.json schema; no other change.
                                  See: page_generator/copy/authoring_contract.json.
  Stage 7: merge_copy_and_gate  — DETERMINISTIC. Merges authored strings into the page
                                  JSON (replacing PENDING_COPY), runs readability on every
                                  string, runs the full gate suite including G6 COPY-SAFETY.
                                  Final output: e2e_page_throwaway_final.json (0 PENDING_COPY).

MILK-DEPTH SCHEMA ASSESSMENT (P43 / TASK-262 — schema v3):
  schema_carries_milk_depth = TRUE (as of P43).

  The canonical v3 schema (page_output_schema_v3.json) adds the 4 per-product
  content fields from the milk-comparison.json gold standard:
    1. consumerTakeaway         — AUTHORED. One-line plain summary (product level).
    2. consumerExplanation      — AUTHORED. expansion sub-object:
                                  whyRated, good[], watchOut[], context, takeaway.
    3. bariInterpretation[]     — DETERMINISTIC+AUTHORED. Per-dimension array:
                                  key/label/score/strength (trace) + interpretation (authored).
    4. bestUseCases[]           — DETERMINISTIC when rule applies; AUTHORED otherwise.
  Page-level:
    5. story_headline / story_teaser / philosophy_note — PRESENT in _meta.page_copy
       (additionalProperties:true — unchanged from v2).

  PIPELINE WIRING (v3):
    - generate_page.py (v1.1.0, SCHEMA_V3): emits bariInterpretation with real
      dimension scores from trace; PENDING_COPY for all authored fields.
    - build_copy_inputs.py: carries bari_interpretation_inputs (key/label/score/strength)
      + best_use_cases_pending flag in each fact sheet.
    - author_copy.py (baseline_placeholder): fills all v3 authored fields. Law-abiding.
    - merge_copy.py: merges consumerTakeaway, consumerExplanation, bariInterpretation
      interpretations (preserving deterministic key/label/score/strength), bestUseCases.
    - run_gates.py G2: checks all 4 v3 authored fields non-PENDING when schema_version=v3.
      G6: scans v3 strings for copy-safety violations.

  P42 ASSESSMENT (historical, now superseded by P43):
    SCHEMA GAP VERDICT was: schema_carries_milk_depth = FALSE.
    That assessment was correct for canonical-v2. P43 fixes it.

Usage:
  cd 03_operations/spine
  python pipeline_e2e.py --execute            # run the full pipeline
  python pipeline_e2e.py --execute --force    # re-run even if already current
  python pipeline_e2e.py --execute --db <path>  # use a custom spine DB

Usage:
  cd 03_operations/spine
  python pipeline_e2e.py --execute            # run the full pipeline
  python pipeline_e2e.py --execute --force    # re-run even if already current
  python pipeline_e2e.py --execute --db <path>  # use a custom spine DB

BSIP0→BSIP1 Builder (minimal inline, documented):
  Located in bsip0_to_bsip1_builder() in this module. It calls:
    - parse_nutrition_numeric(raw_nutrition_dict) → canonical numeric panel
      (canonical path from bsip0_nutrition.py; same path all BSIP1 builders use)
    - Produces a BSIP1 dict matching schema_version "bsip1_v0.1" with:
      canonical_product_id, barcode, canonical_name_he, brand, source_retailers,
      normalized_nutrition_per_100g, ingredients_list, ingredients_text_he,
      allergens_contains, allergens_may_contain, confidence, conflicts_summary,
      missing_fields, inferred_fields, audit_ref, image_url, canonical_trust_level,
      nutrition_consistency_status
  Seam status: CLEAN — output keys match what score_engine/input_loader expects.

Seam-gap table (updated P41):

  SEAM 0 (raw HTML → extract_bsip0):
    Upstream input: raw HTML files in _fixtures_e2e/raw/raw_*.html
    Parser: replay_parse._parse_product_from_html(html, barcode, url)
    Output: BSIP0-shaped dict with nutrition.*_raw keys, ingredients_raw, name_he,
            barcode, image_urls, extraction_confidence.
    Mismatch / gap: The parser requires BeautifulSoup (bs4) — already present in
    the project's environment (replay_parse.py uses it). No new deps introduced.
    SEAM_GAP: ingredients_raw is a raw Hebrew string (comma-separated). The builder
    splits it on comma to produce ingredients_list. This is the same approach used
    by convert_bsip0_to_bsip1.py (hummus). Clean for our synthetic fixtures.

  SEAM 0.5 (extract_bsip0 → build_bsip1):
    Upstream output: BSIP0 JSON files in _e2e_out/bsip0/bsip0_*.json
    Downstream input: bsip0_to_bsip1_builder(bsip0_dict) → BSIP1 JSON
    Mismatch / gap: CLEAN. parse_nutrition_numeric output keys match the
    normalized_nutrition_per_100g schema the score stage reads exactly.
    Sodium: parse_sodium_mg correctly handles the "420 מג" format (appended
    by parse_nutrition_rows when div.name="מג"), so sodium_mg=420 (not 420000).

  SEAM 1 (build_bsip1 → score_products):
    Upstream output: BSIP1-shaped JSON files in _e2e_out/bsip1/ (bsip1_*.json).
    Downstream input: score_engine.score_product(product, signals, cat_result,
                      nova_result, eval_result).
    Mismatch / gap: The scoring pipeline (batch_run_yogurt_001 pattern) calls
    5 modules in sequence: extract_signals → classify_category → infer_nova →
    assign_evaluation_scope → score_product. None of these are CLI-callable; they
    must be imported. This stage does import them directly — the seam is CLEAN when
    the cwd is the score_engine's src/ directory (sys.path injection required).
    SEAM_GAP: score_engine.py imports 'constants', 'signal_extractor', etc. from
    the same proto_v0/src/ directory. Running from spine/ requires sys.path mangling.
    Documented in SEAM_GAP_1 below.

  SEAM 2 (score_products → generate_page):
    Upstream output: _e2e_out/bsip2_traces/products/<product_id>/bsip2_trace.json
    Downstream input: generate_page.py --config e2e_page_config.json
    Mismatch / gap: generate_page.py expects:
      - corpus_dirs: list of dirs containing bsip1_*.json files (with 'barcode' key)
      - run_products_dir: dir containing subdirs each with bsip2_trace.json
      - bsip2_trace.json must have input_reference.barcode
      - bsip1_*.json must have canonical_name_he (Hebrew)
    All of these are satisfied by stages 0, 0.5, 2. The seam is CLEAN once the config
    is correctly wired. See SEAM_GAP_2 note about Hebrew name requirement.

GUARDS:
  - THROWAWAY ONLY: no live category, no yogurts/cereals, no consumer page.
  - Does NOT modify spine_yogurts.py or any live artifact.
  - OFF ban (TASK-238): no Open Food Facts fallback anywhere. Raw HTML fixtures
    contain no OFF data. Builder does not call any OFF source. A field that doesn't
    parse from raw HTML stays null ("data could not be retrieved").
  - Imports runner.py + spine_db.py from the same directory; no new dependencies.
  - bs4 (BeautifulSoup) is an existing project dep (used by replay_parse.py).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (all absolute; scratch dirs only)
# ---------------------------------------------------------------------------

SPINE_DIR = Path(__file__).resolve().parent
REPO = SPINE_DIR.parents[1]

RAW_FIXTURES_DIR = SPINE_DIR / "_fixtures_e2e" / "raw"
FIXTURES_DIR = SPINE_DIR / "_fixtures_e2e"
E2E_OUT = SPINE_DIR / "_e2e_out"
BSIP0_OUT = E2E_OUT / "bsip0"
BSIP1_OUT = E2E_OUT / "bsip1"
BSIP2_TRACES_ROOT = E2E_OUT / "bsip2_traces"
BSIP2_PRODUCTS_DIR = BSIP2_TRACES_ROOT / "products"
PAGE_OUT_DIR = E2E_OUT / "page"
PAGE_JSON = PAGE_OUT_DIR / "e2e_page_throwaway.json"
PAGE_CONFIG = E2E_OUT / "e2e_page_config.json"
SCHEMA_V2 = REPO / "03_operations" / "page_generator" / "contract" / "page_output_schema_v2.json"
SCHEMA_V3 = REPO / "03_operations" / "page_generator" / "contract" / "page_output_schema_v3.json"

SCORE_ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
GENERATE_PAGE_PY = REPO / "03_operations" / "page_generator" / "generate_page.py"
RUN_GATES_PY = REPO / "03_operations" / "page_generator" / "gates" / "run_gates.py"

# Shared BSIP0 parser paths
RAW_STORE_DIR = REPO / "03_operations" / "bsip0" / "raw_store"
SHARED_DIR = REPO / "03_operations" / "bsip0" / "scrape" / "_shared"

# ---------------------------------------------------------------------------
# Copy engine paths (P42)
# ---------------------------------------------------------------------------
COPY_ENGINE_DIR = REPO / "03_operations" / "page_generator" / "copy"
BUILD_COPY_INPUTS_PY = COPY_ENGINE_DIR / "build_copy_inputs.py"
AUTHOR_COPY_PY = COPY_ENGINE_DIR / "author_copy.py"
MERGE_COPY_PY = COPY_ENGINE_DIR / "merge_copy.py"

COPY_OUT_DIR = E2E_OUT / "copy"
FACT_SHEETS_JSON = COPY_OUT_DIR / "fact_sheets.json"
AUTHORED_JSON = COPY_OUT_DIR / "authored.json"
# Separate config for copy stage — build_copy_inputs expects run_products_dir as string
COPY_CONFIG_JSON = COPY_OUT_DIR / "copy_config.json"
# Final merged page (0 PENDING_COPY)
FINAL_PAGE_JSON = PAGE_OUT_DIR / "e2e_page_throwaway_final.json"
# Merged gate report
FINAL_GATE_REPORT = PAGE_OUT_DIR / "e2e_page_throwaway_final_gates_report.md"

# ---------------------------------------------------------------------------
# SEAM_GAP_1: score_engine import path shim
# The score_engine and all its imports live in proto_v0/src/. They use relative
# imports (e.g. `from constants import ...`). We inject the src/ dir onto sys.path
# before importing. This is the only cross-directory path manipulation needed.
# ---------------------------------------------------------------------------

if str(SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(SCORE_ENGINE_SRC))

# ---------------------------------------------------------------------------
# BSIP0 → BSIP1 inline builder
# ---------------------------------------------------------------------------

def bsip0_to_bsip1_builder(bsip0: dict) -> dict:
    """Convert a BSIP0 product dict to a BSIP1 record.

    Minimal inline builder for the e2e pipeline. Documented here (not in a
    separate file) because this is a pipeline proof, not a production builder.

    OFF BAN GUARD: does not call any external source. A field that doesn't
    parse from the BSIP0 raw dict stays null. No Open Food Facts, no fallback.

    Input:  BSIP0 dict as produced by replay_parse._parse_product_from_html:
              - name_he, barcode, brand, image_urls
              - nutrition.*_raw keys (energy_kcal_raw, fat_raw, carbs_raw,
                protein_raw, sodium_raw, sugar_raw, fiber_raw, saturated_fat_raw)
              - ingredients_raw (raw Hebrew comma-separated string)
              - extraction_confidence

    Output: BSIP1 dict matching schema_version "bsip1_v0.1" — the exact shape
            that input_loader.load_product / score_engine expects.

    Nutrition conversion: uses bsip0_nutrition.parse_nutrition_numeric
    (canonical numeric path shared by all BSIP1 builders).

    Seam match with score stage: CLEAN. The normalized_nutrition_per_100g keys
    (energy_kcal, fat_g, fat_saturated_g, fat_trans_g, sodium_mg,
    carbohydrates_g, sugars_g, dietary_fiber_g, protein_g) match exactly.
    """
    # Lazy import after sys.path injection (SHARED_DIR must be on path)
    if str(SHARED_DIR) not in sys.path:
        sys.path.insert(0, str(SHARED_DIR))
    from bsip0_nutrition import parse_nutrition_numeric

    barcode = str(bsip0.get("barcode") or "").strip()
    name_he = bsip0.get("name_he") or ""
    brand = bsip0.get("brand") or None
    image_urls = bsip0.get("image_urls") or []
    image_url = image_urls[0] if image_urls else None
    extraction_confidence = bsip0.get("extraction_confidence", "low")

    # Nutrition: raw string dict → canonical numeric panel
    raw_nutrition = bsip0.get("nutrition") or {}
    numeric_panel = parse_nutrition_numeric(raw_nutrition)
    integrity_flags = numeric_panel.pop("_integrity", [])

    # Ingredients: raw string → list (split on comma, strip whitespace)
    ingr_raw = (bsip0.get("ingredients_raw") or "").strip()
    if ingr_raw:
        ingr_list = [x.strip() for x in ingr_raw.split(",") if x.strip()]
    else:
        ingr_list = []

    # Confidence signals
    has_nutr = bool(
        numeric_panel.get("energy_kcal") is not None
        and numeric_panel.get("protein_g") is not None
    )
    has_ingr = bool(ingr_raw)
    trust_level = "high" if (has_nutr and has_ingr) else ("medium" if has_nutr else "low")

    # Missing fields — note only fields that are genuinely null
    missing: list[str] = []
    if not has_nutr:
        missing.append("normalized_nutrition_per_100g")
    if not has_ingr:
        missing.append("ingredients_raw")
    if not name_he:
        missing.append("canonical_name_he")

    # nutrition_consistency_status
    if integrity_flags:
        nutr_status = "integrity_flags"
    elif has_nutr:
        nutr_status = "ok"
    else:
        nutr_status = "incomplete"

    # canonical_product_id: deterministic from barcode
    pid = f"e2e_raw_{barcode}" if barcode else "e2e_raw_unknown"

    return {
        "schema_version": "bsip1_v0.1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": name_he,
        "brand": brand,
        "source_retailers": [bsip0.get("retailer_id", "e2e_raw_fixture")],
        "normalized_nutrition_per_100g": {
            k: v for k, v in numeric_panel.items() if v is not None
        },
        "ingredients_list": ingr_list,
        "ingredients_text_he": ingr_raw if ingr_raw else None,
        "allergens_contains": [],
        "allergens_may_contain": [],
        "confidence": extraction_confidence,
        "conflicts_summary": [],
        "missing_fields": missing,
        "inferred_fields": [],
        "audit_ref": "e2e_p41_raw_pipeline",
        "image_url": image_url,
        "canonical_trust_level": trust_level,
        "nutrition_consistency_status": nutr_status,
        "_bsip0_source": {
            "retailer_id": bsip0.get("retailer_id", ""),
            "source_url": bsip0.get("source_url", ""),
            "scraped_at": bsip0.get("scraped_at", ""),
            "extraction_method": bsip0.get("extraction_method", ""),
            "extraction_confidence": extraction_confidence,
            "integrity_flags": integrity_flags,
        },
        "_builder": "bsip0_to_bsip1_builder (inline, pipeline_e2e.py, TASK-259/P41)",
        "_off_data_used": False,  # OFF ban: explicitly false; no OFF source called
        "bsip1_converted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------------------
# Stage functions
# ---------------------------------------------------------------------------

def stage_extract_bsip0() -> None:
    """
    Stage 0: extract_bsip0
    Parse raw HTML fixtures from _fixtures_e2e/raw/ using
    replay_parse._parse_product_from_html. Write one BSIP0 JSON per file
    to _e2e_out/bsip0/.

    OFF BAN (TASK-238): parser reads only from the HTML file itself.
    No network access. No Open Food Facts. Missing field = null.
    """
    # Import the parser (requires bs4 — existing dep)
    if str(RAW_STORE_DIR) not in sys.path:
        sys.path.insert(0, str(RAW_STORE_DIR))
    if str(SHARED_DIR) not in sys.path:
        sys.path.insert(0, str(SHARED_DIR))
    from replay_parse import _parse_product_from_html

    BSIP0_OUT.mkdir(parents=True, exist_ok=True)
    raw_files = sorted(RAW_FIXTURES_DIR.glob("raw_*.html"))
    if not raw_files:
        raise RuntimeError(f"No raw_*.html fixtures found in {RAW_FIXTURES_DIR}")

    parsed = 0
    for html_path in raw_files:
        # Derive barcode hint from filename (raw_e2e_001.html → stem = raw_e2e_001)
        # The real barcode comes from the LD+JSON gtin13 field inside the HTML
        code_hint = html_path.stem  # passed as fallback if gtin13 missing
        html = html_path.read_text(encoding="utf-8")
        bsip0 = _parse_product_from_html(html, code_hint, f"file://{html_path}")
        if bsip0 is None:
            raise RuntimeError(f"Parser returned None for {html_path.name}")

        # OFF ban: verify no OFF marker leaked in
        bsip0_str = json.dumps(bsip0, ensure_ascii=False)
        for off_marker in ("openfoodfacts", "open_food_facts", "off.net", "world.off"):
            if off_marker in bsip0_str.lower():
                raise RuntimeError(
                    f"OFF BAN VIOLATION: OFF marker '{off_marker}' found in BSIP0 output "
                    f"for {html_path.name}. Aborting — launch blocker."
                )

        barcode = bsip0.get("barcode", code_hint)
        out_path = BSIP0_OUT / f"bsip0_{barcode}.json"
        out_path.write_text(
            json.dumps(bsip0, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        parsed += 1
        confidence = bsip0.get("extraction_confidence", "?")
        print(f"  [extract_bsip0] {html_path.name} → barcode={barcode}  confidence={confidence}")

    print(f"  [extract_bsip0] Parsed {parsed} product(s) from raw HTML; BSIP0 in {BSIP0_OUT}")


def stage_build_bsip1() -> None:
    """
    Stage 0.5: build_bsip1
    Convert BSIP0 JSON files from _e2e_out/bsip0/ to BSIP1 records in
    _e2e_out/bsip1/ using bsip0_to_bsip1_builder().

    SEAM check: output normalized_nutrition_per_100g keys must match the
    schema that score_engine / input_loader.load_product reads.
    OFF ban: builder uses only parsed BSIP0 data; no external calls.
    """
    BSIP1_OUT.mkdir(parents=True, exist_ok=True)
    bsip0_files = sorted(BSIP0_OUT.glob("bsip0_*.json"))
    if not bsip0_files:
        raise RuntimeError(f"No bsip0_*.json records found in {BSIP0_OUT}")

    built = 0
    for fpath in bsip0_files:
        bsip0 = json.loads(fpath.read_text(encoding="utf-8"))
        bsip1 = bsip0_to_bsip1_builder(bsip0)

        # OFF ban: verify not in bsip1 output either
        bsip1_str = json.dumps(bsip1, ensure_ascii=False)
        for off_marker in ("openfoodfacts", "open_food_facts", "off.net"):
            if off_marker in bsip1_str.lower():
                raise RuntimeError(
                    f"OFF BAN VIOLATION: OFF marker '{off_marker}' in BSIP1 output for "
                    f"{fpath.name}. Launch blocker."
                )

        barcode = bsip1.get("barcode", fpath.stem)
        out_path = BSIP1_OUT / f"bsip1_{barcode}.json"
        out_path.write_text(
            json.dumps(bsip1, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        built += 1

        n = bsip1.get("normalized_nutrition_per_100g", {})
        protein = n.get("protein_g")
        energy = n.get("energy_kcal")
        trust = bsip1.get("canonical_trust_level", "?")
        print(
            f"  [build_bsip1] {barcode}: "
            f"protein_g={protein}  energy_kcal={energy}  trust={trust}"
        )

    print(f"  [build_bsip1] Built {built} BSIP1 record(s); output in {BSIP1_OUT}")


def stage_score_products() -> None:
    """
    Stage 2 (renumbered from P40's Stage 2): score_products
    Import score_engine and its pipeline modules from proto_v0/src/; run
    score_product() on each BSIP1 record; write bsip2_trace.json per product.

    SEAM_GAP_1 (documented): score_engine requires 4 upstream modules to produce
    the inputs it needs. None are CLI tools. We call them exactly as the batch
    runners do (import chain from batch_run_yogurt_001.py pattern).
    """
    # Lazy imports after sys.path injection
    from input_loader import load_product, validate_product
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    from trace_writer import assemble_trace

    BSIP2_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

    bsip1_files = sorted(BSIP1_OUT.glob("bsip1_*.json"))
    if not bsip1_files:
        raise RuntimeError(f"No bsip1_*.json records found in {BSIP1_OUT}")

    scored = 0
    for fpath in bsip1_files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        errors = validate_product(product)
        product["_load_errors"] = errors

        pid = product.get("canonical_product_id", fpath.stem)
        product_dir = BSIP2_PRODUCTS_DIR / pid
        product_dir.mkdir(parents=True, exist_ok=True)

        signals = extract_signals(product)
        cat_result = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = score_product(product, signals, cat_result, nova_result, eval_result)

        trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)

        trace_path = product_dir / "bsip2_trace.json"
        trace_path.write_text(
            json.dumps(trace, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        scored += 1
        fs = trace.get("final_score_estimate")
        gr = trace.get("grade_estimate")
        protein_g = (product.get("normalized_nutrition_per_100g") or {}).get("protein_g")
        print(f"  [score_products] {pid}: score={fs} grade={gr}  (protein_g={protein_g} from raw)")

    print(f"  [score_products] Scored {scored} product(s); traces in {BSIP2_PRODUCTS_DIR}")


def stage_generate_page() -> None:
    """
    Stage 3: generate_page
    Write a page config JSON pointing at the e2e scratch dirs, then call
    generate_page.py via subprocess with --no-gates (gates run in stage 4).

    SEAM_GAP_2 (documented): generate_page.py requires all displayed products to
    have a Hebrew name (canonical_name_he). Our raw HTML fixtures provide this via
    the LD+JSON name field. It also requires the bsip2_trace to have
    input_reference.barcode — trace_writer provides this. The seam is clean.
    """
    import subprocess
    PAGE_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write the page config for this e2e run
    config = {
        "_comment": "THROWAWAY e2e pipeline config — raw HTML fixture category. NOT a live page.",
        "category": "e2e_throwaway",
        "corpus_dirs": [str(BSIP1_OUT)],
        "run_products_dir": [str(BSIP2_PRODUCTS_DIR)],
        "baseline_json": None,
        "subpool_filter": None,
        "exclusions": [],
        "extension_fields": [],
        "boundary_policy": str(REPO / "01_framework" / "governance" / "grade_boundary_policy_v1.json"),
    }
    PAGE_CONFIG.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  [generate_page] Config written to {PAGE_CONFIG}")

    cmd = [
        sys.executable,
        str(GENERATE_PAGE_PY),
        "--config", str(PAGE_CONFIG),
        "--out", str(PAGE_JSON),
        "--no-gates",
        "--timestamp", "2026-06-12T00:00:00Z",
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            print(f"  [generate_page] {line}")
    if result.stderr:
        for line in result.stderr.splitlines():
            print(f"  [generate_page] {line}")
    if result.returncode != 0:
        raise RuntimeError(
            f"generate_page.py exited with code {result.returncode}"
        )
    if not PAGE_JSON.exists():
        raise RuntimeError(f"generate_page.py did not produce {PAGE_JSON}")
    data = json.loads(PAGE_JSON.read_text(encoding="utf-8"))
    product_count = len(data.get("products", []))
    print(f"  [generate_page] Page JSON written: {product_count} product(s) in {PAGE_JSON}")


def stage_gate_page() -> None:
    """
    Stage 4: gate_page
    Run run_gates.py on the generated page JSON.
    Hard failures (FAIL gates) raise RuntimeError, blocking the pipeline.
    Warnings (WARN) are logged but do not block.

    SEAM_GAP_2 continued: G3 (SCOPE) may produce WARNs when corpus records
    don't align with traces for barcodes — expected for synthetic data with
    minimal BSIP1 fields. G5 (GRADE-INTEGRITY) score-vs-trace check will
    WARN (no trace in --run), but grade-vs-score is checked locally. See gate
    report for full detail.
    """
    import subprocess
    cmd = [
        sys.executable,
        str(RUN_GATES_PY),
        str(PAGE_JSON),
        "--schema", str(SCHEMA_V3),
        "--corpus", str(BSIP1_OUT),
        "--run", str(BSIP2_PRODUCTS_DIR),
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            print(f"  [gate_page] {line}")
    if result.stderr:
        for line in result.stderr.splitlines():
            print(f"  [gate_page] {line}")

    gate_exit = result.returncode
    print(f"  [gate_page] Exit code: {gate_exit}")

    report_path = PAGE_OUT_DIR / "e2e_page_throwaway_gates_report.md"
    if gate_exit != 0:
        fail_summary = ""
        if report_path.exists():
            content = report_path.read_text(encoding="utf-8")
            fail_lines = [l for l in content.splitlines() if "FAIL" in l]
            fail_summary = "\n".join(fail_lines[:10])
        raise RuntimeError(
            f"Gate suite FAILED (exit={gate_exit}):\n{fail_summary}"
        )
    print(f"  [gate_page] Gate report: {report_path}")


# ---------------------------------------------------------------------------
# Copy stages (P42)
# ---------------------------------------------------------------------------

def stage_build_copy_inputs() -> None:
    """
    Stage 5: build_copy_inputs  (DETERMINISTIC)
    Reads the generated page JSON + BSIP2 traces; writes fact_sheets.json
    (one fact sheet per product with only verifiable facts).

    Calls build_copy_inputs.py via subprocess.

    COPY CONFIG SEAM: build_copy_inputs.py reads config["run_products_dir"]
    as a plain string (not a list). We write a copy-specific config JSON
    with the scalar form before calling the script.

    OFF ban: build_copy_inputs.py never reads OFF. Fact sheets carry only
    data from the page JSON (which itself came from the BSIP0/BSIP1 pipeline
    which has its own OFF ban). null stays null.
    """
    import subprocess
    COPY_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write a copy-specific config that build_copy_inputs.py can consume.
    # run_products_dir must be a string (single path); corpus_dirs is a list.
    copy_config = {
        "_comment": "Copy-stage config for build_copy_inputs.py (P42 e2e). THROWAWAY.",
        "category": "e2e_throwaway",
        "corpus_dirs": [str(BSIP1_OUT)],
        "run_products_dir": str(BSIP2_PRODUCTS_DIR),
        "baseline_json": None,
    }
    COPY_CONFIG_JSON.write_text(
        json.dumps(copy_config, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    cmd = [
        sys.executable,
        str(BUILD_COPY_INPUTS_PY),
        "--config", str(COPY_CONFIG_JSON),
        "--page", str(PAGE_JSON),
        "--out", str(FACT_SHEETS_JSON),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            print(f"  [build_copy_inputs] {line}")
    if result.stderr:
        for line in result.stderr.splitlines():
            print(f"  [build_copy_inputs] {line}")
    if result.returncode != 0:
        raise RuntimeError(
            f"build_copy_inputs.py exited with code {result.returncode}"
        )
    if not FACT_SHEETS_JSON.exists():
        raise RuntimeError(f"build_copy_inputs.py did not produce {FACT_SHEETS_JSON}")

    data = json.loads(FACT_SHEETS_JSON.read_text(encoding="utf-8"))
    n = len(data.get("sheets", []))
    print(f"  [build_copy_inputs] Fact sheets written: {n} product(s) → {FACT_SHEETS_JSON}")


def stage_author_copy() -> None:
    """
    Stage 6: author_copy  (THE SEAM — baseline_placeholder for this throwaway run)
    Reads fact_sheets.json; writes authored.json with Hebrew copy for every product.

    This stage is the pluggable seam: the real Content Agent (LLM) implements the
    same author(facts) -> authored_dict interface and produces milk-quality copy.
    The authoring contract is at:
      page_generator/copy/authoring_contract.json

    For this throwaway run: author_copy.py uses the BASELINE PLACEHOLDER author
    (deterministic, rule-based). author_engine = "baseline_placeholder".

    The baseline:
      - Obeys all standing editorial law (standalone lines, grade=badge only,
        sodium/fat never causal, no framework leakage, no banned phrases)
      - Does NOT reach milk-quality content depth
      - Is clearly labeled so it is never confused for final copy

    OFF ban: author_copy.py reads only the fact sheet. null stays null.
    No external data source.
    """
    import subprocess

    cmd = [
        sys.executable,
        str(AUTHOR_COPY_PY),
        "--facts", str(FACT_SHEETS_JSON),
        "--out", str(AUTHORED_JSON),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            print(f"  [author_copy] {line}")
    if result.stderr:
        for line in result.stderr.splitlines():
            print(f"  [author_copy] {line}")
    if result.returncode != 0:
        raise RuntimeError(
            f"author_copy.py exited with code {result.returncode}"
        )
    if not AUTHORED_JSON.exists():
        raise RuntimeError(f"author_copy.py did not produce {AUTHORED_JSON}")

    data = json.loads(AUTHORED_JSON.read_text(encoding="utf-8"))
    engine = data.get("_meta", {}).get("author_engine", "?")
    n = len(data.get("products", {}))
    print(f"  [author_copy] Authored {n} product(s).  engine={engine}")
    print(f"  [author_copy] NOTE: {engine} — not final quality.")


def stage_merge_copy_and_gate() -> None:
    """
    Stage 7: merge_copy_and_gate  (DETERMINISTIC)
    Merges authored strings into the page JSON, replacing PENDING_COPY.
    Runs readability on every consumer string (100% is_clean required).
    Runs the full gate suite including G6 COPY-SAFETY.
    Writes the final page JSON (0 PENDING_COPY) and gate report.

    This stage calls merge_copy.py via subprocess with the correct args.

    merge_copy.py:
      - expects --page (the generated page with PENDING_COPY)
      - expects --copy (authored.json)
      - expects --out (final merged page)
      - expects --config (category config with corpus_dirs + run_products_dir)
      - expects --schema
      merge_copy.py calls run_gates.py internally on the final page.

    OFF ban: merge_copy.py merges only authored strings (from fact sheets from
    the page). No external source. null stays null.
    """
    import subprocess

    cmd = [
        sys.executable,
        str(MERGE_COPY_PY),
        "--page", str(PAGE_JSON),
        "--copy", str(AUTHORED_JSON),
        "--out", str(FINAL_PAGE_JSON),
        "--config", str(COPY_CONFIG_JSON),
        "--schema", str(SCHEMA_V3),
        "--sample-out", str(PAGE_OUT_DIR / "e2e_copy_sample.md"),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    stdout_lines = result.stdout.splitlines() if result.stdout else []
    stderr_lines = result.stderr.splitlines() if result.stderr else []
    for line in stdout_lines:
        print(f"  [merge_copy] {line}")
    for line in stderr_lines:
        print(f"  [merge_copy] {line}")

    if result.returncode != 0:
        raise RuntimeError(
            f"merge_copy.py exited with code {result.returncode} — "
            "readability or gate failure. See above for details."
        )
    if not FINAL_PAGE_JSON.exists():
        raise RuntimeError(f"merge_copy.py did not produce {FINAL_PAGE_JSON}")

    # Verify 0 PENDING_COPY in the final page
    final_blob = FINAL_PAGE_JSON.read_text(encoding="utf-8")
    pending_count = final_blob.count("PENDING_COPY")
    if pending_count > 0:
        raise RuntimeError(
            f"merge_copy produced {pending_count} PENDING_COPY occurrences in {FINAL_PAGE_JSON}. "
            "Expected 0."
        )

    data = json.loads(final_blob)
    n = len(data.get("products", []))
    print(
        f"  [merge_copy_and_gate] Final page: {n} product(s), "
        f"PENDING_COPY remaining={pending_count}, {FINAL_PAGE_JSON}"
    )


# ---------------------------------------------------------------------------
# Stage declarations (using runner.Stage)
# ---------------------------------------------------------------------------

def build_stages() -> list:
    """Declare all EXECUTE-mode stages with their input/output contracts.

    Stage order (P42):
      extract_bsip0 (0) → build_bsip1 (0.5) → score_products (2) →
      generate_page (3) → gate_page (4) →
      build_copy_inputs (5) → author_copy (6) → merge_copy_and_gate (7)

    The chain now starts at raw HTML. No pre-built BSIP1 fixtures are used.
    """
    sys.path.insert(0, str(SPINE_DIR))
    from runner import Stage

    # ---- Raw HTML input files
    raw_html_inputs = sorted(RAW_FIXTURES_DIR.glob("raw_*.html"))
    if not raw_html_inputs:
        raise RuntimeError(f"No raw_*.html fixtures found in {RAW_FIXTURES_DIR}")

    # Stage 0: raw HTML → BSIP0 JSON
    bsip0_outputs = [BSIP0_OUT / f"bsip0_{p.stem.replace('raw_e2e_0', '999000000000')}.json"
                     for p in raw_html_inputs]
    # Exact BSIP0 output filenames are derived at runtime from the parsed barcode.
    # We must use the real barcodes (9990000000001 etc.) which come from LD+JSON.
    # Since we know the fixtures, hard-code the expected outputs for the DAG contract.
    # If fixtures change, these outputs would be re-derived by running the stage.
    bsip0_out_paths = [
        BSIP0_OUT / "bsip0_9990000000001.json",
        BSIP0_OUT / "bsip0_9990000000002.json",
        BSIP0_OUT / "bsip0_9990000000003.json",
    ]
    # Trim to actual fixture count (defensive)
    bsip0_out_paths = bsip0_out_paths[: len(raw_html_inputs)]

    stage0 = Stage(
        name="extract_bsip0",
        fn=stage_extract_bsip0,
        inputs=list(raw_html_inputs),
        outputs=bsip0_out_paths,
        code_version="e2e_p41_v1",
    )

    # Stage 0.5: BSIP0 JSON → BSIP1 JSON
    bsip1_out_paths = [
        BSIP1_OUT / f"bsip1_{p.stem.replace('bsip0_', '')}.json"
        for p in bsip0_out_paths
    ]
    stage05 = Stage(
        name="build_bsip1",
        fn=stage_build_bsip1,
        inputs=bsip0_out_paths,
        outputs=bsip1_out_paths,
        code_version="e2e_p41_v1",
    )

    # Stage 2: BSIP1 records → BSIP2 trace dirs
    bsip2_trace_outputs = []
    for p in bsip1_out_paths:
        # canonical_product_id = "e2e_raw_<barcode>"
        barcode = p.stem.replace("bsip1_", "")
        pid = f"e2e_raw_{barcode}"
        bsip2_trace_outputs.append(BSIP2_PRODUCTS_DIR / pid / "bsip2_trace.json")

    stage2 = Stage(
        name="score_products",
        fn=stage_score_products,
        inputs=bsip1_out_paths,
        outputs=bsip2_trace_outputs,
        code_version="e2e_p41_v1",
    )

    # Stage 3: BSIP2 traces + config → page JSON
    stage3 = Stage(
        name="generate_page",
        fn=stage_generate_page,
        inputs=bsip2_trace_outputs,
        outputs=[PAGE_JSON],
        code_version="e2e_p41_v1",
    )

    # Stage 4: page JSON → gated page (gate report is the output artifact)
    gate_report = PAGE_OUT_DIR / "e2e_page_throwaway_gates_report.md"
    stage4 = Stage(
        name="gate_page",
        fn=stage_gate_page,
        inputs=[PAGE_JSON],
        outputs=[gate_report],
        code_version="e2e_p41_v1",
    )

    # Stage 5: page JSON + traces → fact sheets (deterministic)
    stage5 = Stage(
        name="build_copy_inputs",
        fn=stage_build_copy_inputs,
        inputs=[PAGE_JSON],
        outputs=[FACT_SHEETS_JSON],
        code_version="e2e_p42_v1",
    )

    # Stage 6: fact sheets → authored copy (seam — baseline_placeholder for this run)
    stage6 = Stage(
        name="author_copy",
        fn=stage_author_copy,
        inputs=[FACT_SHEETS_JSON],
        outputs=[AUTHORED_JSON],
        code_version="e2e_p42_v1",
    )

    # Stage 7: authored copy + page → final merged page + copy gate report
    stage7 = Stage(
        name="merge_copy_and_gate",
        fn=stage_merge_copy_and_gate,
        inputs=[PAGE_JSON, AUTHORED_JSON],
        outputs=[FINAL_PAGE_JSON],
        code_version="e2e_p42_v1",
    )

    return [stage0, stage05, stage2, stage3, stage4, stage5, stage6, stage7]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="E2E Spine pipeline — raw HTML → page (THROWAWAY fixture — TASK-259 / P41)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the pipeline for real (required; otherwise print plan only)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-run even if all stages are current",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Path to spine.db (default: 03_operations/spine/spine.db)",
    )
    args = parser.parse_args()

    if not args.execute:
        print("Dry-run: declare stages only (pass --execute to run).")
        stages = build_stages()
        for s in stages:
            print(
                f"  Stage: {s.name:25s}  inputs={len(s.inputs)}  "
                f"outputs={len(s.outputs)}  code_version={s.code_version}"
            )
        print(
            "\nChain: raw HTML → extract_bsip0 → build_bsip1 → score_products → "
            "generate_page → gate_page → build_copy_inputs → author_copy → merge_copy_and_gate"
        )
        return

    print("=== pipeline_e2e.py --execute (THROWAWAY — raw HTML start + copy stages P42) ===")
    print(f"  Raw fixtures: {RAW_FIXTURES_DIR}")
    print(f"  Output:       {E2E_OUT}")
    print(
        f"  Chain:  raw_html → extract_bsip0 → build_bsip1 → score_products → "
        f"generate_page → gate_page → build_copy_inputs → author_copy → merge_copy_and_gate"
    )

    sys.path.insert(0, str(SPINE_DIR))
    from runner import run_pipeline

    stages = build_stages()
    db_path = Path(args.db) if args.db else SPINE_DIR / "spine.db"

    results = run_pipeline(stages, db_path=db_path, force=args.force)

    print("\n=== Stage Results ===")
    for name, status in results.items():
        print(f"  {name:25s}: {status}")

    # Print stage_runs + lineage from spine.db
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    stage_names = (
        "('extract_bsip0','build_bsip1','score_products','generate_page','gate_page',"
        "'build_copy_inputs','author_copy','merge_copy_and_gate')"
    )
    print("\n=== spine.db stage_runs ===")
    rows = conn.execute(
        f"SELECT stage_name, status, started_at, finished_at FROM stage_runs "
        f"WHERE stage_name IN {stage_names} ORDER BY started_at"
    ).fetchall()
    for row in rows:
        print(f"  {row['stage_name']:25s}  status={row['status']:7s}  "
              f"started={row['started_at']}  finished={row['finished_at']}")

    print("\n=== spine.db lineage (raw→page, sample) ===")
    lineage_rows = conn.execute(
        "SELECT child_path, parent_path, relation FROM lineage ORDER BY child_path LIMIT 30"
    ).fetchall()
    if lineage_rows:
        for row in lineage_rows:
            child = str(row["child_path"]).replace(str(REPO), "<REPO>")
            parent = str(row["parent_path"]).replace(str(REPO), "<REPO>")
            print(f"  {child}")
            print(f"    <- {parent}  [{row['relation']}]")
    else:
        print("  (no lineage rows yet)")
    conn.close()

    # Raw→score trace: show one parsed value flowing to grade
    print("\n=== Raw → Score trace (protein_g path) ===")
    for bsip0_file in sorted(BSIP0_OUT.glob("bsip0_*.json")):
        bsip0 = json.loads(bsip0_file.read_text(encoding="utf-8"))
        barcode = bsip0.get("barcode", "?")
        protein_raw = (bsip0.get("nutrition") or {}).get("protein_raw", "?")
        print(f"  raw HTML → BSIP0: barcode={barcode}  protein_raw='{protein_raw}'")

    for bsip1_file in sorted(BSIP1_OUT.glob("bsip1_*.json")):
        bsip1 = json.loads(bsip1_file.read_text(encoding="utf-8"))
        barcode = bsip1.get("barcode", "?")
        protein_g = (bsip1.get("normalized_nutrition_per_100g") or {}).get("protein_g", "?")
        print(f"  BSIP0 → BSIP1:  barcode={barcode}  protein_g={protein_g}")

    for pid_dir in sorted(BSIP2_PRODUCTS_DIR.iterdir()) if BSIP2_PRODUCTS_DIR.exists() else []:
        trace_path = pid_dir / "bsip2_trace.json"
        if trace_path.exists():
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
            pid = trace.get("input_reference", {}).get("canonical_product_id", pid_dir.name)
            score = trace.get("final_score_estimate", "?")
            grade = trace.get("grade_estimate", "?")
            print(f"  BSIP1 → score:  {pid}  score={score}  grade={grade}")

    # OFF ban final check: grep all BSIP0/BSIP1 outputs
    print("\n=== OFF ban grep (BSIP0 + BSIP1 outputs) ===")
    off_found = 0
    off_markers = ["openfoodfacts", "open_food_facts", "off.net"]
    for check_dir, label in [(BSIP0_OUT, "BSIP0"), (BSIP1_OUT, "BSIP1")]:
        if check_dir.exists():
            for jf in check_dir.glob("*.json"):
                content = jf.read_text(encoding="utf-8").lower()
                for marker in off_markers:
                    if marker in content:
                        print(f"  FAIL: OFF marker '{marker}' in {label}/{jf.name}")
                        off_found += 1
    if off_found == 0:
        print(f"  PASS: zero OFF markers in all BSIP0 + BSIP1 outputs")

    # Summary
    ran = [n for n, s in results.items() if s == "ran"]
    skipped = [n for n, s in results.items() if s == "skipped"]
    print(f"\nSummary: {len(ran)} ran, {len(skipped)} skipped")
    if PAGE_JSON.exists():
        data = json.loads(PAGE_JSON.read_text(encoding="utf-8"))
        print(f"Stage page (pre-copy):  {PAGE_JSON} ({len(data.get('products', []))} products)")

    if FINAL_PAGE_JSON.exists():
        final_blob = FINAL_PAGE_JSON.read_text(encoding="utf-8")
        pending_count = final_blob.count("PENDING_COPY")
        final_data = json.loads(final_blob)
        author_engine = "?"
        if AUTHORED_JSON.exists():
            authored = json.loads(AUTHORED_JSON.read_text(encoding="utf-8"))
            author_engine = authored.get("_meta", {}).get("author_engine", "?")
        print(f"Final page (copy-complete): {FINAL_PAGE_JSON}")
        print(f"  PENDING_COPY remaining: {pending_count}")
        print(f"  author_engine:          {author_engine}")
        print(f"  products:               {len(final_data.get('products', []))}")


if __name__ == "__main__":
    main()
