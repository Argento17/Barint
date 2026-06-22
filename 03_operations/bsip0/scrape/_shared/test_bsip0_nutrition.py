# -*- coding: utf-8 -*-
"""Unit tests for the canonical BSIP0 nutrition extraction path (TASK-192 / EV-046).

Run:  python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py
   or: python 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py   (no pytest)

Covers the 3rd-recurrence "פחות מ 0.5" total-fat mis-capture (EV-029 family) at BOTH
extraction layers:
  - scrape layer  : classify_nutr_label / parse_nutrition_rows  (Hebrew label -> field)
  - build  layer  : parse_value_bound / parse_num / parse_nutrition_numeric (raw str -> float)

Fixture: the REAL run_cereals_005 BSIP0 raw
(02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json),
the corpus where the bug shipped (57/66 scored products carried fat_g=0.5).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bsip0_nutrition as bn  # noqa: E402

CEREALS_RAW = (
    r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs"
    r"\cereals_bsip0_raw_20260601T152207.json"
)


# ── Legacy reference (the per-builder _parse_num copy) for byte-identity proof ──
import re  # noqa: E402

_LEGACY_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _legacy_parse_num(raw):
    if not raw:
        return None
    m = _LEGACY_NUM_RE.search(str(raw).replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


# ── Scrape layer: label classification ─────────────────────────────────────────

def test_subrow_final_mem_does_not_overwrite_total_fat():
    """The exact EV-046 gap: 'מתוכם …' (final-mem 'of which') must NOT map to total fat."""
    assert bn.classify_nutr_label("מתוכם שומן") is None
    assert bn.classify_nutr_label("מתוכן שומן") is None
    assert bn.classify_nutr_label("מתוכו שומן") is None


def test_total_fat_row_still_classifies_as_fat():
    assert bn.classify_nutr_label("שומנים") == "fat"
    assert bn.classify_nutr_label("שומן") == "fat"


def test_fat_subtypes_keep_their_own_fields():
    assert bn.classify_nutr_label("מתוכם חומצות שומן רוויות") == "saturated_fat"
    assert bn.classify_nutr_label("מתוכם שומן טראנס") == "trans_fat"


def test_sugar_of_which_is_still_captured():
    assert bn.classify_nutr_label("מתוכם סוכרים") == "sugar"
    assert bn.classify_nutr_label("סוכרים") == "sugar"


def test_shufersal_sugar_row_label():
    """
    TASK-378 regression: the actual Shufersal HTML label for the "of which sugars"
    nutrition row is "סוכרים מתוך פחמימות".  The old shufersal_probe_v3.py
    NUTR_LABEL_MAP dict fired "פחמימות"→carbs before "סוכרים"→sugar because
    "פחמימות" is a substring of "סוכרים מתוך פחמימות", causing sugar to be
    silently dropped on 29/31 curated bread products.

    The shared parser (classify_nutr_label) checks sugar BEFORE carbs (sugar
    key "סוכר" at line ~84, carbs key "פחמימ" at line ~86), so this label
    must return "sugar", not "carbs".
    """
    assert bn.classify_nutr_label("סוכרים מתוך פחמימות") == "sugar", (
        "Shufersal sugar-row label must classify as sugar, not carbs"
    )
    # The full panel order on Shufersal puts the sugar sub-row BEFORE the
    # carbs total row.  parse_nutrition_rows first-value-wins must still yield
    # the correct carbs total (from the carbs row) AND capture sugar.
    rows_shufersal_bread = [
        {"value": "220",  "label": "אנרגיה (קלוריות)"},
        {"value": "8.5",  "label": "חלבונים"},
        {"value": "1.8",  "label": "סוכרים מתוך פחמימות"},   # ← sub-row appears first in HTML
        {"value": "38.4", "label": "פחמימות"},                # ← total carbs row after
        {"value": "0.25", "label": "שומנים"},
        {"value": "5.6",  "label": "סיבים תזונתיים"},
        {"value": "380",  "label": "נתרן"},
    ]
    out = bn.parse_nutrition_rows(rows_shufersal_bread)
    assert out["sugar"] == "1.8",  f"expected sugar='1.8', got {out.get('sugar')!r}"
    assert out["carbs"] == "38.4", f"expected carbs='38.4', got {out.get('carbs')!r}"


def test_full_panel_reads_total_not_subrow():
    """Reconstructed Shufersal cereal panel: total fat 34.2, sat/trans sub-rows < 0.5."""
    rows = [
        {"value": "504", "label": "אנרגיה (קלוריות)"},
        {"value": "17.7", "label": "חלבונים"},
        {"value": "27", "label": "פחמימות"},
        {"value": "8", "label": "מתוכם סוכרים"},
        {"value": "34.2", "label": "שומנים"},
        {"value": "פחות מ 0.5", "label": "מתוכם חומצות שומן רוויות"},
        {"value": "פחות מ 0.5", "label": "מתוכם שומן טראנס"},
        {"value": "11.7", "label": "סיבים תזונתיים"},
        {"value": "394", "label": "נתרן"},
    ]
    out = bn.parse_nutrition_rows(rows)
    assert out["fat"] == "34.2"               # total, NOT the 0.5 sub-row
    assert out["saturated_fat"] == "פחות מ 0.5"
    assert out["sugar"] == "8"


# ── Build layer: raw string -> float ───────────────────────────────────────────

def test_parse_value_bound_less_than():
    assert bn.parse_value_bound("פחות מ 0.5") == (0.5, True)
    assert bn.parse_value_bound("< 0.3") == (0.3, True)
    assert bn.parse_value_bound("34.2") == (34.2, False)
    assert bn.parse_value_bound("") == (None, False)
    assert bn.parse_value_bound(None) == (None, False)


def test_parse_num_byte_identical_to_legacy():
    for c in ["פחות מ 0.5", "34.2", "34.2 גרם", "17,7", "504", "", "0.5",
              "1.4", None, "< 0.3", "עד 1"]:
        assert bn.parse_num(c) == _legacy_parse_num(c), c


def test_sat_gt_total_flagged():
    out = bn.parse_nutrition_numeric({"fat_raw": "פחות מ 0.5", "saturated_fat_raw": "5"})
    assert out["fat_g"] == 0.5
    assert out["fat_saturated_g"] == 5.0
    assert any("sat_gt_total_fat" in s for s in out.get("_integrity", []))


def test_clean_panel_no_integrity_key():
    """A correct panel produces NO _integrity key -> byte-identical to legacy output."""
    out = bn.parse_nutrition_numeric({
        "energy_kcal_raw": "504", "protein_raw": "17.7", "carbs_raw": "27",
        "fat_raw": "34.2", "fiber_raw": "11.7", "sodium_raw": "394",
        "sugar_raw": "8", "saturated_fat_raw": "10.0",
    })
    assert "_integrity" not in out
    assert out["fat_g"] == 34.2 and out["fat_saturated_g"] == 10.0


# ── Real-fixture regression: the corpus where the bug shipped ───────────────────

def _load_fixture():
    with open(CEREALS_RAW, encoding="utf-8") as fh:
        return json.load(fh)


def test_fixture_exists_and_carries_the_bug_signature():
    """Documents the captured-at-scrape damage: the raw shows fat_raw='פחות מ 0.5'."""
    data = _load_fixture()
    bugged = [p for p in data if p["nutrition"].get("fat_raw") == "פחות מ 0.5"]
    assert len(bugged) >= 50  # 70/113 in this corpus


def test_target_product_bound_is_recoverable():
    """Barcode 7290106773714: scraper stored 'פחות מ 0.5' in fat (a saturated bound).
    The build layer now correctly recognises it as a less-than bound, so the QA guard /
    re-scrape can recover the true total (34.2g lives on the page's total row)."""
    data = _load_fixture()
    p = next(x for x in data if x.get("barcode") == "7290106773714")
    val, is_bound = bn.parse_value_bound(p["nutrition"]["fat_raw"])
    assert val == 0.5 and is_bound is True


def test_fixture_panels_flagged_by_guard():
    """Every product whose raw fat is 'פחות מ 0.5' at 500+ kcal must be flagged
    implausible by the shared guard (fat understated vs energy)."""
    data = _load_fixture()
    flagged = 0
    for p in data:
        if bn.nutrition_implausible(p["nutrition"]):
            flagged += 1
    assert flagged >= 50


# ── TASK-239: dual-table basis selection (frozen-veg Dorot ginger) ──────────────
#
# REAL fixtures, extracted from saved Shufersal product pages (not synthetic):
#   dorot_ginger_dual_table.html — P_7290018989456 "ג'ינג'ר קצוץ מוקפא": TWO panels
#       Table 0 (100 גרם / per 100g): energy 77 kcal, sodium 12 mg
#       Table 1 (קוביה   / per cube): energy  6 kcal, sodium  1 mg
#   garlic_single_table.html      — P_2253006  "שום כתוש דורות": ONE per-100g panel.
# The bug these prove cannot recur: the per-cube table (6 kcal / 1 mg) being selected
# or overwriting the per-100g table (the defect that was manually JSON-patched).

_FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
_GINGER_DUAL = os.path.join(_FIXTURE_DIR, "dorot_ginger_dual_table.html")
_GARLIC_SINGLE = os.path.join(_FIXTURE_DIR, "garlic_single_table.html")


def _soup(path):
    from bs4 import BeautifulSoup  # local import: bs4 only needed for these tests
    with open(path, encoding="utf-8") as fh:
        return BeautifulSoup(fh.read(), "lxml")


def test_dual_table_selects_per_100g_not_per_cube():
    """The core recurrence-proof: per-cube panel must NOT be selected when per-100g exists."""
    sel = bn.extract_nutrition_selection(_soup(_GINGER_DUAL))
    assert sel["competing_table_count"] == 2, "fixture must carry two competing tables"
    assert sel["selected_basis"] == "per_100g"
    assert sel["selected_table_index"] == 0
    assert "100" in sel["selected_table_header"]
    assert sel["insufficient"] is False


def test_dual_table_values_match_per_100g_fixture():
    """Selected values are the per-100g numbers (77 kcal / 12 mg), NOT per-cube (6 / 1)."""
    sel = bn.extract_nutrition_selection(_soup(_GINGER_DUAL))
    nutr = bn.parse_nutrition_rows(sel["rows"])
    assert bn.parse_num(nutr["energy"]) == 77.0          # per-100g, not 6 (per cube)
    assert bn.parse_sodium_mg(nutr["sodium"]) == 12.0    # per-100g, not 1 (per cube)
    assert bn.parse_num(nutr["carbs"]) == 16.0           # not 1.3 (per cube)
    assert bn.parse_num(nutr["protein"]) == 1.6          # not 0 (per cube)


def test_dual_table_per_cube_never_wins():
    """Explicit negative: none of the per-cube values may appear in the parsed panel."""
    sel = bn.extract_nutrition_selection(_soup(_GINGER_DUAL))
    nutr = bn.parse_nutrition_rows(sel["rows"])
    assert bn.parse_num(nutr["energy"]) != 6.0
    assert bn.parse_sodium_mg(nutr["sodium"]) != 1.0


def test_single_table_still_parses():
    """A normal single-table page selects its lone per-100g panel unchanged."""
    sel = bn.extract_nutrition_selection(_soup(_GARLIC_SINGLE))
    assert sel["competing_table_count"] == 1
    assert sel["selected_basis"] == "per_100g"
    assert sel["insufficient"] is False
    nutr = bn.parse_nutrition_rows(sel["rows"])
    assert bn.parse_num(nutr["energy"]) == 169.0
    assert bn.parse_sodium_mg(nutr["sodium"]) == 400.0


def test_label_is_nutrient_name_not_unit():
    """Regression for the inline-scraper bug: the dict key must be the nutrient name
    ('אנרגיה'/'נתרן'), never the unit ('קל'/'מג'/'גרם')."""
    sel = bn.extract_nutrition_selection(_soup(_GINGER_DUAL))
    nutr = bn.parse_nutrition_rows(sel["rows"])
    assert "energy" in nutr and "sodium" in nutr
    # the raw rows must carry the unit separately from the label
    energy_row = next(r for r in sel["rows"] if bn.classify_nutr_label(r["label"]) == "energy")
    assert energy_row["unit"] in ("קל", "קלוריות") and energy_row["label"] != energy_row["unit"]


def test_multi_table_no_per_100g_is_insufficient():
    """When >1 table exists and none is per-100g, selection is insufficient (gate-fail),
    NOT a silent first-table pick."""
    from bs4 import BeautifulSoup
    synth = (
        '<ul>'
        '<li><div class="nutritionListTitle"><div class="subInfo">קוביה</div></div>'
        '<div class="nutritionList"><div class="nutritionItem">'
        '<div class="number">6</div><div class="name">קל</div><div class="text">אנרגיה</div>'
        '</div></div></li>'
        '<li><div class="nutritionListTitle"><div class="subInfo">מנה</div></div>'
        '<div class="nutritionList"><div class="nutritionItem">'
        '<div class="number">30</div><div class="name">קל</div><div class="text">אנרגיה</div>'
        '</div></div></li>'
        '</ul>'
    )
    sel = bn.select_nutrition_table(bn.extract_nutrition_tables(BeautifulSoup(synth, "lxml")))
    assert sel["selected_basis"] == "unknown"
    assert sel["insufficient"] is True
    assert sel["rows"] == []


def test_classify_basis_tokens():
    assert bn.classify_basis("100 גרם") == "per_100g"
    assert bn.classify_basis("ל-100 גרם") == "per_100g"
    assert bn.classify_basis("per 100g") == "per_100g"
    assert bn.classify_basis("קוביה") == "per_serving"
    assert bn.classify_basis("מנה") == "per_serving"
    assert bn.classify_basis("") == "unknown"


def test_extract_nutrition_raw_carries_selection():
    """extract_nutrition_raw persists every table + the basis decision for offline replay."""
    raw = bn.extract_nutrition_raw(_soup(_GINGER_DUAL))
    assert len(raw["tables"]) == 2
    assert raw["selection"]["selected_basis"] == "per_100g"
    assert raw["selection"]["competing_table_count"] == 2
    # rows persisted are the per-100g rows → replay reproduces 77 kcal
    assert bn.parse_num(bn.parse_nutrition_rows(raw["rows"])["energy"]) == 77.0


# ── TASK-239: Victory retailer parser invariants ───────────────────────────────
#
# Fixture: REAL Victory product 7290005610509 nutrition panel (captured 2026-06).
# Victory uses <th> for labels and <td> for values, with <thead> containing the
# serving-basis header ("ל-100 גרם").

_VICTORY_FIXTURE = os.path.join(_FIXTURE_DIR, "victory_7290005610509.html")


def test_victory_th_td_rows_parse():
    """<th> labels / <td> values parse into correct (field, value, unit) tuples."""
    raw = bn._parse_victory_nutrition(_soup(_VICTORY_FIXTURE))
    assert len(raw["rows"]) == 6
    rows_by_label = {r["label"]: r for r in raw["rows"]}
    assert rows_by_label["energy"]["value"] == "16000"
    assert rows_by_label["fat"]["value"] == "0.1"
    assert rows_by_label["sodium"]["value"] == "39"
    assert rows_by_label["carbs"]["value"] == "3.4"
    assert rows_by_label["fiber"]["value"] == "2"
    assert rows_by_label["protein"]["value"] == "0.68"
    # unit sniff
    assert "קל" in rows_by_label["energy"]["unit"]
    assert "גרם" in rows_by_label["fat"]["unit"]
    assert "מג" in rows_by_label["sodium"]["unit"] or "מ״ג" in rows_by_label["sodium"]["unit"]


def test_victory_basis_per_100g_from_header():
    """Basis is per_100g, and selected_table_header is the actual header text."""
    raw = bn._parse_victory_nutrition(_soup(_VICTORY_FIXTURE))
    assert raw["selection"]["selected_basis"] == "per_100g"
    assert "ל-100 גרם" in raw["selection"]["selected_table_header"]
    assert raw["selection"]["selected_table_header"] == raw["tables"][0]["subInfo"]
    assert raw["selection"]["insufficient"] is False


def test_victory_ambiguous_header_insufficient():
    """Header-less or unrecognized value-header → insufficient=True."""
    from bs4 import BeautifulSoup
    no_header_html = (
        '<section class="nutrition-values"><div class="table-wrapper">'
        "<table><tbody>"
        "<tr><th>אנרגיה (קלוריות)</th><td>16000 קלוריות</td></tr>"
        "</tbody></table></div></section>"
    )
    raw = bn._parse_victory_nutrition(BeautifulSoup(no_header_html, "lxml"))
    assert raw["selection"]["selected_basis"] == "unknown"
    assert raw["selection"]["insufficient"] is True
    assert raw["rows"] == []


def test_victory_multi_td_row_insufficient():
    """A data row with >1 <td> → insufficient (cannot safely choose which value)."""
    from bs4 import BeautifulSoup
    multi_td_html = (
        '<section class="nutrition-values"><div class="table-wrapper">'
        "<table><thead><tr><th>משקל ליחידה</th><th>ל-100 גרם</th></tr></thead><tbody>"
        "<tr><th>אנרגיה (קלוריות)</th><td>16000 קלוריות</td><td>80000 קלוריות</td></tr>"
        "</tbody></table></div></section>"
    )
    raw = bn._parse_victory_nutrition(BeautifulSoup(multi_td_html, "lxml"))
    assert raw["selection"]["insufficient"] is True
    assert raw["rows"] == []


# ── TASK-240 #4 / TASK-247: Yohananof retailer parser invariants ───────────────
#
# Fixture: REAL Yohananof product 16000423534 ("קראנצ'י חטיף שיבולת שועל ושוקולד
# מריר", Nature Valley), captured 2026-05-15 from yochananof.co.il (direct scrape,
# NOT OFF). Yohananof renders nutrition as #simple-tabpanel-1 <li> rows whose label
# is a <span> and whose value is the li's trailing text node; the serving-basis
# caption ("ל100 גרם" — note: NO hyphen on the real page) lives OUTSIDE the tabpanel.

_YOHANANOF_FIXTURE = os.path.join(_FIXTURE_DIR, "yohananof_16000423534.html")


def _yo_soup(li_html, basis_caption="ל100 גרם"):
    """Build a minimal Yohananof page: a basis caption sibling + the tabpanel.

    Structural test scaffold (mirrors the real DOM where the basis is a caption
    outside #simple-tabpanel-1). Pass ``basis_caption=None`` to omit the basis.
    """
    from bs4 import BeautifulSoup
    cap = f'<div class="caption">{basis_caption}</div>' if basis_caption else ""
    html = f'{cap}<div id="simple-tabpanel-1"><div><ul>{li_html}</ul></div></div>'
    return BeautifulSoup(html, "lxml")


def test_yohananof_li_rows_parse_from_real_fixture():
    """Real th/li rows parse to correct (field, value, unit); basis per_100g read
    from the REAL header; selected_table_header == that header verbatim."""
    raw = bn._parse_yohananof_nutrition(_soup(_YOHANANOF_FIXTURE))
    assert raw["selection"]["selected_basis"] == "per_100g"
    assert raw["selection"]["insufficient"] is False
    rows_by_label = {r["label"]: r for r in raw["rows"]}
    assert rows_by_label["energy"]["value"] == "199"
    assert rows_by_label["protein"]["value"] == "3.7"
    assert rows_by_label["carbs"]["value"] == "25.8"
    assert rows_by_label["sugar"]["value"] == "11.3"
    assert rows_by_label["fat"]["value"] == "8.3"
    assert rows_by_label["saturated_fat"]["value"] == "1.4"
    assert rows_by_label["trans_fat"]["value"] == "0.5"     # from "L 0.5"
    assert rows_by_label["sodium"]["value"] == "109"
    assert rows_by_label["fiber"]["value"] == "2.9"
    # unit comes from the label parenthetical, not the bare value
    assert rows_by_label["sodium"]["unit"] == "מג"
    assert "קל" in rows_by_label["energy"]["unit"]
    assert rows_by_label["fat"]["unit"] == "גרם"


def test_yohananof_header_read_verbatim_not_synthesized():
    """The verbatim page header is recorded — the real page shows 'ל100 גרם' with NO
    hyphen. The old parser fabricated the literal 'ל-100 גרם'; that must not recur."""
    raw = bn._parse_yohananof_nutrition(_soup(_YOHANANOF_FIXTURE))
    header = raw["selection"]["selected_table_header"]
    assert header == "ל100 גרם"                 # exactly what the page renders
    assert "ל-100" not in header                # the fabricated hyphenated literal is gone
    assert header == raw["tables"][0]["subInfo"]


def test_yohananof_sodium_mg_preserved_end_to_end():
    """A mg value must survive to the parsed panel as mg (unit-in-label fix). On the
    real fixture sodium=109; a SMALL mg value (7) must NOT be ×1000'd to 7000."""
    parsed = bn.parse_nutrition_rows(
        bn._parse_yohananof_nutrition(_soup(_YOHANANOF_FIXTURE))["rows"])
    assert parsed["sodium"] == "109 מג"
    assert bn.parse_sodium_mg(parsed["sodium"]) == 109.0
    # the failure mode the old value-only sniff caused: low-mg sodium demoted to grams
    small = bn._parse_yohananof_nutrition(
        _yo_soup('<li><div><span>נתרן (מג)</span></div>7</li>'))
    p = bn.parse_nutrition_rows(small["rows"])
    assert p["sodium"] == "7 מג"
    assert bn.parse_sodium_mg(p["sodium"]) == 7.0      # NOT 7000


def test_yohananof_unknown_basis_is_insufficient():
    """Tabpanel present but the page states NO basis caption → insufficient=True,
    rows=[] (match Victory). No silent-accept of unknown-basis rows."""
    raw = bn._parse_yohananof_nutrition(
        _yo_soup('<li><div><span>אנרגיה (קלוריות)</span></div>199</li>',
                 basis_caption=None))
    assert raw["selection"]["selected_basis"] == "unknown"
    assert raw["selection"]["insufficient"] is True
    assert raw["rows"] == []
    # a price-only "₪ / 100 גרם" string must NOT be promoted to a basis
    priced = bn._parse_yohananof_nutrition(
        _yo_soup('<li><div><span>אנרגיה (קלוריות)</span></div>199</li>',
                 basis_caption="‏7.10 ₪ / 100 גרם"))
    assert priced["selection"]["insufficient"] is True
    assert priced["rows"] == []


def test_yohananof_ambiguous_row_is_insufficient():
    """A structurally ambiguous row (>1 numeric token) rejects the whole panel."""
    raw = bn._parse_yohananof_nutrition(
        _yo_soup('<li><div><span>אנרגיה (קלוריות)</span></div>199 240</li>'))
    assert raw["selection"]["insufficient"] is True
    assert raw["rows"] == []


def test_sniff_unit_matches_all_mg_quote_forms():
    """Unit sniff recognises mg in bare / gershayim / ASCII-quote forms (TASK-247 #4)."""
    assert bn._sniff_unit('39 מ"ג') == "מג"          # ASCII double-quote
    assert bn._sniff_unit("39 מ״ג") == "מג"          # Hebrew gershayim U+05F4
    assert bn._sniff_unit("39 מג") == "מג"           # bare
    assert bn._sniff_unit("נתרן (מג)", "109") == "מג"  # unit in label (Yohananof)
    assert bn._sniff_unit("16000 קלוריות") == "קל"
    assert bn._sniff_unit("8.3 גרם") == "גרם"


def test_extract_nutrition_raw_auto_dispatches_by_retailer():
    """Auto-detect routes Shufersal / Victory / Yohananof to the right parser."""
    shuf = _soup(_GINGER_DUAL)
    vic = _soup(_VICTORY_FIXTURE)
    yo = _soup(_YOHANANOF_FIXTURE)
    assert bn._detect_html_format(shuf) == "shufersal"
    assert bn._detect_html_format(vic) == "victory"
    assert bn._detect_html_format(yo) == "yohananof"
    # Shufersal path == extract_nutrition_raw (two competing tables, per-100g chosen)
    auto_shuf = bn.extract_nutrition_raw_auto(shuf)
    assert auto_shuf["selection"]["competing_table_count"] == 2
    assert bn.parse_num(bn.parse_nutrition_rows(auto_shuf["rows"])["energy"]) == 77.0
    # Victory path == _parse_victory_nutrition
    assert bn.extract_nutrition_raw_auto(vic)["rows"] == bn._parse_victory_nutrition(vic)["rows"]
    # Yohananof path == _parse_yohananof_nutrition
    assert bn.extract_nutrition_raw_auto(yo)["selection"]["selected_table_header"] == "ל100 גרם"

# ── TASK-376: Victory sugars_raw → sugars_g regression guard ───────────────────
#
# Root cause: choc_task366b_write_final.py wrote the Victory sugar field under the
# key "sugars_raw" (plural) instead of the canonical "sugar_raw" (singular).
# parse_nutrition_numeric() read n.get("sugar_raw") which returned None → sugars_g=null
# → the chocolate scoring engine scored Lindt 70% as if sugar=0 → inflated score ~61/C
# instead of the correct ~28.7/E.
#
# Fix at the shared layer: parse_nutrition_numeric() now accepts BOTH spellings —
# "sugar_raw" (canonical, checked first) and "sugars_raw" (alternate/Victory) —
# so a wrong-key bug at the builder layer never silently drops sugars again.

def test_victory_sugars_raw_plural_accepted():
    """TASK-376: sugars_raw (plural) must NOT drop to null — same as sugar_raw (singular).

    This is the exact key-mismatch that caused Lindt 70% to be scored as if sugar=0,
    inflating its score from ~28.7/E to ~61/C during the chocolate pass-2 Victory run.
    """
    # Canonical key: works before and after the fix
    out_canonical = bn.parse_nutrition_numeric({
        "energy_kcal_raw": "566", "fat_raw": "41", "saturated_fat_raw": "24",
        "carbs_raw": "34", "sugar_raw": "30", "protein_raw": "9.5",
        "sodium_raw": "39",
    })
    assert out_canonical["sugars_g"] == 30.0, "sugar_raw must map to sugars_g"

    # Alternate key (the Victory builder bug spelling): must now also work
    out_alt = bn.parse_nutrition_numeric({
        "energy_kcal_raw": "566", "fat_raw": "41", "saturated_fat_raw": "24",
        "carbs_raw": "34", "sugars_raw": "30", "protein_raw": "9.5",
        "sodium_raw": "39",
    })
    assert out_alt["sugars_g"] == 30.0, (
        "sugars_raw (plural) must also map to sugars_g — Victory builder uses this spelling"
    )

    # Canonical takes priority over alternate when BOTH are present
    out_both = bn.parse_nutrition_numeric({
        "sugar_raw": "28", "sugars_raw": "99",  # canonical must win
        "energy_kcal_raw": "566", "fat_raw": "41", "saturated_fat_raw": "24",
        "carbs_raw": "34", "protein_raw": "9.5", "sodium_raw": "39",
    })
    assert out_both["sugars_g"] == 28.0, "sugar_raw must take priority over sugars_raw"

    # Neither key present → None (unchanged behaviour)
    out_null = bn.parse_nutrition_numeric({
        "energy_kcal_raw": "566", "fat_raw": "41", "carbs_raw": "34",
        "protein_raw": "9.5", "sodium_raw": "39",
    })
    assert out_null["sugars_g"] is None, "absent sugar must remain None"


def test_lindt_70_sugars_not_null_with_victory_spelling():
    """TASK-376 Lindt 70% reproduction — the exact numeric panel from the Victory API.

    nutrition dict from choc_task366b_write_final.py to_scoring_raw():
      energy=566, fat=41, sat=24, carbs=34, sugar=30, protein=9.5, sodium=39
    The bug: sugar was stored under 'sugars_raw'; parse_nutrition_numeric returned None.
    After the fix: sugars_g must be 30.0 regardless of which spelling is used.
    """
    # Simulate the buggy builder output (key='sugars_raw')
    buggy_raw = {
        "energy_kcal_raw": "566",
        "fat_raw": "41",
        "saturated_fat_raw": "24",
        "trans_fat_raw": "0.5",
        "sodium_raw": "39",
        "carbs_raw": "34",
        "sugars_raw": "30",        # ← the wrong key that caused the bug
        "fiber_raw": "",
        "protein_raw": "9.5",
    }
    panel = bn.parse_nutrition_numeric(buggy_raw)
    assert panel["sugars_g"] == 30.0, (
        f"Lindt 70% sugars_g must be 30.0 g/100g, got {panel['sugars_g']!r} — "
        "sugars_raw key must now be accepted by parse_nutrition_numeric"
    )
    # Confirm other fields unaffected
    assert panel["energy_kcal"] == 566.0
    assert panel["fat_g"] == 41.0
    assert panel["fat_saturated_g"] == 24.0
    assert panel["carbohydrates_g"] == 34.0
    assert panel["protein_g"] == 9.5
    assert panel["sodium_mg"] == 39.0


# ── Bare runner (no pytest dependency) ─────────────────────────────────────────

if __name__ == "__main__":
    import traceback

    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL  {fn.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
