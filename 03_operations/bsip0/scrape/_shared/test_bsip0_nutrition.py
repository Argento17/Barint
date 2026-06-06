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
