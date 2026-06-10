"""
EV-006 Regression Test Runner — functional fiber scoring validation.

Tests:
  1. _detect_functional_fiber signal extraction (12 fixture products)
  2. _score_glycemic_quality_sprint1 capped bonus integration
  3. score_satiety_support capped bonus integration
  4. Score-drift validation (zero drift for clean products)
"""
import sys, pathlib, io
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from signal_extractor import _detect_functional_fiber
from score_engine import _score_glycemic_quality_sprint1, score_satiety_support
from constants import FIBER_FUNCTIONAL_BONUS

PASS = "PASS"; FAIL = "FAIL"

# ===========================================================================
# Part 1: Signal extraction tests (12 fixture products)
# ===========================================================================
print("=" * 72)
print("EV-006 Regression — Signal Extraction (12 fixtures)")
print("=" * 72)

signal_fixtures = [
    # (name, ingredient_text, expected_type, expected_viscous, expected_prebiotic, notes)
    (
        "1. Oat beta-glucan product",
        "שיבולת שועל, בטא גלוקן, מים, מלח",
        "viscous", True, False,
        "Oatmeal with beta-glucan → viscous",
    ),
    (
        "2. Psyllium bread",
        "קמח חיטה מלא, מים, קליפת פסיליום, שמרים, מלח",
        "viscous", True, False,
        "Bread with psyllium husk → viscous",
    ),
    (
        "3. Inulin-fortified protein bar",
        "שיבולת שועל, חלבון אפונה, אינולין, חמאת אגוזים, מלח ים",
        "prebiotic", False, True,
        "Bar with inulin → prebiotic only",
    ),
    (
        "4. Resistant dextrin drink",
        "מים, מלטודקסטרין עמיד, חומצה לימונית, טעם טבעי",
        "prebiotic", False, True,
        "Resistant maltodextrin with qualifier → prebiotic",
    ),
    (
        "5. Mixed viscous + prebiotic",
        "שיבולת שועל, בטא גלוקן, אינולין, פקטין, מים",
        "both", True, True,
        "Oat beta-glucan + inulin + pectin → both viscous and prebiotic",
    ),
    (
        "6. Control — no functional fiber (fiber from whole grain only)",
        "קמח חיטה מלא, מים, שמן זית, מלח",
        "none", False, False,
        "Whole wheat flour provides fiber but no functional fiber vocab match",
    ),
    (
        "7. PHGG product — no viscosity credit",
        "חלבון אפונה, גואר מפורק חלקית, ממתיק טבעי, טעם",
        "prebiotic", False, True,
        "PHGG → prebiotic, native guar suppressed",
    ),
    (
        "8. Bare maltodextrin — excluded",
        "מלטודקסטרין, שמן צמחי, מלח, חומרים משמרים",
        "none", False, False,
        "Bare maltodextrin without resistance qualifier → excluded",
    ),
    (
        "9. Bare dextrin — excluded",
        "דקסטרין, חומרים מתחלבים, מלח",
        "none", False, False,
        "Bare dextrin without resistance qualifier → excluded",
    ),
    (
        "10. Zero declared fiber with functional fiber term",
        "חלב, בטא גלוקן, טעם טבעי",
        "viscous", True, False,
        "Beta-glucan detected in ingredients despite 0g declared fiber → viscous",
    ),
    (
        "11. Non-cereal beta-glucan (yeast) — suppressed",
        "שמרים, בטא גלוקן, מים",
        "none", False, False,
        "Yeast beta-glucan is immune-modulating, not viscous → suppressed",
    ),
    (
        "12. Native guar without PHGG — viscous",
        "מים, גואר, חומרים משמרים, מלח",
        "viscous", True, False,
        "Native guar without PHGG markers → viscous",
    ),
]

signal_passed = 0; signal_failed = 0
for name, text, exp_type, exp_visc, exp_preb, notes in signal_fixtures:
    result = _detect_functional_fiber(text)
    checks = []
    # Check fiber type
    r_type = result["functional_fiber_type"]
    if r_type == exp_type:
        checks.append(f"type={exp_type}")
    else:
        checks.append(f"TYPE FAIL: got '{r_type}' expected '{exp_type}'")
    # Check viscous flag
    has_visc = len(result["functional_fiber_viscous_terms"]) > 0
    if has_visc == exp_visc:
        checks.append(f"viscous={exp_visc}")
    else:
        checks.append(f"VISCOUS FAIL: got {has_visc} expected {exp_visc}")
    # Check prebiotic flag
    has_preb = len(result["functional_fiber_prebiotic_terms"]) > 0
    if has_preb == exp_preb:
        checks.append(f"prebiotic={exp_preb}")
    else:
        checks.append(f"PREBIOTIC FAIL: got {has_preb} expected {exp_preb}")
    # Check detected boolean
    detected = result["functional_fiber_detected"]
    exp_detected = exp_type != "none"
    if detected == exp_detected:
        checks.append(f"detected={exp_detected}")
    else:
        checks.append(f"DETECTED FAIL: got {detected} expected {exp_detected}")
    # Check terms
    matched = result.get("functional_fiber_terms_matched", [])
    terms_ok = (len(matched) > 0) == exp_detected
    checks.append(f"terms={len(matched)}")

    ok = all("FAIL" not in c for c in checks)
    status = PASS if ok else FAIL
    if ok: signal_passed += 1
    else: signal_failed += 1
    mark = "+" if ok else "!"
    print(f"  [{mark}] {name}")
    for c in checks:
        print(f"         {c}")
    if ok:
        visc_terms = result.get("functional_fiber_viscous_terms", [])
        preb_terms = result.get("functional_fiber_prebiotic_terms", [])
        print(f"         viscous_terms={visc_terms} prebiotic_terms={preb_terms}")

print(f"\n  Signals: {signal_passed} passed, {signal_failed} failed out of {len(signal_fixtures)}")

# ===========================================================================
# Part 2: Dimension scoring tests — glycemic_quality bonus
# ===========================================================================
print("\n" + "=" * 72)
print("EV-006 Regression — Dimension Scoring (glycemic_quality + satiety)")
print("=" * 72)

# Build l3 dicts for each scenario
fixture_l3 = []
for name, text, exp_type, exp_visc, exp_preb, notes in signal_fixtures:
    ff = _detect_functional_fiber(text)
    fixture_l3.append({
        "name": name.replace("1. ", "").replace("2. ", "").replace("3. ", "").replace("4. ", "").replace("5. ", "").replace("6. ", "").replace("7. ", "").replace("8. ", "").replace("9. ", "").replace("10. ", "").replace("11. ", "").replace("12. ", ""),
        "l3": {
            "functional_fiber_detected": ff["functional_fiber_detected"],
            "functional_fiber_type": ff["functional_fiber_type"],
            "functional_fiber_terms_matched": ff["functional_fiber_terms_matched"],
            "functional_fiber_viscous_terms": ff["functional_fiber_viscous_terms"],
            "functional_fiber_prebiotic_terms": ff["functional_fiber_prebiotic_terms"],
            "has_whole_grain": "חיטה מלא" in text or "שיבולת שועל" in text,
            "sprint1_allulose_detected": False,
            "sweetener_tier": None,
        },
        "nn": {},  # will be filled per test
        "exp_type": exp_type,
    })

# --- glycemic_quality tests ---
gq_passed = 0; gq_failed = 0

# Each test: (nn, expected_bonus, description)
gq_tests = [
    # Fixture 1: Oat beta-glucan, fiber=3g → viscous bonus +2
    (1, {"sugars_g": 5, "dietary_fiber_g": 3},
     2, "viscous glycemic bonus = +2"),
    # Fixture 2: Psyllium bread, fiber=6g → viscous bonus +2
    (2, {"sugars_g": 2, "dietary_fiber_g": 6},
     2, "viscous glycemic bonus = +2"),
    # Fixture 3: Inulin bar, fiber=8g → prebiotic bonus +1
    (3, {"sugars_g": 12, "dietary_fiber_g": 8},
     1, "prebiotic glycemic bonus = +1"),
    # Fixture 4: Resistant dextrin drink, fiber=0g → prebiotic bonus +1
    (4, {"sugars_g": 0, "dietary_fiber_g": 0},
     1, "prebiotic glycemic bonus = +1 (0g fiber, ingredient-presence only)"),
    # Fixture 5: Mixed viscous + prebiotic → both: 2+1=3 capped to 2
    (5, {"sugars_g": 8, "dietary_fiber_g": 5},
     2, "both: viscous(2)+prebiotic(1)=3 capped to 2"),
    # Fixture 6: Control, fiber=4g → no bonus
    (6, {"sugars_g": 3, "dietary_fiber_g": 4},
     0, "no functional fiber → bonus=0"),
    # Fixture 7: PHGG → prebiotic only (guar suppressed) → +1
    (7, {"sugars_g": 2, "dietary_fiber_g": 2},
     1, "PHGG prebiotic glycemic bonus = +1"),
    # Fixture 8: Bare maltodextrin → none → +0
    (8, {"sugars_g": 10, "dietary_fiber_g": 0},
     0, "bare maltodextrin → no bonus"),
    # Fixture 9: Bare dextrin → none → +0
    (9, {"sugars_g": 5, "dietary_fiber_g": 0},
     0, "bare dextrin → no bonus"),
    # Fixture 10: 0g fiber + beta-glucan → viscous +2 (ingredient-presence)
    (10, {"sugars_g": 3, "dietary_fiber_g": 0},
     2, "0g fiber + beta-glucan → viscous bonus +2 (ingredient-presence)"),
    # Fixture 11: Yeast beta-glucan → suppressed → +0
    (11, {"sugars_g": 1, "dietary_fiber_g": 0},
     0, "yeast beta-glucan → suppressed → no bonus"),
    # Fixture 12: Native guar → viscous +2
    (12, {"sugars_g": 4, "dietary_fiber_g": 1},
     2, "native guar → viscous bonus +2"),
]

print("\n--- glycemic_quality bonus ---")
for fix_idx, nn, exp_bonus, desc in gq_tests:
    entry = fixture_l3[fix_idx - 1]
    l3 = entry["l3"].copy()
    # Use the full nn dict
    score_orig, note_orig = _score_glycemic_quality_sprint1(nn, {**l3, **{k: l3.get(k) for k in ["has_whole_grain", "sprint1_allulose_detected", "sweetener_tier"]}})
    # Also compute without EV-006:
    l3_no_ev006 = {k: v for k, v in l3.items() if not k.startswith("functional_fiber")}
    l3_no_ev006["has_whole_grain"] = l3.get("has_whole_grain", False)
    l3_no_ev006["sprint1_allulose_detected"] = l3.get("sprint1_allulose_detected", False)
    l3_no_ev006["sweetener_tier"] = l3.get("sweetener_tier")
    score_base, note_base = _score_glycemic_quality_sprint1(nn, l3_no_ev006)

    actual_bonus = round(score_orig - score_base, 1)
    # Account for ceiling clamp: if base is at 100, bonus may not be visible
    expected_visible = min(exp_bonus, max(0, 100 - score_base))
    checks = []
    if actual_bonus == expected_visible:
        checks.append(f"bonus={expected_visible}")
        if expected_visible < exp_bonus and score_base >= 100:
            checks.append(f"(base at ceiling, {exp_bonus - expected_visible} pts clamped)")
    else:
        checks.append(f"BONUS FAIL: got +{actual_bonus} expected +{expected_visible} (base={score_base})")
    # Check that trace note contains EV-006
    if exp_bonus > 0:
        if "EV-006" in note_orig:
            checks.append("trace has EV-006")
        else:
            checks.append("TRACE FAIL: no EV-006 in note")
    ok = all("FAIL" not in c for c in checks)
    status = PASS if ok else FAIL
    if ok: gq_passed += 1
    else: gq_failed += 1
    mark = "+" if ok else "!"
    short = entry["name"]
    print(f"  [{mark}] Fixture {fix_idx}: {short}")
    for c in checks:
        print(f"         {c}")
    print(f"         base={score_base} → with_bonus={score_orig} ({desc})")

print(f"\n  glycemic_quality: {gq_passed} passed, {gq_failed} failed out of {len(gq_tests)}")

# --- satiety_support tests ---
ss_passed = 0; ss_failed = 0

ss_tests = [
    (1, {"protein_g": 8, "dietary_fiber_g": 3, "energy_kcal": 180},
     2, "viscous satiety bonus = +2"),
    (2, {"protein_g": 6, "dietary_fiber_g": 6, "energy_kcal": 200},
     2, "viscous satiety bonus = +2"),
    (3, {"protein_g": 15, "dietary_fiber_g": 8, "energy_kcal": 220},
     1, "prebiotic satiety bonus = +1"),
    (4, {"protein_g": 0, "dietary_fiber_g": 0, "energy_kcal": 50},
     1, "prebiotic satiety bonus = +1 (0g fiber)"),
    (5, {"protein_g": 10, "dietary_fiber_g": 5, "energy_kcal": 200},
     2, "both: viscous(2)+prebiotic(1)=3 capped to 2"),
    (6, {"protein_g": 5, "dietary_fiber_g": 4, "energy_kcal": 150},
     0, "no functional fiber → bonus=0"),
    (7, {"protein_g": 12, "dietary_fiber_g": 2, "energy_kcal": 180},
     1, "PHGG prebiotic satiety bonus = +1"),
    (8, {"protein_g": 2, "dietary_fiber_g": 0, "energy_kcal": 100},
     0, "bare maltodextrin → no bonus"),
    (9, {"protein_g": 3, "dietary_fiber_g": 0, "energy_kcal": 120},
     0, "bare dextrin → no bonus"),
    (10, {"protein_g": 4, "dietary_fiber_g": 0, "energy_kcal": 80},
     2, "0g fiber + beta-glucan → viscous bonus +2"),
    (11, {"protein_g": 1, "dietary_fiber_g": 0, "energy_kcal": 60},
     0, "yeast beta-glucan → suppressed → no bonus"),
    (12, {"protein_g": 3, "dietary_fiber_g": 1, "energy_kcal": 90},
     2, "native guar → viscous bonus +2"),
]

print("\n--- satiety_support bonus ---")
for fix_idx, nn, exp_bonus, desc in ss_tests:
    entry = fixture_l3[fix_idx - 1]
    l3 = entry["l3"]

    score_orig, note_orig = score_satiety_support(nn, l3)
    score_base, note_base = score_satiety_support(nn, None)

    actual_bonus = round(score_orig - score_base, 1)
    # Account for ceiling clamp: if base is at 100, bonus may not be visible
    expected_visible = min(exp_bonus, max(0, 100 - score_base))
    checks = []
    if actual_bonus == expected_visible:
        checks.append(f"bonus={expected_visible}")
        if expected_visible < exp_bonus and score_base >= 100:
            checks.append(f"(base at ceiling, {exp_bonus - expected_visible} pts clamped)")
    else:
        checks.append(f"BONUS FAIL: got +{actual_bonus} expected +{expected_visible} (base={score_base})")
    if exp_bonus > 0:
        if "EV-006" in note_orig:
            checks.append("trace has EV-006")
        else:
            checks.append("TRACE FAIL: no EV-006 in note")
    ok = all("FAIL" not in c for c in checks)
    status = PASS if ok else FAIL
    if ok: ss_passed += 1
    else: ss_failed += 1
    mark = "+" if ok else "!"
    short = entry["name"]
    print(f"  [{mark}] Fixture {fix_idx}: {short}")
    for c in checks:
        print(f"         {c}")
    print(f"         base={score_base} → with_bonus={score_orig} ({desc})")

print(f"\n  satiety_support: {ss_passed} passed, {ss_failed} failed out of {len(ss_tests)}")


# ===========================================================================
# Part 3: Score-drift validation
# ===========================================================================
print("\n" + "=" * 72)
print("EV-006 Score-Drift Validation")
print("=" * 72)

# Zero-drift check: products with no functional fiber should have identical scores
drift_passed = 0; drift_failed = 0

for fix_idx, nn, exp_bonus, desc in gq_tests:
    entry = fixture_l3[fix_idx - 1]
    l3 = entry["l3"]
    if not l3.get("functional_fiber_detected", False):
        # Double-check: score should be identical with/without l3 fiber data
        # (because the bonus is 0 when no fiber is detected)
        score_with, note_with = _score_glycemic_quality_sprint1(nn, l3)
        l3_clean = {k: v for k, v in l3.items() if not k.startswith("functional_fiber")}
        l3_clean["has_whole_grain"] = l3.get("has_whole_grain", False)
        l3_clean["sprint1_allulose_detected"] = l3.get("sprint1_allulose_detected", False)
        l3_clean["sweetener_tier"] = l3.get("sweetener_tier")
        score_clean, _ = _score_glycemic_quality_sprint1(nn, l3_clean)
        if score_with == score_clean:
            drift_passed += 1
        else:
            drift_failed += 1
            print(f"  [!] DRIFT: fixture {fix_idx} ({entry['name']}) "
                  f"score drifted {score_clean}→{score_with} despite no functional fiber detected")

print(f"\n  Score-drift: {drift_passed} zero-drift checks passed, {drift_failed} failed")

# ===========================================================================
# Summary
# ===========================================================================
print("\n" + "=" * 72)
print("EV-006 Regression Summary")
print("=" * 72)
total_pass = signal_passed + gq_passed + ss_passed + drift_passed
total_fail = signal_failed + gq_failed + ss_failed + drift_failed
total = len(signal_fixtures) + len(gq_tests) + len(ss_tests) + (drift_passed + drift_failed)
print(f"  Signals:              {signal_passed:3d} / {len(signal_fixtures):3d}  ({signal_failed} failed)")
print(f"  glycemic_quality:     {gq_passed:3d} / {len(gq_tests):3d}  ({gq_failed} failed)")
print(f"  satiety_support:      {ss_passed:3d} / {len(ss_tests):3d}  ({ss_failed} failed)")
print(f"  Score-drift:          {drift_passed:3d} zero-drift checks ({drift_failed} drifted)")
print(f"  {'─' * 42}")
print(f"  TOTAL:                {total_pass:3d} / {total:3d}  ({total_fail} failed)")
print(f"  {'─' * 42}")

if total_fail > 0:
    print(f"\n  RESULT: {FAIL}")
    sys.exit(1)
else:
    print(f"\n  RESULT: {PASS}")
    sys.exit(0)
