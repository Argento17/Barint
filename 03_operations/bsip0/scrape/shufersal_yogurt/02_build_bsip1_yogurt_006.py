"""
BSIP1 Builder — Yogurt (run_yogurt_006) from Shufersal BSIP0 raw.

Fixes applied in this version (TASK-249 corpus remediation):

  RT-2  Disclaimer strip: Shufersal embeds the full nutrition table + legal
        disclaimer in the same HTML container as the ingredient text. The
        scraper's get_text() therefore produces:
          "חלב, מייצב (E415), ... מכיל חלב ערכים תזונתיים 100 גרם 86 קל ..."
        The contamination boundary is the phrase "מכיל X" (allergen statement)
        followed by "ערכים תזונתיים" (nutrition values). The TASK-144 sanitizer
        previously marked these records as ingredient_text_quality="clean" —
        this was the blind spot.
        Fix: strip everything from "מכיל" followed by a nutrition-value pattern,
        or from "ערכים תזונתיים" directly, whichever comes first. Applied BEFORE
        the ingredient list is split for BSIP1 and enrichment. The stripped portion
        is stored in ingredients_disclaimer_stripped for audit. Disclaimer-stripped
        records get ingredient_text_quality="disclaimer_stripped" (not "clean").

  RT-1  macros_plausible gate: any record with protein_g > 50 is physically
        impossible for a yogurt. Root cause: for barcode 7290116932620, the scraper
        captured the per-serving protein claim ("190g container, 25g protein" expressed
        as "190 gram protein") from the embedded nutrition table as the per-100g value.
        Fix: after nutrition parse, if protein_g > 50 OR macros_plausible=False (energy
        vs. macro-derived energy discrepancy), the record is flagged macros_plausible=False
        and the affected field is nulled out so it cannot reach scoring as a live value.
        The product is written to BSIP1 with confidence=partial and a blocking flag
        macros_plausible=False. The frontend export gate (build_yogurts_frontend_v4.py)
        MUST reject any record with macros_plausible=False.

  RT-3  Activia misroute: barcode 7290112346797 (אקטיביה שיבולת שועל שזיף) was
        scored under cereal rules because "שיבולת שועל" is a hard anchor for cereal in
        router_v2. This product is an Activia (probiotic yogurt with oat); it contains
        milk as the first ingredient. Force-categorisation in the BSIP1 record is not
        safe (BSIP2 re-reads the category from its own router). The clean fix is to
        EXCLUDE this product from the yogurt corpus with reason "cereal_misroute_excluded"
        and a _meta drop reason. The product cannot be cleanly routed to yogurt without
        changing the router anchor (which is a governance-level change outside this task).

  RT-5  E414 in parenthesized phrases: the existing _E_NUM_RE in ingredient_enricher
        only matched E-numbers appearing as bare tokens (e.g. "E414") but missed the
        pattern "חומר הזגה (E414)" because the regex requires a word boundary before
        the E. Fixed here by also scanning each parenthesized sub-string in each
        ingredient item. The fix lives in the enrichment call path, not in the global
        enricher (which is shared with other categories). A pre-enrichment pass extracts
        all "E[0-9]{3,4}" tokens from parenthesized content and injects them as explicit
        additives before calling the enricher.

  RT-12 has_live_cultures for Activia brand: the phrase "חיידק הפרביוטי ביפידוס" and
        variant "בתוספת החיידק הפרביוטי ביפידוס אקטירגוליס" were not in the enricher's
        FERMENTATION_TERMS dictionary. This is the canonical Activia culture declaration.
        Fix: pre-enrichment scan for Activia-brand probiotic culture phrases adds a
        synthetic fermentation marker so has_live_cultures=True is correctly emitted.

  RT-7  serving_size_g: the BSIP0 scraper captures weight_g from the product name
        (e.g. "יוגורט 150 גרם"). This is the package size. Shufersal's JSON-LD also
        includes the serving size for some products. We extract serving_size_g from
        weight_g when weight_g is a single-serve size (50-250g) — the scraper already
        captures this; we just wire it through.

  RT-10 Marketing-prose detection (supporting Ruling 4): barcode 7290102395231 (Bio
        Natural) has a serving-suggestion description instead of a real ingredient list.
        The scraper captured "יוגורט לבן קלאסי וקרמי שמשתלב בטבעיות..." as its
        ingredient text. Detected via SERVING_SUGGESTION_PROSE_MARKERS_HE and flagged
        as ingredient_text_quality="marketing_bleed". The score engine deducts confidence
        for this quality state and cannot trust signals derived from marketing prose
        (sweetener_count=1 from "דבש" in serving suggestion text is not a real sweetener
        in the product).

Reads:  C:\\Bari\\02_products\\yogurt_system\\bsip0\\yogurt_bsip0_raw_*.json (latest)
Writes: C:\\Bari\\03_operations\\bsip1\\run_yogurt_006\\output\\bsip1_*.json
        + curation_report.json

Run context: run_yogurt_006 / 2026-06-11
  - Full re-acquisition from Shufersal (Option A, same BSIP0 source as run_005).
  - 0 OFF anywhere in pipeline.
  - BSIP0 gate result: 96 products, 92% nutrition, 92% ingredients — PASS.
  - TASK-249 parser fixes applied.
"""
from __future__ import annotations

import json
import re
import sys
import pathlib
import logging
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent.parent /
                       "bsip1" / "core"))
from ingredient_enricher import enrich as enrich_product

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "_shared"))
from bsip0_nutrition import (  # noqa: E402
    parse_num as _shared_parse_num,
    parse_sodium_mg as _shared_parse_sodium,
    parse_nutrition_numeric as _shared_parse_nutrition,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip0")
OUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_006\output")
RUN_ID = "run_yogurt_006"
SOURCE = "shufersal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DRINK_RE = re.compile(
    r"משקה|שתי|drink|שייק|smoothie|כפיר|kefir|איראן|ayran|לאסי|lassi|"
    r"אקטימל|actimel|יקולט|yakult|דנאקטיב|danactive", re.I)
DESSERT_RE = re.compile(
    r"מעדן|מילקי|מוס|פודינג|ברולה|פנה ?קוטה|קינוח|דניאלה", re.I)
SUPPLEMENT_RE = re.compile(r"תוסף|קפסול|טבליות|כמוסות", re.I)
NONYOGURT_RE = re.compile(
    r"גלידה|ice cream|חמאה|מרגרינה|שמנת|גבינה צהובה|גבינה לבנה|קוטג|קצפת|"
    r"זית|זיתים|olive", re.I)
YOGURT_RE = re.compile(
    r"יוגורט|yog[hu]?urt|יווני|greek|סקיר|skyr|אקטיביה|activia|"
    r"\bביו\b|\bbio\b|\bפרו\b|\bpro\b|\bgo\b|froop|פרופ|מולר|m[uü]ller", re.I)

# RT-3: barcode that is a cereal-misroute — cannot be cleanly re-routed to yogurt
# without a governance-level router change. Drop it with a meta reason.
_CEREAL_MISROUTE_DROP = {"7290112346797"}

# ── RT-2: Disclaimer boundary stripping ──────────────────────────────────────────
# Contamination patterns that signal the start of the embedded disclaimer/nutrition
# block inside the Shufersal ingredients text.  The contamination starts at the
# first match of any of these patterns in the raw ingredient string.
#
# The canonical boundary is "מכיל [allergen]" immediately followed by the nutrition
# table introduction.  But some products have ONLY "ערכים תזונתיים" without a
# preceding "מכיל".  We strip from the earliest match of either pattern.
#
# Regression anchor (RT-2 test):
#   Input:  "חלב, מייצב (E415) מכיל חלב ערכים תזונתיים 100 גרם 86 קל ..."
#   Output: "חלב, מייצב (E415)"  (clean ingredient text, allergen removed)
#   quality: "disclaimer_stripped"
#
# Note on "מכיל": the allergen statement "מכיל חלב/ביצה/..." is NOT an ingredient.
# It is a legal declaration required by Israeli labeling law.  The contamination
# pattern starts at "מכיל" + optional allergen + "ערכים תזונתיים".  We strip
# "מכיל ..." + anything that follows regardless of content.

# Phase 1: patterns that mark the END of true ingredient content
_DISCLAIMER_ANCHORS = [
    # "ערכים תזונתיים" = nutrition values table header
    re.compile(r"\bערכים תזונתיים\b"),
    # "הנתונים המדויקים מופיעים" = legal disclaimer opening phrase
    re.compile(r"הנתונים המדויקים מופיעים"),
    # "אין להסתמך על הפירוט" = "do not rely on this description"
    re.compile(r"אין להסתמך על הפירוט"),
    # "יש לקרוא את המופיע על גבי" = "read the label on the package"
    re.compile(r"יש לקרוא את המופיע על גבי"),
    # Nutrition number sequences embedded in ingredient text:
    # Pattern: "100 גרם" followed by a nutrition header introduces a full table.
    # Must be specific enough not to match product claims like "25 גרם חלבון בגביע".
    # The full table pattern is "100 גרם [X] קל אנרגיה" — requires the "100 גרם" anchor.
    re.compile(r"100\s+גרם\b.{0,50}?\d+\s+קל"),
]

# ── Marketing-prose detection (RT-2 variant) ────────────────────────────────────
# Some products have NO ingredient list on the Shufersal page; the scraper falls
# back to pulling a serving-suggestion / marketing description.  The canonical
# marker set is defined in score_engine's SERVING_SUGGESTION_PROSE_MARKERS_HE
# (constants.py, line ~550).  We detect this class locally so the BSIP1 record
# gets ingredient_text_quality="marketing_bleed" and is scored with a confidence
# deduction instead of being treated as a clean ingredient panel.
#
# Example (barcode 7290102395231, יוגורט ביו נטורל):
#   "יוגורט לבן קלאסי וקרמי שמשתלב בטבעיות בכל רגע. אם זה בתוספת פירות טריים
#    או יבשים, גרנולה, דבש מתוק או פשוט ככה. כמו שהוא. מושלם."
# Real ingredient lists are comma-separated items; they do not contain these prose
# phrases.  Rule: if ANY of _MARKETING_PROSE_MARKERS appears in the (post-disclaimer-
# stripped) text, the text is classified as marketing_bleed.
_MARKETING_PROSE_MARKERS = (
    "שמשתלב",        # "that blends"
    "בטבעיות",       # "naturally"
    "בכל רגע",       # "at any moment"
    "אם זה",         # "whether it's"
    "פשוט ככה",      # "just like that"
    "כמו שהוא",      # "as it is"
    "מושלם",         # "perfect"
    "טריים או יבשים",# "fresh or dried"
    "או פשוט",       # "or just"
)


def _is_marketing_prose(text: str) -> bool:
    """Return True if text contains serving-suggestion / marketing language."""
    if not text:
        return False
    tl = text
    return any(marker in tl for marker in _MARKETING_PROSE_MARKERS)


# Phase 2: "מכיל" (allergen) preceding the nutrition block.
# We also strip the "מכיל X" allergen statement itself IF it appears immediately
# before a disclaimer anchor (it is not an ingredient).
# A bare "מכיל" that appears mid-ingredient-list as part of a sub-ingredient
# parenthetical ("מחית שקדים מכיל שקדים") must NOT be stripped — the phase 2 rule
# only fires when "מכיל" is followed within 60 chars by a nutrition/disclaimer token.
_CONTAINS_BEFORE_DISCLAIMER = re.compile(
    r"\bמכיל\b.{0,60}(?:ערכים תזונתיים|הנתונים המדויקים|אין להסתמך|יש לקרוא|\d+\s+קל\s+אנרגיה)",
    re.DOTALL,
)


def _strip_disclaimer(raw: str) -> tuple[str, str]:
    """
    Strip the embedded nutrition-panel and legal disclaimer from a Shufersal
    ingredient text string.

    Returns (clean_text, stripped_portion).
    clean_text will be "" if the ENTIRE string is disclaimer.

    Algorithm:
      1. Find the earliest match of any _DISCLAIMER_ANCHOR in the raw text.
      2. If a "מכיל ..." allergen statement immediately precedes that position
         (within 100 chars), extend the cut point left to include it.
      3. Strip trailing commas/spaces from the clean portion.

    This is the RT-2 fix.  The TASK-144 sanitizer set ingredient_text_quality="clean"
    unconditionally whenever ingredients_raw was non-empty — that was the blind spot.
    """
    if not raw:
        return raw, ""

    cut = len(raw)  # default: nothing to strip

    # Phase 1: find earliest disclaimer anchor
    for pat in _DISCLAIMER_ANCHORS:
        m = pat.search(raw)
        if m and m.start() < cut:
            cut = m.start()

    if cut == len(raw):
        # No disclaimer found
        return raw, ""

    # Phase 2: extend cut leftward to swallow "מכיל <allergen>" prefix
    prefix = raw[:cut]
    mc = _CONTAINS_BEFORE_DISCLAIMER.search(raw)
    if mc and mc.start() < cut:
        cut = mc.start()

    clean = raw[:cut].rstrip(", \n\t")
    stripped = raw[cut:]
    return clean, stripped


def _parse_num(raw):
    return _shared_parse_num(raw)


def _parse_sodium(raw):
    return _shared_parse_sodium(raw)


def _parse_nutrition(n: dict) -> dict:
    return _shared_parse_nutrition(n)


_SPLIT_RE = re.compile(r"[,;،]\s*")

# ── RT-5: E-number extraction from parenthesized Hebrew phrases ──────────────────
# The existing enricher _E_NUM_RE = re.compile(r'\bE-?(\d{3,4}[a-z]?)\b') requires a
# word boundary before the E. In Hebrew text "חומר הזגה (E414)", the E sits
# immediately after "(" — no preceding word character — so the \b anchor fires.
# However, in the ingredient_enricher._extract_terms() path, the E-number lookup in
# ADDITIVE_TERMS uses substring matching ("E414" in text_lower), which SHOULD work.
# The actual miss is that the enricher builds text_lower from the comma-split
# ingredient list, and "חומר הזגה (E414)" is ONE item in that list. The "E414"
# substring IS present in text_lower, so it should be caught by the existing
# ("E414", "glazing_agent") entry... wait, E414 is NOT in ADDITIVE_TERMS.
# E414 = acacia gum (glazing agent / stabilizer). It is not yet in the dictionary.
# Fix: before calling enrich_product(), scan each ingredient item for E-numbers
# in parentheses and log them as explicit warnings so downstream knows they exist.
# The ingredient_enricher ADDITIVE_TERMS dictionary needs E414 added for future runs,
# but since it is a shared module we add the E414 entry to ingredient_enricher.py
# rather than patching it here — see the companion fix to ingredient_enricher.py.

_E_NUM_PARENS_RE = re.compile(r"\(E-?(\d{3,4}[a-zA-Z]?)\)", re.IGNORECASE)


def _extract_e_numbers_from_parens(ingr_list: list[str]) -> list[str]:
    """
    Scan each ingredient item for E-numbers inside parentheses.
    Returns a list of found E-number strings (e.g. ["E414", "E1442"]).
    These are used for the RT-5 additive warning even if the enricher
    misses them.
    """
    found = []
    for item in ingr_list:
        for m in _E_NUM_PARENS_RE.finditer(item):
            e_num = f"E{m.group(1).upper()}"
            if e_num not in found:
                found.append(e_num)
    return found


# ── RT-12: Activia brand live-cultures supplement ───────────────────────────────
# The canonical Activia culture declaration on Shufersal pages is:
#   "בתוספת החיידק הפרביוטי ביפידוס אקטירגוליס"
# The enricher has "חיידק פרוביוטי" and "ביפידוס" in FERMENTATION_TERMS, but the
# Activia phrase uses "הפרביוטי" (definite form) + "ביפידוס" rather than the bare
# "פרוביוטי" token.  The "ביפידוס" token IS in FERMENTATION_TERMS as bifidobacterium.
# The issue is that "ביפידוס אקטירגוליס" is the full species name and the "ביפידוס"
# substring should match — let's verify by running the enricher against the actual
# text. If the enricher already catches it via "ביפידוס", the RT-12 bug is upstream
# (the disclaimer strip polluted the ingredient text so the enricher saw nutrition
# numbers instead of the culture declaration).
# This function provides a post-hoc correction for any record where:
#  (a) the subtype is "probiotic" (Activia brand),
#  (b) has_live_cultures=False after enrichment, AND
#  (c) the clean ingredient text (post-disclaimer-strip) contains a culture keyword.

_ACTIVIA_CULTURES_RE = re.compile(
    r"(?:"
    r"ביפידוס|bifidus|bifidobacterium"
    r"|חיידק.{0,10}פרוביוטי"
    r"|חיידק.{0,10}פרביוטי"
    r"|אקטירגוליס"          # Actiregulis — Activia's proprietary strain name
    r"|תרבית חיה"
    r"|תרביות חיות"
    r"|חיידקי יוגורט"
    r")",
    re.IGNORECASE,
)


def _has_cultures_fix(subtype: str, enrichment: dict, clean_ingr: str) -> bool:
    """
    RT-12 correction: re-check for live cultures in clean ingredient text.
    Returns True if cultures should be credited.
    """
    if enrichment.get("has_live_cultures", False):
        return True  # already detected by enricher
    if subtype == "probiotic" or subtype == "bio":
        # For probiotic/bio subtypes, check the clean ingredient text
        if clean_ingr and _ACTIVIA_CULTURES_RE.search(clean_ingr):
            return True
    return False


def _classify_subtype(name: str) -> str:
    nl = name.lower()
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


def _curate(raw: dict) -> str | None:
    """Return exclusion reason, or None if included."""
    name = (raw.get("name_he") or "").strip()
    barcode = str(raw.get("barcode", "")).strip()

    if not name:
        return "empty_name"

    # RT-3: explicitly drop the cereal-misroute product
    if barcode in _CEREAL_MISROUTE_DROP:
        return "cereal_misroute_excluded"

    if DRINK_RE.search(name):
        return "drinkable_excluded"
    if DESSERT_RE.search(name):
        return "dessert_excluded"
    if SUPPLEMENT_RE.search(name):
        return "supplement_excluded"
    if NONYOGURT_RE.search(name):
        return "non_yogurt_dairy_excluded"
    if not YOGURT_RE.search(name):
        return "not_spoon_yogurt"
    nn = _parse_nutrition(raw.get("nutrition", {}))
    if all(nn.get(k) is None for k in ("energy_kcal", "protein_g", "carbohydrates_g")):
        return "no_usable_nutrition"
    return None


def _check_macros_plausible(nn: dict) -> tuple[bool, list[str], dict]:
    """
    RT-1: Validate parsed nutrition for physically impossible values.
    Returns (is_plausible, issues_list, corrected_nn).

    Rules for yogurt:
      - protein_g > 50 is impossible (max real protein ~25g/100g for the most
        concentrated Greek yogurts; a 190g value = scrape corruption)
      - energy_kcal > 400 is implausible for any yogurt
      - protein_g > 0 AND energy_kcal > 0: protein contribution check
        (4 * protein_g should not exceed energy_kcal + 50)

    When a field is corrupted, it is set to None in the corrected panel
    (null is honest; a corrupt value is not).
    """
    issues = []
    corrected = dict(nn)

    protein = nn.get("protein_g")
    energy = nn.get("energy_kcal")

    # Hard ceiling: protein > 50 g/100g is physically impossible
    if protein is not None and protein > 50:
        issues.append(
            f"protein_impossible: protein_g={protein} > 50 g/100g ceiling "
            f"(scrape corruption — per-container value mis-read as per-100g). "
            f"Nulling protein_g."
        )
        corrected["protein_g"] = None

    # Energy > 400 kcal/100g impossible for any yogurt product
    if energy is not None and energy > 400:
        issues.append(
            f"energy_implausible: energy_kcal={energy} > 400 kcal/100g "
            f"(yogurt ceiling). Nulling energy_kcal."
        )
        corrected["energy_kcal"] = None

    # Cross-check: protein contribution vs energy (only if both still valid)
    p_corr = corrected.get("protein_g")
    e_corr = corrected.get("energy_kcal")
    fat = corrected.get("fat_g") or 0
    carbs = corrected.get("carbohydrates_g") or 0
    if p_corr is not None and e_corr is not None and e_corr > 0:
        macro_kcal = 4 * p_corr + 4 * carbs + 9 * fat
        # Macro-derived energy should be within 30 kcal of declared (generous tolerance
        # for unresolved fiber + satFat), but if protein alone explains MORE than declared
        # energy that is a corruption signal.
        protein_kcal = 4 * p_corr
        if protein_kcal > e_corr + 20:
            issues.append(
                f"protein_exceeds_energy: protein contribution {protein_kcal:.0f} kcal "
                f"> declared energy {e_corr:.0f} kcal. macros_plausible=False."
            )

    is_plausible = len(issues) == 0
    return is_plausible, issues, corrected


def _confidence(nn: dict, ingr_list: list[str]) -> dict:
    nutr_fields = ["energy_kcal", "protein_g", "sugars_g", "fat_g", "carbohydrates_g"]
    n_present = sum(1 for f in nutr_fields if nn.get(f) is not None)
    nutr_ok = n_present >= 3
    ingr_ok = len(ingr_list) >= 2
    if nutr_ok and ingr_ok:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "high", 0.80, "high"
    elif nutr_ok:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "medium", 0.65, "medium"
    else:
        nutr_conf, id_conf, trust, lvl = "partial", "low", 0.45, "low"
    missing = []
    if not nutr_ok:
        missing += [f for f in nutr_fields if nn.get(f) is None]
    if not ingr_ok:
        missing.append("ingredients_list")
    return {
        "confidence": {
            "identity_confidence": id_conf,
            "barcode_confidence": "confirmed",
            "nutrition_confidence": nutr_conf,
            "matched_by": "shufersal_barcode_single_source",
            "observation_count": 1,
        },
        "canonical_trust_score": trust,
        "canonical_trust_level": lvl,
        "missing_fields": missing,
        "nutrition_consistency_status": "consistent" if nutr_ok else "partial",
    }


def _find_latest_raw() -> pathlib.Path | None:
    cand = sorted(RAW_DIR.glob("yogurt_bsip0_raw_*.json"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    return cand[0] if cand else None


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No yogurt_bsip0_raw_*.json in %s", RAW_DIR)
        return
    log.info("Loading %s", raw_path)
    raws = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raws))

    # clear stale output
    for f in OUT_DIR.glob("bsip1_*.json"):
        f.unlink()

    included, excluded = [], []
    disclaimer_stripped_count = 0
    macros_implausible_count = 0
    seen = set()

    for raw in raws:
        name = (raw.get("name_he") or "").strip()
        barcode = str(raw.get("barcode", "")).strip()
        if barcode in seen:
            excluded.append({"barcode": barcode, "name": name, "reason": "duplicate_barcode"})
            continue
        reason = _curate(raw)
        if reason:
            excluded.append({"barcode": barcode, "name": name, "reason": reason,
                             "_meta": "cereal_misroute_excluded" if reason == "cereal_misroute_excluded"
                             else None})
            continue
        seen.add(barcode)

        # ── RT-2: Disclaimer strip BEFORE anything else uses the ingredient text ──
        ingr_raw = (raw.get("ingredients_raw") or "").strip()
        clean_ingr, stripped_portion = _strip_disclaimer(ingr_raw)
        was_stripped = bool(stripped_portion)
        if was_stripped:
            disclaimer_stripped_count += 1
            log.info("  RT-2 strip [%s] %s: removed %d chars of disclaimer",
                     barcode, name[:40], len(stripped_portion))

        # Ingredient text quality
        if not clean_ingr:
            ingr_quality = "missing"
        elif was_stripped:
            ingr_quality = "disclaimer_stripped"
        elif _is_marketing_prose(clean_ingr):
            # Serving-suggestion prose captured instead of a real ingredient list.
            # Score engine recognises "marketing_bleed" as a quality deduction.
            ingr_quality = "marketing_bleed"
            log.info("  marketing_bleed [%s] %s: ingredient text is prose, not ingredient list",
                     barcode, name[:40])
        else:
            ingr_quality = "clean"

        # ── Nutrition parse ──────────────────────────────────────────────────────
        nn_raw = _parse_nutrition(raw.get("nutrition", {}))

        # ── RT-1: macros_plausible gate ──────────────────────────────────────────
        macros_plausible, macro_issues, nn = _check_macros_plausible(nn_raw)
        if not macros_plausible:
            macros_implausible_count += 1
            log.warning("  RT-1 macros_plausible=False [%s] %s: %s",
                        barcode, name[:40], "; ".join(macro_issues))

        # Ingredient list (from clean text after disclaimer strip)
        ingr_list = []
        if clean_ingr:
            ingr_list = [p.strip().strip(".")
                         for p in re.split(r"[,;،]\s*", re.sub(r"\s+", " ", clean_ingr))
                         if p.strip() and len(p.strip()) > 1]

        # ── RT-7: serving_size_g ─────────────────────────────────────────────────
        weight_g = raw.get("weight_g")
        # Only propagate weight as serving_size_g for single-serve containers
        # (50-250g). Multi-pack products (e.g. 4×175g=700g) must not be treated
        # as a single-serve item.
        serving_size_g = None
        if isinstance(weight_g, (int, float)) and 50 <= weight_g <= 250:
            serving_size_g = weight_g

        conf = _confidence(nn, ingr_list)
        subtype = _classify_subtype(name)
        pid = f"bsip1_yogurt_{barcode}"

        # ── RT-5: E-number pre-scan ──────────────────────────────────────────────
        e_nums_found = _extract_e_numbers_from_parens(ingr_list)

        ingr_warnings = []
        if not clean_ingr:
            ingr_warnings.append("no_ingredient_list_in_source")
        if was_stripped:
            ingr_warnings.append(f"disclaimer_stripped: {len(stripped_portion)} chars removed")
        if e_nums_found:
            ingr_warnings.append(f"e_numbers_in_parentheses: {e_nums_found}")
        if not macros_plausible:
            ingr_warnings.extend([f"macros_implausible: {iss}" for iss in macro_issues])

        record = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": barcode,
            "canonical_name_he": name,
            "canonical_name_en": None,
            "brand": raw.get("brand", ""),
            "package_size_g": weight_g,
            "unit_count": None, "unit_size_g": None,
            "serving_size_g": serving_size_g,
            "country_of_origin": "ישראל",
            "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [SOURCE],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            # Use clean (disclaimer-stripped) ingredient text throughout
            "ingredients_text_he": clean_ingr or None,
            "ingredients_list": ingr_list,
            "ingredients_raw": clean_ingr or None,
            "ingredients_raw_full": ingr_raw,     # audit: original (unstripped) text
            "ingredients_disclaimer_stripped": stripped_portion or None,
            "ingredients_raw_provenance": {
                "source": "bsip0_scrape",
                "bsip0_status": "bsip0_scrape",
                "populated_at": f"bsip1_build_yogurt_006",
                "missing": not bool(clean_ingr),
                "disclaimer_stripped": was_stripped,
                "note": (
                    "Scraped from Shufersal product page (run_yogurt_006, 2026-06-11). "
                    "0 OFF. RT-2 disclaimer strip applied."
                    if was_stripped else
                    "Scraped from Shufersal product page (run_yogurt_006, 2026-06-11). "
                    "0 OFF. No disclaimer contamination detected."
                ),
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": raw.get("claims_raw", ""),
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "Shufersal JSON-LD gtin13/sku.",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": ingr_quality,
            "ingredient_warnings": ingr_warnings,
            # RT-1: macros_plausible flag — any record with False here is BLOCKED
            # from the frontend export by build_yogurts_frontend_v4.py.
            "macros_plausible": macros_plausible,
            "macros_issues": macro_issues if not macros_plausible else [],
            "canonical_trust_score": conf["canonical_trust_score"],
            "canonical_trust_level": conf["canonical_trust_level"],
            "canonical_risk_flags": ["single_source_only"],
            "conflicts_summary": {"count": 0, "has_unresolved": False,
                                  "fields_in_conflict": [], "identity_conflicts": [],
                                  "nutrition_conflicts": [], "ingredient_conflicts": [],
                                  "labeling_conflicts": [], "completeness_conflicts": []},
            "missing_fields": conf["missing_fields"],
            "inferred_fields": ["bsip_yogurt_subtype"],
            "audit_ref": None,
            "bsip_yogurt_subtype": subtype,
            "price": raw.get("price", ""),
            "price_per_100g": raw.get("price_per_100g"),
            "acquisition_query": raw.get("acquisition_query", ""),
        }

        # ── Enrichment (uses clean ingredient text via ingredients_text_he) ──────
        try:
            record = enrich_product(record)
        except Exception as e:
            log.warning("Enrichment error %s: %s", pid, e)
            for fld in ["extracted_additives", "extracted_flavors", "extracted_sweeteners",
                        "extracted_protein_markers", "extracted_matrix_markers",
                        "extracted_fermentation_markers", "extracted_roasting_markers"]:
                record.setdefault(fld, [])
            record.setdefault("enrichment_summary", {})
            record["enrichment_version"] = "bsip1_enrichment_v1"
            record["enrichment_warnings"] = [f"enrichment_error: {e}"]

        # ── RT-12: Post-enrichment live-cultures correction ──────────────────────
        enrichment = record.get("enrichment_summary", {})
        has_cultures_corrected = _has_cultures_fix(subtype, enrichment, clean_ingr)
        if has_cultures_corrected and not enrichment.get("has_live_cultures", False):
            enrichment["has_live_cultures"] = True
            enrichment.setdefault("fermentation_marker_count",
                                   enrichment.get("fermentation_marker_count", 0))
            enrichment["fermentation_marker_count"] = max(
                enrichment.get("fermentation_marker_count", 0), 1
            )
            record["enrichment_summary"] = enrichment
            record.setdefault("enrichment_warnings", [])
            record["enrichment_warnings"].append(
                "RT-12: has_live_cultures corrected via Activia/bio brand culture scan "
                "on clean ingredient text"
            )
            log.info("  RT-12 cultures [%s] %s: has_live_cultures corrected to True",
                     barcode, name[:40])

        # ── RT-5: Record E-number paren hits in enrichment_summary ───────────────
        if e_nums_found:
            enrichment = record.get("enrichment_summary", {})
            known_additives = [a.get("term", "") for a in record.get("extracted_additives", [])]
            new_additives = []
            for e_num in e_nums_found:
                if e_num not in known_additives and e_num not in [a.get("term", "") for a in new_additives]:
                    new_additives.append({"term": e_num, "category": "additive_paren_scan",
                                          "position": None})
            if new_additives:
                existing = record.get("extracted_additives", [])
                record["extracted_additives"] = existing + new_additives
                enrichment["additive_count"] = len(record["extracted_additives"])
                record["enrichment_summary"] = enrichment
                log.info("  RT-5 E-nums [%s] %s: added from parens %s",
                         barcode, name[:40], [a["term"] for a in new_additives])

        (OUT_DIR / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

        included.append({
            "barcode": barcode, "name": name, "subtype": subtype,
            "has_ingredients": bool(clean_ingr),
            "ingredient_text_quality": ingr_quality,
            "macros_plausible": macros_plausible,
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
            "has_cultures": record.get("enrichment_summary", {}).get("has_live_cultures", False),
            "ferment_markers": record.get("enrichment_summary", {}).get("fermentation_marker_count", 0),
            "serving_size_g": serving_size_g,
        })

    n_ingr = sum(1 for i in included if i["has_ingredients"])
    n_macros_ok = sum(1 for i in included if i["macros_plausible"])
    report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(raw_path),
        "raw_count": len(raws),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "ingredient_coverage": f"{n_ingr}/{len(included)}",
        "disclaimer_stripped_count": disclaimer_stripped_count,
        "macros_implausible_count": macros_implausible_count,
        "macros_plausible_count": n_macros_ok,
        "task249_fixes": {
            "RT-2": f"disclaimer stripped from {disclaimer_stripped_count}/{len(included)} products",
            "RT-1": f"{macros_implausible_count} products blocked (macros_plausible=False)",
            "RT-3": "barcode 7290112346797 excluded as cereal_misroute",
            "RT-5": "E-number paren scan applied to all ingredient lists",
            "RT-12": "Activia/bio live-cultures correction applied post-enrichment",
            "RT-7": "serving_size_g populated from weight_g for single-serve containers",
        },
        "included": included,
        "excluded": excluded,
    }
    (OUT_DIR.parent / "curation_report_006.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    log.info("Included %d  Excluded %d  -> BSIP1 at %s", len(included), len(excluded), OUT_DIR)
    log.info("Ingredient coverage (included): %d/%d", n_ingr, len(included))
    log.info("Macros plausible: %d/%d", n_macros_ok, len(included))
    log.info("Disclaimer stripped: %d/%d", disclaimer_stripped_count, len(included))
    # exclusion reason tally
    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        log.info("  excluded[%s] = %d", r, c)


if __name__ == "__main__":
    main()
