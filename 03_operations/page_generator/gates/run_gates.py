"""
run_gates.py — Bari Page Generator Gate Suite
==============================================
Usage:
  python run_gates.py <frontend_json>
      --corpus  <bsip1_output_dir>
      --run     <bsip2_run_products_dir>
      [--baseline <current_live_json>]
      [--schema  <schema.json>]
      [--config  <category_gate_config.json>]

Exit codes: 0 = all gates PASS (or only WARNs), 1 = any FAIL.
Output: gates_report.md written next to the input JSON.

Gates implemented:
  G1 SCHEMA          — JSON Schema validation
  G2 COVERAGE        — field non-null rates; image regression check; Hebrew name check
  G3 SCOPE           — displayed vs scored product count; unexplained missing barcodes
  G4 OFF             — Open Food Facts contamination scan
  G5 GRADE-INTEGRITY — grade/score agreement with central scale + trace
  G6 COPY-SAFETY     — sodium causal framing, prior-run refs, framework leakage, banned phrases
  G7 PARITY          — side-by-side comparison with baseline (when --baseline provided)
  G8 DATA-SANITY     — physically impossible per-100g nutrition (e.g. sodium_mg>5000); nutrition-panel text in ingredients field
"""

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SCHEMA_PATH = (
    Path(__file__).parent.parent / "contract" / "page_output_schema_v1.json"
)

# Central grade scale (floor policy — default)
GRADE_SCALE = [
    ("S", 90),
    ("A", 80),
    ("B", 65),
    ("C", 50),
    ("D", 35),
    ("E", 0),
]

# Score-to-grade using floor policy (an engine E must never display as D)
def score_to_grade(score, policy="floor"):
    """Convert a numeric score to a letter grade using the central scale."""
    if score is None:
        return None
    if policy == "round":
        score = round(score)
    # floor: use raw float, no rounding
    for grade, threshold in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "E"


# OFF markers (TASK-238 hard rule)
OFF_MARKERS = [
    "open_food_facts",
    "openfoodfacts.org",
    "images.openfoodfacts",
    "panel_source.*open_food_facts",
]

# 9 banned phrases from Explanation Engine v2
BANNED_PHRASES_HE = [
    "עיבוד מרבי",
    "בסיס מהונדס",
    "ריבוי ממתיקים",
    "מיצוב פיטנס",
    "מוצר מעובד מאוד",
    "בעיית סוכר",
    "חלבון נמוך",
    "מרכיבים רבים",
    "ציון בסיסי",
]

# Framework vocabulary that must not leak into consumer strings
FRAMEWORK_LEAKAGE_PATTERNS = [
    r"\bNOVA\b",
    r"\bBSIP\b",
    r"\bcap=",
    r"\bproxy\b",
    r"\bdimension\b",
]

# Prior-run reference markers (T4b — forbidden in consumer copy)
PRIOR_RUN_PATTERNS = [
    r"הציון הקודם",
    r"גרסה הקודמת",
    r"שלא הועברו",
    r"run_",
]

# Sodium causal framing: נתרן within 30 chars after כי / בגלל / בשל
# word-boundary guard (P217/C3) — stop `כי` matching inside `נמוכים` / `בשל` inside `מבשל` (EV-051 substring-collision class); optional ו/ש prefix preserves real causal forms `ובגלל`/`שבגלל`.
SODIUM_CAUSAL_PATTERN = re.compile(
    r"(?<![א-ת])(?:[וש])?(?:כי|בגלל|בשל)(?![א-ת]).{0,30}נתרן",
    re.UNICODE,
)

# Hebrew character range (U+0590 – U+05FF)
HEBREW_RE = re.compile(r"[֐-׿]")

# ---------------------------------------------------------------------------
# G8 DATA-SANITY constants (P159 / TASK-301)
# Hard upper bounds per 100g; any breach is physically impossible for real food.
# ---------------------------------------------------------------------------

# Nutrition sanity bounds (per 100g)
DATA_SANITY_BOUNDS = {
    # sodium in mg
    "sodium_mg": 5000,
    # energy in kcal
    "energy_kcal": 900,
    # macro grams
    "fat_g": 100,
    "carbohydrates_g": 100,
    "sugars_g": 100,
    "protein_g": 100,
    "fiber_g": 100,
    "saturated_fat_g": 100,
}

# Hebrew tokens that indicate a nutrition panel was scraped into the ingredients field.
# Require 2+ matches (to reduce false positives on real ingredient lists that may mention
# one nutrient by chance).
NUTRITION_PANEL_TOKENS = [
    "ערכים תזונתיים",
    "קל",  # standalone energy unit (e.g. "121 קל")
    "גרם חלבונים",
    "גרם פחמימות",
    "גרם שומנים",
    "מג נתרן",
    "סיבים תזונתיים",
]

# Standalone Hebrew grade letters (to detect grade-in-prose mismatches)
# Must be bounded so מ"ג, לל"ג, ה- prefixes don't trigger.
# Grade letters as standalone Hebrew words: א (E), ב (D), ג (C), ד (B), ה (A), ס (S)
# (Bari grades are Latin S/A/B/C/D/E, but copy sometimes uses Hebrew equivalents)
# Actually: Bari grades are always Latin letters. The spec says: scan for standalone
# Hebrew grade letters ≠ badge grade. We look for Latin grade letters asserted in prose.
# The spec wording says "standalone Hebrew grade letters (א/ב/ג/ד/ה bounded by non-Hebrew) ≠ badge grade"
# This checks for Hebrew-alphabet grade assertions inside Hebrew prose.
# Map: S=ס, A=א, B=ב, C=ג, D=ד, E=ה  -- but these letters appear in normal Hebrew words.
# The boundary rule: bound the letter so it's not part of a longer Hebrew word.
# We use the spec's own examples: "מ\"ג" (milligrams), "לל\"ג", "ה-" prefix are false positives.
HEBREW_GRADE_MAP = {
    "ס": "S",   # ס
    "א": "A",   # א
    "ב": "B",   # ב
    "ג": "C",   # ג
    "ד": "D",   # ד
    "ה": "E",   # ה
}

# Pattern to find standalone Hebrew grade letters bounded by non-Hebrew context
# We look for: non-Hebrew-letter boundary + grade_letter + non-Hebrew-letter boundary
# And exclude common false-positive patterns like מ"ג, לל"ג, suffix forms
_HEB_LETTER_CLASS = r"[֐-׿]"
_NON_HEB = r"(?<![^֐-׿\s\W])"  # This is complex — use simpler approach below


def find_standalone_hebrew_grade_letters(text):
    """
    Return list of (position, hebrew_letter, mapped_grade) for standalone Hebrew
    grade letters in text. Excludes common false positives.

    Strategy: scan for each grade letter preceded and followed by non-Hebrew chars.
    False-positive filters: gershayim ("), ל-prefix, -prefix, part of longer Hebrew word.
    """
    results = []
    HEBREW_CHARS = set("אבגדהוזחטיךכלםמןנסעףפץצקרשת")
    HEBREW_RANGE_START = 0x0590
    HEBREW_RANGE_END = 0x05FF

    def is_hebrew_char(c):
        return HEBREW_RANGE_START <= ord(c) <= HEBREW_RANGE_END

    for letter, grade in HEBREW_GRADE_MAP.items():
        for m in re.finditer(re.escape(letter), text, re.UNICODE):
            start = m.start()
            end = m.end()

            # Skip if preceded by a Hebrew character (part of Hebrew word)
            if start > 0 and is_hebrew_char(text[start - 1]):
                continue

            # Skip if followed by a Hebrew character (part of Hebrew word)
            if end < len(text) and is_hebrew_char(text[end]):
                continue

            # Skip gershayim pattern: X"Y (e.g., מ"ג)
            if end < len(text) and text[end] in ('"', "'", "״"):
                continue
            if start > 0 and text[start - 1] in ('"', "'", "״"):
                continue

            # Skip ל-prefix (ל + letter) and other Hebrew-article prefixes (ה, ב, כ, מ, ו, ש)
            if start > 0 and text[start - 1] in "להבכמוש":
                continue

            # Skip - prefix
            if start > 0 and text[start - 1] == "-":
                continue

            # Skip if followed by - (as in ה-S, meaning "the S-grade")
            if end < len(text) and text[end] == "-":
                continue

            results.append((start, letter, grade))
    return results


def _is_nutrition_panel_text(text):
    """
    Return True if the ingredients text appears to be a scraped nutrition panel
    rather than an ingredient list. Detects by presence of 2+ Hebrew nutrition
    panel tokens (per P159 spec) AND indicators that this is the *entire* field
    value (e.g. very few real-ingredient separators like commas). This avoids
    false-positives on real ingredient lists that have panel text appended
    (common in current scraped data).
    """
    if not isinstance(text, str) or not text.strip():
        return False
    matches = 0
    for tok in NUTRITION_PANEL_TOKENS:
        if tok == "קל":
            if re.search(r"(?<![\w\u0590-\u05FF])קל(?!\w)", text):
                matches += 1
        elif tok in text:
            matches += 1
    if matches < 2:
        return False
    # Heuristic for "is actually the panel, not ingredients + panel":
    # - Low comma count (real ingr lists use , to separate components)
    # - Or very short overall text containing the panel values
    comma_count = text.count(",")
    if comma_count <= 1:
        return True
    # Also allow if the panel tokens dominate and no long ingredient prefix
    # (e.g. text starts with food name immediately followed by panel tokens, no , before first panel token)
    first_panel_pos = min((text.find(t) for t in NUTRITION_PANEL_TOKENS if t in text), default=-1)
    if first_panel_pos >= 0 and first_panel_pos < 40 and comma_count < 5:
        # short prefix before panel starts, few commas total
        return True
    return False


# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_jsonschema(instance, schema):
    """
    Minimal JSON Schema Draft-7 validator (stdlib only).
    Validates: type, required, properties (type + required sub-schemas), enum,
    additionalProperties, items (array items type).
    Returns list of error strings.
    """
    errors = []
    _validate_node(instance, schema, schema, "#", errors)
    return errors


def _validate_node(node, schema, root_schema, path, errors):
    if not isinstance(schema, dict):
        return

    # Resolve $ref
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/definitions/"):
            def_name = ref[len("#/definitions/"):]
            resolved = root_schema.get("definitions", {}).get(def_name)
            if resolved:
                _validate_node(node, resolved, root_schema, path, errors)
        return

    # type check
    schema_type = schema.get("type")
    if schema_type:
        type_list = [schema_type] if isinstance(schema_type, str) else schema_type
        if not _check_type(node, type_list):
            errors.append(f"{path}: expected type {schema_type}, got {type(node).__name__}")
            return  # stop further checks on wrong type

    # enum
    if "enum" in schema and node not in schema["enum"]:
        errors.append(f"{path}: value {node!r} not in enum {schema['enum']}")

    # object
    if isinstance(node, dict):
        # required
        for req in schema.get("required", []):
            if req not in node:
                errors.append(f"{path}: missing required field '{req}'")
        # properties
        for prop_name, prop_schema in schema.get("properties", {}).items():
            if prop_name in node:
                _validate_node(node[prop_name], prop_schema, root_schema, f"{path}.{prop_name}", errors)
        # additionalProperties = false
        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}).keys())
            for k in node:
                if k not in allowed:
                    errors.append(f"{path}: additional property '{k}' not allowed")

    # array
    if isinstance(node, list):
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(node):
                _validate_node(item, item_schema, root_schema, f"{path}[{i}]", errors)


def _check_type(value, type_list):
    """Check if value matches any of the JSON Schema type names."""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None),
    }
    for t in type_list:
        if t == "integer":
            if isinstance(value, int) and not isinstance(value, bool):
                return True
        elif t == "number":
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return True
        elif t in type_map:
            if isinstance(value, type_map[t]):
                return True
    return False


# ---------------------------------------------------------------------------
# Corpus loading helpers
# ---------------------------------------------------------------------------

def load_bsip1_corpus(corpus_dir):
    """
    Load all bsip1_*.json files from corpus_dir.
    Returns dict: barcode -> record
    """
    corpus = {}
    if not corpus_dir or not os.path.isdir(corpus_dir):
        return corpus
    for fname in os.listdir(corpus_dir):
        if fname.startswith("bsip1_") and fname.endswith(".json"):
            try:
                rec = load_json(os.path.join(corpus_dir, fname))
                bc = str(rec.get("barcode", "")).strip()
                if bc:
                    corpus[bc] = rec
            except Exception:
                pass
    return corpus


def load_bsip2_traces(run_dir):
    """
    Load all bsip2_trace.json files from product subdirs.
    Returns dict: barcode -> trace record
    """
    traces = {}
    if not run_dir or not os.path.isdir(run_dir):
        return traces
    for dname in os.listdir(run_dir):
        dpath = os.path.join(run_dir, dname)
        if not os.path.isdir(dpath):
            continue
        trace_path = os.path.join(dpath, "bsip2_trace.json")
        if os.path.isfile(trace_path):
            try:
                rec = load_json(trace_path)
                bc = str(rec.get("input_reference", {}).get("barcode", "")).strip()
                if bc:
                    traces[bc] = rec
            except Exception:
                pass
    return traces


def get_barcode_from_product(product):
    """Extract barcode from a product record. Tries barcode field, then id field."""
    bc = product.get("barcode")
    if bc:
        return str(bc).strip()
    # Fallback: parse from id (e.g., bsip1_yogurt_7290114312431 -> 7290114312431)
    pid = product.get("id", "")
    parts = pid.rsplit("_", 1)
    if len(parts) == 2:
        return parts[1].strip()
    return ""


def get_corpus_image(corpus_rec):
    """Return the image URL from a BSIP1 corpus record, or None."""
    img = corpus_rec.get("image_url")
    if img:
        return img
    urls = corpus_rec.get("image_urls") or []
    return urls[0] if urls else None


# ---------------------------------------------------------------------------
# Gate implementations
# ---------------------------------------------------------------------------

class GateResult:
    def __init__(self, name):
        self.name = name
        self.status = "PASS"   # PASS / FAIL / WARN / SKIP
        self.lines = []        # evidence lines

    def fail(self, msg):
        self.status = "FAIL"
        self.lines.append(f"  FAIL: {msg}")

    def warn(self, msg):
        if self.status == "PASS":
            self.status = "WARN"
        self.lines.append(f"  WARN: {msg}")

    def info(self, msg):
        self.lines.append(f"  INFO: {msg}")

    def skip(self, msg):
        self.status = "SKIP"
        self.lines.append(f"  SKIP: {msg}")

    def header(self):
        return f"[{self.status}] G{self.name}"


# --------------- G1 SCHEMA -----------------------------------------------

def gate_schema(frontend, schema_path):
    g = GateResult("1 SCHEMA")

    effective_path = schema_path or str(DEFAULT_SCHEMA_PATH)
    if not os.path.isfile(effective_path):
        g.skip(f"Schema file not found: {effective_path}")
        return g

    try:
        schema = load_json(effective_path)
    except Exception as e:
        g.warn(f"Could not load schema file: {e}")
        return g

    errors = validate_jsonschema(frontend, schema)
    if errors:
        for err in errors[:20]:
            g.fail(err)
        if len(errors) > 20:
            g.fail(f"... and {len(errors) - 20} more errors")
    else:
        g.info("Document validates against schema")
    return g


# --------------- G2 COVERAGE --------------------------------------------

def gate_coverage(frontend, corpus):
    g = GateResult("2 COVERAGE")
    products = frontend.get("products", [])
    n = len(products)
    if n == 0:
        g.fail("No products in frontend JSON")
        return g

    # Fields to report coverage on
    DISPLAY_FIELDS = [
        "imageUrl",
        "name",
        "score",
        "grade",
        "insightLine",
    ]
    EXPANSION_NUTRITION_FIELDS = ["energyKcal", "protein", "sugar", "fat", "fiber", "sodium"]

    # Count non-null per field
    for field in DISPLAY_FIELDS:
        count = sum(1 for p in products if p.get(field) is not None and p.get(field) != "")
        g.info(f"{field}: {count}/{n} non-null")

    # Expansion fields
    exp_count = sum(1 for p in products if p.get("expansion") is not None)
    g.info(f"expansion: {exp_count}/{n}")

    ingr_count = sum(
        1 for p in products
        if p.get("expansion", {}) and p["expansion"].get("ingredients") is not None
    )
    g.info(f"expansion.ingredients: {ingr_count}/{n}")

    for nf in EXPANSION_NUTRITION_FIELDS:
        count = sum(
            1 for p in products
            if p.get("expansion", {})
            and isinstance(p["expansion"].get("nutrition"), dict)
            and p["expansion"]["nutrition"].get(nf) is not None
        )
        g.info(f"expansion.nutrition.{nf}: {count}/{n}")

    # confidence labels
    cl_count = sum(
        1 for p in products
        if p.get("expansion", {}) and p["expansion"].get("confidenceLabel")
    )
    g.info(f"expansion.confidenceLabel: {cl_count}/{n}")

    # --- HARD: imageUrl coverage vs corpus ---
    if corpus:
        # Build set of barcodes that have images in BSIP1
        corpus_with_image = {bc for bc, rec in corpus.items() if get_corpus_image(rec)}
        g.info(f"Corpus barcodes with image in BSIP1: {len(corpus_with_image)}/{len(corpus)}")

        # For each displayed product: if corpus has image but frontend doesn't -> FAIL
        missing_image_barcodes = []
        for p in products:
            bc = get_barcode_from_product(p)
            if bc in corpus_with_image and not p.get("imageUrl"):
                missing_image_barcodes.append(bc)

        if missing_image_barcodes:
            for bc in missing_image_barcodes:
                g.fail(f"imageUrl missing in frontend but BSIP1 has image: barcode {bc}")
        else:
            g.info("imageUrl: no regression vs BSIP1 corpus")
    else:
        g.warn("No corpus provided — imageUrl regression check skipped")

    # --- HARD: name must contain Hebrew characters ---
    non_hebrew_names = []
    for p in products:
        name = p.get("name", "") or ""
        if name and not HEBREW_RE.search(name):
            non_hebrew_names.append((get_barcode_from_product(p), name))
    if non_hebrew_names:
        for bc, name in non_hebrew_names:
            g.fail(f"name has no Hebrew characters: barcode={bc} name={name!r}")
    else:
        g.info("name: all products have Hebrew characters in name")

    # --- Schema-agnostic unauthored-copy check (insightLine / rowVerdict) ---
    # Two distinct failures, both checked only AFTER the copy stage has run:
    #   (1) the literal PENDING_COPY placeholder leaked into a served field; and
    #   (2) a row that would render NO verdict at all — insightLine AND rowVerdict both
    #       unauthored (PENDING / null / empty / missing).
    # We deliberately do NOT fault a single empty field on its own: per the view model
    # (src/lib/view-models/index.ts) insightLine="" means "no insight slot rendered", and
    # rowVerdict is DERIVED from insightLine at render for several pages
    # (hummus-comparison-page-data.ts, row-surface.ts) — so a lone null/empty field is
    # legitimate (milk renders via rowVerdict; hummus via insightLine). Only a row with
    # NEITHER authored is genuinely verdict-less. (Red-team MEDIUM 2026-06-18: the prior
    # check caught only the literal PENDING string and missed a fully-nulled row.)
    pending = "PENDING_COPY"

    def _authored(v):
        return isinstance(v, str) and v.strip() != "" and v != pending

    copy_stage_ran = any(
        _authored(p.get("insightLine")) or _authored(p.get("rowVerdict"))
        for p in products
    )
    if not copy_stage_ran:
        g.info("Unauthored-copy check: SKIP (pre-copy generator output)")
    else:
        # (1) literal PENDING_COPY placeholder must never reach a served field
        for field in ("insightLine", "rowVerdict"):
            pending_count = sum(1 for p in products if p.get(field) == pending)
            if pending_count > 0:
                g.fail(
                    f"{field}: {pending_count}/{n} products still PENDING_COPY "
                    f"(page authored but incomplete)"
                )
        # (2) verdict-less rows: NEITHER insightLine NOR rowVerdict authored
        verdictless = [
            get_barcode_from_product(p) for p in products
            if not _authored(p.get("insightLine")) and not _authored(p.get("rowVerdict"))
        ]
        if verdictless:
            shown = ", ".join(verdictless[:8])
            g.fail(
                f"{len(verdictless)}/{n} products render NO verdict — both insightLine "
                f"and rowVerdict are unauthored (PENDING/null/empty/missing) after the "
                f"copy stage ran — barcodes: {shown}"
                + (" ..." if len(verdictless) > 8 else "")
            )
        else:
            g.info("verdict coverage: every product has an authored insightLine or rowVerdict")

    # --- v3 COVERAGE: milk-depth authored fields non-PENDING check ---
    # Only check when the fields are present (v3 pages) AND the copy stage has run.
    # We detect "copy stage ran" by checking that insightLine is non-PENDING on
    # all products. If insightLine is still PENDING, the page is a generator output
    # (pre-copy) — v3 checks are INFO only (the copy stage will fill them).
    schema_ver = frontend.get("_meta", {}).get("schema_version", "")
    if schema_ver == "v3":
        pending = "PENDING_COPY"

        # Detect whether copy stage has run (all insightLines non-PENDING)
        insight_pending = sum(1 for p in products if p.get("insightLine") == pending)
        copy_stage_ran = (insight_pending == 0)

        if not copy_stage_ran:
            g.info(f"v3 milk-depth coverage checks: SKIP (copy stage not yet run; {insight_pending}/{n} insightLines still PENDING)")
        else:
            # consumerTakeaway
            ct_count = sum(1 for p in products if p.get("consumerTakeaway") and p.get("consumerTakeaway") != pending)
            ct_pending = sum(1 for p in products if p.get("consumerTakeaway") == pending)
            g.info(f"v3 consumerTakeaway: {ct_count}/{n} authored ({ct_pending} PENDING)")
            if ct_pending > 0:
                g.fail(f"v3 consumerTakeaway: {ct_pending}/{n} products still PENDING_COPY")

            # expansion.consumerExplanation.whyRated
            # A field that is ABSENT is not "pending" — it means this page does not render
            # the deep-dive block at all (the golden/assessment shape: see brined-cheeses,
            # crackers, yogurt). Only a literal PENDING_COPY placeholder is a failure, which
            # is the semantics consumerTakeaway and bariInterpretation already use. Counting
            # absence as pending made this gate fail on already-shipped pages (crackers).
            def _ce(p):
                ce = (p.get("expansion") or {}).get("consumerExplanation")
                return ce if isinstance(ce, dict) else None

            ce_wr_pending = sum(1 for p in products if _ce(p) and _ce(p).get("whyRated") == pending)
            ce_wr_count = sum(
                1 for p in products
                if _ce(p) and _ce(p).get("whyRated") not in (None, "", pending)
            )
            ce_wr_absent = n - ce_wr_count - ce_wr_pending
            g.info(
                f"v3 consumerExplanation.whyRated: {ce_wr_count}/{n} authored "
                f"({ce_wr_pending} PENDING, {ce_wr_absent} not used by this page)"
            )
            if ce_wr_pending > 0:
                g.fail(f"v3 consumerExplanation.whyRated: {ce_wr_pending}/{n} products still PENDING_COPY")

            # bariInterpretation[].interpretation
            bi_total = 0
            bi_pending_total = 0
            for p in products:
                for entry in (p.get("bariInterpretation") or []):
                    if isinstance(entry, dict):
                        bi_total += 1
                        if entry.get("interpretation") == pending:
                            bi_pending_total += 1
            g.info(f"v3 bariInterpretation.interpretation: {bi_total - bi_pending_total}/{bi_total} authored ({bi_pending_total} PENDING)")
            if bi_pending_total > 0:
                g.fail(f"v3 bariInterpretation.interpretation: {bi_pending_total}/{bi_total} entries still PENDING_COPY")

            # bestUseCases — same rule: an empty/absent list means the page does not render
            # the use-case tag row; only a literal PENDING_COPY tag is a failure.
            buc_pending = sum(
                1 for p in products
                if isinstance(p.get("bestUseCases"), list)
                and any(v == pending for v in p["bestUseCases"])
            )
            buc_count = sum(
                1 for p in products
                if isinstance(p.get("bestUseCases"), list)
                and len(p["bestUseCases"]) > 0
                and not any(v == pending for v in p["bestUseCases"])
            )
            buc_absent = n - buc_count - buc_pending
            g.info(
                f"v3 bestUseCases: {buc_count}/{n} authored "
                f"({buc_pending} PENDING, {buc_absent} not used by this page)"
            )
            if buc_pending > 0:
                g.fail(f"v3 bestUseCases: {buc_pending}/{n} products still PENDING_COPY")
    else:
        g.info(f"v3 milk-depth coverage checks: SKIP (schema_version={schema_ver!r}, not v3)")

    return g


# --------------- G3 SCOPE -----------------------------------------------

def gate_scope(frontend, run_dir):
    g = GateResult("3 SCOPE")
    products = frontend.get("products", [])
    meta = frontend.get("_meta", {})

    displayed_barcodes = {get_barcode_from_product(p) for p in products}
    g.info(f"Displayed products: {len(displayed_barcodes)}")

    # Count scored trace dirs
    if not run_dir or not os.path.isdir(run_dir):
        g.warn(f"Run directory not found: {run_dir}")
        return g

    trace_barcodes = set()
    for dname in os.listdir(run_dir):
        dpath = os.path.join(run_dir, dname)
        if not os.path.isdir(dpath):
            continue
        trace_path = os.path.join(dpath, "bsip2_trace.json")
        if os.path.isfile(trace_path):
            try:
                rec = load_json(trace_path)
                bc = str(rec.get("input_reference", {}).get("barcode", "")).strip()
                if bc:
                    trace_barcodes.add(bc)
            except Exception:
                pass

    g.info(f"Scored products (trace dirs): {len(trace_barcodes)}")

    # Build exclusions map from meta — look for any key containing 'exclu' or 'dedup'
    exclusions = {}
    for key, val in meta.items():
        if any(x in key.lower() for x in ("exclu", "dedup", "remov", "drop")):
            if isinstance(val, dict):
                exclusions.update(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        exclusions[item] = "(no reason provided)"
                    elif isinstance(item, dict):
                        # Generator format: {"barcode": "...", "reason": "...", "product_id": "..."}
                        bc_key = item.get("barcode") or item.get("barcode_str")
                        reason_val = item.get("reason", "(no reason provided)")
                        if bc_key:
                            exclusions[str(bc_key)] = reason_val
            elif isinstance(val, str):
                # Might be a provenance string containing barcode references
                pass

    g.info(f"Declared exclusions in _meta: {len(exclusions)}")

    # Find missing barcodes (scored but not displayed)
    missing = trace_barcodes - displayed_barcodes
    if missing:
        unexplained = []
        for bc in sorted(missing):
            if bc in exclusions:
                g.info(f"  missing barcode {bc}: excluded — {exclusions[bc]}")
            else:
                # Check provenance string for any mention of this barcode
                provenance = meta.get("provenance", "")
                if bc in provenance:
                    g.info(f"  missing barcode {bc}: mentioned in provenance string (treat as explained)")
                else:
                    unexplained.append(bc)

        if unexplained:
            for bc in unexplained:
                g.fail(f"Scored barcode {bc} not in frontend and not explained in _meta exclusions")
    else:
        g.info("All scored barcodes are displayed or explained")

    # Also check: displayed barcodes not in trace (ghost products)
    ghost = displayed_barcodes - trace_barcodes
    if ghost:
        for bc in sorted(ghost):
            g.warn(f"Displayed barcode {bc} has no BSIP2 trace in --run dir (ghost product)")

    return g


# --------------- G4 OFF -------------------------------------------------

def gate_off(frontend, corpus):
    g = GateResult("4 OFF")
    found_any = False

    # Scan the products array only (not _meta, which legitimately references OFF in exclusion
    # documentation). _meta exclusion reasons may name OFF as the exclusion cause — that is
    # correct documentation, not contamination. What matters is that the products array
    # contains no OFF-sourced data.
    products_str = json.dumps(frontend.get("products", []), ensure_ascii=False)
    for marker in OFF_MARKERS:
        matches = re.findall(marker, products_str, re.IGNORECASE)
        if matches:
            g.fail(f"OFF marker '{marker}' found {len(matches)} time(s) in products array")
            found_any = True

    # Also check _meta for any unexpected OFF markers outside the exclusions documentation
    # (warn only, since exclusion reasons legitimately reference OFF as the cause)
    meta = frontend.get("_meta", {})
    meta_str = json.dumps(meta, ensure_ascii=False)
    # Exclude the exclusions list from the check — it's documentation
    meta_without_exclusions = {k: v for k, v in meta.items() if k != "exclusions"}
    meta_clean_str = json.dumps(meta_without_exclusions, ensure_ascii=False)
    for marker in OFF_MARKERS:
        if re.search(marker, meta_clean_str, re.IGNORECASE):
            g.warn(f"OFF marker '{marker}' found in _meta (outside exclusions list) — review")

    # Scan corpus records for displayed barcodes
    if corpus:
        products = frontend.get("products", [])
        displayed_barcodes = {get_barcode_from_product(p) for p in products}
        for bc in displayed_barcodes:
            if bc not in corpus:
                continue
            rec_str = json.dumps(corpus[bc], ensure_ascii=False)
            for marker in OFF_MARKERS:
                if re.search(marker, rec_str, re.IGNORECASE):
                    g.fail(f"OFF marker '{marker}' found in BSIP1 corpus record for barcode {bc}")
                    found_any = True
                    break

    if not found_any:
        g.info("No OFF markers detected in frontend JSON or displayed corpus records")
    return g


# --------------- G5 GRADE-INTEGRITY -------------------------------------

def gate_grade_integrity(frontend, traces, config):
    g = GateResult("5 GRADE-INTEGRITY")
    products = frontend.get("products", [])
    policy = config.get("boundary", "floor") if config else "floor"
    g.info(f"Boundary policy: {policy}")
    score_tolerance = 0.05

    fail_count = 0
    for p in products:
        bc = get_barcode_from_product(p)
        pid = p.get("id", bc)
        json_score = p.get("score")
        json_grade = p.get("grade")

        if json_score is None or json_grade is None:
            # Skip unscored products
            continue

        # Check grade derived from score
        expected_grade = score_to_grade(json_score, policy)
        # Check for per-product cap-exception flag
        cap_exception = None
        for k in p:
            if k.startswith("_") and "cap" in k.lower():
                cap_exception = k
                break

        if expected_grade != json_grade and cap_exception is None:
            g.fail(
                f"barcode={bc}: JSON grade={json_grade} but score={json_score} "
                f"implies grade={expected_grade} (policy={policy})"
            )
            fail_count += 1

        # Check score vs trace
        if bc in traces:
            trace = traces[bc]
            trace_score = trace.get("final_score_estimate")
            trace_grade = trace.get("grade_estimate")

            if trace_score is not None:
                # Spec: tolerance 0.05 after rounding.
                # If the frontend JSON score is an integer, the generator rounded the trace
                # score — so compare round(trace) vs json_score (integer equality check).
                # If the frontend JSON score is a float, compare directly with 0.05 tolerance.
                js_float = float(json_score)
                ts_float = float(trace_score)
                json_is_integer = isinstance(json_score, int) or (
                    isinstance(json_score, float) and json_score == int(json_score)
                )
                if json_is_integer:
                    trace_rounded = round(ts_float)
                    diff = abs(js_float - trace_rounded)
                    if diff > score_tolerance:
                        g.fail(
                            f"barcode={bc}: JSON score={json_score} vs trace score={trace_score} "
                            f"(rounded trace={trace_rounded}, diff={diff:.3f} > tolerance={score_tolerance})"
                        )
                else:
                    # Float score — compare directly
                    diff = abs(js_float - ts_float)
                    if diff > score_tolerance:
                        g.fail(
                            f"barcode={bc}: JSON score={json_score} vs trace score={trace_score} "
                            f"(diff={diff:.3f} > tolerance={score_tolerance})"
                        )
                    fail_count += 1

            # Grade must not be higher band than trace grade
            # (engine E must never display as D)
            if trace_score is not None and json_grade is not None:
                trace_derived_grade = score_to_grade(trace_score, policy)
                json_grade_idx = _grade_index(json_grade)
                trace_grade_idx = _grade_index(trace_derived_grade)
                if json_grade_idx < trace_grade_idx:
                    # json_grade is BETTER than trace grade (lower index = better)
                    g.fail(
                        f"barcode={bc}: displayed grade={json_grade} is better than "
                        f"trace-derived grade={trace_derived_grade} "
                        f"(trace_score={trace_score}) — grade inflation"
                    )
                    fail_count += 1
        else:
            g.warn(f"barcode={bc}: no trace found in --run dir, cannot verify score vs trace")

        # Check inline prose for Hebrew grade letter ≠ badge grade
        copy_fields = _collect_consumer_strings(p)
        for field_name, text in copy_fields:
            _check_hebrew_grade_prose(g, bc, field_name, text, json_grade)

    if fail_count == 0:
        g.info("All grade/score checks passed")
    return g


def _grade_index(grade):
    """Lower index = better grade. S=0, A=1, B=2, C=3, D=4, E=5, unknown=99"""
    order = ["S", "A", "B", "C", "D", "E"]
    try:
        return order.index(grade)
    except ValueError:
        return 99


def _collect_consumer_strings(product):
    """Return list of (field_name, text) for all consumer-facing string fields.
    Includes v3 milk-depth fields: consumerTakeaway, consumerExplanation.*,
    bariInterpretation[].interpretation, bestUseCases[].
    """
    PENDING = "PENDING_COPY"
    fields = []
    for fname in ["insightLine", "rowVerdict", "consumerTakeaway"]:
        val = product.get(fname)
        if val and isinstance(val, str) and val != PENDING:
            fields.append((fname, val))
    exp = product.get("expansion", {}) or {}
    for fname in ["confidenceLabel", "comparisonContext", "servingNote", "bottomLine"]:
        val = exp.get(fname)
        if val and isinstance(val, str) and val != PENDING:
            fields.append((f"expansion.{fname}", val))
    for fname in ["positiveSignals", "limitingFactors", "unknowns", "caveats"]:
        items = exp.get(fname) or []
        for i, item in enumerate(items):
            if item and isinstance(item, str) and item != PENDING:
                fields.append((f"expansion.{fname}[{i}]", item))
    # v3: consumerExplanation sub-fields
    ce = exp.get("consumerExplanation") or {}
    for fname in ["whyRated", "context", "takeaway"]:
        val = ce.get(fname)
        if val and isinstance(val, str) and val != PENDING:
            fields.append((f"expansion.consumerExplanation.{fname}", val))
    for i, item in enumerate(ce.get("good") or []):
        if item and isinstance(item, str) and item != PENDING:
            fields.append((f"expansion.consumerExplanation.good[{i}]", item))
    for i, item in enumerate(ce.get("watchOut") or []):
        if item and isinstance(item, str) and item != PENDING:
            fields.append((f"expansion.consumerExplanation.watchOut[{i}]", item))
    # v3: bariInterpretation[].interpretation
    for i, entry in enumerate(product.get("bariInterpretation") or []):
        if isinstance(entry, dict):
            interp = entry.get("interpretation")
            if interp and isinstance(interp, str) and interp != PENDING:
                fields.append((f"bariInterpretation[{i}].interpretation", interp))
    # v3: bestUseCases[]
    for i, item in enumerate(product.get("bestUseCases") or []):
        if item and isinstance(item, str) and item != PENDING:
            fields.append((f"bestUseCases[{i}]", item))
    return fields


def _check_hebrew_grade_prose(g, bc, field_name, text, badge_grade):
    """Check for standalone Hebrew grade letters that mismatch the badge grade."""
    results = find_standalone_hebrew_grade_letters(text)
    for pos, letter, mapped_grade in results:
        if mapped_grade != badge_grade:
            snippet = text[max(0, pos-10):pos+15]
            g.fail(
                f"barcode={bc} field={field_name}: standalone Hebrew grade letter "
                f"'{letter}' (maps to {mapped_grade}) ≠ badge grade {badge_grade} "
                f"near: ...{snippet!r}..."
            )


# --------------- G6 COPY-SAFETY -----------------------------------------

def gate_copy_safety(frontend):
    g = GateResult("6 COPY-SAFETY")
    products = frontend.get("products", [])
    fail_count = 0

    # Compile patterns once
    prior_run_re = [re.compile(p, re.UNICODE) for p in PRIOR_RUN_PATTERNS]
    framework_re = [re.compile(p, re.UNICODE | re.IGNORECASE) for p in FRAMEWORK_LEAKAGE_PATTERNS]
    banned_re = [re.compile(re.escape(phrase), re.UNICODE) for phrase in BANNED_PHRASES_HE]

    for p in products:
        bc = get_barcode_from_product(p)
        copy_fields = _collect_consumer_strings(p)

        for field_name, text in copy_fields:
            # 1. Sodium causal framing
            m = SODIUM_CAUSAL_PATTERN.search(text)
            if m:
                g.fail(f"barcode={bc} field={field_name}: sodium causally framed: {m.group()!r}")
                fail_count += 1

            # 2. Prior-run references
            for pattern_re in prior_run_re:
                m = pattern_re.search(text)
                if m:
                    g.fail(f"barcode={bc} field={field_name}: prior-run reference: {m.group()!r}")
                    fail_count += 1

            # 3. Framework leakage
            for pattern_re in framework_re:
                m = pattern_re.search(text)
                if m:
                    g.fail(f"barcode={bc} field={field_name}: framework vocabulary leaked: {m.group()!r}")
                    fail_count += 1

            # 4. 9 banned phrases
            for phrase, phrase_re in zip(BANNED_PHRASES_HE, banned_re):
                m = phrase_re.search(text)
                if m:
                    g.fail(f"barcode={bc} field={field_name}: banned phrase '{phrase}' found")
                    fail_count += 1

    # Also scan page-level strings (meta notes if any)
    meta = frontend.get("_meta", {})
    for key in ["scope_note", "editorial_note"]:
        val = meta.get(key)
        if val and isinstance(val, str):
            for pattern_re in framework_re:
                m = pattern_re.search(val)
                if m:
                    g.warn(f"meta.{key}: framework vocabulary: {m.group()!r}")

    if fail_count == 0:
        g.info("No copy-safety violations detected")
    return g


# --------------- G8 DATA-SANITY -----------------------------------------

def gate_data_sanity(frontend):
    """
    G8 DATA-SANITY gate (P159 / TASK-301).
    Fails on:
    - Physically impossible nutrition values per 100g (sodium_mg>5000, energy>900kcal,
      any listed macro gram field >100, saturated_fat_g>100).
    - Ingredients field contains a nutrition panel (2+ matching Hebrew tokens).
    Output format matches other gates: FAIL lines name barcode + field + value.
    """
    g = GateResult("8 DATA-SANITY")
    products = frontend.get("products", [])
    violation_count = 0

    # Map from expansion.nutrition json key -> (logical, bound)
    NUTRITION_CHECKS = [
        ("energyKcal", "energy_kcal", 900),
        ("sodium", "sodium_mg", 5000),
        ("fat", "fat_g", 100),
        ("protein", "protein_g", 100),
        ("sugar", "sugars_g", 100),
        ("fiber", "fiber_g", 100),
    ]

    # Possible keys for saturated fat (not yet mapped into all pages, but future-proof + catch if present)
    SATURATED_KEYS = [
        "saturatedFat", "saturated_fat", "saturatedFat_g", "fat_saturated_g",
        "saturated_fat_g", "fat_saturated", "sat_fat", "satFat",
    ]

    for p in products:
        bc = get_barcode_from_product(p)
        exp = p.get("expansion") or {}
        nutr = exp.get("nutrition") or {}
        ingredients = exp.get("ingredients")

        # 1) Impossible nutrition per 100g
        for json_key, logical, bound in NUTRITION_CHECKS:
            val = nutr.get(json_key)
            if val is not None:
                try:
                    v = float(val)
                    if v > bound:
                        g.fail(f"barcode={bc}: impossible {logical}={v} > {bound} (per 100g)")
                        violation_count += 1
                except (ValueError, TypeError):
                    pass

        # Saturated fat (check known possible keys + any extra keys in the nutr dict that look saturated)
        checked_sat = False
        for sk in SATURATED_KEYS:
            if sk in nutr:
                val = nutr.get(sk)
                if val is not None:
                    try:
                        v = float(val)
                        if v > 100:
                            g.fail(f"barcode={bc}: impossible saturated_fat_g={v} > 100 (per 100g)")
                            violation_count += 1
                    except (ValueError, TypeError):
                        pass
                checked_sat = True
                break
        if not checked_sat:
            # scan any other keys in nutr that might be saturated variants
            for sk, val in nutr.items():
                if "satur" in str(sk).lower() or "sat" == str(sk).lower():
                    try:
                        v = float(val) if val is not None else None
                        if v is not None and v > 100:
                            g.fail(f"barcode={bc}: impossible saturated_fat_g={v} > 100 (per 100g) [key={sk}]")
                            violation_count += 1
                    except (ValueError, TypeError):
                        pass

        # Also check legacy/alt metrics block if present at product root (some schema versions)
        metrics = p.get("metrics") or {}
        for mkey, logical, bound in [
            ("sodium_mg", "sodium_mg", 5000),
            ("protein_g", "protein_g", 100),
            ("fat_g", "fat_g", 100),
            ("fiber_g", "fiber_g", 100),
            ("sugar_g", "sugars_g", 100),
        ]:
            val = metrics.get(mkey)
            if val is not None:
                try:
                    v = float(val)
                    if v > bound:
                        g.fail(f"barcode={bc}: impossible {logical}={v} > {bound} (metrics per 100g)")
                        violation_count += 1
                except (ValueError, TypeError):
                    pass

        # 2) Ingredients field is a nutrition panel
        if _is_nutrition_panel_text(ingredients):
            g.fail(f"barcode={bc}: ingredients field contains nutrition panel text (2+ tokens)")
            violation_count += 1

    if violation_count == 0:
        g.info("No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)")
    else:
        g.info(f"Data sanity violations: {violation_count} across checked products")
    return g


# --------------- G7 PARITY ----------------------------------------------

def gate_parity(frontend, baseline):
    g = GateResult("7 PARITY")
    if baseline is None:
        g.skip("No baseline provided")
        return g

    cur_products = frontend.get("products", [])
    base_products = baseline.get("products", [])

    cur_barcodes = {get_barcode_from_product(p): p for p in cur_products}
    base_barcodes = {get_barcode_from_product(p): p for p in base_products}

    # Product count
    g.info(f"Product count: current={len(cur_products)} baseline={len(base_products)}")

    # Added / removed
    added = sorted(set(cur_barcodes) - set(base_barcodes))
    removed = sorted(set(base_barcodes) - set(cur_barcodes))
    if added:
        g.info(f"Products added vs baseline ({len(added)}): {', '.join(added)}")
    if removed:
        g.info(f"Products removed vs baseline ({len(removed)}): {', '.join(removed)}")

    # Image coverage %
    cur_img = sum(1 for p in cur_products if p.get("imageUrl")) / max(len(cur_products), 1) * 100
    base_img = sum(1 for p in base_products if p.get("imageUrl")) / max(len(base_products), 1) * 100
    g.info(f"Image coverage: current={cur_img:.1f}%  baseline={base_img:.1f}%  delta={cur_img-base_img:+.1f}%")

    # Avg consumer-text chars per product
    def avg_text_chars(products):
        if not products:
            return 0
        total = 0
        for p in products:
            for _, text in _collect_consumer_strings(p):
                total += len(text)
        return total / len(products)

    cur_chars = avg_text_chars(cur_products)
    base_chars = avg_text_chars(base_products)
    g.info(f"Avg consumer-text chars/product: current={cur_chars:.0f}  baseline={base_chars:.0f}  delta={cur_chars-base_chars:+.0f}")

    # Per-barcode grade diffs (products present in both)
    common = sorted(set(cur_barcodes) & set(base_barcodes))
    grade_diffs = []
    for bc in common:
        cg = cur_barcodes[bc].get("grade")
        bg = base_barcodes[bc].get("grade")
        if cg != bg:
            grade_diffs.append((bc, bg, cg))

    if grade_diffs:
        g.info(f"Per-barcode grade changes ({len(grade_diffs)}):")
        for bc, old_g, new_g in grade_diffs:
            name = cur_barcodes[bc].get("name", "")[:40]
            g.info(f"  barcode={bc} [{name}]: {old_g} -> {new_g}")
    else:
        g.info("No grade changes vs baseline")

    # Summary table
    g.info("")
    g.info("=== PARITY SUMMARY TABLE ===")
    g.info(f"  {'Metric':<35} {'Current':>10}  {'Baseline':>10}  {'Delta':>10}")
    g.info(f"  {'Product count':<35} {len(cur_products):>10}  {len(base_products):>10}  {len(cur_products)-len(base_products):>+10}")
    g.info(f"  {'Image coverage %':<35} {cur_img:>10.1f}  {base_img:>10.1f}  {cur_img-base_img:>+10.1f}")
    g.info(f"  {'Avg chars/product':<35} {cur_chars:>10.0f}  {base_chars:>10.0f}  {cur_chars-base_chars:>+10.0f}")
    g.info(f"  {'Grade changes':<35} {len(grade_diffs):>10}  {'—':>10}  {'—':>10}")
    g.info(f"  {'Products added':<35} {len(added):>10}  {'—':>10}  {'—':>10}")
    g.info(f"  {'Products removed':<35} {len(removed):>10}  {'—':>10}  {'—':>10}")

    # Gate 7 never auto-fails
    g.status = "PASS" if g.status not in ("FAIL",) else "PASS"
    return g


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(frontend_path, gates, elapsed_sec):
    lines = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines.append(f"# Bari Page Generator — Gate Report")
    lines.append(f"")
    lines.append(f"**Input:** `{frontend_path}`")
    lines.append(f"**Generated:** {now}  |  **Elapsed:** {elapsed_sec:.1f}s")
    lines.append(f"")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Gate | Status |")
    lines.append(f"|------|--------|")
    for g in gates:
        lines.append(f"| {g.header()} | {g.status} |")
    lines.append("")

    overall = "PASS"
    for g in gates:
        if g.status == "FAIL":
            overall = "FAIL"
            break

    lines.append(f"**Overall: {overall}**")
    lines.append("")

    # Detail per gate
    lines.append("## Detail")
    lines.append("")
    for g in gates:
        lines.append(f"### {g.header()}")
        if g.lines:
            for line in g.lines:
                lines.append(line)
        else:
            lines.append("  (no details)")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import time
    # Force UTF-8 on stdout/stderr (Windows CP1252 default breaks Hebrew output)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time()

    parser = argparse.ArgumentParser(
        description="Bari Page Generator Gate Suite"
    )
    parser.add_argument("frontend_json", help="Path to frontend JSON to validate")
    parser.add_argument("--corpus", help="Path to BSIP1 output directory")
    parser.add_argument("--run", help="Path to BSIP2 run products directory")
    parser.add_argument("--baseline", help="Path to current live JSON for parity check")
    parser.add_argument("--schema", help="Path to JSON Schema file")
    parser.add_argument("--config", help="Path to category gate config JSON")
    args = parser.parse_args()

    # Load inputs
    frontend_path = args.frontend_json
    if not os.path.isfile(frontend_path):
        print(f"ERROR: frontend JSON not found: {frontend_path}", file=sys.stderr)
        sys.exit(1)

    frontend = load_json(frontend_path)
    corpus = load_bsip1_corpus(args.corpus) if args.corpus else {}
    traces = load_bsip2_traces(args.run) if args.run else {}
    baseline = load_json(args.baseline) if args.baseline and os.path.isfile(args.baseline) else None
    config = load_json(args.config) if args.config and os.path.isfile(args.config) else {}

    if corpus:
        print(f"Corpus loaded: {len(corpus)} BSIP1 records from {args.corpus}", file=sys.stderr)
    if traces:
        print(f"Traces loaded: {len(traces)} BSIP2 traces from {args.run}", file=sys.stderr)

    # Run gates
    gates = [
        gate_schema(frontend, args.schema),
        gate_coverage(frontend, corpus),
        gate_scope(frontend, args.run),
        gate_off(frontend, corpus),
        gate_grade_integrity(frontend, traces, config),
        gate_copy_safety(frontend),
        gate_parity(frontend, baseline),
        gate_data_sanity(frontend),
    ]

    elapsed = time.time() - t0

    # Determine exit code
    has_fail = any(g.status == "FAIL" for g in gates)

    # Print summary to stdout
    for g in gates:
        print(f"{g.header()}")
        for line in g.lines:
            print(line)
        print()

    # Write report
    report_path = os.path.join(
        os.path.dirname(os.path.abspath(frontend_path)),
        os.path.basename(frontend_path).replace(".json", "_gates_report.md")
    )
    report_text = build_report(frontend_path, gates, elapsed)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Report written to: {report_path}", file=sys.stderr)
    print(f"Overall: {'FAIL' if has_fail else 'PASS'}", file=sys.stderr)

    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
