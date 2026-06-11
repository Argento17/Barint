"""
BSIP1 Semantic Enrichment — Ingredient Analysis Module
Extracts structured semantic signals from ingredient text.

ARCHITECTURAL CONSTRAINTS:
- No scoring logic. No consumer recommendations. No health inference.
- Evidence-based extraction only: if the term appears, we record it.
- Works on ingredients_text_he (string) and ingredients_list (list).
- All extractions preserve position (1-indexed, matching parsed order).
- Does not modify or replace raw text fields.

Schema additions per product record:
  ingredients_raw              str | None   — raw string, unmodified
  ingredients_raw_provenance   dict         — source + quality metadata
  ingredient_order             list[dict]   — ordered parsed items with position + pct
  extracted_additives          list[dict]   — emulsifiers, stabilizers, etc.
  extracted_flavors            list[dict]   — flavor markers (incl. flavor descriptors)
  extracted_sweeteners         list[dict]   — sugars, syrups, intense sweeteners
  extracted_protein_markers    list[dict]   — isolates, concentrates, whey, casein, etc.
  extracted_matrix_markers     list[dict]   — flour, starch, puffed, extruded, flakes
  extracted_fermentation_markers list[dict] — cultures, yeast, sourdough
  extracted_roasting_markers   list[dict]   — roasted, baked, toasted
  enrichment_version           str          — "bsip1_enrichment_v1"
  enrichment_warnings          list[str]
"""

import re
import pathlib
import json
from typing import Optional

ENRICHMENT_VERSION = "bsip1_enrichment_v1"

# ── Percentage pattern ────────────────────────────────────────────────────────
_PCT_RE = re.compile(r'(?:\()?(\d+(?:[.,]\d+)?)\s*%(?:\))?')
_E_NUM_RE = re.compile(r'\bE-?(\d{3,4}[a-z]?)\b', re.IGNORECASE)


# ── DICTIONARIES ──────────────────────────────────────────────────────────────
# Ordered longest-first so greedy matching works correctly.

def _mk(pairs: list[tuple]) -> list[tuple[str, str]]:
    """Sort keyword list longest-first for greedy substring matching."""
    return sorted(pairs, key=lambda x: len(x[0]), reverse=True)


ADDITIVE_TERMS = _mk([
    # Emulsifiers
    ("לציטין חמניות",          "emulsifier"),
    ("לציטין סויה",             "emulsifier"),
    ("לציטין",                  "emulsifier"),
    ("מתחלבים",                 "emulsifier"),
    ("מתחלב",                   "emulsifier"),
    ("מונוגליצרידים",            "emulsifier"),
    ("מונו ודי-גליצרידים",       "emulsifier"),
    ("פוליסורבט",               "emulsifier"),
    ("E471",                    "emulsifier"),
    ("E472",                    "emulsifier"),
    ("E322",                    "emulsifier"),
    ("E-322",                   "emulsifier"),
    ("E476",                    "emulsifier"),
    ("E-476",                   "emulsifier"),
    # Stabilizers / thickeners
    ("עמילן שינוי",             "modified_starch"),
    ("עמילן מגופף",             "modified_starch"),
    ("מסמיכים",                 "thickener"),
    ("מסמיך",                   "thickener"),
    ("מייצבים",                 "stabilizer"),
    ("מייצב",                   "stabilizer"),
    ("קסנטן",                   "stabilizer_thickener"),
    ("גואר",                    "stabilizer_thickener"),
    ("כרגינן",                  "stabilizer_thickener"),
    ("ג'לטין",                  "thickener"),
    ("ג'לאטין",                 "thickener"),
    ("פקטין",                   "thickener"),
    ("אגר-אגר",                 "thickener"),
    ("אגר",                     "thickener"),
    ("לוקוסט",                  "thickener"),
    ("E440",                    "stabilizer"),
    ("E-440",                   "stabilizer"),
    ("E407",                    "thickener"),
    ("E412",                    "stabilizer_thickener"),
    ("E415",                    "stabilizer_thickener"),
    # Preservatives
    ("חומרי שימור",             "preservative"),
    ("חומר שימור",              "preservative"),
    ("סורבט פוטסיום",           "preservative"),
    ("בנזואט נתרן",             "preservative"),
    ("בנזואט",                  "preservative"),
    ("חומצה סורבית",            "preservative"),
    ("חומצה בנזואית",           "preservative"),
    ("E202",                    "preservative"),
    ("E211",                    "preservative"),
    ("E200",                    "preservative"),
    # Antioxidants
    ("נוגדי חמצון",             "antioxidant"),
    ("נוגד חמצון",              "antioxidant"),
    ("טוקופרול",                "antioxidant"),
    ("חומצה אסקורבית",          "antioxidant"),
    ("אסקורבט",                 "antioxidant"),
    ("E306",                    "antioxidant"),
    ("E307",                    "antioxidant"),
    ("E308",                    "antioxidant"),
    ("E300",                    "antioxidant"),
    # Colors
    ("צבעי מאכל",               "color"),
    ("צבע מאכל",                "color"),
    ("צבעי",                    "color"),
    ("צבע",                     "color"),
    ("קוקצין",                  "color"),
    ("טרטרזין",                 "color"),
    ("ריבופלבין",               "color"),
    ("אנתוציאנינים",             "color"),
    ("ביטא קרוטן",              "color"),
    ("כורכום",                  "color"),
    ("פפריקה",                  "color"),
    ("E102",                    "color"),
    ("E120",                    "color"),
    ("E129",                    "color"),
    ("E150",                    "color"),
    ("E160",                    "color"),
    ("E163",                    "color"),
    # Acidity regulators
    ("מווסתי חומציות",          "acidity_regulator"),
    ("מווסת חומציות",           "acidity_regulator"),
    ("חומצה לימונית",           "acidity_regulator"),
    ("לקטאט נתרן",              "acidity_regulator"),
    ("פוספט",                   "acidity_regulator"),
    ("E330",                    "acidity_regulator"),
    ("E331",                    "acidity_regulator"),
    ("E270",                    "acidity_regulator"),
    # Raising agents
    ("חומרי תפיחה",             "raising_agent"),
    ("חומר תפיחה",              "raising_agent"),
    ("אבקת אפייה",              "raising_agent"),
    ("סודיום ביקרבונט",         "raising_agent"),
    ("ביקרבונט",                "raising_agent"),
    ("פירופוספט",               "raising_agent"),
    ("אמוניום ביקרבונט",        "raising_agent"),
    ("E500",                    "raising_agent"),
    ("E450",                    "raising_agent"),
    ("E503",                    "raising_agent"),
    # Humectants
    ("חומרי הלחה",              "humectant"),
    ("חומר הלחה",               "humectant"),
    ("גליצרול",                 "humectant"),
    ("גליסרין",                 "humectant"),
    ("E422",                    "humectant"),
    # Glazing agents
    # E414 = acacia gum (Arabic gum) — stabilizer/glazing agent.
    # RT-5 (TASK-249): previously missing from ADDITIVE_TERMS. Shufersal labels
    # declare it as "חומר הזגה (E414)" — the E-number appears inside parentheses
    # after the Hebrew function name. The substring "E414" is present in the ingredient
    # item text, so the existing _extract_terms() substring scan will now find it.
    ("חומר הזגה",               "glazing_agent"),   # Hebrew: "glazing agent" (generic)
    ("E414",                    "glazing_agent"),   # acacia gum / Arabic gum
    ("חומר מציפה",              "glazing_agent"),
    ("שעווה קרנאובה",           "glazing_agent"),
    ("שעווה",                   "glazing_agent"),
    ("קרנאובה",                 "glazing_agent"),
    ("שלק",                     "glazing_agent"),
    ("E901",                    "glazing_agent"),
    ("E903",                    "glazing_agent"),
    # Flavor enhancers
    ("גלוטמט חד נתרן",          "flavor_enhancer"),
    ("גלוטמט",                  "flavor_enhancer"),
    ("E621",                    "flavor_enhancer"),
    ("E635",                    "flavor_enhancer"),
    # Anticaking
    ("חומר מונע הידבקות",       "anticaking"),
    ("סיליקון דיוקסיד",         "anticaking"),
    ("E551",                    "anticaking"),
    # Bulking agents / fillers
    ("מלטודקסטרין",             "bulking_agent"),
    ("דקסטרין",                 "bulking_agent"),
    ("אינולין",                 "prebiotic_fiber"),    # chicory inulin — fiber launder signal
    ("שורש עולש",               "prebiotic_fiber"),    # chicory root
    ("שורש ציקוריה",            "prebiotic_fiber"),    # chicory root variant
    ("פוליפרוקטוז",             "prebiotic_fiber"),
])

FLAVOR_TERMS = _mk([
    ("חומרי טעם וריח טבעיים",   "natural_flavor"),
    ("חומרי טעם וריח",          "flavor_generic"),
    ("חומר טעם וריח",           "flavor_generic"),
    ("חומרי טעם טבעיים",        "natural_flavor"),
    ("חומר טעם טבעי",           "natural_flavor"),
    ("חומרי טעם",               "flavor_generic"),
    ("חומר טעם",                "flavor_generic"),
    ("טעמים טבעיים",            "natural_flavor"),
    ("טעם טבעי",                "natural_flavor"),
    ("ארומה טבעית",             "natural_flavor"),
    ("ארומה",                   "flavor_generic"),
    ("ונילין",                  "vanilla_synthetic"),
    ("וניליין",                 "vanilla_synthetic"),
    ("ואניל",                   "vanilla"),
    ("וניל",                    "vanilla"),
    ("בטעם",                    "flavor_descriptor"),  # "in the flavor of" — routing signal
    ("בניחוח",                  "flavor_descriptor"),
])

SWEETENER_TERMS = _mk([
    # Syrups — longest first
    ("סירופ סוכר אינברטי",      "invert_sugar_syrup"),
    ("סוכר אינברטי",            "invert_sugar"),
    ("סירופ גלוקוזה",           "glucose_syrup"),
    ("סירופ גלוקוז",            "glucose_syrup"),
    ("סירופ מייפל",             "maple_syrup"),
    ("סירופ תמרים",             "date_syrup"),
    ("סירופ אגבה",              "agave_syrup"),
    ("סירופ תירס",              "corn_syrup"),
    ("סירופ אורז",              "rice_syrup"),
    ("סירופ מלט",               "malt_syrup"),
    ("סירופ סוכר",              "sugar_syrup"),
    # Raw sugars
    ("סוכר לבן",                "added_sugar"),
    ("סוכר חום",                "brown_sugar"),
    ("גלוקוזה",                 "glucose"),
    ("גלוקוז",                  "glucose"),
    ("פרוקטוז",                 "fructose"),
    ("לקטוז",                   "lactose"),
    ("מלטוז",                   "maltose"),
    ("סוכרוז",                  "sucrose"),
    ("מולסה",                   "molasses"),
    ("דבש",                     "honey"),
    ("אינוורט",                 "invert_sugar"),
    ("סוכר",                    "added_sugar"),
    # Polyols
    ("מלטיטול",                 "maltitol"),
    ("סורביטול",                "sorbitol"),
    ("מניטול",                  "mannitol"),
    ("קסיליטול",                "xylitol"),
    ("איריתריטול",              "erythritol"),
    ("לקטיטול",                 "lactitol"),
    ("פוליאולים",               "polyols_generic"),
    ("ממתיקים",                 "sweetener_generic"),
    ("ממתיק",                   "sweetener_generic"),
    # Intense sweeteners
    ("גליקוזידי סטביה",         "stevia"),
    ("תמצית סטביה",             "stevia"),
    ("סטביה",                   "stevia"),
    ("אספרטם",                  "aspartame"),
    ("סוכרלוזה",                "sucralose"),
    ("סכרין",                   "saccharin"),
    ("אצסולפם-K",               "acesulfame_k"),
    ("אצסולפם K",               "acesulfame_k"),
    ("אצסולפם",                 "acesulfame_k"),
    ("נאוטם",                   "neotame"),
    ("תחליפי סוכר",             "sweetener_generic"),
    ("E955",                    "sucralose"),
    ("E951",                    "aspartame"),
    ("E950",                    "acesulfame_k"),
    ("E960",                    "stevia"),
])

PROTEIN_TERMS = _mk([
    # Milk-derived
    ("מרוכז חלבון מי גבינה",    "whey_protein_concentrate"),
    ("בידוד חלבון מי גבינה",    "whey_protein_isolate"),
    ("חלבון מי גבינה",          "whey_protein"),
    ("מי גבינה",                "whey"),
    ("חלבון קזאין",             "casein"),
    ("מרוכז חלבון חלב",         "milk_protein_concentrate"),
    ("חלבון חלב",               "milk_protein"),
    ("אבקת חלב כחוש",           "skim_milk_powder"),
    ("אבקת חלב מלא",            "whole_milk_powder"),
    ("אבקת חלב",                "milk_powder"),
    ("מוצקי חלב",               "milk_solids"),
    ("קזאין",                   "casein"),
    ("לקטלבומין",               "lactalbumin"),
    # Soy-derived
    ("בידוד חלבון סויה",        "soy_protein_isolate"),
    ("מרוכז חלבון סויה",        "soy_protein_concentrate"),
    ("חלבון סויה",              "soy_protein"),
    ("אבקת סויה",               "soy_powder"),
    # Pea-derived
    ("מרוכז חלבון אפונה",       "pea_protein_concentrate"),
    ("חלבון אפונה",             "pea_protein"),
    # Wheat-derived
    ("גלוטן חיטה חיוני",        "vital_wheat_gluten"),
    ("גלוטן חיטה",              "wheat_gluten"),
    ("חלבון חיטה",              "wheat_protein"),
    # Egg
    ("חלבון ביצה",              "egg_albumen"),
    ("אלבומין ביצה",            "egg_albumen"),
    ("אלבומין",                 "albumin"),
    ("מי ביצה",                 "egg_white"),
    # Rice / other
    ("חלבון אורז",              "rice_protein"),
    ("חלבון תפוח אדמה",         "potato_protein"),
    # Hydrolyzed
    ("חלבון מפורק",             "hydrolyzed_protein"),
    ("מידרוליזט",               "hydrolyzed_protein"),
    ("מידרוליז",                "hydrolyzed_protein"),
    ("הידרוליזט",               "hydrolyzed_protein"),
])

MATRIX_TERMS = _mk([
    # Flours
    ("קמח חיטה מלא",            "whole_wheat_flour"),
    ("קמח חיטה",                "wheat_flour"),
    ("קמח שיפון מלא",           "whole_rye_flour"),
    ("קמח שיפון",               "rye_flour"),
    ("קמח כוסמין",              "spelt_flour"),
    ("קמח אורז",                "rice_flour"),
    ("קמח תירס",                "corn_flour"),
    ("קמח שיבולת שועל",         "oat_flour"),
    ("קמח",                     "flour_generic"),
    # Starches
    ("עמילן תפוח אדמה",         "potato_starch"),
    ("עמילן תירס",              "corn_starch"),
    ("עמילן חיטה",              "wheat_starch"),
    ("עמילן אורז",              "rice_starch"),
    ("עמילן שינוי",             "modified_starch"),
    ("עמילן",                   "starch_generic"),
    # Puffed / expanded
    ("פצפוצי תירס",             "puffed_corn"),
    ("פצפוצי אורז",             "puffed_rice"),
    ("פצפוצי שעורה",            "puffed_barley"),
    ("פצפוצי",                  "puffed_cereal"),
    ("מנופח",                   "puffed"),
    ("מנופחים",                 "puffed"),
    ("מוקפץ",                   "puffed"),
    ("מורחב",                   "expanded"),
    # Flakes
    ("פתיתי שיבולת שועל",       "oat_flakes"),
    ("פתיתי חיטה",              "wheat_flakes"),
    ("פתיתי תירס",              "corn_flakes"),
    ("פתיתי",                   "flakes_generic"),
    # Cereal pieces / crisps
    ("קריספי",                  "crisped_cereal"),
    ("ריספי",                   "crisped_cereal"),
    ("פריכיות אורז",            "rice_cakes"),
    ("פריכיות",                 "rice_cakes"),
    ("כרנצ'י",                  "crunchy_pieces"),
    # Bulking / filler sugars
    ("מלטודקסטרין",             "maltodextrin"),
    ("דקסטרוז",                 "dextrose"),
    ("דקסטרין",                 "dextrin"),
])

FERMENTATION_TERMS = _mk([
    ("תרבויות חיות",            "live_cultures"),
    ("תרבויות ייחוד",           "starter_cultures"),
    ("תרבויות",                 "cultures_generic"),
    ("חיידקים חיים",            "live_bacteria"),
    ("תסיסה לקטית",             "lactic_fermentation"),
    ("לקטובציל בולגריקוס",      "lb_bulgaricus"),
    ("לקטובציל אסידופילוס",     "lb_acidophilus"),
    ("לקטובציל",                "lactobacillus"),
    ("ביפידובקטריום",           "bifidobacterium"),
    ("סטרפטוקוקוס תרמופילוס",  "st_thermophilus"),
    ("סטרפטוקוקוס",             "streptococcus"),
    ("לאקטוקוקוס",              "lactococcus"),
    ("שמרי לחם",                "bread_yeast"),
    ("שמרים",                   "yeast"),
    ("יסט",                     "yeast"),
    ("מחמצת",                   "sourdough_starter"),
    ("מותסס",                   "fermented"),
    ("תסיסה",                   "fermentation"),
    # ── Israeli retail label culture vocabulary (TASK-139B) ──────────────────
    # Real Shufersal yogurt labels declare the live-culture positive with this
    # wording, which the original term set missed (run_yogurt_003: 0/88 credited).
    # Non-interpretive substring matching only — adds no scoring rule. The generic
    # "bacteria" phrasings map to live_cultures (flags has_live_cultures); the named
    # organisms reuse the existing organism categories. Matching is case-insensitive.
    ("חיידק פרוביוטי",          "live_cultures"),     # "probiotic bacterium"
    ("חיידקי פרוביוטי",         "live_cultures"),     # construct form
    ("חיידקים פרוביוטי",        "live_cultures"),     # plural; tolerates OCR "...ים/ם" split
    ("חיידקי ביפידוס",          "live_cultures"),
    ("חיידקי ביפדוס",           "live_cultures"),     # spelling/OCR variant (missing yod)
    ("חיידקי יוגורט",           "live_cultures"),     # "yogurt bacteria"
    ("חיידקי אצידופילוס",       "live_cultures"),
    ("חיידקי אצידופולוס",       "live_cultures"),     # spelling variant
    ("חיידקי bio",              "live_cultures"),     # "חיידקי Bio/BIO" (case-insensitive)
    ("תרבית",                   "cultures_generic"),  # singular of תרבויות
    ("ביפידוס",                 "bifidobacterium"),   # Hebrew bifidus = same organism as ביפידובקטריום
    ("ביפדוס",                  "bifidobacterium"),   # spelling/OCR variant
    ("bifidus",                 "bifidobacterium"),   # Latin (case-insensitive → BIFIDUS/Bifidus)
    # ── RT-12 (TASK-249): Activia canonical culture declaration ──────────────
    # Activia (Danone) labels on Shufersal declare live cultures with the phrase:
    #   "בתוספת החיידק הפרביוטי ביפידוס אקטירגוליס"
    # The definite form "הפרביוטי" (rather than bare "פרוביוטי") and the proprietary
    # strain name "אקטירגוליס" (Actiregulis) were not previously detected.
    # The "ביפידוס" term above already matches, but after RT-2 disclaimer stripping
    # the ingredient text is now clean — the enricher will correctly see "ביפידוס".
    # These entries are added as a belt-and-suspenders guard for any edge case where
    # the ביפידוס match fails (e.g. spelling variants, tokenisation).
    ("החיידק הפרביוטי",         "live_cultures"),     # Activia definite form (RT-12)
    ("אקטירגוליס",              "live_cultures"),     # Actiregulis — Activia proprietary strain
])

ROASTING_TERMS = _mk([
    ("קלויים",                  "roasted"),
    ("קלוי",                    "roasted"),
    ("שנקלה",                   "roasted"),
    ("מושחר",                   "charred"),
    ("אפויים",                  "baked"),
    ("אפוי",                    "baked"),
    ("נאפה",                    "baked"),
    ("מבושל",                   "cooked"),
    ("טוסט",                    "toasted"),
    ("מוטגן",                   "fried"),
])


# ── Parsing helpers ───────────────────────────────────────────────────────────

def _parse_ingredients_ordered(text: str) -> list[dict]:
    """
    Split ingredient string into ordered items, respecting parentheses depth.
    Returns list of {position, text, percentage_declared, has_subgroup}.
    """
    if not text:
        return []

    items: list[str] = []
    current = ""
    depth = 0
    for char in text:
        if char == "(":
            depth += 1
            current += char
        elif char == ")":
            depth -= 1
            current += char
        elif char == "," and depth == 0:
            stripped = current.strip()
            if stripped:
                items.append(stripped)
            current = ""
        else:
            current += char
    if current.strip():
        items.append(current.strip())

    results = []
    for i, item_text in enumerate(items, start=1):
        # Extract declared percentage if present
        pct_match = _PCT_RE.search(item_text)
        pct = float(pct_match.group(1).replace(",", ".")) if pct_match else None
        # Detect nested sub-group (parenthetical content that is not just %)
        has_sub = bool(re.search(r'\([^)]{3,}\)', item_text.replace(pct_match.group(0), "") if pct_match else item_text))
        results.append({
            "position":            i,
            "text":                item_text,
            "percentage_declared": pct,
            "has_subgroup":        has_sub,
        })
    return results


def _extract_terms(text_lower: str, ordered_items: list[dict],
                   term_list: list[tuple[str, str]]) -> list[dict]:
    """
    Match terms against full text and assign position from ordered_items.
    Returns list of {term, category, position} dicts, deduplicated by term.
    """
    seen_terms: set[str] = set()
    results: list[dict] = []

    for keyword, category in term_list:
        kw_lower = keyword.lower()
        if kw_lower not in text_lower:
            continue
        if keyword in seen_terms:
            continue
        seen_terms.add(keyword)

        # Find first ingredient position where this term appears
        position = None
        for item in ordered_items:
            if kw_lower in item["text"].lower():
                position = item["position"]
                break

        results.append({
            "term":     keyword,
            "category": category,
            "position": position,  # None means found in text but position ambiguous
        })

    return results


# ── BSIP0 raw ingredient lookup ───────────────────────────────────────────────

BSIP0_YOHANANOF = pathlib.Path(
    r"C:\Bari\03_operations\bsip0\scrape\yohananof\outputs\yohananof"
)


def _try_bsip0_raw(barcode: Optional[str]) -> tuple[Optional[str], str]:
    """
    Attempt to read ingredients_raw_he from the BSIP0 product file.
    Returns (raw_string_or_None, provenance_source_string).
    """
    if not barcode:
        return None, "no_barcode"
    bsip0_file = BSIP0_YOHANANOF / str(barcode) / "product.json"
    if not bsip0_file.exists():
        return None, "bsip0_file_not_found"
    try:
        with open(bsip0_file, encoding="utf-8") as f:
            raw = json.load(f)
        ing = (raw.get("raw_observations") or {}).get("ingredients_raw_he")
        if ing and str(ing).strip() not in ("None", "null", ""):
            return str(ing).strip(), "bsip0_scrape"
        return None, "bsip0_scrape_missing"
    except Exception as e:
        return None, f"bsip0_read_error:{e}"


# ── Main enrichment function ──────────────────────────────────────────────────

def enrich(record: dict) -> dict:
    """
    Add semantic enrichment fields to a BSIP1 product record.
    Returns the record with new fields added (does not modify existing fields).
    """
    enrichment: dict = {}
    warnings: list[str] = []

    # ── ingredients_raw ───────────────────────────────────────────────────────
    barcode = record.get("barcode")
    existing_text = record.get("ingredients_text_he") or ""

    bsip0_raw, bsip0_source = _try_bsip0_raw(barcode)

    if bsip0_raw:
        ingredients_raw = bsip0_raw
        provenance_source = "bsip0_scrape"
        provenance_note = "Original retailer ingredient string from BSIP0 raw observation"
    elif existing_text:
        ingredients_raw = existing_text
        provenance_source = "bsip1_text_fallback"
        provenance_note = f"BSIP0 unavailable ({bsip0_source}); using BSIP1 ingredients_text_he"
    else:
        ingredients_raw = None
        provenance_source = "missing"
        provenance_note = f"No ingredient text available ({bsip0_source})"
        warnings.append("ingredients_raw: no text available from any source")

    enrichment["ingredients_raw"] = ingredients_raw
    enrichment["ingredients_raw_provenance"] = {
        "source":        provenance_source,
        "bsip0_status":  bsip0_source,
        "populated_at":  ENRICHMENT_VERSION,
        "missing":       ingredients_raw is None,
        "note":          provenance_note,
    }

    # ── ingredient_order ──────────────────────────────────────────────────────
    # Use the best available text for parsing
    parse_source = ingredients_raw or existing_text or ""
    ordered = _parse_ingredients_ordered(parse_source)
    enrichment["ingredient_order"] = ordered

    if not ordered and parse_source:
        warnings.append("ingredient_order: parse produced 0 items from non-empty text")

    # ── semantic extractions ──────────────────────────────────────────────────
    text_lower = parse_source.lower()

    enrichment["extracted_additives"] = _extract_terms(
        text_lower, ordered, ADDITIVE_TERMS)

    enrichment["extracted_flavors"] = _extract_terms(
        text_lower, ordered, FLAVOR_TERMS)

    enrichment["extracted_sweeteners"] = _extract_terms(
        text_lower, ordered, SWEETENER_TERMS)

    enrichment["extracted_protein_markers"] = _extract_terms(
        text_lower, ordered, PROTEIN_TERMS)

    enrichment["extracted_matrix_markers"] = _extract_terms(
        text_lower, ordered, MATRIX_TERMS)

    enrichment["extracted_fermentation_markers"] = _extract_terms(
        text_lower, ordered, FERMENTATION_TERMS)

    enrichment["extracted_roasting_markers"] = _extract_terms(
        text_lower, ordered, ROASTING_TERMS)

    # ── summary counts (convenience for BSIP2) ────────────────────────────────
    enrichment["enrichment_summary"] = {
        "ingredient_count_parsed":        len(ordered),
        "additive_count":                 len(enrichment["extracted_additives"]),
        "flavor_marker_count":            len(enrichment["extracted_flavors"]),
        "sweetener_count":                len(enrichment["extracted_sweeteners"]),
        "protein_marker_count":           len(enrichment["extracted_protein_markers"]),
        "matrix_marker_count":            len(enrichment["extracted_matrix_markers"]),
        "fermentation_marker_count":      len(enrichment["extracted_fermentation_markers"]),
        "roasting_marker_count":          len(enrichment["extracted_roasting_markers"]),
        "has_flavor_descriptor":          any(
            e["category"] == "flavor_descriptor"
            for e in enrichment["extracted_flavors"]
        ),
        "has_prebiotic_fiber":            any(
            e["category"] == "prebiotic_fiber"
            for e in enrichment["extracted_additives"]
        ),
        "has_live_cultures":              any(
            e["category"] in ("live_cultures", "live_bacteria")
            for e in enrichment["extracted_fermentation_markers"]
        ),
        "has_protein_isolate_or_concentrate": any(
            "isolate" in e["category"] or "concentrate" in e["category"]
            for e in enrichment["extracted_protein_markers"]
        ),
    }

    enrichment["enrichment_version"] = ENRICHMENT_VERSION
    enrichment["enrichment_warnings"] = warnings

    return {**record, **enrichment}
