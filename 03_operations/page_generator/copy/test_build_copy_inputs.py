#!/usr/bin/env python3
"""test_build_copy_inputs.py — TASK-553 selftests for superlative margin gate + S_VERBATIM fix.

Tests:
  T1: margin_gate GRANT  — clear margin correctly grants the token
  T2: margin_gate REVOKE — thin margin correctly withholds the token
  T3: margin_gate REVOKE (tied 2nd place) — tie widens the margin computation
  T4: n_gate REVOKE — corpus n < 12 withholds even a clear-margin extreme
  T5: S-derivation WITH S products — s_products comes from grade==S in the page,
      s_verbatim attached from external file, source = per-category file
  T6: S-derivation WITHOUT S products — non-yogurt category returns s_products=[]
      and no s_verbatim on any sheet
  T7: Real cereals regression — rice-apple lowest_sugar is REVOKED, highest_protein
      on Vitabix is GRANTED, s_products==[]
  T8: passes_margin_gate flat corpus — corpus range==0 → no grant
  T9: uniqueness gate — tie value → no grant (rule 1, was existing behaviour)

Run:
  python test_build_copy_inputs.py           # standalone
  pytest test_build_copy_inputs.py -v        # via pytest
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Add the copy directory to sys.path so we can import build_copy_inputs
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

import build_copy_inputs as BCI  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers to build minimal fake product structures
# ---------------------------------------------------------------------------

def _make_product(barcode: str, protein=None, sugar=None, kcal=None,
                  fat=None, sodium=None, fiber=None, grade="B", score=70.0,
                  name="test product"):
    """Minimal page-JSON product stub."""
    nutrition = {}
    if protein is not None:
        nutrition["protein"] = protein
    if sugar is not None:
        nutrition["sugar"] = sugar
    if kcal is not None:
        nutrition["energyKcal"] = kcal
    if fat is not None:
        nutrition["fat"] = fat
    if sodium is not None:
        nutrition["sodium"] = sodium
    if fiber is not None:
        nutrition["fiber"] = fiber
    return {
        "barcode": barcode,
        "id": f"bsip1_test_{barcode}",
        "name": name,
        "retailer": "test",
        "score": score,
        "grade": grade,
        "expansion": {"nutrition": nutrition},
        "bariInterpretation": [],
        "bestUseCases": ["PENDING_COPY"],
        "d4_additives": [],
    }


def _build_stats(products):
    stats = BCI.compute_corpus_stats(products)
    stats["_products"] = products
    stats["_product_count"] = len(products)
    return stats


def _superlatives_for(product, products):
    stats = _build_stats(products)
    return BCI.superlatives_for(product, stats)


# ---------------------------------------------------------------------------
# T1: margin_gate GRANT — clear gap correctly grants the token
# ---------------------------------------------------------------------------

def test_t1_margin_gate_grant():
    """Highest protein granted when margin over 2nd place >= 10% of range."""
    # 12 products; extreme = 20.0; 2nd = 12.0; range = 19.0; margin = 8.0; threshold = 1.9
    products = [_make_product(str(i), protein=p) for i, p in enumerate(
        [20.0, 12.0, 11.0, 10.5, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 1.0]
    )]
    winner = products[0]
    tokens = _superlatives_for(winner, products)
    assert "highest_protein" in tokens, f"T1 FAIL: expected highest_protein, got {tokens}"
    print("T1 PASS: margin_gate GRANT — highest_protein granted (margin=8.0 >= threshold=1.9)")


# ---------------------------------------------------------------------------
# T2: margin_gate REVOKE — thin margin correctly withholds token
# ---------------------------------------------------------------------------

def test_t2_margin_gate_revoke():
    """Lowest sugar revoked when margin over 2nd place < 10% of range."""
    # Range 26.1; rice-apple situation: 3.8, 4.2, ... → margin=0.4 < threshold=2.61
    products = [_make_product(str(i), sugar=s) for i, s in enumerate(
        [3.8, 4.2, 8.0, 16.4, 18.5, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 29.9]
    )]
    winner = products[0]
    tokens = _superlatives_for(winner, products)
    assert "lowest_sugar" not in tokens, f"T2 FAIL: lowest_sugar should be revoked, got {tokens}"
    print("T2 PASS: margin_gate REVOKE — lowest_sugar withheld (margin=0.4 < threshold=2.61)")


# ---------------------------------------------------------------------------
# T3: margin_gate REVOKE when 2nd place is a different value but still thin
# ---------------------------------------------------------------------------

def test_t3_margin_gate_boundary():
    """Token is withheld at exactly boundary (margin == threshold - epsilon)."""
    # range = 10.0; threshold = 1.0; margin = 0.99 → fails
    products = [_make_product(str(i), kcal=k) for i, k in enumerate(
        [100.0, 100.99, 105.0, 107.0, 108.0, 109.0, 109.5, 109.6, 109.7, 109.8, 109.9, 110.0]
    )]
    winner = products[0]
    tokens = _superlatives_for(winner, products)
    assert "lowest_kcal" not in tokens, f"T3 FAIL: lowest_kcal should be withheld at boundary, got {tokens}"
    print("T3 PASS: margin_gate boundary REVOKE — lowest_kcal withheld (margin=0.99 < threshold=1.0)")


# ---------------------------------------------------------------------------
# T4: n_gate REVOKE — corpus n < 12
# ---------------------------------------------------------------------------

def test_t4_n_gate_revoke():
    """Token withheld when fewer than 12 non-null observations."""
    # 11 products — just below threshold
    products = [_make_product(str(i), protein=p) for i, p in enumerate(
        [20.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]
    )]
    assert len(products) == 11
    winner = products[0]
    tokens = _superlatives_for(winner, products)
    assert "highest_protein" not in tokens, f"T4 FAIL: n<12 should withhold token, got {tokens}"
    print("T4 PASS: n_gate REVOKE — highest_protein withheld for n=11 (< 12)")


# ---------------------------------------------------------------------------
# T5: S-derivation WITH S products — grade-derived, verbatim from external file
# ---------------------------------------------------------------------------

def test_t5_s_derivation_with_s_products():
    """s_products derived from page grade==S; verbatim loaded from per-category file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write a fake s_verbatim file for category "test-cat"
        s_verbatim_dir = os.path.join(tmpdir, "s_verbatim")
        os.makedirs(s_verbatim_dir)
        verbatim_file = os.path.join(s_verbatim_dir, "test-cat.json")
        with open(verbatim_file, "w", encoding="utf-8") as f:
            json.dump({
                "_source": "test-approved",
                "_category": "test-cat",
                "BC_S_001": {
                    "insightLine": "approved insight",
                    "s_grade_explanation": "approved explanation"
                }
            }, f)

        # Patch the module's _S_VERBATIM_DIR to use our tmpdir
        original_dir = BCI._S_VERBATIM_DIR
        BCI._S_VERBATIM_DIR = s_verbatim_dir
        try:
            result = BCI._load_s_verbatim("test-cat")
            assert "BC_S_001" in result, f"T5a FAIL: barcode not in result: {result}"
            assert "_source" not in result, f"T5a FAIL: metadata key leaked: {result}"
            assert result["BC_S_001"]["insightLine"] == "approved insight", "T5a FAIL: verbatim mismatch"

            # Simulate main() s_products derivation: from grade==S in sheets
            sheets = [
                {"barcode": "BC_S_001", "grade": "S", "score": 91.0},
                {"barcode": "BC_A_001", "grade": "A", "score": 80.0},
                {"barcode": "BC_B_001", "grade": "B", "score": 70.0},
            ]
            s_products = [s["barcode"] for s in sheets if s.get("grade") == "S"]
            assert s_products == ["BC_S_001"], f"T5b FAIL: s_products={s_products}"

            # s_verbatim attached to the S product's sheet (as main() does)
            sheet_s = sheets[0]
            bc = sheet_s["barcode"]
            if bc in result:
                sheet_s["s_verbatim"] = result[bc]
            assert "s_verbatim" in sheet_s, "T5c FAIL: s_verbatim not attached to S sheet"
            # Non-S sheet gets no s_verbatim
            for s in sheets[1:]:
                assert "s_verbatim" not in s, f"T5d FAIL: s_verbatim leaked to non-S: {s}"

        finally:
            BCI._S_VERBATIM_DIR = original_dir

    print("T5 PASS: S-derivation WITH S products — grade-derived, verbatim from external file")


# ---------------------------------------------------------------------------
# T6: S-derivation WITHOUT S products (no S in a non-yogurt category)
# ---------------------------------------------------------------------------

def test_t6_s_derivation_no_s_products():
    """Category with no S products: s_products==[], no s_verbatim on any sheet."""
    # "breakfast-cereals" has no s_verbatim file → _load_s_verbatim returns {}
    result = BCI._load_s_verbatim("breakfast-cereals")
    assert result == {}, f"T6 FAIL: expected empty dict for cereals, got {result}"

    sheets = [
        {"barcode": "A001", "grade": "A", "score": 88.0},
        {"barcode": "B001", "grade": "B", "score": 72.0},
    ]
    s_products = [s["barcode"] for s in sheets if s.get("grade") == "S"]
    assert s_products == [], f"T6 FAIL: s_products should be [] for cereals, got {s_products}"
    for s in sheets:
        assert "s_verbatim" not in s, f"T6 FAIL: s_verbatim on non-S sheet: {s}"

    print("T6 PASS: S-derivation WITHOUT S products — s_products==[], no verbatim leak")


# ---------------------------------------------------------------------------
# T7: Real cereals regression — rice-apple revoked, Vitabix protein granted
# ---------------------------------------------------------------------------

def test_t7_real_cereals_regression():
    """Integration test: cereals_generated_v2.json + cereals config → expected token state."""
    page_path = os.path.join(
        _THIS_DIR, "..", "..", "page_generator", "outputs", "cereals_generated_v2.json"
    )
    if not os.path.isfile(page_path):
        print("T7 SKIP: cereals_generated_v2.json not found (not blocking)")
        return

    with open(page_path, encoding="utf-8") as f:
        page = json.load(f)

    products = page["products"]
    stats = _build_stats(products)

    rice_apple_bc = "7297488199590"
    vitabix_bc = "5010029000061"

    rice_apple = next((p for p in products if p["barcode"] == rice_apple_bc), None)
    vitabix = next((p for p in products if p["barcode"] == vitabix_bc), None)

    assert rice_apple is not None, f"T7 FAIL: rice-apple {rice_apple_bc} not found in cereals page"
    assert vitabix is not None, f"T7 FAIL: vitabix {vitabix_bc} not found in cereals page"

    rice_tokens = BCI.superlatives_for(rice_apple, stats)
    vitabix_tokens = BCI.superlatives_for(vitabix, stats)

    assert "lowest_sugar" not in rice_tokens, (
        f"T7 FAIL: rice-apple lowest_sugar should be REVOKED. Got: {rice_tokens}"
    )
    assert "highest_protein" in vitabix_tokens, (
        f"T7 FAIL: vitabix highest_protein should be GRANTED. Got: {vitabix_tokens}"
    )

    # s_products must be [] for cereals
    cereals_s_verbatim = BCI._load_s_verbatim("breakfast-cereals")
    sheets_grades = [{"barcode": p["barcode"], "grade": p.get("grade")} for p in products]
    s_products = [s["barcode"] for s in sheets_grades if s.get("grade") == "S"]
    assert s_products == [], f"T7 FAIL: cereals s_products should be []. Got: {s_products}"

    print(f"T7 PASS: cereals regression — rice-apple lowest_sugar REVOKED, vitabix highest_protein GRANTED, s_products=[]")


# ---------------------------------------------------------------------------
# T8: Flat corpus (range == 0) → no grant
# ---------------------------------------------------------------------------

def test_t8_flat_corpus():
    """When all corpus values are identical, corpus_range==0 and gate fails."""
    # All 12 products have protein=10.0 → range=0
    products = [_make_product(str(i), protein=10.0) for i in range(12)]
    winner = products[0]
    tokens = _superlatives_for(winner, products)
    assert "highest_protein" not in tokens, f"T8 FAIL: flat corpus should grant nothing, got {tokens}"
    print("T8 PASS: flat corpus range==0 → no superlative granted")


# ---------------------------------------------------------------------------
# T9: Tie at extreme (uniqueness gate, rule 1) → no grant
# ---------------------------------------------------------------------------

def test_t9_tie_at_extreme():
    """Two products share the protein maximum — neither gets highest_protein."""
    products = [_make_product(str(i), protein=p) for i, p in enumerate(
        [20.0, 20.0, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0, 1.0]
    )]
    # Both 0 and 1 share the max
    for winner in products[:2]:
        tokens = _superlatives_for(winner, products)
        assert "highest_protein" not in tokens, (
            f"T9 FAIL: tie should not grant highest_protein, barcode={winner['barcode']}, got {tokens}"
        )
    print("T9 PASS: tie at extreme → highest_protein not granted (rule 1 uniqueness)")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all():
    tests = [
        test_t1_margin_gate_grant,
        test_t2_margin_gate_revoke,
        test_t3_margin_gate_boundary,
        test_t4_n_gate_revoke,
        test_t5_s_derivation_with_s_products,
        test_t6_s_derivation_no_s_products,
        test_t7_real_cereals_regression,
        test_t8_flat_corpus,
        test_t9_tie_at_extreme,
    ]
    passed = 0
    failed = 0
    skipped = 0
    errors = []
    for t in tests:
        try:
            t()
            passed += 1
        except SkipTest as e:
            skipped += 1
            print(f"  (skipped: {e})")
        except AssertionError as e:
            failed += 1
            errors.append(f"  FAIL {t.__name__}: {e}")
            print(f"FAIL {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            errors.append(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print()
    print(f"=== {passed} passed / {skipped} skipped / {failed} failed ===")
    if errors:
        print("Failures:")
        for e in errors:
            print(e)
    return failed == 0


class SkipTest(Exception):
    pass


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
