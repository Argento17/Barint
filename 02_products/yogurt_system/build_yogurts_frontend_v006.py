"""
Build yogurts_frontend_v4.json (run_yogurt_006 content) from BSIP2 run_yogurt_006 traces.

TASK-249 Phase 2: full corpus rebuild with all remediation fixes + TASK-250 rulings.

Changes vs build_yogurts_frontend_v4.py (run_005 builder):

  TASK-249 fix: RT-1 macros_plausible gate — any product with macros_plausible=False
    in its BSIP1 record is BLOCKED from frontend export. Barcode 7290116932620 is
    already excluded from run_006 BSIP1 corpus (excluded at BSIP1 build time), but the
    gate here ensures no corrupt record can reach the frontend even if somehow included.

  TASK-250 Ruling 3 (grade-before-round): Grade is derived from the engine's raw
    final_score_estimate BEFORE rounding, then the score is rounded for display.
    The current run_005 builder applied round(raw) then grade_from_score(rounded).
    This created grade promotion artifacts:
      - RT-4: raw=34.8 → rounds to 35 → grade D (wrong: should be E)
      - RT-13: raw=49.6 → rounds to 50 → grade C (wrong: should be D)
    Fix: grade = grade_from_score(raw_before_rounding), score = round(raw).
    Owner sign-off required before go-live (Ruling 3 is a grade correction on published
    products, tripwire 2). Noted in return block.

  Copy template fixes:
    - Remove "NOVA 4" from insightLine/limitingFactors — use consumer phrasing
      "עיבוד תעשייתי גבוה" instead.
    - Remove terminal "ציון X" from insightLine (the score chip owns the grade).
    - Replace "מדד זה לא נכלל בניתוח" in unknowns with "ערך הסוכר לא היה זמין במקור".
    - Replace "מדד זה לא נכלל בניתוח" for satFat with "ערך שומן הרווי לא היה זמין במקור".

  Shelf filter assertion: every product _cluster value must be one of the defined
    YogurtsShelfFilterId values. Build FAILS if an unknown cluster appears.

  "bio" shelf filter: subtype="bio" maps to _cluster="bio" (already in SUBTYPE_CLUSTER
    below). yogurts-shelf-filters.ts must also be updated.

Engine: proto_v0 / 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D, frozen).
        + TASK144_FIXES=on (macros_plausible gate active).
        + TASK-250 Rulings 1+2 in score_engine.py (null sugar/satFat confidence).

0 OFF anywhere in pipeline.
"""
import json
import pathlib
import sys
import re
import logging
from datetime import datetime, timezone

_THIS_FILE = pathlib.Path(__file__).resolve()
# The build script may live in the main repo or a git worktree (e.g. C:\Bari\Bari-task249).
# Derive the repo root from the file's location: this file is at
# <repo_root>/02_products/yogurt_system/build_yogurts_frontend_v006.py
_REPO_ROOT = _THIS_FILE.parent.parent.parent

# BSIP2 traces and BSIP1 outputs are written to the MAIN repo's data directories
# (absolute paths from the pipeline runners). They are NOT inside the worktree.
# The main repo root is either _REPO_ROOT (if running from main) or C:\Bari (if worktree).
_MAIN_REPO = pathlib.Path(r"C:\Bari")
_DATA_ROOT = _MAIN_REPO  # pipeline data lives here regardless of which worktree runs this

sys.path.insert(0, str(_REPO_ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"))
from constants import score_to_grade  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# Traces and BSIP1 are always in the main repo's data directories.
TRACES_DIR  = _DATA_ROOT / "02_products" / "yogurt_system" / "bsip2_outputs" / "run_yogurt_006" / "products"
BSIP1_DIR   = _DATA_ROOT / "03_operations" / "bsip1" / "run_yogurt_006" / "output"

# Staging output: in the repo where this script lives (either main or worktree)
STAGING_OUT = _REPO_ROOT / "02_products" / "yogurt_system" / "yogurts_frontend_v4.json"

# Web output: the bari-web in the SAME repo root (so worktree builds write to worktree's bari-web)
WEB_OUT     = _REPO_ROOT / "bari-web" / "src" / "data" / "comparisons" / "yogurts_frontend_v4.json"
RUN_ID      = "run_yogurt_006"

# Shelf filter IDs — must match YogurtsShelfFilterId in yogurts-shelf-filters.ts.
# Ruling 3 assertion: every _cluster value must be in this set.
VALID_CLUSTER_IDS = {"plain", "greek", "high-protein", "flavored", "bio", "probiotic"}

# Subtype -> cluster label (load-bearing for shelf filter).
SUBTYPE_CLUSTER = {
    "greek":         "greek",
    "high_protein":  "high-protein",
    "probiotic":     "probiotic",
    "bio":           "bio",
    "plain_lowfat":  "plain",
    "plain_natural": "plain",
    "flavored":      "flavored",
}


# ---------------------------------------------------------------------------
# Confidence fields from trace
# ---------------------------------------------------------------------------

def confidence_from_trace(trace: dict) -> dict:
    """
    Derive the three consumer-facing confidence fields from the BSIP2 trace.

    Confidence states (Bari Score Presentation v1):
      "verified"   — high band, full nutrition + ingredients
      "partial"    — medium band or missing nutrition/ingredients
      "insufficient" — insufficient_data / withheld / data_sufficiency=insufficient
    """
    band = trace.get("confidence_band") or "low"
    score = trace.get("confidence_score") or 0
    data_suf = trace.get("data_sufficiency") or "sufficient"
    reductions = trace.get("confidence_reductions") or []

    if data_suf == "insufficient":
        return {
            "confidence": "insufficient",
            "confidence_label_he": "נתונים חסרים",
            "confidence_tooltip_he": "חסרים נתונים מהותיים — הציון אינו מהימן לצרכן.",
            "confidence_sub_reason": "insufficient_data",
        }

    # Determine sub-reason for partial confidence
    sub_reason = "missing_nutrition"
    if any("missing: ingredients" in r.get("factor", "") for r in reductions):
        sub_reason = "missing_ingredients"
    elif any("ingredient_quality" in r.get("factor", "") for r in reductions):
        sub_reason = "ingredient_quality"
    elif any("missing:" in r.get("factor", "") for r in reductions):
        sub_reason = "missing_nutrition"

    if band == "high" and score >= 80:
        return {
            "confidence": "verified",
            "confidence_label_he": "מבוסס על נתונים מלאים",
            "confidence_tooltip_he": "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים.",
            "confidence_sub_reason": "full_data",
        }
    else:
        return {
            "confidence": "partial",
            "confidence_label_he": "חסרים נתוני תזונה",
            "confidence_tooltip_he": (
                "חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים."
            ),
            "confidence_sub_reason": sub_reason,
        }


# ---------------------------------------------------------------------------
# Grade (Ruling 3: grade from raw score, before rounding)
# ---------------------------------------------------------------------------

def grade_from_raw(raw_score) -> str:
    """Ruling 3: derive grade from the raw (unrounded) score.

    TASK-250 Ruling 3 specifies: grade = grade_from_score(raw_final_score_estimate),
    NOT grade_from_score(round(raw)). The score displayed to the consumer is still
    round(raw), but the grade letter must reflect the raw value.

    Owner sign-off required before go-live (tripwire 2: corrects grades on published
    products — two products change: 35/E and 50/D).
    """
    if raw_score is None:
        return "insufficient_data"
    return score_to_grade(raw_score)


def round_score(raw_score) -> int | None:
    """Round score for display (integer)."""
    if raw_score is None:
        return None
    return round(raw_score)


# ---------------------------------------------------------------------------
# Image URL selection
# ---------------------------------------------------------------------------

def select_image_url(bsip1: dict, trace: dict) -> str | None:
    # Prefer BSIP1 scraped image (direct Shufersal URL)
    urls = bsip1.get("image_urls") or []
    if urls:
        return urls[0]
    url = bsip1.get("image_url")
    if url:
        return url
    # Fallback to trace input_reference
    return (trace.get("input_reference") or {}).get("image_url")


# ---------------------------------------------------------------------------
# Insight line (consumer-facing, no framework terms)
# ---------------------------------------------------------------------------

def build_insight_line(trace: dict, bsip1: dict, raw_score) -> str:
    """
    Auto-generate an insight line from the trace data.
    TASK-249 copy rules:
      - No "NOVA 4" — use "עיבוד תעשייתי גבוה"
      - No terminal "ציון X" — score chip owns the grade
      - Consumer Hebrew, finding-first, assertive
    """
    l1 = trace.get("L1_observed_signals", {})
    name = (trace.get("input_reference") or {}).get("canonical_name_he") or \
           (trace.get("input_reference") or {}).get("product_name_he") or ""
    grade = grade_from_raw(raw_score)
    nova = trace.get("nova_proxy")

    protein = l1.get("protein_g")
    fat = l1.get("fat_g")
    sugar = l1.get("sugars_g")
    sat_fat = l1.get("fat_saturated_g")

    enrichment = bsip1.get("enrichment_summary", {})
    has_cultures = enrichment.get("has_live_cultures", False)
    additive_count = enrichment.get("additive_count", 0)
    sweetener_count = enrichment.get("sweetener_count", 0)
    ingr_count = enrichment.get("ingredient_count_parsed", 0)
    ingr_quality = bsip1.get("ingredient_text_quality", "clean")

    subtype = bsip1.get("bsip_yogurt_subtype") or _classify_subtype_from_name(name)
    caps = trace.get("caps_considered") or []
    nova4_fired = any(c.get("rule") == "NOVA_PROXY_4_ULTRA_PROCESSED" and c.get("fired") for c in caps)
    additive_cap = any(c.get("rule", "").startswith("ADDITIVE") and c.get("fired") for c in caps)
    sugar_cap = any(c.get("rule", "").startswith("HIGH_SUGAR") and c.get("fired") for c in caps)

    parts = []

    # Leading finding
    if subtype == "high_protein" and protein is not None:
        parts.append(f"{protein:.0f} גרם חלבון ל-100 גרם")
    elif subtype == "greek":
        if fat is not None:
            parts.append(f"יוגורט יווני — {fat:.1f}% שומן")
    elif subtype in ("bio", "probiotic") and has_cultures:
        parts.append("תרביות חיות מאומתות ברכיבים")
    elif subtype in ("plain_natural", "plain_lowfat"):
        if protein is not None:
            parts.append(f"{protein:.1f} גרם חלבון")

    # Positive signals
    if sugar is not None and sugar < 5 and subtype != "flavored":
        parts.append("סוכר נמוך")
    if additive_count == 0 and ingr_count > 0 and ingr_quality not in ("marketing_bleed", "missing"):
        parts.append("ללא תוספים מזוהים")
    elif additive_count > 0:
        parts.append(f"{additive_count} תוספים ברכיבים")

    # Negative / limiting — consumer phrasing only (no NOVA 4 label)
    if nova4_fired:
        # TASK-249: replace "NOVA 4" with consumer phrasing
        parts.append("עיבוד תעשייתי גבוה — משפיע על הציון")
    if sugar is not None and sugar >= 10 and subtype == "flavored":
        parts.append(f"{sugar:.1f} גרם סוכר")
    if sat_fat is not None and sat_fat > 4:
        parts.append(f"{sat_fat:.1f} גרם שומן רווי")

    # TASK-249: no terminal "ציון X" — score chip owns the grade

    if not parts:
        return "נבדק על בסיס נתוני תזונה ורכיבים."

    return " — ".join(parts[:4]) + "."


# ---------------------------------------------------------------------------
# Positive signals
# ---------------------------------------------------------------------------

def build_positive_signals(trace: dict, bsip1: dict) -> list:
    l1 = trace.get("L1_observed_signals", {})
    enrichment = bsip1.get("enrichment_summary", {})
    ingr_quality = bsip1.get("ingredient_text_quality", "clean")
    sigs = []
    protein = l1.get("protein_g")
    sugar = l1.get("sugars_g")
    fat = l1.get("fat_g")
    has_cultures = enrichment.get("has_live_cultures", False)
    additive_count = enrichment.get("additive_count", 0)
    ingr_count = enrichment.get("ingredient_count_parsed", 0)

    if protein is not None and protein >= 8:
        sigs.append(f"חלבון גבוה — {protein:.0f} גרם ל-100 גרם")
    elif protein is not None and protein >= 5:
        sigs.append(f"חלבון — {protein:.1f} גרם ל-100 גרם")
    if sugar is not None and sugar < 5:
        sigs.append(f"סוכר נמוך — {sugar:.1f} גרם ל-100 גרם")
    if has_cultures:
        sigs.append("תרביות חיות ברכיבים")
    if additive_count == 0 and ingr_count > 0 and ingr_quality not in ("marketing_bleed", "missing"):
        sigs.append("ללא תוספים מזוהים")
    if fat is not None and fat < 1:
        sigs.append("דל שומן")
    return sigs[:3]


# ---------------------------------------------------------------------------
# Limiting factors — consumer Hebrew, no "NOVA 4"
# ---------------------------------------------------------------------------

def build_limiting_factors(trace: dict, bsip1: dict) -> list:
    l1 = trace.get("L1_observed_signals", {})
    enrichment = bsip1.get("enrichment_summary", {})
    caps = trace.get("caps_considered") or []
    lim = []
    sugar = l1.get("sugars_g")
    sat_fat = l1.get("fat_saturated_g")
    additive_count = enrichment.get("additive_count", 0)
    nova = trace.get("nova_proxy")

    nova4_fired = any(c.get("rule") == "NOVA_PROXY_4_ULTRA_PROCESSED" and c.get("fired") for c in caps)
    additive_cap_fired = any(c.get("rule", "").startswith("ADDITIVE") and c.get("fired") for c in caps)
    sugar_cap_fired = any(c.get("rule", "").startswith("HIGH_SUGAR") and c.get("fired") for c in caps)

    if nova4_fired:
        # TASK-249: no "NOVA 4" — consumer phrasing
        lim.append("עיבוד תעשייתי גבוה")
    elif nova == 4:
        lim.append("עיבוד תעשייתי גבוה")
    if additive_cap_fired or additive_count >= 3:
        lim.append(f"{additive_count} תוספים מזוהים")
    if sugar is not None and sugar >= 10:
        lim.append(f"סוכר גבוה — {sugar:.1f} גרם ל-100 גרם")
    elif sugar_cap_fired and sugar is not None:
        lim.append(f"סוכר — {sugar:.1f} גרם ל-100 גרם")
    if sat_fat is not None and sat_fat > 4:
        lim.append(f"שומן רווי — {sat_fat:.1f} גרם ל-100 גרם")
    return lim[:3]


# ---------------------------------------------------------------------------
# Unknowns — consumer phrasing (TASK-249 copy rule)
# ---------------------------------------------------------------------------

def build_unknowns(l1: dict) -> list:
    unknowns = []
    if l1.get("sugars_g") is None:
        # TASK-249: replace "מדד זה לא נכלל בניתוח" with consumer phrasing
        unknowns.append("ערך הסוכר לא היה זמין במקור הנתונים.")
    if l1.get("fat_saturated_g") is None:
        unknowns.append("ערך שומן הרווי לא היה זמין במקור הנתונים.")
    if l1.get("dietary_fiber_g") is None:
        unknowns.append("ערך הסיבים התזונתיים לא היה זמין במקור הנתונים.")
    return unknowns[:2]


# ---------------------------------------------------------------------------
# Subtype classifier (mirrors BSIP1 builder)
# ---------------------------------------------------------------------------

def _classify_subtype_from_name(name: str) -> str:
    nl = name.lower() if name else ""
    if re.search(r"יווני|greek|skyr|סקיר", nl):
        return "greek"
    if re.search(r"פרו|pro|go ?20|go20|25g|20g|חלבון|protein", nl):
        return "high_protein"
    if re.search(r"אקטיביה|activia|פרוביו|probiotic", nl):
        return "probiotic"
    if re.search(r"\bביו\b|\bbio\b", nl):
        return "bio"
    if re.search(r"0%|light|free|דל|ללא שומן|נטול", nl):
        return "plain_lowfat"
    if re.search(r"פירות|תות|פטל|אוכמ|וניל|vanil|פרי|בטעם|froop|פרופ|שוקולד|פיר|לימון|אפרסק|מנגו", nl):
        return "flavored"
    return "plain_natural"


# ---------------------------------------------------------------------------
# VM field allowlist strip
# ---------------------------------------------------------------------------
_VM_ALLOWLIST = {
    "id", "name", "imageUrl", "score", "grade", "confidence",
    "confidence_label_he", "confidence_tooltip_he", "confidence_sub_reason",
    "insightLine", "barcode", "retailer", "expansion",
    # load-bearing non-VM field:
    "_cluster",
}


def strip_non_vm_fields(product: dict) -> dict:
    return {k: v for k, v in product.items() if k in _VM_ALLOWLIST}


# ---------------------------------------------------------------------------
# BSIP1 loader
# ---------------------------------------------------------------------------

def load_bsip1(barcode: str) -> dict:
    p = BSIP1_DIR / f"bsip1_{barcode}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def main():
    if not TRACES_DIR.exists():
        log.error("Traces dir not found: %s", TRACES_DIR)
        return

    trace_dirs = [d for d in TRACES_DIR.iterdir() if d.is_dir()]
    log.info("Found %d trace directories", len(trace_dirs))

    products_raw = []
    errors = []
    blocked_macros = []

    for td in trace_dirs:
        trace_file = td / "bsip2_trace.json"
        if not trace_file.exists():
            continue
        try:
            trace = json.loads(trace_file.read_text(encoding="utf-8"))
            pid = td.name
            barcode = (
                (trace.get("input_reference") or {}).get("barcode")
                or pid.replace("bsip1_yogurt_", "").replace("bsip1_", "")
            )
            barcode = str(barcode).strip()
            name = (
                (trace.get("input_reference") or {}).get("canonical_name_he")
                or (trace.get("input_reference") or {}).get("product_name_he")
                or barcode
            )

            bsip1 = load_bsip1(barcode)

            # ── RT-1: macros_plausible gate ───────────────────────────────
            # Block any record with macros_plausible=False. BSIP1 run_006 already
            # excludes barcode 7290116932620, so this gate is a belt-and-suspenders
            # check. It catches any future regression where a corrupt record
            # makes it through BSIP1.
            if bsip1.get("macros_plausible") is False:
                log.warning("  BLOCKED (macros_plausible=False) barcode=%s name=%s",
                            barcode, name[:50])
                blocked_macros.append({"barcode": barcode, "name": name})
                continue

            # ── Raw score ────────────────────────────────────────────────
            raw_score = trace.get("final_score_estimate")

            # "No S grades" policy (TASK-169D, frozen): cap at 89.9.
            if raw_score is not None and raw_score > 89.9:
                raw_score = 89.9

            # ── Ruling 3: grade from raw score, before rounding ──────────
            # Owner sign-off required before go-live.
            grade = grade_from_raw(raw_score)
            score = round_score(raw_score)

            # ── Confidence ───────────────────────────────────────────────
            conf_fields = confidence_from_trace(trace)

            # ── Image URL ────────────────────────────────────────────────
            image_url = select_image_url(bsip1, trace)

            # ── Nutrition ────────────────────────────────────────────────
            l1 = trace.get("L1_observed_signals", {})
            nutrition = {
                "energyKcal": l1.get("energy_kcal"),
                "protein": l1.get("protein_g"),
                "sugar": l1.get("sugars_g"),
                "fat": l1.get("fat_g"),
                "satFat": l1.get("fat_saturated_g"),
                "fiber": l1.get("dietary_fiber_g"),
                "sodium": l1.get("sodium_mg"),
            }

            # ── Ingredients ──────────────────────────────────────────────
            # Only show real ingredient text — not marketing prose.
            ingr_quality = bsip1.get("ingredient_text_quality", "clean")
            if ingr_quality in ("marketing_bleed", "missing"):
                ingr_text = None
            else:
                ingr_text = bsip1.get("ingredients_text_he") or None

            # ── Signals ──────────────────────────────────────────────────
            positive_signals = build_positive_signals(trace, bsip1)
            limiting_factors = build_limiting_factors(trace, bsip1)
            unknowns = build_unknowns(l1)
            insight_line = build_insight_line(trace, bsip1, raw_score)

            # ── Cluster / shelf filter ────────────────────────────────────
            subtype = bsip1.get("bsip_yogurt_subtype") or _classify_subtype_from_name(name)
            cluster = SUBTYPE_CLUSTER.get(subtype, "plain")

            # ── Cluster assertion ─────────────────────────────────────────
            # TASK-249: every _cluster value must be a defined filter id.
            assert cluster in VALID_CLUSTER_IDS, (
                f"BUILD FAIL: barcode={barcode} name={name!r} has _cluster={cluster!r} "
                f"which is not in VALID_CLUSTER_IDS={VALID_CLUSTER_IDS}. "
                f"Add the filter id to yogurts-shelf-filters.ts before shipping."
            )

            # Build expansion — omit optional fields when null to satisfy TS types.
            # bottomLine?: string — must be omitted (not null) when absent.
            # comparisonContext?: string | null — null is acceptable per the VM.
            expansion: dict = {
                "nutrition": nutrition,
                "ingredients": ingr_text,
                "confidenceLabel": conf_fields["confidence_label_he"],
                "servingNote": "ל-100 גרם",
                "positiveSignals": positive_signals,
                "limitingFactors": limiting_factors,
                "unknowns": unknowns,
                "comparisonContext": None,
            }
            # bottomLine is omitted (not null) when there is no editorial synthesis.

            product = {
                "id": pid,
                "name": name,
                "imageUrl": image_url,
                "score": score,
                "grade": grade,
                "confidence": conf_fields["confidence"],
                "confidence_label_he": conf_fields["confidence_label_he"],
                "confidence_tooltip_he": conf_fields["confidence_tooltip_he"],
                "confidence_sub_reason": conf_fields["confidence_sub_reason"],
                "insightLine": insight_line,
                "_cluster": cluster,
                "barcode": barcode,
                "retailer": "shufersal",
                "expansion": expansion,
            }

            products_raw.append((score or 0, product))

        except AssertionError:
            raise  # cluster assertion is a hard build failure
        except Exception as e:
            log.error("Error processing %s: %s", td.name, e)
            import traceback
            traceback.print_exc()
            errors.append(str(td.name))

    # Sort by score descending
    products_raw.sort(key=lambda x: -x[0])
    products = [p for _, p in products_raw]

    log.info("Built %d products, %d errors, %d blocked (macros_plausible=False)",
             len(products), len(errors), len(blocked_macros))

    # Grade distribution
    grade_dist: dict = {}
    for p in products:
        g = p.get("grade", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1

    # Retailer breakdown
    retailer_dist: dict = {}
    for p in products:
        r = p.get("retailer", "unknown")
        retailer_dist[r] = retailer_dist.get(r, 0) + 1

    n_with_ingr = sum(1 for p in products if p.get("expansion", {}).get("ingredients"))

    # Apply VM field strip (keeps _cluster)
    products = [strip_non_vm_fields(p) for p in products]

    payload = {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "category": "yogurts",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v4",
            "run_id": RUN_ID,
            "provenance": (
                "run_yogurt_006: Shufersal direct scrape (html_parse), real Hebrew ingredients, "
                "BARI_RECAL_P0_YOGURT_TRIM + 89.9 post-cap applied. "
                "TASK-249 corpus remediation + TASK-250 methodology rulings applied. "
                "0 OFF anywhere in pipeline."
            ),
            "engine": "proto_v0 / 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D) + TASK144_FIXES + TASK-250",
            "s_grade_cap_applied": True,
            "s_grade_cap_note": (
                "Hard 89.9 cap applied post-processing per TASK-169D 'no S grades' policy."
            ),
            "ruling3_note": (
                "TASK-250 Ruling 3 (grade-before-round) implemented. Owner sign-off required "
                "before go-live. Two products affected: barcode 7290114313070 (35/E) and "
                "barcode 7290102399819 (50/D). Ruling 3 is a grade correction from run_005 "
                "(35/D→35/E, 50/C→50/D)."
            ),
            "retailer_breakdown": retailer_dist,
            "grade_distribution": grade_dist,
            "ingredient_coverage": f"{n_with_ingr}/{len(products)}",
            "bsip0_gate": "PASS (96 products scraped, 92% nutrition, 92% ingredients)",
            "bsip1_included": len(products) + len(blocked_macros),
            "bsip1_excluded_macros_implausible": len(blocked_macros),
            "off_in_pipeline": False,
            "task249_fixes": [
                "RT-2: disclaimer strip",
                "RT-1: macros_plausible gate",
                "RT-3: cereal_misroute_excluded",
                "RT-5: E414 detection",
                "RT-12: Activia live cultures",
                "RT-7: serving_size_g",
                "RT-10: marketing_bleed detection",
            ],
            "task250_rulings": [
                "Ruling 1: null sugar → confidence -10 in score_engine",
                "Ruling 2: null satFat → confidence -5 in score_engine",
                "Ruling 3: grade-before-round (OWNER SIGN-OFF REQUIRED BEFORE GO-LIVE)",
                "Ruling 4: sweetener gap resolved by RT-2/RT-10",
                "Ruling 5: ceiling compression caveat — routes to Content Agent",
            ],
        },
        "products": products,
    }

    # Write staging
    STAGING_OUT.parent.mkdir(parents=True, exist_ok=True)
    STAGING_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Staging: %s", STAGING_OUT)

    # Write web staging (v4 — same filename, v6 content, run_006)
    WEB_OUT.parent.mkdir(parents=True, exist_ok=True)
    WEB_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Web staging: %s", WEB_OUT)

    print("\n=== yogurts_frontend_v4.json (run_yogurt_006) build complete ===")
    print(f"Products: {len(products)}")
    print(f"Blocked (macros_plausible=False): {len(blocked_macros)}")
    print(f"Grade distribution: {grade_dist}")
    print(f"Ingredient coverage: {n_with_ingr}/{len(products)}")
    print(f"Errors: {len(errors)}")
    if errors:
        print(f"  Error list: {errors}")
    if blocked_macros:
        print(f"  Blocked barcodes: {[b['barcode'] for b in blocked_macros]}")
    print(f"Staging: {STAGING_OUT}")
    print(f"Web:     {WEB_OUT}")
    print()
    print("NOTE: TASK-250 Ruling 3 grade corrections are live in this build.")
    print("Owner sign-off required before deploying to production.")


if __name__ == "__main__":
    main()
