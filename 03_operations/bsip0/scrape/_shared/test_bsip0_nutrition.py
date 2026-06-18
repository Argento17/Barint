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
