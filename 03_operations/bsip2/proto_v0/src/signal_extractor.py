"""
BSIP2 Prototype v0 — Signal Extractor
Extracts L1-L6 signals from a BSIP1 product without modifying it.
All inferences are labelled by taxonomy layer and carry explicit uncertainty.
"""
import re
import os
from input_loader import get_nutrition, get_ingredients, get_ingredients_text, get_trust
import ingredient_taxonomy as itax   # TASK-133A — named-additive + fragmentation identity
from constants import KCAL_PLAUSIBLE_UPPER, KCAL_PLAUSIBLE_LOWER  # EV-047

# TASK-144 — activation toggle for the three approved fixes (Fix1 sanitize / Fix3 dairy
# source typing live here; Fix2 fiber-not-applicable lives in score_engine and reads the
# same env flag).
#
# ACTIVATION SCOPE (governance Check 3): the approved scope is the MAADANIM run only.
# Frozen dairy categories (yogurt, cheese, milk) share the `dairy_protein` routing
# category with maadanim, so a category-level gate cannot separate them — and the
# blast-radius check confirmed Fix 2/Fix 3 would otherwise move FROZEN yogurt/cheese
# scores (incl. into A), which is out of scope and must not ship without Product sign-off.
# Therefore the DEFAULT is OFF; only batch_run_maadanim_001.py opts in by setting
# BARI_TASK144_FIXES=on before import. Set =on for the maadanim run; leave unset (off)
# everywhere else. This is fully reversible: unset the env var → frozen behavior returns.
TASK144_FIXES_ON = os.environ.get("BARI_TASK144_FIXES", "off").lower() == "on"

# ---------------------------------------------------------------------------
# Hebrew ingredient keyword lists
# ---------------------------------------------------------------------------

# Added sugar markers (SC classification: SC-3 through SC-5 signals)
ADDED_SUGAR_MARKERS_HE = [
    "סוכר",             # sugar
    "סירופ גלוקוזה",    # glucose syrup
    "סירופ גלוקוז",     # glucose syrup (variant)
    "סירופ גלוקוז-פרוקטוז",  # glucose-fructose syrup
    "סירופ גלוקוזה-פרוקטוזה",
    "פרוקטוזה",         # fructose
    "דקסטרוזה",         # dextrose
    "מולסה",            # molasses
    "סירופ תמרים",      # date syrup (SC-4)
    "סירופ מייפל",      # maple syrup
    "סוכר קנים",        # cane sugar
    "סוכר חום",         # brown sugar
    "סירופ סוכר",       # sugar syrup
    "סירופ אגבה",       # agave syrup
    "מלטוז",            # maltose
    "לקטוז",            # lactose (not added, but sugar)
    "סירופ תירס",       # corn syrup
    "סירופ קרמל",       # caramel syrup
    "אינברטי",          # inverted sugar
    "ריבה",             # jam
    "רכז פרות",         # fruit concentrate (SC-4)
    "מיץ פרות מרוכז",   # concentrated fruit juice (SC-4)
    "דבש",              # honey
    "אגבה",             # agave
    "פרי",              # fruit (weaker signal)
]

ADDED_SUGAR_MARKERS_EN = ["glucose", "fructose", "dextrose", "maltose", "sucrose",
                          "syrup", "honey", "molasses"]

# Sweetener markers by tier (non-nutritive).
# Worst tier present in a product determines its sweetener_tier classification.
# Tier A: fermentation-derived or plant-derived natural sweeteners
SWEETENER_TIER_A_HE = [
    "סטביה",               # stevia
    "גליקוזידים של סטביול", # steviol glycosides
    "נאוהספרידין",          # neohesperidin DC (citrus-derived)
    "תאומאטין",             # thaumatin (fermentation-derived protein)
    "ממתיק מונק פרוט",      # monkfruit sweetener
    "ממתיק פרי נזיר",       # monkfruit sweetener (alt spelling)
]
SWEETENER_TIER_A_E = ["E-960", "E960", "E-957", "E957", "E-959", "E959"]

# Tier B: sugar alcohols — metabolically distinct from refined sugar but not natural
SWEETENER_TIER_B_HE = [
    "סורביטול",    # sorbitol
    "מניטול",      # mannitol
    "קסיליטול",    # xylitol
    "אריתריטול",   # erythritol
    "מלטיטול",     # maltitol
    "איזומאלט",    # isomalt
    "לקטיטול",     # lactitol
]
SWEETENER_TIER_B_E = [
    "E-420", "E-421", "E-953", "E-965", "E-966", "E-967", "E-968",
    "E420",  "E421",  "E953",  "E965",  "E966",  "E967",  "E968",
]

# Tier C: synthetic high-intensity sweeteners — full penalty
SWEETENER_TIER_C_HE = [
    "אספרטם",      # aspartame
    "סוכרלוזה",    # sucralose
    "סוכרלוז",     # sucralose (variant)
    "אצסולפם",     # acesulfame-K
    "נאוטאם",      # neotame
    "אדוונטאם",    # advantame
    "סוכרין",      # saccharin
    "ציקלמאט",     # cyclamate
    "ממתיק",       # general/unspecified sweetener → conservative default
]
SWEETENER_TIER_C_E = [
    "E-950", "E-951", "E-952", "E-954", "E-955", "E-961", "E-962",
    "E950",  "E951",  "E952",  "E954",  "E955",  "E961",  "E962",
]

# Additive category markers (each detection = +1 additive marker)
ADDITIVE_MARKER_PATTERNS = [
    # Emulsifiers
    (r"מתחלב|לציטין|E-322|E322|E-471|E471|E-472|E472|E-476|E476|E-481|E481", "emulsifier"),
    # Stabilizers
    (r"מייצב|קרגינן|גואר|גומי|E-407|E407|E-410|E410|E-412|E412|E-415|E415|E-440|E440", "stabilizer"),
    # Thickeners
    (r"מסמיך|עמילן מוקשה|עמילן משונה|E-1400|E-1404|E-1410|E-1412|E-1414|E-1420|E-1422|E-1440|E-1442|E-1450", "thickener"),
    # Preservatives
    (r"חומר שימור|שומר טריות|E-200|E200|E-202|E202|E-210|E210|E-211|E211|E-220|E220|E-250|E250|E-252|E252", "preservative"),
    # Antioxidants
    (r"מעכב חמצון|טוקופרול|E-300|E300|E-301|E301|E-302|E302|E-306|E306|E-307|E307|E-308|E308|E-309|E309|E-310|E310|E-320|E320|E-321|E321", "antioxidant"),
    # Humectants
    (r"חומר הלחה|גליצרין|גליצרול|סורביטול|E-422|E422", "humectant"),
    # Acidity regulators
    (r"מווסת חומציות|חומצה ציטרית|חומצת לימון|E-330|E330|E-331|E331|E-332|E332|E-333|E333|E-334|E334", "acidity_regulator"),
    # Colors
    (r"צבע מאכל|E-1[0-9]{2}|E-[0-9]{3}(?= )|קרוטן|קרמל|כורכום|טרטרזין|אנתוציאנין", "color"),
    # Flavor enhancers / artificial flavors — strongest NOVA 4 signal
    (r"חומרי טעם וריח|טעמים מלאכותיים|ונילין|ואניל|E-621|E621|E-627|E627|E-631|E631|E-635|E635", "flavor_enhancer"),
    # Leavening agents (weaker signal)
    (r"חומר מתפיח|E-500|E500|E-501|E501|E-503|E503|E-450|E450|E-451|E451|E-452|E452|סודה", "leavening_agent"),
    # Flour treatment agents
    (r"E-300|E-920|E920|חומר הוספה לקמח", "flour_treatment"),
]

# Seed oil markers
SEED_OIL_MARKERS_HE = [
    "שמן חמניות",   # sunflower oil
    "שמן קנולה",    # canola oil
    "שמן תירס",     # corn oil
    "שמן סויה",     # soy oil
    "שמן צמחי",     # vegetable oil (often seed oil blend)
    "שמנים צמחיים", # vegetable oils
]

# Palm oil markers (flagged separately, not seed oil)
PALM_OIL_MARKERS_HE = [
    "שמן דקל", "שמן קוקוס", "שומן קוקוס", "שמן דקל אדום",
    "דקל",      # palm (when in fat context)
    "קוקוס",    # coconut (when in fat context)
]

# Whole grain markers
WHOLE_GRAIN_MARKERS_HE = [
    "דגנים מלאים", "חיטה מלאה", "שיבולת שועל מלאה",
    "אורז מלא", "קמח מלא", "קמח חיטה מלא", "שעורה מלאה",
    "גרגרים מלאים", "תירס מלא",
    # Bakery additions
    "שיפון מלא", "קמח שיפון מלא",   # whole rye flour (common in crispbread/sourdough)
    "כוסמין",                         # spelt (inherently whole grain in Israeli usage)
    "כוסמת",                          # buckwheat
]

# Fermentation markers
# TASK-139 (parent closing re-score): the BSIP1 enricher (TASK-139B) was extended to
# the real Shufersal live-culture label vocabulary, but the BSIP2 scorer derives
# `has_fermentation` from THIS independent list — so the 139B fix never reached the
# score (49/86 yogurt SKUs detected as live-culture in BSIP1, 0/86 credited in BSIP2,
# fermentation_bonus_applied=0). Mirroring 139B's vocabulary here so the already-active
# fermentation bonus (R-02 direct + WFI ferm_bonus) sees real labels. Non-interpretive
# substring matching only — no new scoring rule/weight/threshold. Collision-audited:
# 0 has_fermentation flips on every frozen/non-dairy corpus (milk_001/002, snacks
# run_001, bread_light_001, bread_retail_003, cereals_001/002, hummus_001).
FERMENTATION_MARKERS_HE = [
    "תרבויות חיות", "תרביות חיות", "חיידקים פרוביוטיים",
    "לקטובציל", "בידפידוס", "חומצה לקטית", "חמץ",
    "מחמצת", "ספיח", "שמר",
    # ── Israeli retail live-culture vocabulary (mirror of TASK-139B FERMENTATION_TERMS) ──
    "תרבויות",                                  # plain plural (label often omits "חיות")
    "חיידק פרוביוטי", "חיידקי פרוביוטי", "חיידקים פרוביוטי",
    "חיידקי ביפידוס", "חיידקי ביפדוס",          # incl. OCR/spelling variant (missing yod)
    "חיידקי יוגורט", "חיידקי אצידופילוס", "חיידקי אצידופולוס",
    "ביפידוס", "ביפדוס", "bifidus",             # bifidobacterium (case-insensitive → BIFIDUS)
    "תרבית",                                    # singular "culture"
]

# Protein isolate markers
PROTEIN_ISOLATE_MARKERS_HE = [
    "חלבון מי גבינה", "חלבון סויה", "חלבון חיטה",
    "חלבון אפונה", "חלבון ביצה", "חלבון קזאין",
    "אבקת חלב",   # milk powder — mixed signal
    "קזאין",
    "אייזולאט", "איזולאט",
]

# F2 / TASK-133B — reconstructed-protein markers: extracted protein FRACTIONS
# (isolates / concentrates). This is a PRECISION SUBSET of PROTEIN_ISOLATE_MARKERS_HE
# that DELIBERATELY EXCLUDES whole dried-dairy ingredients — "אבקת חלב" (milk powder)
# and bare "קזאין" — which are reconstructed dairy but NOT protein isolates, and so
# must not trigger the F2 quality discount (verified false-positive source on the
# snack-bar corpus: milk-powder chocolate/cereal bars). Genuine "חלבון X" fractions
# (whey/soy/pea/egg/casein protein) and explicit isolate terms DO trigger it.
RECONSTRUCTED_PROTEIN_MARKERS_HE = [
    "חלבון מי גבינה", "חלבון סויה", "חלבון חיטה",
    "חלבון אפונה", "חלבון ביצה", "חלבון קזאין",
    "אייזולאט", "איזולאט",
]

# F2 / TASK-133B — collagen: reconstructed protein with an incomplete amino-acid
# profile (no tryptophan); lowest matrix DIAAS. Detected separately so the protein
# quality dimension can apply the strongest matrix discount (collagen sub-penalty).
COLLAGEN_MARKERS_HE = [
    "קולגן", "פפטידי קולגן", "חלבון קולגן", "collagen", "collagen peptides",
]

# Fortification detection — synthetic vitamins/minerals added as ingredients.
# Signals: explicit "מועשר/מחוזק" language, or ≥2 distinct synthetic vitamins in ingredient text.
FORTIFICATION_EXPLICIT_HE = [
    "מועשר",   # "enriched"
    "מחוזק",   # "fortified"
]
SYNTHETIC_VITAMIN_HE = [
    "ויטמין C", "חומצה אסקורבית", "אסקורבאט",
    "ויטמין D", "כולקלציפרול", "ארגוקלציפרול",
    "ויטמין B12", "ציאנוקובלמין",
    "ויטמין B6", "פירידוקסין",
    "חומצה פולית", "פולאט",
    "ניאצין", "ניאצינאמיד",
    "ריבופלאבין",
    "תיאמין",
    "ביוטין",
    "פנטותנאט", "חומצה פנטותנית",
]

# Fruit concentrate markers (SC-4: treated as added sugar)
FRUIT_CONCENTRATE_MARKERS_HE = [
    "רכז", "תרכיז", "מיץ מרוכז", "רכז פרות",
    "סירופ תמרים", "סירופ תפוחים", "סירופ ענבים",
]

# ---------------------------------------------------------------------------
# Sprint 1 vocabulary — EV-003, EV-004, EV-005, EV-019
# ---------------------------------------------------------------------------

# EV-003 Tier 1 — High-risk emulsifiers (gut barrier disruption evidence)
HIGH_RISK_EMULSIFIER_PATTERNS = [
    "E466", "E-466", "carboxymethylcellulose", "carboxymethyl cellulose",
    "קרבוקסי מתיל צלולוזה", "קרבוקסי מתיל",
    "E433", "E-433", "polysorbate 80", "polysorbate-80",
    "פוליסורבט 80", "פוליסורבט-80",
    "E407", "E-407", "קרגינן", "carrageenan",
]

# EV-003 Tier 2 — Neutral emulsifiers (lecithin: exempt from additive penalty)
NEUTRAL_EMULSIFIER_PATTERNS = [
    "לציטין סויה", "לציטין חמניות", "לציטין חמניה", "סויה לציטין",
    "לציטין",
    "E322", "E-322",
]

# EV-019 — Prebiotic gums (exempt from stabilizer penalty)
PREBIOTIC_GUM_PATTERNS = [
    "גומי ערבי", "גומי אקאציה", "gum arabic", "acacia gum",
    "arabinogalactan",
    "E414", "E-414",
]

# EV-004 — Allulose detection
ALLULOSE_PATTERNS = [
    "allulose", "d-allulose", "psicose",
    "אלולוז", "d-אלולוז",
]

# EV-005 — Polyol type map (name → detection terms)
POLYOL_TYPE_MAP = {
    "sorbitol":   ["סורביטול", "sorbitol",    "E420", "E-420"],
    "mannitol":   ["מניטול",   "mannitol",    "E421", "E-421"],
    "xylitol":    ["קסיליטול", "xylitol",     "E967", "E-967"],
    "erythritol": ["אריתריטול","erythritol",  "E968", "E-968"],
    "maltitol":   ["מלטיטול",  "maltitol",    "E965", "E-965"],
    "isomalt":    ["איזומאלט", "isomalt",     "E953", "E-953"],
    "lactitol":   ["לקטיטול",  "lactitol",    "E966", "E-966"],
}

# Non-lecithin synthetic emulsifiers that still count in additive penalty
NON_LECITHIN_EMULSIFIER_RE = re.compile(
    r"E-?471|E-?472|E-?476|E-?481|DATEM|מונו.{0,5}גליצריד|דיגליצריד",
    re.IGNORECASE
)

# EV-005 humectant refinement — polyols inside manufacturer-declared humectant
# groups ("חומרי הלחה (גליצרול, סורביטול)") are moisture-retention agents,
# not sweetener loads. Captured content is the parenthetical group text.
HUMECTANT_GROUP_RE = re.compile(
    r'חומר(?:י)?\s+הלח[הא]\s*\(([^)]+)\)',
    re.IGNORECASE | re.UNICODE
)


def _search(text: str, patterns: list[str]) -> list[str]:
    """Return list of matched patterns (case-insensitive, multiline)."""
    found = []
    combined_text = text.lower()
    for p in patterns:
        if p.lower() in combined_text:
            found.append(p)
    return found


def _search_re(text: str, patterns: list[tuple]) -> dict[str, bool]:
    """Search regex patterns; return {category: True} for matched categories."""
    found = {}
    for pattern, category in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found[category] = True
    return found


# ---------------------------------------------------------------------------
# Sprint 1 detection helpers — EV-003, EV-004, EV-005, EV-019
# ---------------------------------------------------------------------------

def _detect_high_risk_emulsifier(text: str) -> tuple:
    found = [t for t in HIGH_RISK_EMULSIFIER_PATTERNS if t.lower() in text.lower()]
    return bool(found), found


def _detect_neutral_emulsifier(text: str) -> tuple:
    found = [t for t in NEUTRAL_EMULSIFIER_PATTERNS if t.lower() in text.lower()]
    return bool(found), found


def _detect_prebiotic_gum(text: str) -> tuple:
    found = [t for t in PREBIOTIC_GUM_PATTERNS if t.lower() in text.lower()]
    return bool(found), found


def _detect_allulose(text: str) -> bool:
    return any(p.lower() in text.lower() for p in ALLULOSE_PATTERNS)


def _count_polyol_types(text: str) -> tuple:
    detected = []
    for name, terms in POLYOL_TYPE_MAP.items():
        if any(t.lower() in text.lower() for t in terms):
            detected.append(name)
    return len(detected), detected


def _extract_humectant_group_polyols(text: str) -> set:
    """Return polyol names found inside manufacturer-labelled humectant groups."""
    result: set = set()
    for m in HUMECTANT_GROUP_RE.finditer(text):
        group = m.group(1)
        for name, terms in POLYOL_TYPE_MAP.items():
            if any(t.lower() in group.lower() for t in terms):
                result.add(name)
    return result


# ---------------------------------------------------------------------------
# TASK-144 Fix 1 — Ingredient-list OCR/disclaimer-bleed sanitizer (UPSTREAM HYGIENE)
# ---------------------------------------------------------------------------
# Bari evidence registry: EV-026 (TASK-144). Israeli retailer scrapes routinely glue
# nutrition-panel text and site disclaimers onto the ingredient list when the scraper
# captures a whole label/page block instead of just the ingredient statement. These
# phantom "ingredients" inflate ingredient_count and (with 0 additives, 0 added sugar)
# are the ONLY thing tripping the NOVA proxy ">5 ingredients" → NOVA 3 path
# (nova_proxy.py:117). This is a DATA-HYGIENE fix, not a scoring rule: it removes the
# cause (bad count) rather than adding a compensating penalty/relief. No new cap,
# floor, weight, or threshold. Conservative by design — it only drops items that are
# unambiguous non-ingredient bleed, and only TRUNCATES bleed glued onto an otherwise
# real ingredient (preserving the real head, e.g. "אבקת חלב.n20 גרם..." → "אבקת חלב").
# Observable: emits ingredient_sanitization{raw_count,clean_count,dropped,truncated}.

# Nutrition-panel tokens: appearance of these in an "ingredient" item marks it as a
# captured nutrition table, not an ingredient.
_BLEED_NUTRITION_TOKENS = [
    "ערכים תזונתיים", "ערך תזונתי", "אנרגיה", "קלוריות",
    " קל ", " קל,", "מג נתרן", "מג סידן", "מ\"ג", "מג ", "קל אנרגיה",
    "פחמימות מתוכן", "מתוכן סוכרים", "ל-100 גרם", "ל 100 גרם",
    "100 גרם", "100 מ\"ל", "100 מל",
]
# Disclaimer / boilerplate phrases captured from the retailer site.
_BLEED_DISCLAIMER_TOKENS = [
    "אין להסתמך", "יש לקרוא", "יתכנו טעויות", "אי התאמות",
    "להמחשה בלבד", "על גבי אריזת המוצר", "על גבי המוצר",
    "המופיע באתר", "התמונות והתאריכים", "לפני השימוש",
    "הנתונים המדויקים", "הינם להמחשה", "מופיע באתר",
]
# Gram/quantity-fragment pattern: an item that is essentially "<number> גרם <macro>"
# is a nutrition fragment, not an ingredient. Requires a number adjacent to a unit.
_BLEED_QTY_RE = re.compile(r"\d+(?:[.,]\d+)?\s*(?:גרם|ג'|מ\"ג|מג|קל|מ\"ל|מל)\b")
# Cut marker: bleed frequently glued onto a real ingredient via an OCR artifact like
# ".n" / ".\n" or a digit-led nutrition fragment. We truncate at the first such marker.
_BLEED_GLUE_RE = re.compile(r"\.?n?(?=\d)|\.n|\.\s")


# Panel-connector lead words: an "ingredient" that begins with one of these is a
# nutrition-breakdown fragment ("מתוכם 10.7 גרם..."), never a real ingredient.
_BLEED_CONNECTOR_LEADS = ("מתוכם", "מתוכן", "מהם", "הנתונים", "ובהם", "מזה")


def _looks_like_bleed(item: str) -> bool:
    """True if an ingredient-list item is non-ingredient OCR/nutrition/disclaimer bleed."""
    t = (item or "").strip()
    if not t:
        return True
    low = t
    if any(tok in low for tok in _BLEED_DISCLAIMER_TOKENS):
        return True
    if any(tok in low for tok in _BLEED_NUTRITION_TOKENS):
        return True
    # Heavy quantity-fragment content (e.g. "9.3 גרם קזאינים ... 72 קל אנרגיה ...")
    qty_hits = len(_BLEED_QTY_RE.findall(low))
    if qty_hits >= 2:
        return True
    # An item that STARTS with a quantity fragment ("10.7 גרם...") is panel bleed,
    # not an ingredient — real ingredients lead with the substance, not a measurement.
    if re.match(r"^\s*\d", t):
        return True
    # An item that STARTS with a nutrition-breakdown connector word is panel bleed even
    # after the trailing quantity is truncated off ("מתוכם" / "מהם" / "הנתונים").
    first_word = t.split()[0] if t.split() else ""
    if first_word in _BLEED_CONNECTOR_LEADS:
        return True
    return False


# Phrases that mark the START of nutrition-panel/disclaimer bleed glued onto a real
# ingredient head — truncate at the earliest of these (keep everything before).
_BLEED_CUT_PHRASES = [
    "ערכים תזונתיים", "ערך תזונתי", "הנתונים המדויקים", "אין להסתמך",
    "יש לקרוא", "יתכנו טעויות", "להמחשה בלבד", "מכיל חלב ערכים",
]


def _truncate_glued_bleed(item: str) -> str:
    """If a real ingredient has bleed glued on (e.g. 'אבקת חלב.n20 גרם...' or
    'חומוס ערכים תזונתיים 100 גרם...'), keep the head and drop the bleed tail."""
    t = (item or "").strip()
    cut = len(t)
    # Cut ONLY at unambiguous bleed glue: the '.n' OCR artifact (newline mis-captured),
    # or a digit-led quantity fragment ("... 20 גרם", "... 117 קל"). A BARE '.' is NOT a
    # cut point — in Israeli ingredient lists '.' is frequently an item SEPARATOR
    # ("חלב מפוסטר.מייצב"), so cutting there would silently delete a real downstream
    # ingredient (and its processing signal). Such separators are left intact.
    m = re.search(r"\.n(?=\d)|\.n\b|(?<=\D)\s\d+(?:[.,]\d+)?\s*(?:גרם|ג'|מ\"ג|מג|קל)\b", t)
    if m:
        cut = min(cut, m.start())
    # Nutrition-panel / disclaimer phrase boundary.
    for ph in _BLEED_CUT_PHRASES:
        idx = t.find(ph)
        if idx != -1:
            cut = min(cut, idx)
    if cut < len(t):
        head = t[:cut].strip(" .,;")
        if head:
            return head
    return t


def sanitize_ingredient_list(ingredients: list[str]) -> dict:
    """TASK-144 Fix 1 (EV-026): strip nutrition-panel / disclaimer bleed from a scraped
    ingredient list. Returns {clean, raw_count, clean_count, dropped, truncated}.
    Pure function, deterministic, no scoring side effects."""
    raw = [str(i) for i in (ingredients or [])]
    clean: list[str] = []
    dropped: list[str] = []
    truncated: list[dict] = []
    for item in raw:
        head = _truncate_glued_bleed(item)
        if head != item.strip():
            # head salvaged from a glued real ingredient; keep head only if it is itself
            # not bleed
            if head and not _looks_like_bleed(head):
                clean.append(head)
                truncated.append({"from": item, "to": head})
                continue
        if _looks_like_bleed(item):
            dropped.append(item)
            continue
        clean.append(item.strip())
    return {
        "clean": clean,
        "raw_count": len(raw),
        "clean_count": len(clean),
        "dropped": dropped,
        "truncated": truncated,
    }


def extract_signals(product: dict) -> dict:
    """
    Extract all signal layers for a product.
    Returns a structured dict with L1-L6 layers.
    All fields are explicit: None means absent, not zero.
    """
    nn = get_nutrition(product)
    ingredients_raw = get_ingredients(product)
    # TASK-144 Fix 1 (EV-026) — sanitize OCR/disclaimer bleed BEFORE any count or NOVA
    # inference. All downstream signal extraction uses the cleaned list; the raw list and
    # the sanitization delta are retained in L1 for full traceability.
    if TASK144_FIXES_ON:
        _san = sanitize_ingredient_list(ingredients_raw)
    else:
        _san = {"clean": list(ingredients_raw), "raw_count": len(ingredients_raw),
                "clean_count": len(ingredients_raw), "dropped": [], "truncated": []}
    ingredients = _san["clean"]
    ing_text = get_ingredients_text(product)
    trust_level, trust_score = get_trust(product)

    # -----------------------------------------------------------------------
    # L1: Observed facts (direct from BSIP1 — no inference)
    # -----------------------------------------------------------------------
    l1 = {
        "energy_kcal":      nn["energy_kcal"],
        "fat_g":            nn["fat_g"],
        "fat_saturated_g":  nn["fat_saturated_g"],
        "fat_trans_g":      nn["fat_trans_g"],
        "sodium_mg":        nn["sodium_mg"],
        "carbohydrates_g":  nn["carbohydrates_g"],
        "sugars_g":         nn["sugars_g"],
        "dietary_fiber_g":  nn["dietary_fiber_g"],
        "protein_g":        nn["protein_g"],
        "ingredient_count": len(ingredients),
        "ingredient_list":  ingredients,
        "ingredient_count_raw": _san["raw_count"],
        "ingredient_sanitization": {
            "raw_count":   _san["raw_count"],
            "clean_count": _san["clean_count"],
            "dropped":     _san["dropped"],
            "truncated":   _san["truncated"],
            "note": ("TASK-144 Fix1/EV-026: non-ingredient OCR/nutrition/disclaimer "
                     "bleed removed before NOVA count inference"),
        },
        "ingredient_text_quality": product.get("ingredient_text_quality"),
        "bsip1_trust_level":  trust_level,
        "bsip1_trust_score":  trust_score,
        "bsip1_risk_flags":   product.get("canonical_risk_flags") or [],
        "nutrition_consistency_status": product.get("nutrition_consistency_status"),
        "nutrition_consistency_warnings": product.get("nutrition_consistency_warnings") or [],
        "missing_nutrition_fields": [
            f for f in ["energy_kcal","fat_g","fat_saturated_g","sodium_mg",
                        "carbohydrates_g","sugars_g","dietary_fiber_g","protein_g"]
            if nn.get(f) is None
        ],
    }

    # Data consistency checks
    kcal  = nn["energy_kcal"]
    sugar = nn["sugars_g"]
    carbs = nn["carbohydrates_g"]
    sat_f = nn["fat_saturated_g"]
    fat   = nn["fat_g"]

    prot = nn["protein_g"]
    # TASK-144 (EV-026 companion) — macro plausibility. A single macro per 100g cannot
    # exceed ~100g, and the macro-implied energy cannot vastly exceed declared kcal. This
    # is a DATA-INTEGRITY check (sibling of kcal_plausible), not a scoring rule — it
    # catches OCR parse errors like protein_g=190 (a "19.0"→"190" misread) that would
    # otherwise survive into the score. Surfaced as a confidence deduction in score_engine.
    macro_over_100 = any((v is not None and v > 100) for v in (prot, fat, carbs))
    macro_kcal = None
    if any(v is not None for v in (prot, fat, carbs)):
        macro_kcal = (prot or 0) * 4 + (carbs or 0) * 4 + (fat or 0) * 9
    macro_energy_implausible = (
        kcal is not None and macro_kcal is not None and kcal > 0
        and macro_kcal > kcal * 2.0 + 50   # macros imply >2x the declared energy
    )
    macros_plausible = None
    if prot is not None or fat is not None or carbs is not None:
        macros_plausible = not (macro_over_100 or macro_energy_implausible)

    l1["consistency_checks"] = {
        "sugar_le_carbs":  None if (sugar is None or carbs is None) else (sugar <= carbs),
        "satfat_le_fat":   None if (sat_f is None or fat is None)   else (sat_f <= fat),
        "kcal_plausible":  None if kcal is None else (KCAL_PLAUSIBLE_LOWER <= kcal <= KCAL_PLAUSIBLE_UPPER),  # EV-047: upper raised 700→800
        "macros_plausible": macros_plausible,
    }

    # -----------------------------------------------------------------------
    # L2: Derived metrics (deterministic math on L1, never re-inferred)
    # -----------------------------------------------------------------------
    fat_pct_kcal = (fat * 9 / kcal * 100) if (fat is not None and kcal and kcal > 0) else None
    sat_frac     = (sat_f / fat) if (sat_f is not None and fat and fat > 0) else None
    sugar_carb_r = (sugar / carbs) if (sugar is not None and carbs and carbs > 0) else None
    prot_per_kcal = (nn["protein_g"] / kcal) if (nn["protein_g"] is not None and kcal and kcal > 0) else None

    l2 = {
        "fat_pct_of_kcal":       round(fat_pct_kcal, 2) if fat_pct_kcal is not None else None,
        "saturated_fat_fraction": round(sat_frac, 3)     if sat_frac is not None else None,
        "sugar_to_carb_ratio":   round(sugar_carb_r, 3) if sugar_carb_r is not None else None,
        "protein_per_kcal":      round(prot_per_kcal, 4) if prot_per_kcal is not None else None,
        "derivation_notes": [
            "fat_pct_of_kcal = (fat_g * 9 / energy_kcal) * 100",
            "saturated_fat_fraction = fat_saturated_g / fat_g",
            "sugar_to_carb_ratio = sugars_g / carbohydrates_g",
            "protein_per_kcal = protein_g / energy_kcal",
        ],
    }

    # -----------------------------------------------------------------------
    # L3: Inferred classifications (judgment required, confidence explicit)
    # -----------------------------------------------------------------------
    full_text = ing_text + " " + " ".join(ingredients)

    # Sweetener detection — tiered classification
    tier_a_he = _search(full_text, SWEETENER_TIER_A_HE)
    tier_a_e  = [e for e in SWEETENER_TIER_A_E if e.lower() in full_text.lower()]
    tier_b_he = _search(full_text, SWEETENER_TIER_B_HE)
    tier_b_e  = [e for e in SWEETENER_TIER_B_E if e.lower() in full_text.lower()]
    tier_c_he = _search(full_text, SWEETENER_TIER_C_HE)
    tier_c_e  = [e for e in SWEETENER_TIER_C_E if e.lower() in full_text.lower()]

    has_tier_a = bool(tier_a_he or tier_a_e)
    has_tier_b = bool(tier_b_he or tier_b_e)
    has_tier_c = bool(tier_c_he or tier_c_e)
    has_sweetener = has_tier_a or has_tier_b or has_tier_c

    # Worst tier dominates (C > B > A)
    if has_tier_c:
        sweetener_tier = "C"
    elif has_tier_b:
        sweetener_tier = "B"
    elif has_tier_a:
        sweetener_tier = "A"
    else:
        sweetener_tier = None

    sweetener_matches = tier_a_he + tier_a_e + tier_b_he + tier_b_e + tier_c_he + tier_c_e

    # Additive marker detection
    additive_categories = _search_re(full_text, ADDITIVE_MARKER_PATTERNS)
    # flavor_enhancer is the strongest NOVA 4 signal
    has_flavor_enhancer = additive_categories.get("flavor_enhancer", False)
    has_color = additive_categories.get("color", False)
    additive_marker_count = len(additive_categories)
    additive_categories_list = sorted(additive_categories.keys())

    # --- Sprint 1: EV-003/019 emulsifier tier detection ---
    high_risk_emuls_detected, high_risk_emuls_found = _detect_high_risk_emulsifier(full_text)
    neutral_emuls_detected,   neutral_emuls_found   = _detect_neutral_emulsifier(full_text)
    prebiotic_gum_detected,   prebiotic_gum_found   = _detect_prebiotic_gum(full_text)

    sprint1_additive_correction = 0
    correction_notes = []
    if "emulsifier" in additive_categories and neutral_emuls_detected:
        if not NON_LECITHIN_EMULSIFIER_RE.search(full_text) and not high_risk_emuls_detected:
            sprint1_additive_correction -= 1
            correction_notes.append("EV-003/019: lecithin-only emulsifier removed (-1)")
    if prebiotic_gum_detected and "stabilizer" in additive_categories:
        OTHER_STAB_RE = re.compile(r"E-?410|E-?412|E-?415|E-?440|מייצב(?!\s*גומי)", re.IGNORECASE)
        if not OTHER_STAB_RE.search(full_text):
            sprint1_additive_correction -= 1
            correction_notes.append("EV-019: prebiotic gum removed from stabilizer count (-1)")
    if high_risk_emuls_detected:
        sprint1_additive_correction += 2
        correction_notes.append(f"EV-003: high-risk emulsifier (+2): {high_risk_emuls_found[:2]}")
    sprint1_additive_count = max(0, additive_marker_count + sprint1_additive_correction)

    # --- TASK-133 (F1/F2/F4): ingredient identity + fragmentation via taxonomy ---
    # Resolves named additives (emulsifier identity, BHA/BHT) and structural form
    # (native vs modified starch, reconstructed protein, collagen) from ingredient
    # text. Magnitudes are applied downstream in the engine; this only emits IDENTITY.
    ingredient_order = [{"text": ing, "position": i + 1} for i, ing in enumerate(ingredients)]
    if not ingredient_order and ing_text:
        # fall back to the comma/and-split text when no structured list is present
        parts = [p.strip() for p in re.split(r"[,;•\n]| ו(?=[א-ת])", ing_text) if p.strip()]
        ingredient_order = [{"text": p, "position": i + 1} for i, p in enumerate(parts)]

    tax_emulsifier_concern: list[str] = []   # carrageenan / CMC / polysorbate-80 (F1 up)
    tax_emulsifier_benign:  list[str] = []   # soy / sunflower lecithin (F1 down)
    tax_named_concern_additives: list[str] = []
    tax_bha_present = False                  # F4 named penalty
    tax_bht_present = False                  # F4 explicitly NOT penalized
    for item in ingredient_order:
        ident = itax.resolve_additive(item["text"], None)
        if ident is None:
            continue
        if ident.additive_class == "emulsifier_concern" and ident.canonical not in tax_emulsifier_concern:
            tax_emulsifier_concern.append(ident.canonical)
        elif ident.additive_class == "emulsifier_benign" and ident.canonical not in tax_emulsifier_benign:
            tax_emulsifier_benign.append(ident.canonical)
        if ident.canonical == "bha":
            tax_bha_present = True
        if ident.canonical == "bht":
            tax_bht_present = True
        if ident.is_named_concern and ident.canonical not in tax_named_concern_additives:
            tax_named_concern_additives.append(ident.canonical)

    # Structural form of the PRIMARY ingredients (Req 3/Req 5 — gaming-resistant)
    frag_profile = itax.primary_fragmentation_profile(ingredient_order, [])

    # Native vs modified starch (F1: native starch leaves the additive burden)
    tax_native_starch = False
    tax_modified_starch = False
    for item in ingredient_order:
        s_ident = itax.resolve_structural(item["text"], None)
        if s_ident is None:
            continue
        if s_ident.canonical == "native_starch":
            tax_native_starch = True
        elif s_ident.canonical == "modified_starch":
            tax_modified_starch = True

    # F2: collagen marker (reconstructed-protein matrix form is set below, once the
    # isolate-marker detection has run).
    has_collagen = bool(_search(full_text, COLLAGEN_MARKERS_HE))

    # --- Sprint 1: EV-004 allulose ---
    allulose_detected = _detect_allulose(full_text)

    # --- Sprint 1: EV-005 polyol count with humectant refinement ---
    polyol_count, detected_polyols   = _count_polyol_types(full_text)
    humectant_polyols_detected        = _extract_humectant_group_polyols(full_text)
    penalty_polyols                   = [p for p in detected_polyols if p not in humectant_polyols_detected]
    penalty_polyol_count              = len(penalty_polyols)

    # Seed oil
    seed_oil_matches = _search(full_text, SEED_OIL_MARKERS_HE)
    has_seed_oil = bool(seed_oil_matches)

    # Palm oil
    palm_oil_matches = _search(full_text, PALM_OIL_MARKERS_HE)
    has_palm_oil = bool(palm_oil_matches)

    # Whole grain
    whole_grain_matches = _search(full_text, WHOLE_GRAIN_MARKERS_HE)
    has_whole_grain = bool(whole_grain_matches)

    # R-04: plain dairy detection (first three ingredients) — computed here (ahead of the
    # protein-source block) because TASK-144 Fix 3 dairy-source typing depends on it.
    DAIRY_BASE_MARKERS_HE = ["חלב", "יוגורט", "גבינת", "מי גבינה", "קזאין"]
    first_three_text = " ".join(ingredients[:3]).lower() if ingredients else ing_text[:200].lower()
    product_type_dairy = any(m in first_three_text for m in DAIRY_BASE_MARKERS_HE)

    # Protein source
    isolate_matches = _search(full_text, PROTEIN_ISOLATE_MARKERS_HE)
    # TASK-144 Fix 3 / EV-028 — dairy protein source typing.
    # Pure-dairy protein (whey + casein + milk-protein, reconstituted from milk powder)
    # is a complete, high-DIAAS protein; the generic "mixed" ×0.85 haircut is for
    # genuinely blended/uncertain sources and is not justified here. Type as "dairy"
    # (factor 1.0) ONLY when the product is a dairy matrix AND every isolate marker found
    # is a WHOLE dried-dairy ingredient (milk powder / milk protein), i.e. NOT an
    # extracted protein FRACTION/isolate. This deliberately does NOT relieve reconstructed
    # protein-isolate products (whey/soy/pea/egg fractions) — those keep "mixed", and the
    # F2/TASK-133B bar-format reconstructed discount (which gates on RECONSTRUCTED_PROTEIN
    # markers, never on milk powder) remains fully intact. No collision: Fix 3 sets the
    # source FACTOR; F2 sets an independent matrix-form DISCOUNT multiplier.
    DAIRY_WHOLE_PROTEIN_MARKERS = ["אבקת חלב", "חלבון חלב", "חלבוני חלב", "קזאין"]
    NONDAIRY_OR_FRACTION_MARKERS = [
        "חלבון מי גבינה", "חלבון סויה", "חלבון חיטה", "חלבון אפונה",
        "חלבון ביצה", "חלבון קזאין", "אייזולאט", "איזולאט",
    ]
    if isolate_matches:
        has_fraction = any(m in full_text for m in NONDAIRY_OR_FRACTION_MARKERS)
        if TASK144_FIXES_ON and product_type_dairy and not has_fraction:
            protein_source = "dairy"   # complete dairy protein — no mixed haircut (EV-028)
            protein_source_basis = [m for m in isolate_matches] + ["dairy matrix, no extracted fraction"]
        else:
            protein_source = "mixed"   # likely mixed whole+isolate
            protein_source_basis = isolate_matches
    elif nn["protein_g"] and nn["protein_g"] > 0:
        protein_source = "whole_food"
        protein_source_basis = ["no isolate markers detected"]
    else:
        protein_source = "unknown"
        protein_source_basis = ["insufficient protein signal"]

    # F2 / TASK-133B — protein matrix form (drives the bar-format quality discount).
    # PRIMARY-INGREDIENT GATED (Req 3 / Req 5): only a protein fraction in the primary
    # positions counts — a trace garnish (e.g. 0.6% soy-protein crisps, 1.5% collagen
    # on a milk base) must NOT discount the dominant whole/dairy protein. The
    # most-primary protein marker decides the form:
    #   collagen      — incomplete AA profile, lowest matrix DIAAS (strongest discount)
    #   reconstructed — extracted protein FRACTION (whey/soy/pea/egg/casein, isolate);
    #                   excludes milk powder (not a fraction)
    #   None          — whole-food / in-context / trace-only protein (no discount)
    PROTEIN_PRIMARY_WINDOW = 3
    protein_matrix_form = None
    for item in ingredient_order:
        pos = item.get("position") or 99
        if pos > PROTEIN_PRIMARY_WINDOW:
            continue
        txt = item.get("text", "")
        if any(m in txt for m in COLLAGEN_MARKERS_HE):
            protein_matrix_form = "collagen"
            break
        if any(m in txt for m in RECONSTRUCTED_PROTEIN_MARKERS_HE):
            protein_matrix_form = "reconstructed"
            break

    # Added sugar sources (for SC classification and MULTIPLE_ADDED_SUGAR_MARKERS)
    added_sugar_matches = [m for m in ADDED_SUGAR_MARKERS_HE
                          if m in full_text and m != "דבש"]  # honey is SC-2 adjacent
    added_sugar_count = len(added_sugar_matches)

    # Fruit concentrate (SC-4 signal)
    fruit_conc_matches = _search(full_text, FRUIT_CONCENTRATE_MARKERS_HE)
    has_fruit_concentrate = bool(fruit_conc_matches)

    # Fermentation
    ferm_matches = _search(full_text, FERMENTATION_MARKERS_HE)
    has_fermentation = bool(ferm_matches)

    # Trans fat flag
    # fat_trans_g == 0.5 exactly is the Israeli nutritional labeling convention for "< 1g"
    # (mandatory declaration threshold). Treat as a possible artifact, not a confirmed real signal.
    trans_fat_g = nn["fat_trans_g"]
    if trans_fat_g is not None and trans_fat_g > 1.0:
        trans_fat_status = "veto"
    elif trans_fat_g is not None and trans_fat_g > 0.5:
        trans_fat_status = "high_concern"
    elif trans_fat_g is not None and trans_fat_g == 0.5:
        trans_fat_status = "threshold_declaration"
    elif trans_fat_g is not None and trans_fat_g > 0.2:
        trans_fat_status = "present"
    else:
        trans_fat_status = "not_detected"
    trans_fat_threshold_artifact = (trans_fat_g == 0.5)

    # EV-050 — Partially-hydrogenated vegetable oil (PHVO) detection.
    # PHVO is the sole source of industrial trans fat in packaged foods. Natural dairy trans
    # fat (CLA, vaccenic acid) does NOT originate from PHVO and cannot be identified by PHVO
    # markers. Absence of PHVO markers is therefore the necessary condition for the natural-
    # dairy-trans-fat exemption gate in evaluate_guardrails (score_engine.py).
    # Hebrew terms: "שומן צמחי מוקשה" (hydrogenated vegetable fat),
    # "שמן צמחי מוקשה" (hydrogenated vegetable oil), "מוקשה חלקית" (partially hydrogenated),
    # "partially hydrogenated" (English label imports). The bare "מוקשה" (hardened/modified)
    # is NOT included — it appears in thickener context ("עמילן מוקשה") and is already
    # caught by ADDITIVE_MARKER_PATTERNS; adding it here would false-fire on starch.
    _PHVO_MARKERS = [
        "שומן צמחי מוקשה",    # hydrogenated vegetable fat
        "שמן צמחי מוקשה",     # hydrogenated vegetable oil
        "מוקשה חלקית",        # partially hydrogenated
        "partially hydrogenated",
    ]
    has_phvo = any(m in full_text for m in _PHVO_MARKERS)

    # Fortification detection
    has_fortification_explicit = any(m in full_text for m in FORTIFICATION_EXPLICIT_HE)
    vitamin_hits = [v for v in SYNTHETIC_VITAMIN_HE if v in full_text]
    has_fortification_inferred = len(set(vitamin_hits)) >= 2
    has_fortification = has_fortification_explicit or has_fortification_inferred
    fortification_evidence = (
        (["explicit: מועשר/מחוזק"] if has_fortification_explicit else []) +
        (vitamin_hits[:6] if has_fortification_inferred else [])
    )

    # Israeli red labels (Israeli Ministry of Health thresholds)
    red_labels = []
    if sugar is not None and sugar > 17.5:
        red_labels.append("sugar")
    if sat_f is not None and sat_f > 5.0:
        red_labels.append("sat_fat")
    if nn["sodium_mg"] is not None and nn["sodium_mg"] > 600:
        red_labels.append("sodium")

    # Hyper-palatability patterns (raw compositional check; NOVA gate applied in score_engine)
    hp_fat_sugar_raw = (
        fat_pct_kcal is not None and fat_pct_kcal >= 30 and
        sugar is not None and sugar >= 20
    )
    hp_fat_sodium_raw = (
        fat_pct_kcal is not None and fat_pct_kcal >= 25 and
        nn["sodium_mg"] is not None and nn["sodium_mg"] >= 300
    )

    l3 = {
        "sweetener_detected":       has_sweetener,
        "sweetener_tier":           sweetener_tier,
        "sweetener_matches":        sweetener_matches,
        "additive_marker_count":    additive_marker_count,
        "additive_categories":      additive_categories_list,
        "has_flavor_enhancer":      has_flavor_enhancer,
        "has_artificial_color":     has_color,
        "has_seed_oil":             has_seed_oil,
        "seed_oil_matches":         seed_oil_matches,
        "has_palm_oil":             has_palm_oil,
        "palm_oil_matches":         palm_oil_matches,
        "has_whole_grain":          has_whole_grain,
        "whole_grain_matches":      whole_grain_matches,
        "protein_source":           protein_source,
        "protein_source_basis":     protein_source_basis,
        "added_sugar_sources_count": added_sugar_count,
        "added_sugar_matches":      added_sugar_matches[:8],  # cap list for readability
        "has_fruit_concentrate":    has_fruit_concentrate,
        "has_fermentation":         has_fermentation,
        "product_type_dairy":       product_type_dairy,
        "has_fortification":        has_fortification,
        "fortification_evidence":   fortification_evidence,
        "trans_fat_status":         trans_fat_status,
        "trans_fat_threshold_declaration_possible": trans_fat_threshold_artifact,
        "has_phvo":                 has_phvo,   # EV-050: partially-hydrogenated vegetable oil marker
        "red_labels":               red_labels,
        "red_label_count":          len(red_labels),
        "hp_fat_sugar_pattern_raw": hp_fat_sugar_raw,
        "hp_fat_sodium_pattern_raw": hp_fat_sodium_raw,
        # Sprint 1 fields — EV-003/004/005/019
        "sprint1_high_risk_emulsifier_detected": high_risk_emuls_detected,
        "sprint1_high_risk_emulsifier_found":    high_risk_emuls_found,
        "sprint1_neutral_emulsifier_detected":   neutral_emuls_detected,
        "sprint1_neutral_emulsifier_found":      neutral_emuls_found,
        "sprint1_prebiotic_gum_detected":        prebiotic_gum_detected,
        "sprint1_prebiotic_gum_found":           prebiotic_gum_found,
        "sprint1_additive_count":                sprint1_additive_count,
        "sprint1_additive_correction":           sprint1_additive_correction,
        "sprint1_additive_correction_notes":     correction_notes,
        "sprint1_allulose_detected":             allulose_detected,
        "sprint1_polyol_count":                  polyol_count,
        "sprint1_detected_polyols":              detected_polyols,
        "sprint1_humectant_polyols":             sorted(humectant_polyols_detected),
        "sprint1_penalty_polyol_count":          penalty_polyol_count,
        "sprint1_penalty_polyols":               penalty_polyols,
        # TASK-133 (F1/F2/F4) — ingredient identity + fragmentation (magnitudes applied downstream)
        "tax_emulsifier_concern":                tax_emulsifier_concern,      # F1: carrageenan/CMC/P80 (up)
        "tax_emulsifier_benign":                 tax_emulsifier_benign,       # F1: lecithin (toward neutral)
        "tax_named_concern_additives":           tax_named_concern_additives,
        "tax_native_starch":                     tax_native_starch,           # F1: out of additive burden
        "tax_modified_starch":                   tax_modified_starch,         # F1: stays penalized
        "tax_bha_present":                       tax_bha_present,             # F4: small named penalty
        "tax_bht_present":                       tax_bht_present,             # F4: explicitly NOT penalized
        "has_collagen":                          has_collagen,                # F2: strongest matrix discount
        "protein_matrix_form":                   protein_matrix_form,         # F2: collagen|reconstructed|None
        # TASK-144 Fix1/EV-026 — sanitized ingredient count (OCR/disclaimer bleed removed).
        # nova_proxy consumes THIS rather than the raw product list so phantom ingredients
        # no longer trip the ">5 ingredients" NOVA-3 path.
        "sanitized_ingredient_count":            len(ingredients),
        "primary_fragmentation":                 frag_profile.get("dominant_fragmentation"),
        "inference_confidence_notes": [
            "Ingredient analysis uses keyword matching on Hebrew text — may miss transliterations or abbreviations",
            "Sweetener detection relies on known Hebrew/E-number terms; novel sweeteners not in dictionary will be missed",
            "Additive count reflects distinct functional categories detected, not total additive instances",
            "Sprint 1: EV-003/019/004/005 signals active; sprint1_additive_count is the scoring-ready count",
            "EV-005 humectant refinement: penalty_polyol_count excludes polyols in humectant groups",
        ],
    }

    # -----------------------------------------------------------------------
    # L4: Interpreted concerns (threshold-based guardrail decisions)
    # Populated by score_engine; listed here as placeholders for trace clarity
    # -----------------------------------------------------------------------
    l4 = {
        "note": "L4 interpreted concerns are evaluated in score_engine and written to caps_applied / penalties_applied",
        "pre_evaluation_flags": [],
    }
    if l1["consistency_checks"]["sugar_le_carbs"] is False:
        l4["pre_evaluation_flags"].append("SUGAR_EXCEEDS_CARBS: data integrity concern, score confidence reduced")
    if l1["consistency_checks"]["satfat_le_fat"] is False:
        l4["pre_evaluation_flags"].append("SATFAT_EXCEEDS_FAT: data integrity concern, score confidence reduced")
    if l1["consistency_checks"]["kcal_plausible"] is False:
        l4["pre_evaluation_flags"].append(f"KCAL_IMPLAUSIBLE: outside {KCAL_PLAUSIBLE_LOWER}-{KCAL_PLAUSIBLE_UPPER} range, confidence severely reduced")
    if product.get("nutrition_consistency_status") == "suspicious":
        l4["pre_evaluation_flags"].append("BSIP1_SUSPICIOUS_NUTRITION: product may have per-serving/per-100g confusion")
    if product.get("nutrition_consistency_status") == "warnings":
        l4["pre_evaluation_flags"].append("BSIP1_NUTRITION_WARNINGS: cross-retailer disagreement detected")

    # -----------------------------------------------------------------------
    # L5: Behavioral hypotheses embedded in the scoring model
    # -----------------------------------------------------------------------
    l5 = {
        "hypotheses_active": [
            "High added sugar (>17.5g) correlates with poorer glycemic outcomes at population level",
            "NOVA 4 ultra-processed foods associate with poorer health outcomes at population level (epidemiological evidence)",
            "HP patterns (fat+sugar, fat+sodium) may override satiety signaling",
            "Whole grain presence modulates glycemic response",
            "Low calorie density (within whole-food context) associates with lower energy intake",
        ],
        "hypothesis_limitations": [
            "Per-100g frame does not reflect actual consumption volume",
            "Individual product does not establish population-level risk",
            "HP patterns rely on compositional thresholds, not behavioral evidence for specific product",
        ],
    }

    # -----------------------------------------------------------------------
    # L6: Normative / policy decisions embedded in the scoring architecture
    # -----------------------------------------------------------------------
    l6 = {
        "policy_commitments": [
            "NOVA 1 single-ingredient whole foods receive minimum score of 75 (normative floor, not empirical)",
            "Sweetener presence caps score at 70 regardless of other signals (policy commitment: sweeteners ≠ quality improvement)",
            "Trans fat veto (score=0) is a hard safety commitment, not a continuous signal",
            "Israeli red labels are incorporated as regulatory signals (policy: regulatory alignment)",
            "Whole-food floors override architecture-mismatch caps (SRC-01 policy)",
        ],
        "architecture_version": "bsip2_concept_v1 + score_resolution_contract_SRC-v1",
    }

    return {
        "L1_observed_signals":        l1,
        "L2_derived_signals":         l2,
        "L3_inferred_classifications": l3,
        "L4_interpreted_concerns":    l4,
        "L5_behavioral_hypotheses":   l5,
        "L6_policy_decisions":        l6,
    }
