"""
BSIP1 Enrichment + BSIP2 Scoring — Brined Cheeses (run_brined_001)
TASK-266, factory run #6

Source: Shufersal BSIP0 scrape — brined_cheese_bsip0_raw_20260613T065721.json
Corpus: 48 IN_SCORED products only (per corpus_filter.json 2026-06-13)
Engine: proto_v0 / score_engine.py — UNMODIFIED (no weight/threshold changes)

Flag config (CRITICAL — per task spec):
  BARI_RECAL_P0=on          — standard dairy path (EV-021 A-ceiling, graded fat penalty R5)
  BARI_RECAL_P0_YOGURT_TRIM=off   — yogurt-specific trim; not applicable here
  BARI_REDLABEL_V1=off      — default off; brined_food 0.7 sodium path governs (score_engine.py:2052)
  BARI_SODIUM_CEREAL=off    — cereal-only scope; off by design for this run
  BARI_TASK144_FIXES=off    — frozen behavior
  BARI_TASK250_CONF=off     — yogurt-only conf rulings; not applicable here
  BARI_GLASSBOX_W4=on       — shipped 2026-06-05 (always on)

Methodology ref: brined_cheeses_scoring_interpretation_v1.md
  - Single pool, dairy_protein category context → EV-021 A-ceiling applies
  - brined_food flag: already wired in evaluation_scope.py (EV-052 / TASK-266)
    keywords: "בולגרית", "פטה", "צפתית", "חלומי", "גבינה מלוחה" + sodium>500 validator
  - sodium_weight=0.7 for brined_food (score_engine.py:1905)
  - HIGH_SODIUM_700MG_PLUS cap rises to 72 (not 60) for brined_food products
  - HP_FAT_SODIUM suppression NOT implemented (D7 deferred) — let it fire, report it
  - Do NOT generate frontend JSON — scoring only

OFF ban: absolute. off_used=0. No field filled from any source other than direct BSIP0 scrape.
"""
import os
import sys
import json
import re
import pathlib
import logging
import datetime
import hashlib

# --- Flag config BEFORE engine imports ---
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "off"
os.environ["BARI_GLASSBOX_D5D6"] = "off"
os.environ["BARI_GLASSBOX_W15"] = "off"
os.environ["BARI_GLASSBOX_W2"] = "off"
# BARI_GLASSBOX_W4 defaults to on (module-level default)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# --- Paths ---
ROOT       = pathlib.Path(r"C:\Bari")
BSIP0_FILE = ROOT / "02_products" / "brined_cheeses" / "bsip0_outputs" / \
             "brined_cheese_bsip0_raw_20260613T065721.json"
CORPUS_FILE = ROOT / "02_products" / "brined_cheeses" / "factory_run_001" / "corpus_filter.json"
BSIP1_OUTPUT = ROOT / "03_operations" / "bsip1" / "run_brined_cheeses_001" / "output"
BSIP2_OUTPUT = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_001"
REPORT_ROOT  = ROOT / "02_products" / "brined_cheeses" / "reports"
RUN_ID = "run_brined_001"

BSIP1_OUTPUT.mkdir(parents=True, exist_ok=True)
(BSIP2_OUTPUT / "products").mkdir(parents=True, exist_ok=True)
REPORT_ROOT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# BSIP1 Enrichment Helpers
# ---------------------------------------------------------------------------

# E-number patterns for NOVA inference
NOVA4_PAT = re.compile(
    r"(E339|E340|E341|E-339|E-340|E-341|פוספט|שמן דקלים|שמן צמחי מוקשה)",
    re.UNICODE,
)
NOVA3_PAT = re.compile(
    r"(עמילן מתוקן|E\d{3,4}[a-z]?|חומר\s+(מייצב|ייצוב|מונע|עיכוב)|קרגינן|"
    r"חומצה ציטרית|גומי זרעי חרובים|אגר|קסנטן|גואר|לוקוסט|כרגינן)",
    re.UNICODE | re.IGNORECASE,
)
E_PAT = re.compile(r"E[-\s]?\d{3,4}[a-z]?", re.IGNORECASE)
# Culture markers for EV-015 fermentation credit
CULTURE_PAT = re.compile(
    r"(תרביות\s+חיידקים|תרבית\s+חיידקים|תרביות\s+פעילות|cultures|"
    r"חיידקי\s+מחמצת|חיידקי\s+גבינה|מחמצת|rennet|קואגולנט|קורנית)",
    re.UNICODE | re.IGNORECASE,
)
# Potassium sorbate / preservatives
PRESERVATIVE_PAT = re.compile(
    r"(פוטסיום\s+סורבאט|חומר\s+משמר|E200|E202|E203|E210|E211|E212|E213|נטריום\s+בנזואט)",
    re.UNICODE | re.IGNORECASE,
)
# Flavor-vs-marker guard: only "תרבית לטעם" disqualifies; "תרביות חיידקים" qualifies
FLAVOR_CULTURE_PAT = re.compile(r"תרבית\s+לטעם", re.UNICODE | re.IGNORECASE)


def parse_float_he(raw: str):
    """Parse Hebrew/comma-formatted numeric string. Returns float or None."""
    if not raw:
        return None
    # Handle "פחות מ X" → treat as X/2 (conservative)
    m = re.search(r"פחות\s+מ\s+([\d.]+)", raw)
    if m:
        return float(m.group(1)) / 2
    # Remove commas (Israeli thousands separator), take first number
    cleaned = raw.replace(",", "").strip()
    m = re.search(r"([\d.]+)", cleaned)
    if m:
        return float(m.group(1))
    return None


def extract_clean_ingredients(raw: str) -> str:
    """
    Extract clean ingredient text from the Shufersal raw dump.
    The Shufersal scraper merges ingredients + nutrition table + disclaimer into one string.
    Algorithm:
      1. Find LAST 'הנתונים המדויקים' — cut everything from that point.
      2. Find LAST 'יתכנו טעויות' — cut everything from that point.
      3. Find 'מכיל חלב' or 'מכיל:' — cut everything from that point (allergen boilerplate).
      4. Clean up trailing nutrition-table fragments (digits + Hebrew units).
      5. Strip whitespace; if result < 5 chars, return "".
    """
    if not raw:
        return ""
    text = raw

    # Cut at disclaimer markers
    for marker in ["הנתונים המדויקים", "יתכנו טעויות", "התמונות והתאריכים"]:
        idx = text.rfind(marker)
        if idx != -1:
            text = text[:idx]

    # Cut at allergen boilerplate (but keep "מכיל חלב" as a marker that text before is ingredient)
    allergen_markers = ["מכיל חלב", "מכיל:", "עלול להכיל"]
    for am in allergen_markers:
        idx = text.rfind(am)
        if idx != -1:
            text = text[:idx]

    # Remove trailing nutrition-table fragments (common: " 100 גרם 2.4 גרם ...")
    text = re.sub(r"\s*100\s+גרם.*$", "", text.strip(), flags=re.UNICODE)
    text = re.sub(r"\s*\d+[\d.,]*\s*(גרם|מג|קל|kcal|mg|g)\b.*$", "", text.strip(), flags=re.UNICODE)

    text = text.strip().rstrip(",. ")
    if len(text) < 5:
        return ""
    return text


def infer_nova_brined(ing_text: str, additives: list) -> dict:
    """
    NOVA inference for brined cheese.
    NOVA 1: minimal (milk/goat-milk/sheep-milk + salt + rennet/cultures), no E-numbers
    NOVA 2: one non-controversial E-number or CaCl2 only
    NOVA 3: stabilizers, preservatives, modified starch, gums (non-phosphate)
    NOVA 4: phosphate emulsifiers (processed cheese), hydrogenated oil
    No ingredient text: default NOVA 2 / low confidence
    """
    if not ing_text:
        return {
            "nova_proxy": 2,
            "nova_confidence": 0.30,
            "nova_confidence_band": "low",
            "nova_notes": ["no_ingredient_text: NOVA 2 default (low confidence)"],
        }

    has_nova4 = bool(NOVA4_PAT.search(ing_text))
    if has_nova4:
        return {
            "nova_proxy": 4,
            "nova_confidence": 0.90,
            "nova_confidence_band": "high",
            "nova_notes": ["phosphates_or_hydrogenated_fat: NOVA 4"],
        }

    # E-numbers detected
    e_numbers = E_PAT.findall(ing_text)
    e_count = len(e_numbers)

    has_nova3 = bool(NOVA3_PAT.search(ing_text)) or e_count >= 2
    if has_nova3:
        return {
            "nova_proxy": 3,
            "nova_confidence": 0.80,
            "nova_confidence_band": "high",
            "nova_notes": [f"stabilizers_or_preservatives: NOVA 3 (e_count={e_count}, additives={additives[:3]})"],
        }

    # CaCl2 (E509) is a coagulation aid in cheese — single E-number, not NOVA 3
    # Calcium chloride alone → NOVA 1 still
    if e_count == 1:
        return {
            "nova_proxy": 2,
            "nova_confidence": 0.70,
            "nova_confidence_band": "medium",
            "nova_notes": [f"single_E_number ({e_numbers[0]}): NOVA 2"],
        }

    # Clean: milk/goat/sheep + salt + cultures/rennet
    return {
        "nova_proxy": 1,
        "nova_confidence": 0.88,
        "nova_confidence_band": "high",
        "nova_notes": ["minimal_ingredients_milk_salt_cultures_rennet: NOVA 1"],
    }


def detect_additives_list(ing_text: str) -> list:
    """Detect E-numbers and named additives."""
    if not ing_text:
        return []
    found = list(set(E_PAT.findall(ing_text)))
    # Named additives
    named = []
    if "פוטסיום סורבאט" in ing_text or "חומר משמר" in ing_text:
        named.append("preservative")
    if "גומי זרעי חרובים" in ing_text:
        named.append("E410_locust_bean_gum")
    if "אגר" in ing_text:
        named.append("E406_agar")
    if "קרגינן" in ing_text or "קסנטן" in ing_text:
        named.append("E407_carrageenan_or_xanthan")
    if "עמילן מתוקן" in ing_text:
        named.append("modified_starch")
    return sorted(set(found + named))


def detect_live_cultures(ing_text: str) -> bool:
    """EV-015: true only if confirmed culture marker, with flavor-vs-marker guard."""
    if not ing_text:
        return False
    if FLAVOR_CULTURE_PAT.search(ing_text):
        return False  # "תרבית לטעם" is flavor, not live culture
    return bool(CULTURE_PAT.search(ing_text))


def normalize_nutrition(n: dict) -> dict:
    """Parse raw nutrition fields from BSIP0 format to normalized per-100g dict."""
    return {
        "energy_kcal":      parse_float_he(n.get("energy_kcal_raw", "")),
        "fat_g":            parse_float_he(n.get("fat_raw", "")),
        "fat_saturated_g":  parse_float_he(n.get("saturated_fat_raw", "")),
        "fat_trans_g":      None,
        "sodium_mg":        parse_float_he(n.get("sodium_raw", "")),
        "carbohydrates_g":  parse_float_he(n.get("carbs_raw", "")),
        "sugars_g":         parse_float_he(n.get("sugar_raw", "")),
        "dietary_fiber_g":  parse_float_he(n.get("fiber_raw", "")),
        "protein_g":        parse_float_he(n.get("protein_raw", "")),
    }


def build_bsip1(product: dict, ts: str) -> dict:
    """Build BSIP1 product record from BSIP0 raw product."""
    barcode  = str(product.get("barcode", ""))
    name_he  = product.get("name_he", "")
    brand    = product.get("brand", "")
    raw_ing  = product.get("ingredients_raw", "")
    image_urls = product.get("image_urls", [])
    image_url  = image_urls[0] if image_urls else None
    price    = product.get("price")
    source_url = product.get("source_url", "")
    scraped_at = product.get("scraped_at", "")

    nn = normalize_nutrition(product.get("nutrition", {}))

    # Ingredient extraction (EV-015 + §4.5 flavor-vs-marker guard)
    ing_text = extract_clean_ingredients(raw_ing)
    additives = detect_additives_list(ing_text)
    nova_result = infer_nova_brined(ing_text, additives)
    has_live_cultures = detect_live_cultures(ing_text)
    has_preservatives = bool(PRESERVATIVE_PAT.search(ing_text)) if ing_text else False

    # Ingredient list (comma/semicolon split)
    ing_list = [p.strip().rstrip(".") for p in re.split(r"[,;]", ing_text) if p.strip() and len(p.strip()) > 1] if ing_text else []

    # Consistency checks
    sugar   = nn.get("sugars_g")
    carbs   = nn.get("carbohydrates_g")
    sat_fat = nn.get("fat_saturated_g")
    fat     = nn.get("fat_g")
    kcal    = nn.get("energy_kcal")
    prot    = nn.get("protein_g")

    sugar_le_carbs = True if (sugar is None or carbs is None) else (sugar <= carbs + 0.15)
    satfat_le_fat  = True if (sat_fat is None or fat is None) else (sat_fat <= fat + 0.15)
    kcal_plausible = True if kcal is None else (50 <= kcal <= 600)
    macros_ok      = True if prot is None else (prot < 100)

    missing = [k for k, v in nn.items() if v is None and k in ("energy_kcal", "fat_g", "protein_g", "sodium_mg")]

    trust_score = 0.75
    risk_flags = ["single_source_shufersal"]
    if not (sugar_le_carbs and satfat_le_fat):
        trust_score -= 0.2
        risk_flags.append("consistency_warning")
    if not kcal_plausible:
        trust_score -= 0.1
        risk_flags.append("kcal_implausible")
    if not ing_text:
        trust_score -= 0.1
        risk_flags.append("no_ingredient_text")
    trust_score = round(max(0.1, min(1.0, trust_score)), 2)
    trust_level = "high" if trust_score >= 0.80 else ("medium" if trust_score >= 0.50 else "low")

    doc = {
        "schema_version":              "bsip1_v0_1",
        "file_type":                   "product",
        "canonical_product_id":        f"bsip1_brinedcheese_{barcode}",
        "barcode":                     barcode,
        "canonical_name_he":           name_he,
        "brand":                       brand,
        "weight_g":                    None,
        "category":                    "dairy_protein",
        "bsip_cheese_subpool":         "brined_cheese",
        "source_retailers":            ["shufersal"],
        "retailer_prices":             {"shufersal": float(price) if price else None},
        "image_url":                   image_url,
        "normalized_nutrition_per_100g": nn,
        "energy_kcal":                 nn.get("energy_kcal"),
        "fat_g":                       nn.get("fat_g"),
        "fat_saturated_g":             nn.get("fat_saturated_g"),
        "fat_trans_g":                 None,
        "protein_g":                   nn.get("protein_g"),
        "carbohydrates_g":             nn.get("carbohydrates_g"),
        "sugars_g":                    nn.get("sugars_g"),
        "sodium_mg":                   nn.get("sodium_mg"),
        "dietary_fiber_g":             nn.get("dietary_fiber_g"),
        "calcium_mg":                  None,
        "ingredients_text_he":         ing_text if ing_text else None,
        "ingredients_list":            ing_list,
        "ingredient_count":            len(ing_list),
        "ingredient_text_quality":     "good" if len(ing_list) >= 2 else ("present" if ing_text else "absent"),
        "allergens_contains":          ["milk"],
        "allergens_may_contain":       [],
        "off_source_used":             False,
        "nova_proxy":                  nova_result["nova_proxy"],
        "nova_confidence":             nova_result["nova_confidence"],
        "nova_confidence_band":        nova_result["nova_confidence_band"],
        "nova_notes":                  nova_result["nova_notes"],
        "detected_additives":          additives,
        "additive_count":              len(additives),
        "has_live_cultures_bsip1":     has_live_cultures,
        "has_preservatives_bsip1":     has_preservatives,
        "confidence":                  trust_score,
        "canonical_trust_level":       trust_level,
        "canonical_trust_score":       trust_score,
        "canonical_risk_flags":        risk_flags,
        "missing_fields":              missing,
        "inferred_fields":             [],
        "consistency_checks":          {
            "sugar_le_carbs": sugar_le_carbs,
            "satfat_le_fat":  satfat_le_fat,
            "kcal_plausible": kcal_plausible,
            "macros_ok":      macros_ok,
        },
        "nutrition_consistency_status": "consistent" if (sugar_le_carbs and satfat_le_fat) else "warnings",
        "data_sufficiency":            "sufficient",
        "bsip1_trust_level":           trust_level,
        "bsip1_trust_score":           trust_score,
        "bsip1_risk_flags":            risk_flags,
        "provenance": {
            "source":              "shufersal_direct_scrape",
            "fetched_at":          scraped_at,
            "source_url":          source_url,
            "panel_source":        "shufersal_storefront",
            "verification_status": "candidate",
            "off_used":            False,
        },
        "enrichment_timestamp":        ts,
        "run_id":                      RUN_ID,
    }
    return doc


# ---------------------------------------------------------------------------
# BSIP2 pipeline
# ---------------------------------------------------------------------------

def run_bsip2_pipeline(bsip1_product: dict) -> dict:
    """Run full BSIP2 scoring pipeline on a BSIP1 product record."""
    signals      = extract_signals(bsip1_product)
    cat_result   = classify_category(bsip1_product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(bsip1_product, l3)
    eval_result  = assign_evaluation_scope(bsip1_product, cat_result["category"])
    score_result = score_product(bsip1_product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(bsip1_product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    log.info("=== BSIP1 + BSIP2 Brined Cheeses — %s ===", RUN_ID)
    log.info("Flags: RECAL_P0=on | REDLABEL_V1=off | SODIUM_CEREAL=off | TASK250_CONF=off")
    log.info("Category context: dairy_protein (EV-021 A-ceiling applies)")
    log.info("Sodium path: brined_food 0.7 weight (EV-052 wired in evaluation_scope.py)")

    # Load corpus filter — build IN_SCORED barcode set
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored_barcodes = {
        str(p["barcode"]) for p in corpus["products"]
        if p["decision"] == "IN_SCORED"
    }
    log.info("IN_SCORED barcodes from corpus_filter: %d", len(in_scored_barcodes))

    # Load BSIP0
    bsip0_raw = json.loads(BSIP0_FILE.read_text(encoding="utf-8"))
    all_products = bsip0_raw  # top-level array

    # Filter to IN_SCORED only
    to_score = [p for p in all_products if str(p.get("barcode", "")) in in_scored_barcodes]
    log.info("BSIP0 products matched to IN_SCORED: %d", len(to_score))

    if len(to_score) != 48:
        log.warning("Expected 48 IN_SCORED, got %d — check barcode alignment", len(to_score))

    # -----------------------------------------------------------------------
    # Stage 4: BSIP1 Enrichment
    # -----------------------------------------------------------------------
    log.info("--- Stage 4: BSIP1 Enrichment ---")
    bsip1_records = []
    bsip1_errors  = []
    nova_dist = {}
    ing_coverage = 0

    for product in to_score:
        barcode = str(product.get("barcode", ""))
        name    = product.get("name_he", "")
        try:
            doc = build_bsip1(product, ts)
            out_path = BSIP1_OUTPUT / f"bsip1_brinedcheese_{barcode}.json"
            out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            bsip1_records.append(doc)
            if doc.get("ingredients_text_he"):
                ing_coverage += 1
            nk = f"NOVA_{doc['nova_proxy']}"
            nova_dist[nk] = nova_dist.get(nk, 0) + 1
            log.info("  BSIP1 %-40s NOVA=%s ing=%s cultures=%s",
                     name[:38], doc["nova_proxy"],
                     "yes" if doc.get("ingredients_text_he") else "no",
                     doc["has_live_cultures_bsip1"])
        except Exception as e:
            log.error("  BSIP1 ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            bsip1_errors.append({"barcode": barcode, "name": name, "error": str(e)})

    log.info("BSIP1 done. Enriched=%d errors=%d NOVA=%s ing_coverage=%d/%d",
             len(bsip1_records), len(bsip1_errors), nova_dist, ing_coverage, len(to_score))

    # Coverage gate: warn if <15% have ingredient text
    ing_pct = ing_coverage / len(to_score) * 100 if to_score else 0
    if ing_pct < 15:
        log.warning("COVERAGE GATE WARNING: only %.0f%% have ingredient text (threshold 15%%)", ing_pct)
    else:
        log.info("Coverage gate: %.0f%% ingredient text coverage (gate=15%%) — PASS", ing_pct)

    # -----------------------------------------------------------------------
    # Stage 5: BSIP2 Scoring
    # -----------------------------------------------------------------------
    log.info("--- Stage 5: BSIP2 Scoring ---")
    traces = []
    score_errors = []
    brined_flag_fired = []
    brined_flag_not_fired = []
    hp_fat_sodium_fired = []

    for doc in bsip1_records:
        barcode = doc.get("barcode", "")
        name    = doc.get("canonical_name_he", "")
        try:
            trace = run_bsip2_pipeline(doc)
            write_trace(trace, BSIP2_OUTPUT)
            traces.append(trace)

            score   = trace.get("final_score_estimate")
            grade   = trace.get("grade_estimate")
            cat     = trace.get("category")
            nova    = trace.get("nova_proxy")
            ctx_flag = trace.get("evaluation_scope", {}).get("context_flag")
            sodium_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") or 0

            # brined_food flag check
            if ctx_flag == "brined_food":
                brined_flag_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val, "score": score, "grade": grade,
                })
            else:
                brined_flag_not_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val,
                    "ctx_flag": ctx_flag,
                    "score": score, "grade": grade,
                    "note": "sodium<=500 or name not matched" if sodium_val <= 500 else "name not matched",
                })

            # HP_FAT_SODIUM_COMBO check
            caps_list = trace.get("score_detail", {}).get("penalties_applied", []) or []
            pens_list = trace.get("score_detail", {}).get("penalties_applied", []) or []
            # Also check caps_considered
            caps_considered = trace.get("score_detail", {}).get("caps_considered", []) or []
            pens_considered = trace.get("score_detail", {}).get("penalties_considered", []) or []
            hp_fired = any(
                x.get("rule") == "HP_FAT_SODIUM_COMBO"
                for x in (pens_list + pens_considered)
                if x.get("fired", True)
            )
            if hp_fired:
                fat_val = (doc.get("normalized_nutrition_per_100g") or {}).get("fat_g") or 0
                hp_fat_sodium_fired.append({
                    "barcode": barcode, "name": name,
                    "fat_g": fat_val, "sodium_mg": sodium_val,
                    "score": score, "grade": grade,
                })

            log.info("  BSIP2 %-40s score=%-5s grade=%-2s cat=%-14s nova=%s ctx=%s",
                     name[:38], score, grade, cat, nova, ctx_flag or "standard")
        except Exception as e:
            log.error("  BSIP2 ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": barcode, "name": name, "error": str(e)})

    # -----------------------------------------------------------------------
    # Score distribution analysis
    # -----------------------------------------------------------------------
    all_scores = [t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None]
    grade_dist = {}
    for t in traces:
        g = t.get("grade_estimate", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1

    if all_scores:
        scores_sorted = sorted(all_scores)
        n = len(scores_sorted)
        median = scores_sorted[n // 2] if n % 2 else (scores_sorted[n//2 - 1] + scores_sorted[n//2]) / 2
        score_min = min(all_scores)
        score_max = max(all_scores)
    else:
        median = score_min = score_max = None

    # Score histogram (10-point bands)
    histogram = {}
    for s in all_scores:
        band = f"{int(s // 10) * 10}-{int(s // 10) * 10 + 9}"
        histogram[band] = histogram.get(band, 0) + 1

    # Anti-collapse verdict
    score_range = (score_max - score_min) if (score_max is not None and score_min is not None) else 0
    num_grade_bands = len([g for g in grade_dist if g not in ("?", None)])
    if score_range >= 20 and num_grade_bands >= 2:
        anti_collapse_result = "SPREAD_HONEST: range={:.1f} pts ({:.1f}–{:.1f}), {} grade bands — genuine differentiation".format(
            score_range, score_min, score_max, num_grade_bands)
    elif score_range < 10:
        anti_collapse_result = "CLUSTERED: range={:.1f} pts ({:.1f}–{:.1f}), {} grade bands — honest finding (butter rule)".format(
            score_range, score_min or 0, score_max or 0, num_grade_bands)
    else:
        anti_collapse_result = "MODERATE_SPREAD: range={:.1f} pts ({:.1f}–{:.1f}), {} grade bands".format(
            score_range, score_min or 0, score_max or 0, num_grade_bands)

    # Top 3 and bottom 3
    traces_scored = [t for t in traces if t.get("final_score_estimate") is not None]
    traces_sorted = sorted(traces_scored, key=lambda t: t.get("final_score_estimate", 0), reverse=True)

    def extract_top_drivers(trace):
        """Pull top scoring drivers from trace."""
        sd = trace.get("score_detail") or {}
        bonuses = sd.get("bonuses_applied") or []
        caps = [c for c in (sd.get("caps_applied") or []) if c.get("cap") is not None]
        pens = sd.get("penalties_applied") or []
        drivers = []
        for b in bonuses[:3]:
            drivers.append(f"+{b.get('amount','?')} {b.get('rule','?')}")
        for p in pens[:3]:
            drivers.append(f"-{p.get('amount','?')} {p.get('rule','?')}")
        for c in caps[:2]:
            drivers.append(f"cap={c.get('cap','?')} {c.get('rule','?')}")
        return drivers or ["(no drivers in trace)"]

    top3 = []
    for t in traces_sorted[:3]:
        top3.append({
            "barcode": (t.get("input_reference") or {}).get("barcode") or t.get("barcode"),
            "name": (t.get("input_reference") or {}).get("canonical_name_he") or t.get("canonical_name_he"),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "nova": t.get("nova_proxy"),
            "drivers": extract_top_drivers(t),
        })
    bottom3 = []
    for t in traces_sorted[-3:]:
        bottom3.append({
            "barcode": (t.get("input_reference") or {}).get("barcode") or t.get("barcode"),
            "name": (t.get("input_reference") or {}).get("canonical_name_he") or t.get("canonical_name_he"),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "nova": t.get("nova_proxy"),
            "drivers": extract_top_drivers(t),
        })

    # -----------------------------------------------------------------------
    # Run record
    # -----------------------------------------------------------------------
    run_record = {
        "run_id":          RUN_ID,
        "task":            "TASK-266",
        "category_slug":   "brined-cheeses",
        "category_context": "dairy_protein",
        "generated":       ts,
        "engine":          "proto_v0 / score_engine.py (unmodified)",
        "flag_config": {
            "BARI_RECAL_P0":            "on",
            "BARI_RECAL_P0_YOGURT_TRIM":"off",
            "BARI_REDLABEL_V1":         "off",
            "BARI_SODIUM_CEREAL":       "off",
            "BARI_TASK144_FIXES":       "off",
            "BARI_TASK250_CONF":        "off",
            "BARI_GLASSBOX_D5D6":       "off",
            "BARI_GLASSBOX_W15":        "off",
            "BARI_GLASSBOX_W2":         "off",
            "BARI_GLASSBOX_W4":         "on (default)",
        },
        "sodium_path":     "brined_food 0.7 weight (EV-052) — fires when name keyword matches AND sodium>500",
        "hp_suppression":  "NOT implemented (D7 deferred) — HP_FAT_SODIUM fires if conditions met",
        "off_used":        False,
        "corpus_source":   str(CORPUS_FILE),
        "bsip0_source":    str(BSIP0_FILE),
        "in_scored_count": len(in_scored_barcodes),
        "bsip0_matched":   len(to_score),
        "bsip1": {
            "output_dir":   str(BSIP1_OUTPUT),
            "enriched":     len(bsip1_records),
            "errors":       len(bsip1_errors),
            "ing_coverage": f"{ing_coverage}/{len(to_score)} ({ing_pct:.0f}%)",
            "nova_dist":    nova_dist,
        },
        "bsip2": {
            "output_dir":   str(BSIP2_OUTPUT),
            "scored":       len(traces),
            "errors":       len(score_errors),
        },
        "score_distribution": {
            "min":       score_min,
            "max":       score_max,
            "median":    median,
            "range":     score_range if score_range else None,
            "histogram": histogram,
            "grade_dist": grade_dist,
        },
        "anti_collapse_verdict": anti_collapse_result,
        "brined_flag": {
            "fired_count":     len(brined_flag_fired),
            "not_fired_count": len(brined_flag_not_fired),
            "not_fired_list":  brined_flag_not_fired,
        },
        "hp_fat_sodium": {
            "fired_count": len(hp_fat_sodium_fired),
            "fired_list":  hp_fat_sodium_fired,
        },
        "top3":    top3,
        "bottom3": bottom3,
        "errors":  score_errors + bsip1_errors,
    }

    run_record_path = BSIP2_OUTPUT / "run_record.json"
    run_record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", run_record_path)

    # Summary JSON for reporting
    summary = {
        "run_id":          RUN_ID,
        "generated":       ts,
        "task":            "TASK-266",
        "flag_config":     run_record["flag_config"],
        "scored":          len(traces),
        "errors":          len(score_errors),
        "score_distribution": run_record["score_distribution"],
        "anti_collapse":   anti_collapse_result,
        "brined_flag_fired": len(brined_flag_fired),
        "brined_flag_not_fired": len(brined_flag_not_fired),
        "hp_fat_sodium_fired": len(hp_fat_sodium_fired),
        "off_used": False,
        "products": [{
            "barcode": t.get("barcode") or (t.get("input_reference") or {}).get("barcode"),
            "name":    (t.get("input_reference") or {}).get("canonical_name_he") or t.get("canonical_name_he"),
            "score":   t.get("final_score_estimate"),
            "grade":   t.get("grade_estimate"),
            "category": t.get("category"),
            "nova":    t.get("nova_proxy"),
            "context_flag": (t.get("evaluation_scope") or {}).get("context_flag"),
            "binding_cap":  t.get("binding_cap"),
        } for t in traces],
    }
    summary_path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", summary_path)

    # -----------------------------------------------------------------------
    # Console report
    # -----------------------------------------------------------------------
    print("\n" + "="*70)
    print(f"BRINED CHEESES BSIP2 RUN — {RUN_ID}")
    print("="*70)
    print(f"Flag config: RECAL_P0=on | REDLABEL_V1=off | SODIUM_CEREAL=off")
    print(f"Category context: dairy_protein | EV-021 A-ceiling active")
    print(f"Sodium path: brined_food 0.7 weight (EV-052)")
    print()
    print(f"Corpus: {len(in_scored_barcodes)} IN_SCORED | matched in BSIP0: {len(to_score)}")
    print(f"BSIP1 enriched: {len(bsip1_records)} | NOVA dist: {nova_dist}")
    print(f"Ingredient coverage: {ing_coverage}/{len(to_score)} ({ing_pct:.0f}%)")
    print()
    print(f"BSIP2 scored: {len(traces)} | errors: {len(score_errors)}")
    print()
    print("SCORE DISTRIBUTION:")
    print(f"  Min: {score_min}  Max: {score_max}  Median: {median}")
    print(f"  Range: {score_range:.1f} pts")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print(f"  Grade distribution: {dict(sorted(grade_dist.items()))}")
    print()
    print(f"ANTI-COLLAPSE VERDICT: {anti_collapse_result}")
    print()
    print(f"BRINED_FOOD FLAG:")
    print(f"  Fired: {len(brined_flag_fired)}/{len(traces)}")
    if brined_flag_not_fired:
        print(f"  NOT fired (expected — sodium<=500):")
        for p in brined_flag_not_fired:
            print(f"    {p['barcode']} {p['name'][:35]} sodium={p['sodium_mg']} reason={p['note']}")
    print()
    print(f"HP_FAT_SODIUM_COMBO fired: {len(hp_fat_sodium_fired)}")
    if hp_fat_sodium_fired:
        print("  Products with HP_FAT_SODIUM_COMBO (D7 deferred — report only):")
        for p in hp_fat_sodium_fired:
            print(f"    {p['barcode']} {p['name'][:35]} fat={p['fat_g']}g sodium={p['sodium_mg']}mg score={p['score']}")
    print()
    print("TOP 3:")
    for i, p in enumerate(top3, 1):
        print(f"  {i}. [{p['score']}/{p['grade']}] {p['name'][:50]}")
        print(f"     Drivers: {'; '.join(p['drivers'][:3])}")
    print()
    print("BOTTOM 3:")
    for i, p in enumerate(bottom3, 1):
        print(f"  {i}. [{p['score']}/{p['grade']}] {p['name'][:50]}")
        print(f"     Drivers: {'; '.join(p['drivers'][:3])}")
    print()
    print(f"Run record:  {run_record_path}")
    print(f"Summary:     {summary_path}")
    print(f"BSIP1 dir:   {BSIP1_OUTPUT}")
    print(f"BSIP2 dir:   {BSIP2_OUTPUT}")
    print("="*70)

    return run_record


if __name__ == "__main__":
    main()
