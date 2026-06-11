"""
Regression test for annotate_fallback (DA-013 structural fix).

Verifies that annotate_fallback re-derives from the product's data state
and never trusts a generator-written 'verified' when the panel is null.

Run:  python -m pytest test_confidence_annotation_fallback.py -v
  or: python test_confidence_annotation_fallback.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import confidence_annotation as CA


def _product(confidence, sub_reason=None, nutrition=None, ingredients=None):
    """Build a minimal frontend-JSON product dict for testing."""
    exp = {"nutrition": nutrition or {}, "ingredients": ingredients}
    return {
        "id": "test",
        "confidence": confidence,
        "confidence_sub_reason": sub_reason,
        "expansion": exp,
    }


# --- DA-013 core invariant: null panel ⇒ never verified ---------------------

def test_null_panel_verified_flips_to_partial_missing_nutrition():
    """Generator wrote 'verified' but no nutrition panel — must become partial/missing."""
    prod = _product("verified", nutrition={
        "energyKcal": None, "protein": None, "sugar": None, "fat": None,
    })
    r = CA.annotate_fallback(prod)
    assert r["confidence"] == "partial"
    assert r["confidence_sub_reason"] == "missing_nutrition"


def test_null_panel_missing_dict_also_flips():
    """Empty expansion.nutrition dict is also a null panel."""
    prod = _product("verified", nutrition={})
    r = CA.annotate_fallback(prod)
    assert r["confidence"] == "partial"
    assert r["confidence_sub_reason"] == "missing_nutrition"


def test_null_panel_partial_stays_partial_missing_nutrition():
    """Already-partial product with null panel: stays partial/missing_nutrition."""
    prod = _product("partial", "partial_field", nutrition={
        "energyKcal": None, "protein": None,
    })
    r = CA.annotate_fallback(prod)
    assert r["confidence"] == "partial"
    assert r["confidence_sub_reason"] == "missing_nutrition"


# --- Panel present: verified must be preserved ------------------------------

def test_panel_present_verified_stays_verified():
    """A product with real nutrition data and generator-written 'verified' is kept."""
    prod = _product("verified", nutrition={"energyKcal": 350.0, "protein": 8.0})
    r = CA.annotate_fallback(prod)
    assert r["confidence"] == "verified"
    assert r["confidence_sub_reason"] is None


def test_panel_present_partial_preserves_sub_reason():
    """Panel present + already-partial: sub_reason is carried forward."""
    prod = _product("partial", "partial_field", nutrition={"energyKcal": 310.0})
    r = CA.annotate_fallback(prod)
    assert r["confidence"] == "partial"
    assert r["confidence_sub_reason"] == "partial_field"


def test_panel_present_partial_low_extraction_preserved():
    prod = _product("partial", "low_extraction", nutrition={"energyKcal": 280.0})
    r = CA.annotate_fallback(prod)
    assert r["confidence"] == "partial"
    assert r["confidence_sub_reason"] == "low_extraction"


# --- Never produces insufficient -------------------------------------------

def test_never_insufficient_null_panel():
    prod = _product("insufficient", nutrition={})
    r = CA.annotate_fallback(prod)
    assert r["confidence"] != "insufficient"


def test_never_insufficient_panel_present():
    prod = _product("insufficient", nutrition={"energyKcal": 200.0})
    r = CA.annotate_fallback(prod)
    assert r["confidence"] != "insufficient"


# --- Hebrew strings are populated ------------------------------------------

def test_label_and_tooltip_populated_for_partial():
    prod = _product("verified", nutrition={})
    r = CA.annotate_fallback(prod)
    assert r["confidence_label_he"]
    assert r["confidence_tooltip_he"]


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
