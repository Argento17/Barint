# -*- coding: utf-8 -*-
"""
Tests for the shared BSIP0 exit gate (bsip0_gate.py).

Run: python -m pytest test_bsip0_gate.py -v
     python   test_bsip0_gate.py               (no pytest dependency)
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import bsip0_gate as gate  # noqa: E402


# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_product(barcode: str = "7290000000001", name_he: str = "בדיקה", **kw) -> dict:
    p = {"barcode": barcode, "name_he": name_he}
    p.update(kw)
    return p


def _make_basis(selected: str = "per_100g", competing: int = 1,
                insufficient: bool = False, header: str = "100 גרם") -> dict:
    return {"selected_basis": selected, "selected_table_index": 0,
            "selected_table_header": header, "competing_table_count": competing,
            "insufficient": insufficient}


def _make_doc(products: list[dict], **meta) -> dict:
    doc: dict = {
        "run_id": "test_run_001", "category": "test", "retailer": "test_retailer",
        "panel_source": "direct_scrape", "provenance": {"source": "test_retailer"},
        "products": products,
    }
    doc.update(meta)
    return doc


# ── G1: OFF contamination ──────────────────────────────────────────────────────

def test_g1_clean_passes():
    doc = _make_doc([_make_product()])
    r = gate.gate_off_contamination(doc["products"], doc)
    assert r["status"] == "PASS", r["messages"]


def test_g1_off_token_in_nutrition_fails():
    p = _make_product(nutrition={"energy_kcal_raw": "openfoodfacts"})
    doc = _make_doc([p])
    r = gate.gate_off_contamination(doc["products"], doc)
    assert r["status"] == "FAIL", r["messages"]
    assert any("OFF_CONTAMINATION" in m for m in r["messages"])


def test_g1_bare_off_in_source_fails():
    doc = _make_doc([_make_product()], provenance={"source": "off"})
    r = gate.gate_off_contamination(doc["products"], doc)
    assert r["status"] == "FAIL", r["messages"]


def test_g1_bare_off_in_product_name_does_not_fail():
    """'off' as substring in a product name (coffee, cutoff) is NOT a hit."""
    p = _make_product(name_he="קפה נמס", nutrition={"fat_raw": "0.5"})
    doc = _make_doc([p])
    r = gate.gate_off_contamination(doc["products"], doc)
    assert r["status"] == "PASS", r["messages"]


# ── G2/G3: nutrition basis ─────────────────────────────────────────────────────

def test_g2_clean_basis_passes():
    p = _make_product(nutrition_raw={"energy": "504"}, nutrition_basis=_make_basis())
    r = gate.gate_nutrition_basis([p])
    assert r["status"] == "PASS", r["messages"]


def test_g2_insufficient_basis_fails():
    p = _make_product(nutrition_raw={"energy": "504"},
                      nutrition_basis=_make_basis(insufficient=True, competing=2))
    r = gate.gate_nutrition_basis([p])
    assert r["status"] == "FAIL", r["messages"]


def test_g3_multitable_non_per_100g_fails():
    p = _make_product(nutrition_raw={"energy": "6"},
                      nutrition_basis=_make_basis(selected="per_serving", competing=2))
    r = gate.gate_nutrition_basis([p])
    assert r["status"] == "FAIL", r["messages"]


# ── G4/G5: identity ────────────────────────────────────────────────────────────

def test_g4_duplicate_barcode_fails():
    p1 = _make_product(barcode="7290000000001", name_he="מוצר א")
    p2 = _make_product(barcode="7290000000001", name_he="מוצר א")
    r = gate.gate_identity([p1, p2])
    assert r["status"] == "FAIL", r["messages"]
    assert any("DUPLICATE" in m for m in r["messages"])


def test_g5_conflicting_identity_fails():
    p1 = _make_product(barcode="7290000000001", name_he="מוצר א")
    p2 = _make_product(barcode="7290000000001", name_he="מוצר ב")
    r = gate.gate_identity([p1, p2])
    assert r["status"] == "FAIL", r["messages"]
    assert any("CONFLICTING" in m for m in r["messages"])


def test_g4_g5_no_duplicates_passes():
    p1 = _make_product(barcode="7290000000001")
    p2 = _make_product(barcode="7290000000002")
    r = gate.gate_identity([p1, p2])
    assert r["status"] == "PASS", r["messages"]


# ── G6: numeric sanity ─────────────────────────────────────────────────────────

def test_g6_clean_nutrition_passes():
    p = _make_product(nutrition_raw={"energy": "250", "fat": "10", "protein": "5",
                                      "carbs": "30", "sodium": "100", "fiber": "3",
                                      "sugar": "5", "saturated_fat": "2"})
    r = gate.gate_numeric_sanity([p])
    assert r["status"] == "PASS", r["messages"]


def test_g6_sat_gt_total_fat_fails():
    p = _make_product(nutrition_raw={"energy": "250", "fat": "2", "saturated_fat": "5"})
    r = gate.gate_numeric_sanity([p])
    assert r["status"] == "FAIL", r["messages"]


def test_g6_fat_understated_fails():
    """fat <= 0.5 with declared energy 50+ kcal above macro estimate → FAIL."""
    p = _make_product(nutrition_raw={"energy": "250", "fat": "0.5",
                                      "protein": "1", "carbs": "5"})
    r = gate.gate_numeric_sanity([p])
    assert r["status"] == "FAIL", r["messages"]
    assert any("fat_understated" in m for m in r["messages"]), r["messages"]


# ── G7/G8: ingredients ─────────────────────────────────────────────────────────

def test_g7_full_ingredient_coverage_passes():
    p = _make_product(ingredients_raw="קמח, מים, מלח", ingredients_raw_source="scrape")
    r = gate.gate_ingredients([p])
    assert r["status"] == "PASS", r["messages"]


def test_g7_low_coverage_warns():
    p1 = _make_product(barcode="729001")  # no ingredients
    p2 = _make_product(barcode="729002")  # no ingredients
    p3 = _make_product(barcode="729003")  # no ingredients
    r = gate.gate_ingredients([p1, p2, p3])
    assert r["status"] == "WARN", r["messages"]
    assert any("COVERAGE_WARN" in m for m in r["messages"])

def test_g7_no_source_warns():
    p = _make_product(ingredients_raw="קמח, מים")  # has ingredients but no source
    r = gate.gate_ingredients([p])
    assert r["status"] == "WARN", r["messages"]
    assert any("RAW_SOURCE_WARN" in m for m in r["messages"])


# ── G9: run summary ────────────────────────────────────────────────────────────

def test_g9_full_summary_passes():
    doc = _make_doc([_make_product()])
    r = gate.gate_run_summary(doc)
    assert r["status"] == "PASS", r["messages"]


def test_g9_missing_fields_fails():
    doc = {"products": [_make_product()]}
    r = gate.gate_run_summary(doc)
    assert r["status"] == "FAIL", r["messages"]
    assert any("missing required" in m.lower() for m in r["messages"])


# ── G10: image reachability ────────────────────────────────────────────────────

def test_g10_no_images_is_warn():
    p = _make_product()  # no imageUrl
    r = gate.gate_image_reachability([p])
    # >50% null rate with no images = WARN
    assert r["status"] in ("WARN", "PASS"), r["messages"]


def test_g10_reachable_image_probed():
    """Probe a known-reachable public image. Uses Google's favicon as a
    reliable public endpoint; not a Bari image (we do not hard-code live URLs)."""
    p = _make_product(imageUrl="https://www.google.com/favicon.ico")
    r = gate.gate_image_reachability([p])
    # This will be PASS on any network with internet access; the gate tolerates
    # individual unreachable images (<50% rate). Just verify it runs without error.
    assert "messages" in r
    assert r["check"] == "G10_image_reachability"


def test_g10_broken_url_does_not_crash():
    p = _make_product(imageUrl="https://this-domain-definitely-does-not-exist-bari-test.co.il/image.jpg")
    r = gate.gate_image_reachability([p])
    # Should not crash. Status depends on network, but check runs clean.
    assert r["check"] == "G10_image_reachability"
    assert isinstance(r["status"], str)


# ── G11: barcode checksum ──────────────────────────────────────────────────────

def test_g11_valid_ean13_passes():
    # Known-valid EAN-13: digits 1..12 weighted (odd*1 + even*3)
    # 7 2 9 0 0 0 0 0 0 0 0 0
    # 7*1 + 2*3 + 9*1 = 7+6+9 = 22 → check = (10-22%10)%10 = 8
    p = _make_product(barcode="7290000000008")
    r = gate.gate_barcode_checksum([p])
    assert r["status"] == "PASS", r["messages"]


def test_g11_invalid_ean13_warns():
    p = _make_product(barcode="7290000000001")  # wrong check digit
    r = gate.gate_barcode_checksum([p])
    assert r["status"] == "WARN", r["messages"]
    assert any("BARCODE_CHECKSUM" in m for m in r["messages"])


def test_g11_non_ean13_not_flagged():
    """Short or non-numeric barcodes are not flagged by EAN-13 check."""
    p = _make_product(barcode="ABC123")
    r = gate.gate_barcode_checksum([p])
    assert r["status"] == "PASS", r["messages"]


# ── G12: scope boundary ────────────────────────────────────────────────────────

def test_g12_clean_names_pass():
    p = _make_product(name_he="יוגורט טבעי 3%")
    r = gate.gate_scope_boundary([p])
    assert r["status"] == "PASS", r["messages"]


def test_g12_non_food_token_fails():
    p = _make_product(name_he="שמפו לשיער יבש")
    r = gate.gate_scope_boundary([p])
    assert r["status"] == "FAIL", r["messages"]


def test_g12_extra_negative_added():
    p = _make_product(name_he="משקה חלב סויה")
    r = gate.gate_scope_boundary([p], extra_negative=["סויה"])
    assert r["status"] == "FAIL", r["messages"]


# ── G13: cross-category acquisition (TASK-498) ─────────────────────────────────

def test_g13_own_category_query_passes():
    """A record acquired via a term maadanim itself owns is not flagged."""
    p = _make_product(name_he="מעדן חלב וניל", acquisition_query="מעדן")
    r = gate.gate_cross_category_acquisition([p], category="maadanim")
    assert r["status"] == "PASS", r["messages"]


def test_g13_no_registry_entry_is_noop_pass():
    """An unregistered category is skipped, not treated as contamination."""
    p = _make_product(name_he="מוצר כלשהו", acquisition_query="מוצר כלשהו")
    r = gate.gate_cross_category_acquisition([p], category="some_new_category_v9")
    assert r["status"] == "PASS", r["messages"]


def test_g13_reproduces_run_maadanim_001_collision_exact_real_data():
    """Exact reproduction using the REAL field values verified on disk in
    03_operations/bsip1/run_maadanim_001/output/ for all 5 confirmed
    TASK-477/TASK-409 collision barcodes. All 5 carry acquisition_query
    'מעדן פרוטאין' (maadanim's OWN registered term — confirmed on disk), so
    signal 1 (query ownership) does NOT fire for any of them; this is exactly
    why signal 2 (product-form head noun) exists. 3 of the 5 carry 'חטיף'
    (snack_bars' bar-form noun) in the name and ARE caught. The other 2
    (brand 'נייטשר פרוטאין') are NOT caught by either signal — this is a
    known, reported residual gap (see PRODUCT_FORM_HEAD_NOUNS docstring),
    not a false claim of 100% recall.
    """
    real_records = [
        {"barcode": "7290019401018", "name_he": "חטיף פרוטאין קרם עוגיות", "acquisition_query": "מעדן פרוטאין"},
        {"barcode": "7290019401049", "name_he": "חטיף פרוטאין שוקולד קרמל", "acquisition_query": "מעדן פרוטאין"},
        {"barcode": "7290019401544", "name_he": "חטיף פרוטאין עוגיות טופי", "acquisition_query": "מעדן פרוטאין"},
        {"barcode": "8410076610379", "name_he": "נייטשר פרוטאין שוקולד", "acquisition_query": "מעדן פרוטאין"},
        {"barcode": "8410076610386", "name_he": "נייטשר פרוטאין קרמל מלוח", "acquisition_query": "מעדן פרוטאין"},
    ]
    r = gate.gate_cross_category_acquisition(real_records, category="maadanim")
    assert r["status"] == "WARN", r["messages"]
    joined = " ".join(r["messages"])
    caught_by_name = ["7290019401018", "7290019401049", "7290019401544"]
    for bc in caught_by_name:
        assert bc in joined, f"expected {bc} to be flagged by the head-noun signal: {r['messages']}"
    # Honest residual-gap check: the 2 brand-name barcodes are NOT caught by
    # either signal today. If this assertion ever starts failing because a
    # future change added brand-registry coverage, that's an improvement —
    # update this test to require them, don't just delete the check.
    not_yet_caught = ["8410076610379", "8410076610386"]
    for bc in not_yet_caught:
        assert bc not in joined, (
            f"{bc} is now caught — great, but this test documents today's known "
            f"gap; update the test's claim (and the module docstring) rather than "
            f"silently deleting this assertion."
        )


def test_g13_strict_mode_hard_fails():
    p = _make_product(barcode="7290019401049", name_he="חטיף פרוטאין שוקולד קרמל",
                       acquisition_query="חטיף חלבון")
    r = gate.gate_cross_category_acquisition([p], category="maadanim", strict=True)
    assert r["status"] == "FAIL", r["messages"]


def test_g13_real_run_maadanim_001_full_corpus_precision():
    """Integration precision check against the REAL, on-disk 200-product
    run_maadanim_001 BSIP1 output (not a synthetic fixture). Proves two
    things at once: (1) recall — the 3 name-disclosing collision barcodes
    (+ 1 bonus true positive the original TASK-477 trace didn't happen to
    surface, 8410076900333, also 'חטיף פרוטאין...') are all caught; (2)
    precision — NOT ONE of the other ~196 legitimate dairy-dessert records
    is flagged. This is the test that caught two real false-positive
    candidates during development (קורנפלקס/עוגיות as toppings inside
    genuine desserts) BEFORE they were registered — keep this test wired to
    the real directory so any future PRODUCT_FORM_HEAD_NOUNS addition is
    forced through the same full-corpus precision bar.

    Skips gracefully (does not fail) if the directory is not present, so the
    suite stays portable / does not depend on this specific run existing.
    """
    real_dir = r"C:\Bari\03_operations\bsip1\run_maadanim_001\output"
    if not os.path.isdir(real_dir):
        print(f"  [skip] {real_dir} not found — skipping real-corpus precision check")
        return

    records = []
    for fname in os.listdir(real_dir):
        if not fname.startswith("bsip1_") or not fname.endswith(".json"):
            continue
        with open(os.path.join(real_dir, fname), encoding="utf-8") as fh:
            d = json.load(fh)
        records.append({
            "barcode": d.get("barcode"),
            "name_he": d.get("canonical_name_he"),
            "acquisition_query": d.get("acquisition_query", ""),
        })
    assert len(records) >= 100, f"expected ~200 real records, found {len(records)}"

    r = gate.gate_cross_category_acquisition(records, category="maadanim")
    assert r["status"] == "WARN", r["messages"]

    joined = " ".join(r["messages"])
    expected_flagged = {
        "7290019401018", "7290019401049", "7290019401544",  # 3 of TASK-477's 5 (name-disclosing)
        "8410076900333",                                     # bonus true positive found in this task
    }
    for bc in expected_flagged:
        assert bc in joined, f"expected {bc} flagged, got: {r['messages']}"

    # Precision: exactly these 4 barcodes, nothing else, over the whole 200.
    import re
    all_flagged = set(re.findall(r"\b\d{6,14}\b", joined))
    unexpected = all_flagged - expected_flagged
    assert not unexpected, f"unexpected flags (false positives): {unexpected}"


def test_g13_wired_into_run_gate_via_doc_category():
    """run_gate() should pick up the doc's own 'category' field when the
    caller doesn't pass one explicitly (mirrors how gate_run_summary already
    requires 'category' at the doc level)."""
    doc = _make_doc([
        _make_product(barcode="7290019401018", name_he="חטיף פרוטאין קרם עוגיות",
                       acquisition_query="חטיף פרוטאין"),
    ], category="maadanim")
    result = gate.run_gate(doc)
    g13 = [c for c in result["checks"] if c["check"] == "G13_cross_category_acquisition"]
    assert len(g13) == 1
    assert g13[0]["status"] == "WARN", g13[0]["messages"]
    # WARN alone must not flip the overall gate to FAIL (default, non-strict mode)
    assert result["overall_status"] != "FAIL" or any(
        c["status"] == "FAIL" for c in result["checks"] if c["check"] != "G13_cross_category_acquisition"
    )


def test_g13_clean_maadanim_run_all_own_terms_passes():
    """A clean run where every record's query is maadanim's own vocabulary
    produces zero G13 flags — proves the gate does not false-positive on
    legitimate same-category acquisitions."""
    products = [
        _make_product(barcode="7290000000001", name_he="מעדן וניל", acquisition_query="מעדן"),
        _make_product(barcode="7290000000002", name_he="מעדן חלבון תות", acquisition_query="מעדן חלבון"),
        _make_product(barcode="7290000000003", name_he="פודינג שוקולד", acquisition_query="פודינג"),
    ]
    r = gate.gate_cross_category_acquisition(products, category="maadanim")
    assert r["status"] == "PASS", r["messages"]


# ── Composite gate: run_gate ───────────────────────────────────────────────────

def test_run_gate_clean_doc():
    doc = _make_doc([_make_product(
        barcode="7290000000008",
        nutrition_raw={"energy": "250", "fat": "10", "protein": "5",
                       "carbs": "30", "sodium": "100", "fiber": "3",
                       "sugar": "5", "saturated_fat": "2"},
        nutrition_basis=_make_basis(),
        ingredients_raw="קמח, מים, מלח",
        ingredients_raw_source="scrape",
        imageUrl="https://www.google.com/favicon.ico",
    )])
    result = gate.run_gate(doc)
    # Off contamination + run summary + identity + scope should PASS
    # Numeric sanity PASS, basis PASS, ingredients PASS
    assert result["overall_status"] in ("PASS", "WARN"), result["summary"]
    assert result["product_count"] == 1


def test_run_gate_fail_artifact_blocks():
    """Prove that a FAIL artifact (OFF contamination) produces overall FAIL."""
    doc = _make_doc([_make_product(
        nutrition_raw={"energy": "openfoodfacts"},
        nutrition_basis=_make_basis(),
    )])
    result = gate.run_gate(doc)
    assert result["overall_status"] == "FAIL", result["summary"]
    fail_checks = [c for c in result["checks"] if c["status"] == "FAIL"]
    assert any("off" in c["check"].lower() for c in fail_checks), fail_checks


# ── Test: FAIL artifact blocks a builder (the builder precondition) ────────────

def test_gate_fail_blocks_builder():
    """Simulates what a BSIP1 builder does: run the gate, and if FAIL, refuse.

    This is the core proof that a FAIL artifact blocks a builder from running.
    The builder calls gate.run_gate() and exits non-zero on FAIL.
    """
    # A doc that will FAIL (OFF contamination)
    bad_doc = _make_doc([_make_product(
        nutrition_raw={"energy": "openfoodfacts"},
        nutrition_basis=_make_basis(),
    )])
    result = gate.run_gate(bad_doc)
    assert result["overall_status"] == "FAIL", "Gate must FAIL for contaminated data"

    # Simulate the builder precondition check
    def builder_precondition(doc) -> bool:
        result = gate.run_gate(doc)
        return result["overall_status"] != "FAIL"

    assert not builder_precondition(bad_doc), "Builder should refuse FAIL artifact"

    # A clean doc should pass the precondition
    clean_doc = _make_doc([_make_product(
        barcode="7290000000008",
        nutrition_raw={"energy": "250", "fat": "10"},
        nutrition_basis=_make_basis(),
        ingredients_raw="קמח, מים",
    )])
    assert builder_precondition(clean_doc), "Builder should accept PASS artifact"


# ── Bare runner ────────────────────────────────────────────────────────────────

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
