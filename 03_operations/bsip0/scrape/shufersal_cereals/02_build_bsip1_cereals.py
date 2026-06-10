"""
BSIP1 Builder — Breakfast Cereals (run_cereals_002) from Shufersal BSIP0 raw.

Reads:  C:\\Bari\\02_products\\breakfast_cereals\\bsip0_outputs\\cereals_bsip0_raw_*.json (latest)
Writes: C:\\Bari\\03_operations\\bsip1\\run_cereals_002\\output\\bsip1_*.json
        + curation_report.json
        + cereals_constructs_report.json  (category-level rollup of the 4 governance constructs)

Schema: bsip1_v0_1 — mirrors run_yogurt_003 BSIP1 files.
Enrichment: core ingredient_enricher.py (additives / matrix markers / sweeteners).

APPLIES THE FOUR CEREALS GOVERNANCE CONSTRUCTS (cereals_gap_resolution_v1.md), as
label-observable CLASSIFICATION / DISCLOSURE layers — NOT score changes:
  C1 Granola sub-pool      (Constitution Art. II Rule 5 / Resolution 3, Sec 2.9)
  C2 Children's product    (Constitution Art. II Sec 2.8 / Resolution 1)
  C3 Whole-grain threshold (Guardrails v2 Sec 5.2.1 / Resolution 4)
  C4 Endemic fortification (Constitution Art. VI Sec 6.4 / Resolution 2, DISTORTION-004)
"""
from __future__ import annotations

import json
import re
import sys
import pathlib
import logging
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip1\core")))
from ingredient_enricher import enrich as enrich_product

# Canonical BSIP0 numeric extraction (TASK-192 / EV-046). The per-builder _parse_num /
# _parse_sodium / _parse_nutrition below now DELEGATE to the single shared path so the
# "פחות מ N" less-than handling, the total_fat >= saturated_fat invariant, and the
# field set can never drift between categories (the drift that let the EV-029 fat
# mis-capture recur a 3rd time in run_cereals_005).
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")))
from bsip0_nutrition import (  # noqa: E402
    parse_num as _shared_parse_num,
    parse_sodium_mg as _shared_parse_sodium,
    parse_nutrition_numeric as _shared_parse_nutrition,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

import os
RAW_DIR = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs")
# RUN_ID overridable so a re-curated clean run (EV-045) writes to a new dir and the
# frozen run_cereals_002 corpus stays intact. Default preserves original behavior.
RUN_ID = os.environ.get("CEREALS_RUN_ID", "run_cereals_002")
OUT_DIR = pathlib.Path(rf"C:\Bari\03_operations\bsip1\{RUN_ID}\output")
SOURCE = "shufersal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Curation signals (final pass — defends against scrape leakage) ──────────────
BAR_RE       = re.compile(r"חטיף|\bbar\b|\bבר\b|מקופלת|ביסקוויט|עוגי|ופל|wafer", re.I)
# Non-cereal contaminants that leak via grain tokens (כוסמין/דגנים/שיבולת שועל):
# breads, pita, rolls, sourdough loaves, and dairy desserts. Same false-positive class as
# the run_yogurt_003 olive leak — removed at curation for corpus purity (Constitution Art. II).
NONCEREAL_RE = re.compile(r"קרקר|cracker|פריכי|rice cake|משקה|\bdrink\b|יוגורט|yog[hu]?urt|"
                          r"דייסת תינוק|מטרנה|סימילק|תוסף|קפסול|חמאת|ממרח|שוקולד למריחה|"
                          r"לחם|לחמני|פיתה|פיתות|מחמצת|בגט|baguette|מעדן|פודינג|מוס", re.I)

# ── EV-045 — PTITIM / pasta exclusion (TASK-140 corpus contamination, owner 2026-06-05) ──
# Israeli "פתיתים" (standalone plural noun) = toasted wheat/spelt-flour PASTA (Osem /
# Intaria / השדה), sold in shapes (קוסקוס / טבעות / כוכבים / אורז / בן גוריון). It is a
# STARCH SIDE-DISH, not a bowl-and-milk breakfast cereal. The homonym trap that
# contaminated run_cereals_002/004: the CEREAL_RE token "פתיתי" matched these.
# Disambiguation rule:
#   • "פתיתי X" (construct form, e.g. פתיתי תירס = corn FLAKES) IS cereal — uses yod ending.
#   • "פתיתים" (plural noun, mem-sofit ending) + אפויים / אורגנים / a pasta-shape token,
#     OR whose ingredients are essentially "[grain] flour (+ semolina) + water", is PASTA.
# This is a CORPUS-PURITY exclusion (remove), NOT a scoring penalty — see
# contamination_not_calibration_v1 governance rule.
PTITIM_PASTA_NAME_RE = re.compile(
    r"פתיתים\s+אפויים|פתיתים\s+אורגנים|"
    r"פתיתים.*(קוסקוס|טבעות|כוכבים|כוכבונים|בן\s*גוריון|אותיות)", re.I)
PTITIM_WORD_RE = re.compile(r"\bפתיתים\b|^פתיתים", re.I)
# Ingredient signature of ptitim pasta: flour/semolina (+water), nothing else cereal-like.
PASTA_INGREDIENT_RE = re.compile(r"קמח\s+(חיטה|כוסמין|דורום)|סולת|semolina|durum", re.I)
NON_PASTA_INGREDIENT_RE = re.compile(
    r"סוכר|דבש|סילאן|שיבולת שועל|שיפון|פצפוצי|תירס|אגוז|שקד|צימוק|פירות|"
    r"שוקולד|קקאו|ויטמין|פתית|flake|sugar|honey|oat|corn|nut|raisin", re.I)


# A breakfast cereal is never the plural NOUN "פתיתים" as its head word — cereal
# flakes use the construct "פתיתי X" (פתיתי תירס = corn flakes). A name HEADED by
# "פתיתים" is the ptitim pasta product (incl. gluten-free corn/rice ptitim).
PTITIM_HEAD_RE = re.compile(r"^\s*פתיתים\b")

# Bread/baked-good leakage: a yeast/sourdough-leavened loaf masquerading as "whole
# spelt/wheat cereal" (e.g. כוסמין מלא 100% = spelt bread). RTE breakfast cereals are
# not yeast-leavened, so yeast / sourdough / "מהלחם" in the ingredient panel = bread.
# CRITICAL substring trap (EV-029 family): the yeast word "שמרים" is a substring of the
# PRESERVATIVES word "משמרים" ("ללא חומרים משמרים" = "no preservatives"). A naive match
# falsely excludes Nesquik / Cini Minis / Lion. Hebrew word-boundary lookbehind required:
# require שמרים to NOT be preceded by a Hebrew letter (so מ-שמרים = preservatives is skipped).
BREAD_INGREDIENT_RE = re.compile(r"(?<![א-ת])שמרים|מחמצת|מהלחם|sourdough|\byeast\b", re.I)


def _is_ptitim_pasta(name: str, ingr_text: str) -> bool:
    """True iff the product is Israeli ptitim PASTA masquerading as a cereal."""
    if PTITIM_HEAD_RE.search(name) or PTITIM_PASTA_NAME_RE.search(name):
        return True
    # Standalone "פתיתים" (plural noun) whose ingredient panel is just flour(+water).
    if PTITIM_WORD_RE.search(name):
        if PASTA_INGREDIENT_RE.search(ingr_text) and not NON_PASTA_INGREDIENT_RE.search(ingr_text):
            return True
    return False


def _is_bread_leakage(ingr_text: str) -> bool:
    """True iff the ingredient panel reveals a yeast/sourdough-leavened bread."""
    return bool(BREAD_INGREDIENT_RE.search(ingr_text or ""))


# ── EV-045b — full food-class contaminant sweep (TASK-140 full-QA pass, owner 2026-06-05) ──
# The first EV-045 pass removed ptitim + bread. A complete shelf audit found four more
# contaminant classes that leaked in: pasta, flour-as-product, chocolate confections, and a
# drink. All are removed at curation (GATE 1, contamination ≠ calibration), not re-graded.
PASTA_RE   = re.compile(r"פסטה|נודלס|פטוצ|אטריות|ספגטי|קנג'?אק|konjac|\bnoodle", re.I)
DRINK_RE   = re.compile(r"\bמשקה\b|מיצוי שיבולת שועל|משקה שיבולת", re.I)
# A dry RTE breakfast cereal/granola is ~250–540 kcal/100g. Below this floor the product is
# either a wet product (drink/fresh) or carries an implausible per-serving parse — not a
# trustworthy dry-cereal value. Lowest legitimate dry items observed: oat bran 246, Weetabix 342.
DRY_CEREAL_ENERGY_FLOOR = 150.0


def _first_ingredient(ingr_text: str) -> str:
    return re.split(r"[,\(]", (ingr_text or "").strip())[0]


def _is_confection(name: str, ingr_text: str) -> bool:
    """Chocolate bar / candy-coated cluster masquerading as cereal. Distinguished from a
    legitimate chocolate-FLAVOURED grain cereal (which lists a grain flour first) by:
    chocolate as the product head, the first ingredient, ≥50% by mass, a chocolate coating,
    or a sugar-first panel built on cocoa butter."""
    head = (name or "").strip().split(" ")[0] if name else ""
    if head == "שוקולד":
        return True
    fi = _first_ingredient(ingr_text)
    if "שוקולד" in fi:
        return True
    m = re.search(r"שוקולד[^,]{0,14}\((\d{2})", ingr_text or "")
    if m and int(m.group(1)) >= 50:
        return True
    if (ingr_text or "").strip().startswith("ציפוי שוקולד"):
        return True
    if fi.startswith("סוכר") and "חמאת קקאו" in (ingr_text or ""):
        return True
    return False


# ── EV-045d — plain oats OUT OF SCOPE for breakfast-cereals (owner directive 2026-06-05) ──
# Plain rolled / quick / instant oats, Quaker, and oat bran (porridge staples eaten cooked) are
# NOT boxed RTE breakfast cereals and NOT granola — the owner ruled them off the cereals page and
# off the site (not a separate category). This is a SCOPE exclusion (owner choice), mechanically a
# curation drop. Scoped to the product BEING plain oats (name headed by שיבולת שועל / סובין / קוואקר
# / Quaker / rolled-oats), and GUARDED so it never catches oat-FLOUR RTE cereals (Cheerios/צ'יריוס),
# granola/muesli, or flavoured grain cereals that merely contain oats.
PLAIN_OATS_NAME_RE = re.compile(
    r"^\s*שיבולת\s+שועל|^\s*סובין\s+שיבולת\s+שועל|^\s*קוואקר|\bquaker\b|"
    r"rolled\s+oats|steel.?cut\s+oats|porridge\s+oats", re.I)
PLAIN_OATS_GUARD_RE = re.compile(
    r"דגני|פצפוצ|טבעות|כדורי|מוזלי|גרנולה|granola|muesli|צ['׳]?יריוס|cheerios|"
    r"ריבוע|צדפי|שוקולד|קקאו|תירס|cocoa|choco", re.I)


def _is_plain_oats(name: str) -> bool:
    """True iff the product is plain porridge oats / oat bran (out of cereals scope)."""
    return bool(PLAIN_OATS_NAME_RE.search(name or "")) and not PLAIN_OATS_GUARD_RE.search(name or "")


def _contaminant_reason(name: str, ingr_text: str, energy_kcal) -> str | None:
    """Return an exclusion reason if the product is not a dry breakfast cereal, else None."""
    if PASTA_RE.search(name) or PASTA_RE.search(ingr_text):
        return "pasta_excluded"
    if (name or "").strip().split(" ")[0] == "קמח":          # flour AS the product (not as an ingredient)
        return "flour_product_excluded"
    if _is_confection(name, ingr_text):
        return "chocolate_confection_excluded"
    if DRINK_RE.search(name) or DRINK_RE.search(ingr_text) or "וויט" in (name or ""):
        return "drink_excluded"
    if energy_kcal is not None and energy_kcal < DRY_CEREAL_ENERGY_FLOOR:
        return "energy_implausible_for_dry_cereal"  # wet product or per-serving parse error
    return None


# ── EV-045c — Nestlé "Fitness" savory-cracker guard (TASK-184 multi-retailer recall, owner 2026-06-05) ──
# Recall finding on UNSEEN data: the Nestlé "Fitness / פיטנס" brand line spans TWO food classes —
# (a) genuine RTE breakfast CEREALS (קורנפלקס פיטנס, Fitness almond/honey, Chocolate&Rice cereal,
# Fitness granola) and (b) savory CRACKERS / crispbreads / פרכיות (פיטנס מלח פלפל, רוזמרין, סלק, בטטה,
# זיתים, Veggie Mix, Thin/Thins, קרקר כפרי). The crackers evade EV-045b: they carry no קרקר token in
# the *price-feed* name on some SKUs, are not chocolate, and ride in on the broad fitness/פיטנס token
# in CEREAL_RE. Their macro signature separates them: fat ≥ ~13 g/100g (476 kcal/22.4g salt-pepper;
# 461/17g; 460/16.7g Veggie) vs genuine Fitness *cereals* at 2–8 g fat.
#
# POLICY = FLAG-NOT-DROP (per TASK-183 §2 #5 brand-line policy + contamination_not_calibration_v1).
# We do NOT silently exclude (a bare fat-floor would false-positive a real Fitness GRANOLA — granola
# legitimately runs 13–16 g fat). Instead we MARK the SKU with a quarantine flag carried into the
# BSIP1 record; the downstream router already misroutes most of these to default/beverage, and the
# flag makes the curation-layer evidence explicit + auditable rather than relying on router luck.
#
# SCOPE: only SKUs whose cereal eligibility rests on the fitness/פיטנס brand token (FITNESS_BRAND_RE).
# A non-Fitness granola is never touched by this guard.
# TRIGGER (within scope):
#   • a SAVORY descriptor in the name (מלח/פלפל/רוזמרין/שום/סלק/בטטה/זית/צ'ילי/כפרי/מתובל/תיבול/
#     veggie/vegetable/cracker/קרקר/thin/thins/פרכי/פריכי), OR
#   • fat ≥ 13 g/100g AND the SKU shows NO sweet/granola/muesli signal (no granola/muesli token and
#     sugars < 12 g) — i.e. a high-fat NON-sweet Fitness item, which is the cracker, not the granola.
# Hebrew word-boundary discipline (EV-029 family): the savory token "מלח" (salt) is a substring of
# "מלא" only by sharing מל — guarded by requiring the descriptor as a whole token where ambiguous;
# "זית" (olive) is the construct head of "זיתים". Tokens chosen to avoid the משמרים/שמרים-class trap.
FITNESS_BRAND_RE      = re.compile(r"\bfitness\b|פיטנס", re.I)
FITNESS_SAVORY_RE     = re.compile(
    r"(?<![א-ת])מלח(?![א-ת])|פלפל|רוזמרין|(?<![א-ת])שום(?![א-ת])|(?<![א-ת])סלק|בטטה|"
    r"(?<![א-ת])זית|צ'?ילי|chili|כפרי|מתובל|תיבול|veggie|vegetable|"
    r"קרקר|cracker|(?<![א-ת])thins?\b|פרכי|פריכי", re.I)
FITNESS_SWEET_RE      = re.compile(r"גרנולה|granola|מוזלי|מוסלי|muesli|דבש|honey|שוקולד|chocolate|"
                                   r"חמוצי|cranberr|פירות|צימוק|almond|שקד", re.I)
FITNESS_FAT_FLOOR     = 13.0


def fitness_noncereal_flag(name: str, ingr_text: str, nn: dict) -> dict | None:
    """EV-045c — flag (do NOT drop) a Fitness-brand SKU that is a savory cracker, not a cereal.
    Returns a quarantine-flag dict to attach to the BSIP1 record, or None if not flagged."""
    name = name or ""
    if not FITNESS_BRAND_RE.search(name):
        return None  # out of scope — guard only fires on the Fitness brand line
    savory = bool(FITNESS_SAVORY_RE.search(name))
    fat = nn.get("fat_g") if isinstance(nn, dict) else None
    sugars = nn.get("sugars_g") if isinstance(nn, dict) else None
    sweet_signal = bool(FITNESS_SWEET_RE.search(name + " " + (ingr_text or ""))) or \
        (sugars is not None and sugars >= 12.0)
    high_fat_nonsweet = (fat is not None and fat >= FITNESS_FAT_FLOOR) and not sweet_signal
    if not (savory or high_fat_nonsweet):
        return None
    triggers = []
    if savory:
        triggers.append("savory_descriptor_in_name")
    if high_fat_nonsweet:
        triggers.append(f"fat_ge_{FITNESS_FAT_FLOOR:g}_and_no_sweet_signal")
    return {
        "flag": "fitness_savory_cracker_suspect",
        "policy": "flag_not_drop",
        "triggers": triggers,
        "fat_g": fat,
        "sugars_g": sugars,
        "evidence_ref": "EV-045c (TASK-184) — Nestlé Fitness savory-cracker brand-line guard; "
                        "curation flag, contamination != calibration; no score change.",
        "note": "Fitness brand-line SKU whose macro/name signature matches a savory cracker/crispbread "
                "rather than an RTE breakfast cereal. Quarantined for review; not silently excluded.",
    }
CEREAL_RE    = re.compile(r"דגני|דגנים|קורנפלקס|corn ?flakes|גרנולה|granola|מוזלי|מוסלי|muesli|"
                          r"שיבולת שועל|קוואקר|quaker|צ'יריוס|cheerios|נסקוויק|nesquik|"
                          r"קוקו ?פופס|coco ?pops|צ'וקפיק|chocapic|פצפוצי|פצפוצים|כריות|"
                          r"פתיתי|בראן|\bbran\b|fitness|פיטנס|kellogg|weetabix|ויטבי|כוסמין|"
                          r"\bcereal\b|דייסה", re.I)

# ── EV-051 — Marketing-bleed ingredient detection (TASK-198) ─────────────────
# A small number of Nestlé/multinational cereal pages serve FRONT-OF-PACK MARKETING
# COPY (bullet-point benefit claims) as the ingredient declaration instead of the actual
# ingredient list. These can be identified by the presence of:
#   (a) promotional boilerplate phrases that never appear in real ingredient lists, OR
#   (b) absence of standard ingredient-list structure (comma-separated food substances).
#
# Marketing-bleed PHRASES: phrases that unambiguously belong to marketing copy, not
# ingredient declarations. Conservative: we require at least one phrase that is diagnostic.
#   "תענוג פראי" / "תענוג" alone → promotional tagline (Lion "wild delight!")
#   "ניתן להוסיף" → "you can add" — serving suggestion, not an ingredient
#   "לארוחת בוקר" → "for breakfast" — usage description
#   "מס' 1" → "#1 brand/cereal" — marketing rank claim
# STRUCTURE ABSENCE: a real ingredient list must contain at least one comma-separated or
# period-separated substance name. If the text has no commas (the primary Hebrew separator)
# and contains a marketing phrase, we flag it.
# Tier 1 — phrases that are CATEGORICALLY IMPOSSIBLE in a real ingredient declaration
# and therefore sufficient alone to confirm marketing bleed, regardless of commas:
#   "ניתן להוסיף" = "you can add" (serving suggestion)
#   "תענוג פראי" = "wild delight" (promotional tagline)
# These two phrases are present in Lion. They cannot appear in a real ingredient list.
_MARKETING_BLEED_TIER1 = re.compile(
    r"ניתן להוסיף|תענוג פראי",
    re.I
)
# Tier 2 — phrases that are strong marketing copy indicators, but require corroboration
# (bullet-format and low real comma count) because they could theoretically appear as
# part of a product name within an otherwise real ingredient list:
_MARKETING_BLEED_TIER2 = re.compile(
    r"לארוחת בוקר\s+ניתן|מספר 1 ב|מס[''׳]? ?1 (?:חיטה|דגן)|"
    r"מספר אחד|#1\s|מוביל בישראל|הדגן המוביל|לאכול עם חלב",
    re.I
)


def _detect_marketing_bleed(ingr_text: str) -> tuple[bool, str | None]:
    """Return (is_bleed, reason) — True when the ingredient text is marketing copy.

    Two-tier detection:
    Tier 1: A phrase that is categorically impossible in a real ingredient declaration
      ("ניתן להוסיף" = serving suggestion; "תענוג פראי" = promotional tagline).
      These are sufficient alone — no structural condition required.
    Tier 2: Phrases that are strong marketing indicators but could theoretically appear
      in a name-within-ingredients context. Require corroboration: bullet-format
      separators AND the comma count is attributable to the marketing phrases, not to
      a real ingredient list structure.

    Note: Lion's text has 4 commas, but they all come from the serving suggestion phrase
    "ניתן להוסיף : חלב, פרי טרי, מים" — not from ingredient separators. The Tier 1
    detection catches this correctly without needing to parse comma origin.
    """
    if not ingr_text:
        return False, None
    # Tier 1: categorically impossible phrases — sufficient alone
    if _MARKETING_BLEED_TIER1.search(ingr_text):
        phrases_found = _MARKETING_BLEED_TIER1.findall(ingr_text)
        return True, f"marketing_tier1_definitive_phrase: {phrases_found[0] if phrases_found else 'match'}"
    # Tier 2: corroboration required
    has_bullet = "•" in ingr_text
    if _MARKETING_BLEED_TIER2.search(ingr_text) and has_bullet:
        return True, "marketing_tier2_phrase_plus_bullet_format"
    return False, None

# TASK-192 / EV-046: these three thin wrappers DELEGATE to the canonical shared path.
# Byte-identical to the former local copies for every value already handled; the shared
# version additionally preserves the "פחות מ N" less-than flag and enforces
# total_fat >= saturated_fat (surfaced via the _integrity key for the QA guard).
def _parse_num(raw):
    return _shared_parse_num(raw)


def _parse_sodium(raw):
    return _shared_parse_sodium(raw)


def _parse_nutrition(n: dict) -> dict:
    return _shared_parse_nutrition(n)


_SPLIT_RE = re.compile(r"[,;،]\s*")


def _parse_ingredients(raw: str) -> list[str]:
    if not raw:
        return []
    raw = re.sub(r"\s+", " ", raw).strip()
    out = []
    for p in _SPLIT_RE.split(raw):
        p = p.strip().strip(".")
        if p and len(p) > 1:
            out.append(p)
    return out


def _classify_subtype(name: str, ingr: str) -> str:
    t = (name + " " + ingr).lower()
    if re.search(r"גרנולה|granola", t):
        return "granola"
    if re.search(r"מוזלי|מוסלי|muesli", t):
        return "muesli"
    if re.search(r"קוקו ?פופס|נסקוויק|צ'וקפיק|coco ?pops|nesquik|chocapic|כריות|frosties|טריקס|trix", t):
        return "childrens_character"
    if re.search(r"בראן|\bbran\b|סובין", t):
        return "bran"
    if re.search(r"שיבולת שועל|קוואקר|quaker|oat", t):
        return "oat_cereal"
    if re.search(r"פצפוצי|פצפוצים|puffed|מנופח", t):
        return "puffed_extruded"
    if re.search(r"מלא|כוסמין מלא|whole|דגנים מלאים|weetabix|ויטבי", t):
        return "whole_grain_flakes"
    if re.search(r"קורנפלקס|corn ?flakes|פתיתי תירס", t):
        return "cornflakes"
    return "cereal_other"


def _curate(raw: dict) -> str | None:
    name = (raw.get("name_he") or "").strip()
    if not name:
        return "empty_name"
    if BAR_RE.search(name):
        return "bar_excluded_snack_overlap"
    if NONCEREAL_RE.search(name):
        return "non_cereal_excluded"
    ingr_raw = raw.get("ingredients_raw") or ""
    if _is_ptitim_pasta(name, ingr_raw):
        return "ptitim_pasta_excluded"   # EV-045 — starch side-dish, not a cereal
    if _is_bread_leakage(ingr_raw):
        return "bread_ingredient_leakage"  # EV-045 — yeast/sourdough loaf, not a cereal
    # EV-045b — full contaminant sweep (pasta / flour / chocolate confection / drink / wet)
    energy_kcal = _parse_num((raw.get("nutrition", {}) or {}).get("energy_kcal_raw"))
    contam = _contaminant_reason(name, ingr_raw, energy_kcal)
    if contam:
        return contam
    if _is_plain_oats(name):
        return "plain_oats_out_of_scope"   # EV-045d — porridge oats, owner ruled off the page
    if not CEREAL_RE.search(name):
        return "not_cereal"
    nn = _parse_nutrition(raw.get("nutrition", {}))
    if all(nn.get(k) is None for k in ("energy_kcal", "protein_g", "carbohydrates_g")):
        return "no_usable_nutrition"
    return None


def _confidence(nn: dict, ingr_list: list[str]) -> dict:
    nutr_fields = ["energy_kcal", "protein_g", "sugars_g", "fat_g", "carbohydrates_g"]
    n_present = sum(1 for f in nutr_fields if nn.get(f) is not None)
    nutr_ok = n_present >= 3
    ingr_ok = len(ingr_list) >= 2

    # TASK-190 sodium sanity gate: a product with a physically impossible sodium value
    # (>2000 mg/100g, unit-corruption artefact) must NOT be scored as if the value is real.
    # Force data_sufficiency=insufficient so the BSIP2 scorer suppresses it.
    integrity_flags = nn.get("_integrity") or []
    sodium_corrupt = any("sodium_implausible" in flag for flag in integrity_flags)

    if nutr_ok and ingr_ok and not sodium_corrupt:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "high", 0.80, "high"
    elif nutr_ok and not sodium_corrupt:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "medium", 0.65, "medium"
    else:
        nutr_conf, id_conf, trust, lvl = "partial", "low", 0.45, "low"
    missing = []
    if not nutr_ok:
        missing += [f for f in nutr_fields if nn.get(f) is None]
    if not ingr_ok:
        missing.append("ingredients_list")
    if sodium_corrupt:
        missing.append("sodium_mg_corrupt__unit_error")
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
        "nutrition_consistency_status": "consistent" if (nutr_ok and not sodium_corrupt) else "partial",
        "data_sufficiency": "insufficient" if sodium_corrupt else ("sufficient" if nutr_ok else "insufficient"),
    }


# ══════════════════════════════════════════════════════════════════════════════
# THE FOUR CEREALS GOVERNANCE CONSTRUCTS
# ══════════════════════════════════════════════════════════════════════════════

WHOLE_GRAIN_RE   = re.compile(r"מלא|מלאה|מלאים|דגן(?:ים)? מלא|חיטה מלאה|שיפון מלא|"
                              r"כוסמין מלא|שיבולת שועל|whole ?grain|whole ?wheat|wholemeal", re.I)
WHOLE_CLAIM_RE   = re.compile(r"מלא|מלאה|מלאים|דגנים מלאים|חיטה מלאה|whole ?grain|whole ?wheat|100%", re.I)
REFINED_FLOUR_RE = re.compile(r"קמח חיטה(?!\s*מלא)|קמח לבן|סולת|semolina|קמח תירס", re.I)
KIDS_NAME_RE     = re.compile(r"ילדים|kids|junior|ג'וניור|מיני\b|mini\b|קטנטנים|growing|לגדול", re.I)
# Recognized child-mascot cereal brands: the brand name IS the animated-mascot identity
# (Nesquik=Quicky, Trix=rabbit, Coco Pops=Coco the monkey, Chocapic, Frosties=Tony). For these,
# the brand token jointly satisfies D1 (visual mascot) + D2 (child-targeting name). Auditable list,
# not open-ended. Per cereals_gap_resolution_v1 Sec 2.8 D1 definition (child-targeted mascot brand).
CHILD_MASCOT_RE  = re.compile(r"נסקוויק|nesquik|קוקו ?פופס|coco ?pops|קוקומן|cocoman|"
                              r"צ'וקפיק|chocapic|frosties|פרוסטיז|טריקס|trix|smacks|"
                              r"honey monster|כריות נוגט|כריות שוקו|כריות במילוי|lion|ליאון", re.I)
KIDS_CLAIM_RE    = re.compile(r"גדיל|לגדול|בית ?ספר|לילדים|growing|מתאים לילדים", re.I)
NAV_BOILERPLATE_RE = re.compile(r"קטגוריה|לתפריט הראשי|טוען מוצרים")
FORTIFY_RE       = re.compile(r"ויטמין|מינרל|מועשר|fortif|vitamin|ברזל\b|iron|אבץ|zinc|"
                              r"חומצה פולית|folic|ניאצין|niacin|ריבופלבין|riboflavin|"
                              r"תיאמין|thiamin|\bb1\b|\bb2\b|\bb6\b|\bb12\b|סידן", re.I)
OIL_RE           = re.compile(r"שמן|oil", re.I)
SYRUP_RE         = re.compile(r"סירופ|סילאן|דבש|honey|syrup|מולסה|נופת", re.I)


def _whole_grain_construct(name, claims, ingr_text, ingredient_order) -> dict:
    """Construct 3 — Guardrails v2 Sec 5.2.1 whole-grain threshold + Marketing Divergence Finding.
    Claim text source = name + ingredient/marketing text (claims_raw is nav boilerplate, unusable)."""
    claim_text = f"{name} {ingr_text}"
    claim_present = bool(WHOLE_CLAIM_RE.search(claim_text))

    # First grain ingredient test (ordering-based, per 5.2.1 detection method)
    first_grain_whole = None
    first_grain_pos = None
    for item in sorted(ingredient_order, key=lambda x: x.get("position") or 999):
        txt = item.get("text", "")
        is_grain = bool(re.search(r"קמח|דגן|חיטה|שיפון|כוסמין|שיבולת שועל|תירס|אורז|שעורה|oat|wheat|corn|rice|grain", txt, re.I))
        if is_grain:
            first_grain_pos = item.get("position")
            first_grain_whole = bool(WHOLE_GRAIN_RE.search(txt)) and not REFINED_FLOUR_RE.search(txt)
            break

    whole_present = bool(WHOLE_GRAIN_RE.search(ingr_text))
    refined_present = bool(REFINED_FLOUR_RE.search(ingr_text))

    # Composition (>=30%): whole grain present AND not dominated by a refined flour ahead of it
    composition_supported = whole_present and (first_grain_whole is True or not refined_present)
    # Dominant (>=51%): whole grain is the first grain ingredient
    dominant_supported = first_grain_whole is True

    # Marketing Divergence Finding: claim present but composition not supported (all 3 conditions)
    mdf = claim_present and not composition_supported

    return {
        "whole_grain_claim_present": claim_present,
        "first_grain_ingredient_position": first_grain_pos,
        "first_grain_is_whole": first_grain_whole,
        "composition_threshold_supported_30pct": composition_supported,
        "dominant_threshold_supported_51pct": dominant_supported,
        "marketing_divergence_finding": mdf,
        "mdf_note": ("Whole-grain claim present but ingredient ordering does not support the "
                     ">=30% composition threshold (refined flour leads or no whole grain found)."
                     if mdf else None),
        "evidence_ref": "cereals_gap_resolution_v1 Sec 5.2.1 (Resolution 4); Guardrails v2",
    }


def _granola_construct(name, ingr_text, subtype, nn) -> dict:
    """Construct 1 — Architectural Divergence Sub-Category Rule (Rule 5 / Sec 2.9)."""
    sugar = nn.get("sugars_g")
    fat = nn.get("fat_g")
    ind_sugar = sugar is not None and sugar >= 15.0        # proxy for added sugar >=10 (Resolution 3 mitigation)
    ind_fat = fat is not None and fat >= 10.0
    ind_processing = bool(re.search(r"גרנולה|granola|מוזלי|muesli", name + " " + ingr_text, re.I)) \
        or (bool(OIL_RE.search(ingr_text)) and bool(SYRUP_RE.search(ingr_text)))
    score = sum([ind_sugar, ind_fat, ind_processing])
    name_granola = bool(re.search(r"גרנולה|granola", name, re.I))
    # EV-045b — muesli and toasted grain/fruit/nut MIXES are the same architectural family as
    # granola (oats + oil/sweetener + fruit/nut) and belong in the granola+muesli category.
    name_muesli = bool(re.search(r"מוזלי|muesli|^תע\.?\s*דגנים|תערובת דגנים", name, re.I))
    # 2-of-3 → granola sub-pool; boundary (name granola + any 1) defaults to granola (conservative)
    in_granola_pool = score >= 2 or (name_granola and score >= 1) or name_muesli
    return {
        "subpool": "granola" if in_granola_pool else "standard_cereal",
        "indicators": {
            "added_sugar_proxy_ge15g": ind_sugar,
            "fat_ge10g": ind_fat,
            "processing_proxy_nova3plus": ind_processing,
        },
        "indicator_count": score,
        "boundary_defaulted_to_granola": in_granola_pool and score < 2,
        "nova_confirmation_pending_bsip2": True,
        "evidence_ref": "cereals_gap_resolution_v1 Sec 2.9 (Resolution 3, Constitution Art. II Rule 5)",
    }


def _childrens_construct(name, ingr_text, serving_g) -> dict:
    """Construct 2 — Developmental Product Definition (Sec 2.8 / Resolution 1)."""
    text = name + " " + ingr_text
    mascot_brand = bool(CHILD_MASCOT_RE.search(name))
    # D1 visual mascot: not directly observable from text, EXCEPT recognized child-mascot brands
    # whose brand identity encodes the mascot (documented, auditable list).
    d1_visual = True if mascot_brand else None
    d2_name = bool(KIDS_NAME_RE.search(name)) or mascot_brand
    d3_serving = serving_g is not None and serving_g <= 25.0
    d4_claim = bool(KIDS_CLAIM_RE.search(text))
    present = sum([d1_visual is True, bool(d2_name), bool(d3_serving), bool(d4_claim)])
    is_childrens = present >= 2
    # single-indicator candidate: one signal only (e.g. generic 'kids' word, no mascot) — CE Controller resolves
    single_indicator_candidate = (present == 1)
    return {
        "is_childrens_product": is_childrens,
        "indicators": {
            "D1_visual_mascot": d1_visual,           # True only for recognized mascot brands; else null
            "D2_name_language": d2_name,
            "D3_pediatric_serving_le25g": d3_serving,
            "D4_developmental_claim": d4_claim,
        },
        "indicators_present_count": present,
        "mascot_brand_detected": mascot_brand,
        "single_indicator_candidate": single_indicator_candidate,
        "pool": "developmental" if is_childrens else "general",
        "recall_caveat": "Pure visual mascots on non-listed brands are not detectable from a text-only "
                         "scrape; D3 serving size was rarely on the page. Recall is conservative — "
                         "single-indicator candidates are flagged for CE Controller visual confirmation.",
        "anti_immunity": "Classification cannot improve score (Anti-Immunity Rule).",
        "evidence_ref": "cereals_gap_resolution_v1 Sec 2.8 (Resolution 1)",
    }


def _fortification_flag(claims, ingr_text) -> bool:
    """Construct 4 (per-product half) — DISTORTION-004 fortification presence."""
    return bool(FORTIFY_RE.search(f"{claims} {ingr_text}"))


def _find_latest_raw() -> pathlib.Path | None:
    cand = sorted(RAW_DIR.glob("cereals_bsip0_raw_*.json"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    return cand[0] if cand else None


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No cereals_bsip0_raw_*.json in %s", RAW_DIR)
        return
    log.info("Loading %s", raw_path)
    raws = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raws))

    for f in OUT_DIR.glob("bsip1_*.json"):
        f.unlink()

    included, excluded = [], []
    seen = set()
    for raw in raws:
        name = (raw.get("name_he") or "").strip()
        barcode = str(raw.get("barcode", "")).strip()
        if barcode in seen:
            excluded.append({"barcode": barcode, "name": name, "reason": "duplicate_barcode"})
            continue
        reason = _curate(raw)
        if reason:
            excluded.append({"barcode": barcode, "name": name, "reason": reason})
            continue
        seen.add(barcode)

        nn = _parse_nutrition(raw.get("nutrition", {}))
        ingr_text = (raw.get("ingredients_raw") or "").strip()
        ingr_list = _parse_ingredients(ingr_text)
        claims_raw_in = raw.get("claims_raw", "")
        # Shufersal claims_raw is polluted with nav-menu boilerplate; blank it when detected.
        claims = "" if NAV_BOILERPLATE_RE.search(claims_raw_in) else claims_raw_in
        serving_g = raw.get("serving_size_g_hint")
        conf = _confidence(nn, ingr_list)
        subtype = _classify_subtype(name, ingr_text)
        pid = f"bsip1_cereal_{barcode}"

        record = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": barcode,
            "canonical_name_he": name,
            "canonical_name_en": None,
            "brand": raw.get("brand", ""),
            "package_size_g": raw.get("weight_g"),
            "unit_count": None, "unit_size_g": None,
            "serving_size_g": serving_g,
            "country_of_origin": "ישראל",
            "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [SOURCE],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_text,
            "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": "bsip0_scrape",
                "bsip0_status": "bsip0_scrape",
                "populated_at": "bsip1_build_cereals_002",
                "missing": not bool(ingr_text),
                "note": "Scraped from Shufersal product page (run_cereals_002)",
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": claims,
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "Shufersal JSON-LD gtin13/sku.",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "data_sufficiency": conf["data_sufficiency"],
            "nutrition_consistency_warnings": [],
            # EV-051 / TASK-198 — marketing-bleed detection (Nestlé-style front-of-pack copy
            # served as ingredient declaration). When detected: quality = "marketing_bleed"
            # so downstream NOVA proxy and confidence scorer treat ingredient signals as
            # unreliable (same degradation path as "corrupted"/"malformed").
            "ingredient_text_quality": (
                "missing" if not ingr_text
                else ("marketing_bleed" if _detect_marketing_bleed(ingr_text)[0] else "clean")
            ),
            "ingredient_warnings": (
                ["no_ingredient_list_in_source"] if not ingr_text
                else (
                    [f"marketing_bleed_detected: {_detect_marketing_bleed(ingr_text)[1]}; "
                     "ingredient signals suppressed — front-of-pack copy served as ingredient list; "
                     "real ingredients (sugar, cocoa, caramel, emulsifiers) not captured. "
                     "Evidence: TASK-198 / EV-051."]
                    if _detect_marketing_bleed(ingr_text)[0] else []
                )
            ),
            "canonical_trust_score": conf["canonical_trust_score"],
            "canonical_trust_level": conf["canonical_trust_level"],
            "canonical_risk_flags": ["single_source_only"],
            "conflicts_summary": {"count": 0, "has_unresolved": False,
                                  "fields_in_conflict": [], "identity_conflicts": [],
                                  "nutrition_conflicts": [], "ingredient_conflicts": [],
                                  "labeling_conflicts": [], "completeness_conflicts": []},
            "missing_fields": conf["missing_fields"],
            "inferred_fields": ["bsip_cereal_subtype"],
            "audit_ref": None,
            "bsip_cereal_subtype": subtype,
            "price": raw.get("price", ""),
            "price_per_100g": raw.get("price_per_100g"),
            "acquisition_query": raw.get("acquisition_query", ""),
        }

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

        ingredient_order = record.get("ingredient_order", [])

        # ── Apply the four governance constructs ──────────────────────────────
        wg = _whole_grain_construct(name, claims, ingr_text, ingredient_order)
        gr = _granola_construct(name, ingr_text, subtype, nn)
        ch = _childrens_construct(name, ingr_text, serving_g)
        fortified = _fortification_flag(ingr_text, ingr_text)
        record["cereals_governance"] = {
            "construct_1_granola_subpool": gr,
            "construct_2_childrens": ch,
            "construct_3_whole_grain": wg,
            "construct_4_fortification_flag": {
                "fortified": fortified,
                "evidence_ref": "cereals_gap_resolution_v1 Sec 6.4 (Resolution 2, DISTORTION-004)",
            },
        }
        # EV-045c — Nestlé Fitness savory-cracker guard (flag-not-drop, curation only)
        ev045c = fitness_noncereal_flag(name, ingr_text, nn)
        if ev045c:
            record["cereals_governance"]["ev_045c_fitness_noncereal_flag"] = ev045c
            record.setdefault("canonical_risk_flags", []).append("fitness_savory_cracker_suspect")

        (OUT_DIR / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        included.append({
            "barcode": barcode, "name": name, "subtype": subtype,
            "has_ingredients": bool(ingr_text),
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
            "data_sufficiency": conf["data_sufficiency"],
            "subpool": gr["subpool"],
            "is_childrens": ch["is_childrens_product"],
            "childrens_candidate": ch["single_indicator_candidate"],
            "wg_claim": wg["whole_grain_claim_present"],
            "wg_mdf": wg["marketing_divergence_finding"],
            "fortified": fortified,
        })

    # ── Curation report ──────────────────────────────────────────────────────
    n_ingr = sum(1 for i in included if i["has_ingredients"])
    n_suff = sum(1 for i in included if i["data_sufficiency"] == "sufficient")
    report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(raw_path),
        "raw_count": len(raws),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "ingredient_coverage": f"{n_ingr}/{len(included)}",
        "data_sufficient": f"{n_suff}/{len(included)}",
        "included": included,
        "excluded": excluded,
    }
    (OUT_DIR.parent / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── Constructs category-level rollup ───────────────────────────────────────
    displayable = [i for i in included if i["data_sufficiency"] == "sufficient"]
    n_disp = max(len(displayable), 1)
    granola_pool = [i for i in displayable if i["subpool"] == "granola"]
    childrens_pool = [i for i in displayable if i["is_childrens"]]
    childrens_candidates = [i for i in displayable if i.get("childrens_candidate")]
    mdf_list = [i for i in displayable if i["wg_mdf"]]
    wg_claims = [i for i in displayable if i["wg_claim"]]
    fortified = [i for i in displayable if i["fortified"]]
    fort_pct = 100.0 * len(fortified) / n_disp

    if fort_pct >= 80:
        lang = "most products in this category"
    elif fort_pct >= 66:
        lang = "the majority of products"
    elif fort_pct >= 50:
        lang = "approximately half of products"
    else:
        lang = None  # not endemic

    endemic_note = None
    if lang:
        endemic_note = (
            "CATEGORY NOTE — Fortification\n\n"
            "מוצרי דגני בוקר מועשרים לעיתים קרובות בוויטמינים ובמינרלים (ברזל, ויטמיני B, סידן, ויטמין D). "
            "הציון של Bari אינו כולל את תרומת המיקרו-נוטריאנטים כגורם חיובי.\n\n"
            f"מגבלה זו חלה על {('כמחצית המוצרים' if fort_pct < 66 else ('רוב המוצרים' if fort_pct < 80 else 'מרבית המוצרים בקטגוריה'))} בקטגוריה. "
            "הציון משקף ארכיטקטורת מאקרו-נוטריאנטים, איכות עיבוד ושלמות רכיבים. "
            "הציון אינו לוכד את הערך התזונתי של ויטמינים ומינרלים מוספים. "
            "מוצר מועשר עשוי לספק תועלת מיקרו-נוטריאנטית משמעותית שאינה נראית בציון."
        )

    constructs_report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "displayable_count": len(displayable),
        "construct_1_granola_subpool": {
            "granola_pool_count": len(granola_pool),
            "standard_pool_count": len(displayable) - len(granola_pool),
            "granola_members": [{"barcode": i["barcode"], "name": i["name"]} for i in granola_pool],
            "rule": "Art. II Rule 5 proxy 2-of-3 (added-sugar>=15g proxy / fat>=10g / processing); NOVA confirmed at BSIP2.",
        },
        "construct_2_childrens": {
            "developmental_pool_count": len(childrens_pool),
            "members": [{"barcode": i["barcode"], "name": i["name"]} for i in childrens_pool],
            "single_indicator_candidates_for_ce_review": [
                {"barcode": i["barcode"], "name": i["name"]} for i in childrens_candidates],
            "rule": "Sec 2.8 — 2-of-4 indicators. Recognized child-mascot brands satisfy D1+D2 jointly; "
                    "single-indicator products flagged for CE Controller visual confirmation.",
        },
        "construct_3_whole_grain": {
            "products_with_whole_grain_claim": len(wg_claims),
            "marketing_divergence_findings": len(mdf_list),
            "mdf_members": [{"barcode": i["barcode"], "name": i["name"]} for i in mdf_list],
            "rule": "Sec 5.2.1 — first-grain-ingredient test; MDF when claim present but composition <30% unsupported.",
        },
        "construct_4_fortification_endemic": {
            "fortified_count": len(fortified),
            "fortified_pct": round(fort_pct, 1),
            "endemic_threshold_pct": 50,
            "is_endemic": lang is not None,
            "graduated_language": lang,
            "category_note_he": endemic_note,
            "rule": "Sec 6.4 — category-level note required when DISTORTION-004 affects >=50% of displayable products.",
        },
    }
    (OUT_DIR.parent / "cereals_constructs_report.json").write_text(
        json.dumps(constructs_report, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("Included %d  Excluded %d  -> BSIP1 at %s", len(included), len(excluded), OUT_DIR)
    log.info("Ingredient coverage (included): %d/%d", n_ingr, len(included))
    log.info("Data sufficient: %d/%d", n_suff, len(included))
    log.info("Granola pool: %d | Children's: %d | WG claims: %d | MDF: %d | Fortified: %d/%d (%.1f%%, endemic=%s)",
             len(granola_pool), len(childrens_pool), len(wg_claims), len(mdf_list),
             len(fortified), len(displayable), fort_pct, lang is not None)
    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        log.info("  excluded[%s] = %d", r, c)


if __name__ == "__main__":
    main()
