"""
Regression tests for TASK-249 corpus-remediation fixes in 02_build_bsip1_yogurt_006.py.

RT-2: disclaimer_strip  — contaminated fixture is cleaned, clean fixture is unchanged.
RT-1: macros_plausible  — protein=190 blocked; normal protein passes.
RT-3: cereal_misroute   — barcode 7290112346797 is excluded.
RT-5: E414 detection    — "חומר הזגה (E414)" is detected as additive.
RT-12: live cultures    — Activia culture phrase triggers has_live_cultures=True.

Run with:
    python test_bsip1_yogurt_006_fixes.py
Exit 0 = all pass.  Exit 1 = failures found.
"""
from __future__ import annotations
import sys
import io
import pathlib
import importlib

# Force UTF-8 output on Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── path setup ────────────────────────────────────────────────────────────────
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                              # 02_build_bsip1_yogurt_006
sys.path.insert(0, str(HERE.parent.parent.parent /
                        "bsip1" / "core"))                 # ingredient_enricher
sys.path.insert(0, str(HERE.parent / "_shared"))           # bsip0_nutrition

# Import the module under test
import importlib.util
spec = importlib.util.spec_from_file_location(
    "builder_006", str(HERE / "02_build_bsip1_yogurt_006.py"))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}" + (f": {detail}" if detail else ""))
        failures.append(name)


# ────────────────────────────────────────────────────────────────────────────
# RT-2: Disclaimer strip
# ────────────────────────────────────────────────────────────────────────────
print("\n[RT-2] Disclaimer strip")

# Fixture 1: Real contaminated text from barcode 7290116932620
contaminated = (
    "רכיבי חלב (54%) , חלב, אבקת חלב. n25 גרם חלבון בגביע , מתוכם11.5   גרם "
    "חלבוני מי גבינה , 13.5 גרם קזאין מכיל חלב ערכים תזונתיים 100 גרם 86 קל "
    "אנרגיה 190 גרם חלבונים 4.4 גרם פחמימות 2 גרם שומנים 72 מג נתרן הנתונים "
    "המדויקים מופיעים על גבי המוצר, אין להסתמך על הפירוט המופיע באתר"
)
clean, stripped = builder._strip_disclaimer(contaminated)
check("RT-2.1 contaminated text is stripped",
      bool(stripped) and len(stripped) > 20,
      f"stripped={repr(stripped[:60])}")
check("RT-2.2 clean text contains real ingredient (קזאין)",
      "קזאין" in clean,
      f"clean={repr(clean[:120])}")
check("RT-2.3 'ערכים תזונתיים' not in clean",
      "ערכים תזונתיים" not in clean,
      f"clean={repr(clean[:200])}")
check("RT-2.4 '190 גרם חלבונים' not in clean",
      "190 גרם חלבונים" not in clean and "190" not in clean.split("קזאין")[-1],
      f"clean={repr(clean[-100:])}")

# Fixture 2: Activia Oat Plum (barcode 7290112346797) — should be clean after strip
activia_raw = (
    "חלב מפוסטר, שיבולת שועל מבושלת (שיבולת שועל, מים) (13.3%), מיץ שזיף (10.2%), "
    "רכיבי חלב, סוכר חום, סוכר, סיבים תזונתיים, רכז לימון, מלח, חומרי טעם וריח, "
    "בתוספת החיידק הפרביוטי ביפידוס אקטירגוליס. מכיל חלב ערכים תזונתיים 100 גרם "
    "1.2 גרם סיבים תזונתיים 8.9 גרם סוכרים מתוך פחמימות 89 קל אנרגיה 4.3 גרם חלבונים"
)
a_clean, a_stripped = builder._strip_disclaimer(activia_raw)
check("RT-2.5 Activia disclaimer stripped",
      bool(a_stripped),
      f"stripped={repr(a_stripped[:60])}")
check("RT-2.6 Activia clean keeps culture phrase",
      "ביפידוס" in a_clean or "אקטירגוליס" in a_clean,
      f"clean={repr(a_clean[-100:])}")

# Fixture 3: Clean product — no disclaimer — must not be touched
clean_product_ingr = "חלב מפוסטר, רכיבי חלב, מייצב (E415)"
cp_clean, cp_stripped = builder._strip_disclaimer(clean_product_ingr)
check("RT-2.7 clean product not modified",
      cp_stripped == "" and cp_clean == clean_product_ingr,
      f"clean={repr(cp_clean)}, stripped={repr(cp_stripped)}")

# Fixture 4: Danone Pro product with per-serving nutrition embedded
danone_raw = (
    "חלב מפוסטר, מים, חומרי טעם וריח, עמילן טפיוקה מעובד (E1442), מייצב "
    "(לוקוסט- בין גאם), ממתיקים (אצסולפאם K, סוכרלוז), רכז לימון, מלח,  "
    "מכיל חיידקי יוגורט. מאפיינים נוספים ללא תוספת סוכר מכיל חלב ערכים "
    "תזונתיים 100 גרם 3.2 גרם סוכרים"
)
d_clean, d_stripped = builder._strip_disclaimer(danone_raw)
check("RT-2.8 Danone Pro disclaimer stripped",
      bool(d_stripped),
      f"stripped={repr(d_stripped[:60])}")
check("RT-2.9 Danone clean keeps 'מכיל חיידקי יוגורט' or core ingredients",
      "חומרי טעם וריח" in d_clean or "חלב מפוסטר" in d_clean,
      f"clean={repr(d_clean[-100:])}")


# ────────────────────────────────────────────────────────────────────────────
# RT-1: macros_plausible gate
# ────────────────────────────────────────────────────────────────────────────
print("\n[RT-1] macros_plausible gate")

# Fixture: protein=190 (the actual corruption from barcode 7290116932620)
nn_corrupt = {
    "energy_kcal": 86.0, "protein_g": 190.0, "carbohydrates_g": 4.4,
    "fat_g": 2.0, "sugars_g": None, "fat_saturated_g": None,
    "sodium_mg": 72.0, "dietary_fiber_g": None,
}
ok, issues, corrected = builder._check_macros_plausible(nn_corrupt)
check("RT-1.1 protein=190 flagged as implausible",
      not ok,
      f"issues={issues}")
check("RT-1.2 protein_g nulled in corrected panel",
      corrected.get("protein_g") is None,
      f"corrected protein_g={corrected.get('protein_g')}")
check("RT-1.3 energy_kcal preserved (86 is plausible)",
      corrected.get("energy_kcal") == 86.0,
      f"energy_kcal={corrected.get('energy_kcal')}")

# Fixture: normal product — should pass
nn_normal = {
    "energy_kcal": 88.0, "protein_g": 10.5, "carbohydrates_g": 4.2,
    "fat_g": 3.5, "sugars_g": 3.0, "fat_saturated_g": None,
    "sodium_mg": 60.0, "dietary_fiber_g": None,
}
ok2, issues2, corrected2 = builder._check_macros_plausible(nn_normal)
check("RT-1.4 normal panel is plausible",
      ok2,
      f"issues={issues2}")
check("RT-1.5 protein_g unchanged in normal panel",
      corrected2.get("protein_g") == 10.5,
      f"protein_g={corrected2.get('protein_g')}")

# Fixture: protein=25 (high protein yogurt) — should pass
nn_high_protein = {
    "energy_kcal": 120.0, "protein_g": 25.0, "carbohydrates_g": 4.0,
    "fat_g": 0.5, "sugars_g": 2.0, "fat_saturated_g": None,
    "sodium_mg": 50.0, "dietary_fiber_g": None,
}
ok3, issues3, _ = builder._check_macros_plausible(nn_high_protein)
check("RT-1.6 protein=25 passes plausibility",
      ok3,
      f"issues={issues3}")


# ────────────────────────────────────────────────────────────────────────────
# RT-3: cereal misroute exclusion
# ────────────────────────────────────────────────────────────────────────────
print("\n[RT-3] Cereal misroute exclusion")

misroute_raw = {
    "name_he": "אקטיביה שיבולת שועל שזיף",
    "barcode": "7290112346797",
    "nutrition": {
        "energy_kcal_raw": "89", "protein_raw": "4.3",
        "carbs_raw": "10.7", "fat_raw": "2.5",
        "fiber_raw": "1.2", "sodium_raw": "68 מג",
        "sugar_raw": "8.9", "saturated_fat_raw": "",
    },
    "ingredients_raw": "חלב מפוסטר, שיבולת שועל...",
}
reason = builder._curate(misroute_raw)
check("RT-3.1 Activia Oat Plum excluded as cereal_misroute",
      reason == "cereal_misroute_excluded",
      f"reason={reason!r}")

# Confirm a different Activia (non-oat) is NOT excluded
activia_plain = {
    "name_he": "אקטיביה תות",
    "barcode": "7290112346798",
    "nutrition": {
        "energy_kcal_raw": "75", "protein_raw": "3.5",
        "carbs_raw": "9.0", "fat_raw": "1.5",
        "fiber_raw": "", "sodium_raw": "50 מג",
        "sugar_raw": "7.0", "saturated_fat_raw": "",
    },
    "ingredients_raw": "חלב מפוסטר, סוכר, בתוספת חיידקי יוגורט",
}
reason_ok = builder._curate(activia_plain)
check("RT-3.2 other Activia products not excluded by misroute rule",
      reason_ok is None,
      f"reason={reason_ok!r}")


# ────────────────────────────────────────────────────────────────────────────
# RT-5: E414 detection
# ────────────────────────────────────────────────────────────────────────────
print("\n[RT-5] E414 in parenthesized Hebrew phrases")

ingr_list_e414 = [
    "חלב מפוסטר",
    "חלבוני חלב",
    "שוקולד",
    "חומר הזגה (E414)",   # RT-5 target
    "לציטין סויה",
]
e_nums = builder._extract_e_numbers_from_parens(ingr_list_e414)
check("RT-5.1 E414 detected from '(E414)' pattern",
      "E414" in e_nums,
      f"found={e_nums}")

# Confirm ingredient_enricher.py now has E414
import ingredient_enricher
additive_terms_lower = [t[0].lower() for t in ingredient_enricher.ADDITIVE_TERMS]
check("RT-5.2 E414 in ADDITIVE_TERMS after fix",
      "e414" in additive_terms_lower,
      f"additive_terms sample={additive_terms_lower[:20]}")

# Test that the enricher detects E414 via substring match in ingredients text
record_e414 = {
    "ingredients_text_he": "חלב מפוסטר, חלבוני חלב, שוקולד, חומר הזגה (E414), לציטין סויה",
    "barcode": "test_e414",
}
enriched_e414 = ingredient_enricher.enrich(record_e414)
additive_terms_found = [a["term"] for a in enriched_e414.get("extracted_additives", [])]
check("RT-5.3 enricher detects E414 via substring match",
      "E414" in additive_terms_found or "חומר הזגה" in additive_terms_found,
      f"additives found={additive_terms_found}")
check("RT-5.4 additive_count > 0 after E414 detection",
      enriched_e414.get("enrichment_summary", {}).get("additive_count", 0) > 0,
      f"additive_count={enriched_e414.get('enrichment_summary', {}).get('additive_count')}")

# Control: ingredients WITHOUT E414 → additive_count should not increase
record_no_e414 = {
    "ingredients_text_he": "חלב מפוסטר, חלבוני חלב, תמצית וניל",
    "barcode": "test_no_e414",
}
enriched_no = ingredient_enricher.enrich(record_no_e414)
check("RT-5.5 no false positive for ingredients without E414",
      "E414" not in [a["term"] for a in enriched_no.get("extracted_additives", [])],
      f"additives={[a['term'] for a in enriched_no.get('extracted_additives', [])]}")


# ────────────────────────────────────────────────────────────────────────────
# RT-12: Live cultures detection
# ────────────────────────────────────────────────────────────────────────────
print("\n[RT-12] Live cultures detection")

# Check enricher detects "ביפידוס" in clean text
record_bifidus = {
    "ingredients_text_he": (
        "חלב מפוסטר, שיבולת שועל מבושלת (13.3%), מיץ שזיף (10.2%), "
        "בתוספת החיידק הפרביוטי ביפידוס אקטירגוליס"
    ),
    "barcode": "test_activia",
}
enriched_act = ingredient_enricher.enrich(record_bifidus)
check("RT-12.1 enricher detects ביפידוס as live culture",
      enriched_act.get("enrichment_summary", {}).get("has_live_cultures", False),
      f"ferment_markers={enriched_act.get('extracted_fermentation_markers', [])}")

# Check the RT-12 post-hoc correction in builder
mock_enrichment_false = {"has_live_cultures": False, "fermentation_marker_count": 0}
result = builder._has_cultures_fix("probiotic", mock_enrichment_false,
                                    "בתוספת החיידק הפרביוטי ביפידוס אקטירגוליס")
check("RT-12.2 _has_cultures_fix returns True for Activia culture phrase",
      result is True,
      f"result={result}")

# Check it does NOT incorrectly override for plain products
mock_enrichment_false2 = {"has_live_cultures": False, "fermentation_marker_count": 0}
result2 = builder._has_cultures_fix("plain_natural", mock_enrichment_false2,
                                     "חלב מפוסטר, סוכר, עמילן")
check("RT-12.3 _has_cultures_fix returns False for plain product without culture phrase",
      result2 is False,
      f"result={result2}")

# Check that new FERMENTATION_TERMS entries work
ferment_terms_lower = [t[0].lower() for t in ingredient_enricher.FERMENTATION_TERMS]
check("RT-12.4 'אקטירגוליס' in FERMENTATION_TERMS",
      "אקטירגוליס" in ferment_terms_lower,
      f"terms (sample)={ferment_terms_lower[:10]}")
check("RT-12.5 'החיידק הפרביוטי' in FERMENTATION_TERMS",
      "החיידק הפרביוטי" in ferment_terms_lower,
      f"terms (sample)={ferment_terms_lower[:10]}")


# ────────────────────────────────────────────────────────────────────────────
# Summary
# ────────────────────────────────────────────────────────────────────────────
print()
if failures:
    print(f"FAILED: {len(failures)} test(s): {failures}")
    sys.exit(1)
else:
    total = 5 + 3 + 4 + 5 + 2 + 6 + 2 + 5 + 3 + 5  # count above
    print(f"ALL TESTS PASS")
    sys.exit(0)
