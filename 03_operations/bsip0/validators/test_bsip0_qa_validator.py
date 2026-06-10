# -*- coding: utf-8 -*-
"""
Test suite for bsip0_qa_validator.py — TASK-218.

Run with:
    python -m pytest C:/Bari/03_operations/bsip0/validators/test_bsip0_qa_validator.py -v
or:
    python C:/Bari/03_operations/bsip0/validators/test_bsip0_qa_validator.py

Covers all 6 checks and the GateSelfPassError guard.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

# Allow direct import when run from any working directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsip0_qa_validator import (
    GateSelfPassError,
    check_portal_availability,
    validate_consumer_output,
    validate_no_fabrication,
    validate_run_summary,
    validate_scope_boundaries,
    verify_product_identity,
)


# ── Test 1: Anti-fabrication detected ─────────────────────────────────────────

class TestFabricationDetected(unittest.TestCase):
    """Round-hour timestamps AND identical nutrition across 4 products → FAIL."""

    def _make_record(self, barcode: str, source: str, ts: str, energy="350") -> dict:
        return {
            "barcode": barcode,
            "source": source,
            "scraped_at": ts,
            "nutrition": {
                "energy_kcal_raw": energy,
                "fat_raw": "28",
                "protein_raw": "25",
                "carbs_raw": "1",
            },
        }

    def test_fabrication_detected_round_hour_timestamps(self):
        """4 products across 2 retailers with hh:00:00 timestamps → FAIL."""
        records = [
            self._make_record("7290001001", "yohananof", "2026-06-07T10:00:00", "380"),
            self._make_record("7290001002", "shufersal", "2026-06-07T11:00:00", "390"),
            self._make_record("7290001003", "yohananof", "2026-06-07T12:00:00", "370"),
            self._make_record("7290001004", "shufersal", "2026-06-07T13:00:00", "360"),
        ]
        result = validate_no_fabrication(records)
        self.assertEqual(result["status"], "FAIL",
                         f"Expected FAIL for round-hour timestamps, got {result}")
        self.assertTrue(any("FABRICATION" in m for m in result["messages"]),
                        f"Expected FABRICATION message, got: {result['messages']}")

    def test_fabrication_detected_identical_nutrition(self):
        """4 products across 2 retailers with identical nutrition dicts → FAIL."""
        identical_nutrition = {
            "energy_kcal_raw": "350",
            "fat_raw": "28.5",
            "protein_raw": "24.0",
            "carbs_raw": "0.5",
        }
        # Use varied timestamps to isolate the nutrition check from timestamp check
        records = [
            {"barcode": "7290001001", "source": "yohananof",
             "scraped_at": "2026-06-07T10:14:37", "nutrition": dict(identical_nutrition)},
            {"barcode": "7290001002", "source": "shufersal",
             "scraped_at": "2026-06-07T10:22:11", "nutrition": dict(identical_nutrition)},
            {"barcode": "7290001003", "source": "yohananof",
             "scraped_at": "2026-06-07T10:35:55", "nutrition": dict(identical_nutrition)},
            {"barcode": "7290001004", "source": "victory",
             "scraped_at": "2026-06-07T10:47:03", "nutrition": dict(identical_nutrition)},
        ]
        result = validate_no_fabrication(records)
        self.assertEqual(result["status"], "FAIL",
                         f"Expected FAIL for identical nutrition, got {result}")
        self.assertTrue(any("FABRICATION" in m for m in result["messages"]),
                        f"Expected FABRICATION message: {result['messages']}")


# ── Test 2: Clean input passes ────────────────────────────────────────────────

class TestCleanInputPasses(unittest.TestCase):
    """Real-looking varied timestamps and varied nutrition → PASS."""

    def _make_record(self, barcode: str, source: str, ts: str, energy: str, fat: str) -> dict:
        return {
            "barcode": barcode,
            "source": source,
            "scraped_at": ts,
            "nutrition": {
                "energy_kcal_raw": energy,
                "fat_raw": fat,
                "protein_raw": "22",
                "carbs_raw": "3",
            },
        }

    def test_clean_input_passes(self):
        """Varied timestamps, varied nutrition, consistent source/barcode → PASS."""
        records = [
            # Yohananof barcodes start with 729 — source tag matches
            self._make_record("7290001001", "yohananof", "2026-06-07T10:14:37", "350", "27.5"),
            self._make_record("7290001002", "yohananof", "2026-06-07T10:22:11", "380", "30.1"),
            self._make_record("7290001003", "yohananof", "2026-06-07T10:35:55", "410", "33.8"),
            self._make_record("7290001004", "yohananof", "2026-06-07T10:47:03", "290", "21.2"),
            # Shufersal with non-729 barcodes (correct for shufersal source)
            self._make_record("5010026515919", "shufersal", "2026-06-07T11:02:44", "320", "24.0"),
        ]
        result = validate_no_fabrication(records)
        self.assertEqual(result["status"], "PASS",
                         f"Expected PASS for clean input, got {result}")

    def test_single_round_hour_not_flagged(self):
        """A single product with a round-hour timestamp is not a fabrication signal."""
        records = [
            # Only one round-hour timestamp — not the fabrication pattern
            {"barcode": "7290001001", "source": "yohananof",
             "scraped_at": "2026-06-07T10:00:00",
             "nutrition": {"energy_kcal_raw": "350", "fat_raw": "27"}},
            {"barcode": "7290001002", "source": "yohananof",
             "scraped_at": "2026-06-07T10:22:11",
             "nutrition": {"energy_kcal_raw": "380", "fat_raw": "30"}},
        ]
        result = validate_no_fabrication(records)
        # Should be PASS or WARN (single-source) but NOT FAIL
        self.assertNotEqual(result["status"], "FAIL",
                            f"Single round-hour should not be FAIL, got {result}")


# ── Test 3: NOVA leakage detected ─────────────────────────────────────────────

class TestNovaLeakageDetected(unittest.TestCase):
    """positiveSignals containing 'NOVA 1 — מיץ סחוט טרי' → FAIL."""

    def _write_frontend_json(self, products: list[dict]) -> str:
        """Write a temp frontend JSON file and return its path."""
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump({"products": products}, fh, ensure_ascii=False)
        fh.close()
        return fh.name

    def test_nova_leakage_detected(self):
        """NOVA framework term in positiveSignals → FAIL."""
        products = [
            {
                "id": "j-001",
                "barcode": "7290001001",
                "imageUrl": "https://example.com/j001.jpg",
                "positiveSignals": ["NOVA 1 — מיץ סחוט טרי", "ללא סוכר מוסף"],
                "limitingFactors": [],
                "insightLine": "מיץ טבעי ב-100%",
            },
            {
                "id": "j-002",
                "barcode": "7290001002",
                "imageUrl": "https://example.com/j002.jpg",
                "positiveSignals": ["ללא חומרים משמרים"],
                "limitingFactors": [],
                "insightLine": "מיץ תפוחים טבעי",
            },
        ]
        path = self._write_frontend_json(products)
        try:
            result = validate_consumer_output(path)
            self.assertEqual(result["status"], "FAIL",
                             f"Expected FAIL for NOVA leakage, got {result}")
            self.assertTrue(any("FRAMEWORK_LEAKAGE" in m for m in result["messages"]),
                            f"Expected FRAMEWORK_LEAKAGE message: {result['messages']}")
            self.assertTrue(any("NOVA" in m for m in result["messages"]),
                            f"Expected 'NOVA' in messages: {result['messages']}")
        finally:
            os.unlink(path)

    def test_bsip_term_in_insightline_detected(self):
        """'BSIP' in insightLine → FAIL."""
        products = [
            {
                "id": "j-003",
                "barcode": "7290001003",
                "imageUrl": "https://example.com/j003.jpg",
                "positiveSignals": ["ללא סוכר מוסף"],
                "limitingFactors": [],
                "insightLine": "BSIP score: high matrix_integrity",
            },
        ]
        path = self._write_frontend_json(products)
        try:
            result = validate_consumer_output(path)
            self.assertEqual(result["status"], "FAIL",
                             f"Expected FAIL for BSIP in insightLine, got {result}")
        finally:
            os.unlink(path)


# ── Test 4: Clean consumer output passes ──────────────────────────────────────

class TestCleanConsumerOutputPasses(unittest.TestCase):
    """Valid positiveSignals with no forbidden terms → PASS."""

    def _write_frontend_json(self, products: list[dict]) -> str:
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump({"products": products}, fh, ensure_ascii=False)
        fh.close()
        return fh.name

    def test_clean_consumer_output_passes(self):
        """No forbidden terms, adequate imageUrls, short ingredients → PASS."""
        products = [
            {
                "id": "j-001",
                "barcode": "7290001001",
                "imageUrl": "https://example.com/j001.jpg",
                "positiveSignals": ["100% מיץ פרי טבעי", "ללא חומרים משמרים"],
                "limitingFactors": ["סוכר טבעי גבוה"],
                "insightLine": "מיץ תפוחים טהור — בחירה טובה לאנשים פעילים",
                "expansion": {
                    "ingredients": "תפוחים סחוטים טריים"
                },
            },
            {
                "id": "j-002",
                "barcode": "7290001002",
                "imageUrl": "https://example.com/j002.jpg",
                "positiveSignals": ["ויטמין C טבעי"],
                "limitingFactors": [],
                "insightLine": "מיץ תפוזים סחוט",
                "expansion": {
                    "ingredients": "תפוזים"
                },
            },
        ]
        path = self._write_frontend_json(products)
        try:
            result = validate_consumer_output(path)
            self.assertEqual(result["status"], "PASS",
                             f"Expected PASS for clean output, got {result}")
        finally:
            os.unlink(path)

    def test_null_imageurls_warns_not_fails(self):
        """null imageUrl rate > 50% → WARN, not FAIL (when no other violations)."""
        products = [
            {
                "id": f"j-{i:03d}",
                "barcode": f"729000100{i}",
                "imageUrl": None,
                "positiveSignals": ["ללא סוכר מוסף"],
                "limitingFactors": [],
                "insightLine": "מיץ טבעי",
            }
            for i in range(6)
        ]
        path = self._write_frontend_json(products)
        try:
            result = validate_consumer_output(path)
            self.assertEqual(result["status"], "WARN",
                             f"Expected WARN for high null imageUrl rate, got {result}")
            self.assertTrue(any("IMAGE_NULL_RATE" in m for m in result["messages"]),
                            f"Expected IMAGE_NULL_RATE warning: {result['messages']}")
        finally:
            os.unlink(path)


# ── Test 5: Scope boundary rejects out-of-scope products ──────────────────────

class TestScopeBoundaryRejects(unittest.TestCase):
    """Oat drink in fruit juice run → rejected with reason."""

    POSITIVE_TYPES = ["מיץ", "juice", "פרי", "לימון", "תפוח", "תפוז"]
    NEGATIVE_TYPES = ["סויה", "שיבולת שועל", "עגבנייה", "קפה", "חלב", "אבקה"]

    def test_oat_drink_rejected(self):
        """שיבולת שועל (oat) drink is in negative_types → rejected with reason."""
        products = [
            {"barcode": "7290001001", "name_he": "מיץ תפוחים טבעי 100%"},
            {"barcode": "7290001002", "name_he": "מיץ תפוזים סחוט"},
            {"barcode": "7290001003", "name_he": "משקה שיבולת שועל עם ויטמינים"},  # oat drink
            {"barcode": "7290001004", "name_he": "מיץ לימון טבעי"},
        ]
        result = validate_scope_boundaries(products, self.POSITIVE_TYPES, self.NEGATIVE_TYPES)
        self.assertEqual(result["status"], "FAIL",
                         f"Expected FAIL when oat drink present, got {result['status']}")
        self.assertEqual(len(result["rejected"]), 1,
                         f"Expected 1 rejected product, got {result['rejected']}")
        rejected_barcode = "7290001003"
        self.assertIn(rejected_barcode, result["rejection_reasons"],
                      f"Expected barcode {rejected_barcode} in rejection_reasons")
        reason = result["rejection_reasons"][rejected_barcode]
        self.assertIn("SCOPE_FAIL", reason, f"Expected SCOPE_FAIL in reason: {reason}")
        self.assertEqual(len(result["passed"]), 3,
                         f"Expected 3 passed products")

    def test_soy_and_tomato_both_rejected(self):
        """Multiple out-of-scope products are each rejected with their own reason."""
        products = [
            {"barcode": "7290001001", "name_he": "מיץ תפוחים"},
            {"barcode": "7290001002", "name_he": "משקה סויה וניל"},        # soy
            {"barcode": "7290001003", "name_he": "מיץ עגבנייה קר"},         # tomato
            {"barcode": "7290001004", "name_he": "קפה קר עם חלב"},          # coffee
        ]
        result = validate_scope_boundaries(products, self.POSITIVE_TYPES, self.NEGATIVE_TYPES)
        self.assertEqual(result["status"], "FAIL")
        # tomato has both a positive hit ("מיץ") and a negative hit ("עגבנייה")
        # negative takes priority — 3 should be rejected
        self.assertEqual(len(result["passed"]), 1,
                         f"Expected only the apple juice to pass, got: "
                         f"{[p['name_he'] for p in result['passed']]}")
        self.assertEqual(len(result["rejected"]), 3)

    def test_all_valid_products_pass(self):
        """When all products are in scope, result is PASS and rejected list is empty."""
        products = [
            {"barcode": "7290001001", "name_he": "מיץ תפוחים"},
            {"barcode": "7290001002", "name_he": "מיץ תפוזים"},
            {"barcode": "7290001003", "name_he": "מיץ אשכולית"},
        ]
        result = validate_scope_boundaries(products, self.POSITIVE_TYPES, self.NEGATIVE_TYPES)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(result["rejected"]), 0)
        self.assertEqual(len(result["passed"]), 3)


# ── Test 6: GateSelfPassError raised on unresolved FAILs ─────────────────────

class TestGateSelfPassRaises(unittest.TestCase):
    """GateSelfPassError must be raised when gate has unresolved FAILs."""

    def test_gate_self_pass_raises_on_fabrication_fail(self):
        """run_full_gate raises GateSelfPassError when fabrication is detected."""
        from bsip0_qa_validator import run_full_gate

        # 4 products with round-hour timestamps across 2 retailers + identical nutrition
        identical_nutrition = {
            "energy_kcal_raw": "420",
            "fat_raw": "32.0",
            "protein_raw": "26.0",
            "carbs_raw": "0.0",
        }
        records = [
            {"barcode": "7290001001", "source": "yohananof",
             "scraped_at": "2026-06-07T09:00:00", "nutrition": dict(identical_nutrition)},
            {"barcode": "7290001002", "source": "shufersal",
             "scraped_at": "2026-06-07T10:00:00", "nutrition": dict(identical_nutrition)},
            {"barcode": "7290001003", "source": "yohananof",
             "scraped_at": "2026-06-07T11:00:00", "nutrition": dict(identical_nutrition)},
            {"barcode": "7290001004", "source": "carrefour",
             "scraped_at": "2026-06-07T12:00:00", "nutrition": dict(identical_nutrition)},
        ]
        valid_summary = {
            "scrape_success_rate": 1.0,
            "source_verified": True,
            "null_imageUrl_rate": 0.0,
            "scope_rejected_count": 0,
            "portal_availability": {"https://yochananof.co.il": "UP"},
        }
        with self.assertRaises(GateSelfPassError) as ctx:
            run_full_gate(records, valid_summary)

        exc = ctx.exception
        self.assertIsInstance(exc.unresolved_fails, list,
                              "GateSelfPassError.unresolved_fails must be a list")
        self.assertGreater(len(exc.unresolved_fails), 0,
                           "GateSelfPassError must carry the unresolved FAILs")
        self.assertIn("FAIL", str(exc),
                      f"Exception message should mention FAIL: {exc}")

    def test_gate_self_pass_raises_on_summary_fail(self):
        """GateSelfPassError raised when run summary has missing required fields."""
        from bsip0_qa_validator import run_full_gate

        clean_records = [
            {"barcode": "7290001001", "source": "yohananof",
             "scraped_at": "2026-06-07T10:14:37",
             "nutrition": {"energy_kcal_raw": "350", "fat_raw": "27"}},
        ]
        # Missing required fields in summary
        incomplete_summary = {
            "scrape_success_rate": 0.90,
            # missing: source_verified, null_imageUrl_rate, scope_rejected_count, portal_availability
        }
        with self.assertRaises(GateSelfPassError):
            run_full_gate(clean_records, incomplete_summary)

    def test_clean_gate_does_not_raise(self):
        """run_full_gate does NOT raise when all checks pass."""
        from bsip0_qa_validator import run_full_gate

        clean_records = [
            {"barcode": "7290001001", "source": "yohananof",
             "scraped_at": "2026-06-07T10:14:37",
             "nutrition": {"energy_kcal_raw": "350", "fat_raw": "27", "protein_raw": "22", "carbs_raw": "3"}},
            {"barcode": "7290001002", "source": "yohananof",
             "scraped_at": "2026-06-07T10:22:11",
             "nutrition": {"energy_kcal_raw": "380", "fat_raw": "30", "protein_raw": "25", "carbs_raw": "2"}},
        ]
        clean_summary = {
            "scrape_success_rate": 1.0,
            "source_verified": True,
            "null_imageUrl_rate": 0.0,
            "scope_rejected_count": 0,
            "portal_availability": {"https://yochananof.co.il": "UP"},
        }
        # Should not raise
        try:
            result = run_full_gate(clean_records, clean_summary)
            self.assertIn(result["overall_status"], ("PASS", "WARN"))
        except GateSelfPassError as e:
            self.fail(f"run_full_gate raised GateSelfPassError unexpectedly: {e}")


# ── Additional edge-case tests ─────────────────────────────────────────────────

class TestVerifyProductIdentity(unittest.TestCase):
    """Check 3: product page identity verification."""

    def test_barcode_match_passes(self):
        result = verify_product_identity("7290001001", "7290001001", "גבינה צהובה", [])
        self.assertEqual(result["status"], "PASS")

    def test_barcode_mismatch_and_no_keywords_fails(self):
        result = verify_product_identity("7290001999", "7290001001", "קשקבל 31%", [])
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("IDENTITY" in m for m in result["messages"]))

    def test_keyword_match_passes_when_barcode_absent(self):
        result = verify_product_identity(None, "7290001001", "Baby Bel גבינה עגולה",
                                         ["baby bel"])
        self.assertEqual(result["status"], "PASS")

    def test_wrong_card_fails(self):
        """Simulates the hc-030 failure: scraper captured adjacent product."""
        result = verify_product_identity(
            "7290001999",  # wrong barcode
            "7290001001",  # target barcode
            "קשקבל 31% שומן גבינה קשה",  # wrong product name
            ["baby bel", "בייבי בל"],  # keywords for Baby Bell
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("IDENTITY_MISMATCH" in m for m in result["messages"]))


class TestValidateRunSummary(unittest.TestCase):
    """Check 6: run summary mandatory fields."""

    def test_complete_summary_passes(self):
        summary = {
            "scrape_success_rate": 0.85,
            "source_verified": True,
            "null_imageUrl_rate": 0.10,
            "scope_rejected_count": 2,
            "portal_availability": {"https://yochananof.co.il": "UP"},
        }
        result = validate_run_summary(summary)
        self.assertEqual(result["status"], "PASS")

    def test_missing_fields_fails(self):
        summary = {"scrape_success_rate": 0.85}
        result = validate_run_summary(summary)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("MISSING_FIELDS" in m for m in result["messages"]))

    def test_low_scrape_rate_fails(self):
        summary = {
            "scrape_success_rate": 0.50,  # below 0.70 threshold
            "source_verified": True,
            "null_imageUrl_rate": 0.05,
            "scope_rejected_count": 0,
            "portal_availability": {},
        }
        result = validate_run_summary(summary)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("SCRAPE_RATE_FAIL" in m for m in result["messages"]))

    def test_source_unverified_fails(self):
        summary = {
            "scrape_success_rate": 0.90,
            "source_verified": False,
            "null_imageUrl_rate": 0.05,
            "scope_rejected_count": 0,
            "portal_availability": {},
        }
        result = validate_run_summary(summary)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("SOURCE_UNVERIFIED" in m for m in result["messages"]))


# ── Entry point for running without pytest ────────────────────────────────────

if __name__ == "__main__":
    import sys
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test_class in [
        TestFabricationDetected,
        TestCleanInputPasses,
        TestNovaLeakageDetected,
        TestCleanConsumerOutputPasses,
        TestScopeBoundaryRejects,
        TestGateSelfPassRaises,
        TestVerifyProductIdentity,
        TestValidateRunSummary,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
