# BSIP2-061 Pilot Re-Run Specification — v2

**Task:** TASK-051A  
**Owner:** Frontend Architect  
**Status:** Pending implementation  
**Prerequisite:** revised_signal_definition_bsip2_061.md (TASK-051A)  
**Pilot v1 baseline:** bsip2_061_pilot_results.md (TASK-051)

---

## Objective

Implement the three revisions from TASK-051A into `bsip2_061_water_predominance.py`, re-run the pilot against run_hummus_002, and measure whether the revised logic produces the expected activation profile:

- WATER_PREDOMINANT: ~4 products (low-percentage chickpea compound + standalone water)
- WATER_EARLY: ~13 products (functional at pos 1, water at pos 2, below concentration floor)
- No false positives on tahini-first products
- No WATER_PREDOMINANT on products where primary ingredient ≥ 70%

---

## Section 1 — Code Changes Required

All changes are confined to `bsip2_061_water_predominance.py`. No other files are modified.

### 1.1 Bump signal version

```python
# Line 16 — change
SIGNAL_VERSION = "pilot_v1"
# to
SIGNAL_VERSION = "pilot_v2"
```

### 1.2 Add percentage extraction constant

Add after the existing constants block (after `WFI_REDUCTION_EARLY`):

```python
import re

# Chickpea-percentage gate threshold (Trigger B)
CHICKPEA_PERCENTAGE_THRESHOLD = 45.0   # percent; ≤ this triggers WATER_PREDOMINANT

# Concentration floor — suppress WATER_EARLY when primary ingredient is dominant
CONCENTRATION_FLOOR_PCT = 70.0          # percent; ≥ this suppresses WATER_EARLY

# Regex for extracting the first declared percentage from an ingredient string
# Matches: "61%", "(61%)", "61.5%", "(44%)" etc.
_PCT_RE = re.compile(r"(\d+\.?\d*)%")
```

### 1.3 Add `_extract_percentage()` helper

Add after `_is_water_ingredient()`:

```python
def _extract_percentage(ingredient: str) -> float | None:
    """
    Extract the first declared percentage from an ingredient string.
    Returns None if no percentage is found.

    Handles formats:
      "חומוס מבושל 61% (מים, ...)"  → 61.0
      "חומוס מבושל (44%)"           → 44.0
      "חומוס מבושל 34% [מים, ...]"  → 34.0
      "חציל קלוי 72%"               → 72.0
    """
    m = _PCT_RE.search(ingredient)
    if m:
        return float(m.group(1))
    return None
```

### 1.4 Add Trigger B detection helper

Add after `_extract_percentage()`:

```python
def _is_chickpea_compound_below_threshold(ingredient: str) -> tuple[bool, float | None]:
    """
    Returns (fires, percentage) for Trigger B — the chickpea-percentage gate.

    Fires when:
    - ingredient starts with a chickpea term (cooked form)
    - AND the declared percentage is ≤ CHICKPEA_PERCENTAGE_THRESHOLD (45%)

    Returns (True, pct) if Trigger B fires, (False, pct_or_None) otherwise.
    """
    if not _ing_starts_with(ingredient, CHICKPEA_TERMS):
        return False, None
    pct = _extract_percentage(ingredient)
    if pct is None:
        # No declared percentage — Trigger B cannot fire; signal is ambiguous
        return False, None
    return pct <= CHICKPEA_PERCENTAGE_THRESHOLD, pct
```

### 1.5 Add concentration floor check helper

```python
def _concentration_floor_met(ingredient: str, ing_type: str) -> bool:
    """
    Returns True if the primary ingredient at position 1 has a declared
    percentage ≥ CONCENTRATION_FLOOR_PCT, suppressing WATER_EARLY.

    Only checks for types where a percentage is declared in this corpus
    (chickpea, eggplant, nut). Tahini products are handled by the
    tahini-first protection before reaching this check.
    """
    pct = _extract_percentage(ingredient)
    if pct is None:
        return False   # no declared percentage — floor cannot suppress signal
    return pct >= CONCENTRATION_FLOOR_PCT
```

### 1.6 Revise `evaluate_water_predominance()` — full replacement

Replace the existing function body with the revised logic. The function signature is unchanged.

```python
def evaluate_water_predominance(
    product: dict,
    category: str,
    wfi_score_current: float | None = None,
) -> dict:
    """
    BSIP2-061 v2 — Water Predominance signal evaluation.
    Implements revised logic per TASK-051A:
      - Trigger B: chickpea-percentage gate (new WATER_PREDOMINANT path)
      - Tahini-first protection (explicit)
      - Concentration floor (WATER_EARLY suppressed at ≥ 70%)
    """
    name_he     = product.get("canonical_name_he") or ""
    ingredients = list(product.get("ingredients_list") or [])

    # ------------------------------------------------------------------
    # Step 0 — Category hard exclusion
    # ------------------------------------------------------------------
    if category in EXCLUDED_CATEGORIES:
        return _result(
            state="NOT_EVALUABLE",
            note=f"category '{category}' is hard-excluded from BSIP2-061",
            water_pos=None, func_type="n/a", func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=False, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 1 — Ingredient list check
    # ------------------------------------------------------------------
    if len(ingredients) < 2:
        return _result(
            state="NOT_EVALUABLE",
            note="ingredient list absent or too short (< 2 items)",
            water_pos=None, func_type="unknown", func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=False, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 2 — Matbucha detection (manual review, no auto-score)
    # ------------------------------------------------------------------
    is_matbucha = _is_matbucha(name_he, ingredients)
    if is_matbucha:
        water_position = None
        for idx in (0, 1):
            if idx < len(ingredients) and _is_water_ingredient(ingredients[idx]):
                water_position = idx + 1
                break
        func_type, func_position = _detect_primary_functional_ingredient(
            ingredients, category_hint=category)
        return _result(
            state="MATBUCHA_MANUAL_REVIEW",
            note=(
                f"Matbucha product — manual review required before BSIP2-061 scoring. "
                f"water_position={water_position}, functional={func_type} at pos {func_position}. "
                f"Tomato natural water vs. added water is unresolvable from label alone."
            ),
            water_pos=water_position, func_type=func_type, func_pos=func_position,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=True, is_fp_candidate=True,
        )

    # ------------------------------------------------------------------
    # Step 3 — Tahini-first protection
    # If the first ingredient is tahini/sesame, treat tahini as primary.
    # Water between tahini (pos 1) and chickpeas (pos 3+) is architecturally
    # expected in tahini-dominant formulations — not a dilution signal.
    # ------------------------------------------------------------------
    first_ing = ingredients[0] if ingredients else ""
    first_is_tahini = _ing_starts_with(first_ing, TAHINI_TERMS)

    if first_is_tahini:
        # Tahini protection: check water at pos 2 → WATER_EARLY; else NOT_PREDOMINANT
        water_position = None
        if len(ingredients) > 1 and _is_water_ingredient(ingredients[1]):
            water_position = 2
        if water_position is None:
            return _result(
                state="NOT_PREDOMINANT",
                note="tahini-first product; water not at position 2 → no dilution signal",
                water_pos=None, func_type="tahini", func_pos=1,
                wfi_reduction=0.0, final_delta=0.0,
                is_matbucha=False, is_fp_candidate=False,
            )
        # Water at pos 2 after tahini → WATER_EARLY
        wfi_reduction = WFI_REDUCTION_EARLY
        raw_delta = wfi_reduction * WFI_WEIGHT
        wfi_new = max(0.0, wfi_score_current - wfi_reduction) if wfi_score_current is not None else None
        eff_delta = ((wfi_score_current - wfi_new) * WFI_WEIGHT) if wfi_new is not None else raw_delta
        return _result(
            state="WATER_EARLY",
            note=(
                f"Tahini-first protection: tahini at pos 1, water at pos 2. "
                f"WATER_EARLY (not WATER_PREDOMINANT) — water between tahini and chickpeas "
                f"is architecturally expected for tahini-dominant formulations. "
                f"WFI reduced by {wfi_reduction:.0f} pts."
            ),
            water_pos=water_position, func_type="tahini", func_pos=1,
            wfi_reduction=wfi_reduction, final_delta=round(eff_delta, 2),
            is_matbucha=False, is_fp_candidate=False,
            wfi_score_current=wfi_score_current, wfi_score_new=wfi_new,
        )

    # ------------------------------------------------------------------
    # Step 4 — Trigger B: Chickpea-percentage gate (NEW in v2)
    # Fires when: chickpea compound at pos 1, pct ≤ 45%, water at pos 2.
    # This detects two-level dilution: diluted compound + standalone water.
    # ------------------------------------------------------------------
    trigger_b_fires, chickpea_pct = _is_chickpea_compound_below_threshold(first_ing)
    water_at_pos2 = len(ingredients) > 1 and _is_water_ingredient(ingredients[1])

    if trigger_b_fires and water_at_pos2:
        wfi_reduction = WFI_REDUCTION_PREDOMINANT
        raw_delta = wfi_reduction * WFI_WEIGHT
        wfi_new = max(0.0, wfi_score_current - wfi_reduction) if wfi_score_current is not None else None
        eff_delta = ((wfi_score_current - wfi_new) * WFI_WEIGHT) if wfi_new is not None else raw_delta
        return _result(
            state="WATER_PREDOMINANT",
            note=(
                f"Trigger B (chickpea-percentage gate): '{first_ing[:50]}' at pos 1 "
                f"declares {chickpea_pct:.0f}% ≤ {CHICKPEA_PERCENTAGE_THRESHOLD:.0f}% threshold; "
                f"standalone water at pos 2. Two-level dilution detected. "
                f"WFI reduced by {wfi_reduction:.0f} pts."
            ),
            water_pos=2, func_type="chickpea", func_pos=1,
            wfi_reduction=wfi_reduction, final_delta=round(eff_delta, 2),
            is_matbucha=False, is_fp_candidate=False,
            wfi_score_current=wfi_score_current, wfi_score_new=wfi_new,
        )

    # ------------------------------------------------------------------
    # Step 5 — Trigger A: original water-position check
    # ------------------------------------------------------------------
    water_position: int | None = None
    for idx in (0, 1):
        if idx < len(ingredients) and _is_water_ingredient(ingredients[idx]):
            water_position = idx + 1
            break

    if water_position is None:
        return _result(
            state="NOT_PREDOMINANT",
            note="water not present at position 1 or 2",
            water_pos=None, func_type="n/a", func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=False, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 6 — Detect primary functional ingredient
    # ------------------------------------------------------------------
    func_type, func_position = _detect_primary_functional_ingredient(
        ingredients, category_hint=category)

    if func_type == "unknown" or func_position is None:
        return _result(
            state="NOT_EVALUABLE",
            note=f"primary functional ingredient not detectable (type={func_type})",
            water_pos=water_position, func_type=func_type, func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=False, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 7 — Classify state (Trigger A path)
    # ------------------------------------------------------------------
    is_high_water = _is_high_water_veg_product(func_type)

    if func_position > 2:
        # Functional ingredient at position 3+ — check for WATER_PREDOMINANT
        if is_high_water:
            # High-water vegetable: downgrade to WATER_EARLY per spec
            state = "WATER_EARLY"
            wfi_reduction = WFI_REDUCTION_EARLY
            note = (
                f"water at pos {water_position}, {func_type} (naturally high-water veg) "
                f"at pos {func_position}. Per spec: WATER_EARLY for high-water vegetables."
            )
        else:
            # Non-high-water functional ingredient at pos 3+ → WATER_PREDOMINANT (Trigger A)
            state = "WATER_PREDOMINANT"
            wfi_reduction = WFI_REDUCTION_PREDOMINANT
            note = (
                f"Trigger A: water at pos {water_position}, {func_type} at pos {func_position} "
                f"(>2). WFI reduced by {wfi_reduction:.0f} pts."
            )
    else:
        # Functional ingredient at pos 1 or 2 — check concentration floor before WATER_EARLY
        pct_at_pos1 = _extract_percentage(first_ing)
        floor_met = (pct_at_pos1 is not None and pct_at_pos1 >= CONCENTRATION_FLOOR_PCT)

        if floor_met:
            # Primary ingredient dominates (≥ 70%) — water at pos 2 is minor
            return _result(
                state="NOT_PREDOMINANT",
                note=(
                    f"Concentration floor: {func_type} at pos 1 declares "
                    f"{pct_at_pos1:.0f}% ≥ {CONCENTRATION_FLOOR_PCT:.0f}% threshold. "
                    f"Water at pos {water_position} is not a dilution signal at this concentration."
                ),
                water_pos=water_position, func_type=func_type, func_pos=func_position,
                wfi_reduction=0.0, final_delta=0.0,
                is_matbucha=False, is_fp_candidate=False,
            )

        state = "WATER_EARLY"
        wfi_reduction = WFI_REDUCTION_EARLY
        pct_note = f" ({pct_at_pos1:.0f}%)" if pct_at_pos1 is not None else ""
        note = (
            f"water at pos {water_position}, {func_type}{pct_note} at pos {func_position} "
            f"(both in top-2) → WATER_EARLY. WFI reduced by {wfi_reduction:.0f} pts."
        )

    # ------------------------------------------------------------------
    # Step 8 — Compute score delta
    # ------------------------------------------------------------------
    raw_delta = wfi_reduction * WFI_WEIGHT
    if wfi_score_current is not None:
        wfi_new = max(0.0, wfi_score_current - wfi_reduction)
        eff_delta = (wfi_score_current - wfi_new) * WFI_WEIGHT
    else:
        wfi_new = None
        eff_delta = raw_delta

    return _result(
        state=state,
        note=note,
        water_pos=water_position,
        func_type=func_type,
        func_pos=func_position,
        wfi_reduction=wfi_reduction,
        final_delta=round(eff_delta, 2),
        is_matbucha=False,
        is_fp_candidate=False,
        wfi_score_current=wfi_score_current,
        wfi_score_new=wfi_new,
    )
```

---

## Section 2 — Test Cases

Run these manually after code changes to confirm correct behavior before the full corpus re-run.

### Unit test cases

| Case | Input | Expected state | Rationale |
|------|-------|---------------|-----------|
| TC-01 | ingredients[0]="חומוס מבושל (34%)", ingredients[1]="מים" | WATER_PREDOMINANT | Trigger B: 34% ≤ 45% + water at pos 2 |
| TC-02 | ingredients[0]="חומוס מבושל (44%)", ingredients[1]="מים" | WATER_PREDOMINANT | Trigger B: 44% ≤ 45% + water at pos 2 |
| TC-03 | ingredients[0]="חומוס מבושל (46%)", ingredients[1]="מים" | WATER_EARLY | 46% > 45%; threshold not met |
| TC-04 | ingredients[0]="חומוס מבושל (50%)", ingredients[1]="מים" | WATER_EARLY | 50% > 45%; standard WATER_EARLY |
| TC-05 | ingredients[0]="חומוס מבושל 61%", ingredients[1]="מים" | WATER_EARLY | 61% > 45% |
| TC-06 | ingredients[0]="טחינה גולמית 40%", ingredients[1]="מים", ingredients[2]="חומוס מבושל 26%" | WATER_EARLY | Tahini-first protection; chickpea at pos 3 does NOT trigger WP |
| TC-07 | ingredients[0]="טחינה גולמית 37%", ingredients[1]="מים" | WATER_EARLY | Tahini-first protection; water at pos 2 |
| TC-08 | ingredients[0]="חציל קלוי 72%", ingredients[1]="מים" | NOT_PREDOMINANT | Concentration floor: 72% ≥ 70% |
| TC-09 | ingredients[0]="חציל קלוי 44%", ingredients[1]="מים" | WATER_EARLY | 44% < 70% floor; high-water veg at pos 1 |
| TC-10 | ingredients[0]="חומוס מבושל 61% [מים", ingredients[1]="חומוס", ingredients[2]="מווסת...", ingredients[3]="מים" | NOT_PREDOMINANT | Water at pos 4 — not in trigger range; compound at 61% > 45% |
| TC-11 | ingredients[0]="חומוס מבושל", ingredients[1]="מים" (no pct declared) | WATER_EARLY | Trigger B requires declared pct — falls through to Trigger A; WATER_EARLY since chickpea at pos 1 |
| TC-12 | category="beverage", ingredients[0]="מים" | NOT_EVALUABLE | Hard category exclusion |
| TC-13 | ingredients = [] | NOT_EVALUABLE | Insufficient ingredient data |
| TC-14 | name="מטבוחה אמיתית", ingredients[0]="עגבניות" | MATBUCHA_MANUAL_REVIEW | Matbucha detection |

---

## Section 3 — Re-Pilot Execution Plan

### 3.1 What to run

```
cd C:\Bari\03_operations\bsip2\experimental
python run_bsip2_061_pilot.py
```

The runner script (`run_bsip2_061_pilot.py`) requires no changes — it already reads from `bsip2_061_water_predominance.py` and applies the signal to run_hummus_002. After the code changes, re-running the pilot will automatically use the v2 logic.

The report output path is the same: `bsip2_061_pilot_results.md` — **this will overwrite the v1 report.** Back up the v1 report before re-running:

```
copy bsip2_061_pilot_results.md bsip2_061_pilot_results_v1.md
python run_bsip2_061_pilot.py
```

### 3.2 Measurements required

The runner already captures all required measurements. After re-run, verify:

| Measurement | What to check |
|-------------|---------------|
| WATER_PREDOMINANT count | Expect 4 (Trigger B activations) |
| WATER_EARLY count | Expect 13 (down from 18) |
| NOT_PREDOMINANT count | Expect 38 (up from 37) |
| False positive candidates | Expect 0 (no FP flag on any WATER_PREDOMINANT) |
| Grade changes | Expect same 4 as v1; verify no new grade changes |
| Max combined stack | Should remain ≤ 20 pts |
| Tahini-first products | "חומוס עשיר ב40% טחינה" → WATER_EARLY (not WATER_PREDOMINANT) |
| Concentration floor products | "חציל על האש" (72%) → NOT_PREDOMINANT (not WATER_EARLY) |

### 3.3 Manual review required after re-run

For each WATER_PREDOMINANT activation, record:

| Field | What to assess |
|-------|---------------|
| Chickpea % | Confirm it matches what the Trigger B extraction reports |
| Standalone water identity | Confirm ingredients[1] is genuinely standalone "מים", not a sub-ingredient |
| Overall reconstruction pattern | Does the product also have: seed oils, stabilizers, gums, preservatives? (corroborates dilution diagnosis) |
| Grade change direction | If the activation caused a grade change, is the lower grade appropriate for this product? |

---

## Section 4 — Expected Re-Pilot Outcomes

### 4.1 Activation count comparison

| State | Pilot v1 | Pilot v2 (expected) | Delta |
|-------|----------|---------------------|-------|
| WATER_PREDOMINANT | 0 | **4** | +4 |
| WATER_EARLY | 18 | **13** | −5 |
| NOT_PREDOMINANT | 37 | **38** | +1 |
| MATBUCHA_MANUAL_REVIEW | 0 | 0 | — |
| NOT_EVALUABLE | 14 | 14 | — |

### 4.2 Expected WATER_PREDOMINANT activations (Trigger B)

| Product | Chickpea % | Score before | Score after (v2) | Score v1 | Grade |
|---------|-----------|-------------|-----------------|---------|-------|
| חומוס מסעדות | 34% | 75.7 | 74.1 | 74.9 | B |
| חומוס מסבחה | 44% | 64.2 | 62.6 | 63.4 | C |
| חומוס גרגרים בתטבילה | 34% | 63.1 | 61.5 | 62.3 | C |
| חומוס עם חציל פיקנטי | 42% | 57.9 | 56.3 | 57.1 | C |

### 4.3 Expected products returning to NOT_PREDOMINANT (concentration floor)

| Product | Primary % | v1 state | v2 state | Score change |
|---------|-----------|----------|----------|-------------|
| חציל על האש | 72% eggplant | WATER_EARLY | NOT_PREDOMINANT | +0.8 (restored) |

### 4.4 Products confirmed staying WATER_EARLY (not upgraded to WATER_PREDOMINANT)

These are hummus products with chickpea compound > 45% that remain WATER_EARLY:

| Product | Chickpea % | Score |
|---------|-----------|-------|
| חומוס אסלי | 50% | 70.6 → 69.8 |
| חומוס | 50% | 70.6 → 69.8 |
| חומוס אבו גוש | 53% | 69.9 → 69.1 |
| חומוס גלילי | 55% | 69.1 → 68.3 |
| סלט חומוס עם טחינה | 46% | 68.5 → 67.7 |
| חומוס ישראלי | 64% | 68.3 → 67.5 |
| סלט חומוס+מסבחה | 49% | 68.2 → 67.4 |
| חומוס עם צנובר אחלה | 59% | 65.4 → 64.6 |
| חומוס עם זעתר | 60% | 65.2 → 64.4 |
| חומוס עשיר ב40% טחינה | tahini-first | 68.3 → 67.5 |
| חומוס מועשר 40% עם חריף | tahini-first | 65.4 → 64.6 |
| מעדן חצילים | 40% eggplant | 58.1 → 57.3 |
| חציל על האש בטחינה | 44% eggplant | 50.0 → 49.2 |

### 4.5 Expected grade distribution after v2

| Grade | v1 with signal | v2 expected |
|-------|---------------|-------------|
| A | 8 | 8 |
| B | 25 | 25 |
| C | 29 | 29 |
| D | 5 | 5 |
| E | 0 | 0 |
| insufficient_data | 2 | 2 |

No new grade changes expected from the WATER_PREDOMINANT upgrades — all 4 products move by an additional −0.8 pts (from −0.8 to −1.6) without crossing a grade boundary.

---

## Section 5 — Success Criteria for Re-Pilot

| Criterion | Threshold | Check |
|-----------|-----------|-------|
| WATER_PREDOMINANT count | 4 (±1 for data variation) | Compare to expected list |
| False positives | 0 on tahini-first products | Manual review of WP list |
| Concentration floor | 0 WATER_EARLY on ≥ 70% primary ingredients | Check activation list |
| Grade changes | Same 4 as v1 (no new ones) | Compare grade distribution tables |
| Max stack | ≤ 20 pts | Check Appendix B of report |
| Matbucha | 0 WATER_PREDOMINANT | Check matbucha section |

---

## Section 6 — Failure Conditions

If any of the following occur, pause and report to CNO before proceeding:

| Failure | Condition | Action |
|---------|-----------|--------|
| Unexpected WATER_PREDOMINANT | Product with chickpea % > 45% fires WATER_PREDOMINANT | Bug in Trigger B extraction — debug percentage regex |
| Tahini-first product gets WATER_PREDOMINANT | "חומוס עשיר ב40% טחינה" or similar returns WATER_PREDOMINANT | Tahini-first protection not firing — check ordering of detection steps |
| Concentration floor not firing | "חציל על האש" (72%) still returns WATER_EARLY | Bug in concentration floor check |
| New grade changes | Grade changes beyond the 4 expected | Investigate which products are newly affected |
| Combined stack > 20 | Any product reaches > −20 pts combined | Verify with Appendix B; do not promote to Option C |

---

## Section 7 — Post Re-Pilot Path

### If v2 pilot passes:

1. Write updated results to `bsip2_061_pilot_results.md` (overwrite v1 draft — v1 is backed up to `_v1.md`)
2. Update the signal status from EXPERIMENTAL/REVISE to EXPERIMENTAL/PILOT_VALIDATED
3. CNO review of the 4 WATER_PREDOMINANT activations for manual confirmation
4. If CNO confirms directional accuracy ≥ 85%: signal is ready for promotion criteria Gate 1 (Section 5 of revised_signal_definition_bsip2_061.md)
5. Wait for BSIP2-062 pilot to complete (Gate 4 prerequisite) before production promotion

### If v2 pilot fails:

1. Document which failure condition fired and why
2. Return to signal definition for a second revision cycle
3. Do NOT promote to Option C or production under any failure condition

---

## Appendix — Trigger B Decision Matrix

This matrix shows all expected chickpea-percentage outcomes for the hummus corpus:

| Product | Ingredient[0] | Pct | > 45%? | Trigger B | State |
|---------|--------------|-----|--------|-----------|-------|
| חומוס מסעדות | חומוס מבושל (34%) | 34% | No | FIRES | WATER_PREDOMINANT |
| חומוס גרגרים בתטבילה | חומוס מבושל 34% | 34% | No | FIRES | WATER_PREDOMINANT |
| חומוס עם חציל פיקנטי | חומוס מבושל 42% | 42% | No | FIRES | WATER_PREDOMINANT |
| חומוס מסבחה | חומוס מבושל (44%) | 44% | No | FIRES | WATER_PREDOMINANT |
| סלט חומוס+מסבחה | חומוס מבושל (49%) | 49% | Yes | dormant | WATER_EARLY |
| חומוס אסלי | חומוס מבושל (50%) | 50% | Yes | dormant | WATER_EARLY |
| חומוס | חומוס מבושל (50%) | 50% | Yes | dormant | WATER_EARLY |
| אבו גוש | חומוס מבושל (53%) | 53% | Yes | dormant | WATER_EARLY |
| חומוס גלילי | חומוס מבושל 55% | 55% | Yes | dormant | WATER_EARLY |
| סלט חומוס עם טחינה | חומוס מבושל (46%) | 46% | Yes | dormant | WATER_EARLY |
| חומוס עם צנובר אחלה | חומוס מבושל 59% | 59% | Yes | dormant | WATER_EARLY |
| חומוס עם זעתר | חומוס מבושל 60% | 60% | Yes | dormant | WATER_EARLY |
| חומוס ישראלי | חומוס* מבושל 64% | 64% | Yes | dormant | WATER_EARLY |
| חומוס עשיר ב40% טחינה | טחינה גולמית 40% | — | — | tahini protection | WATER_EARLY |
| חומוס מועשר 40% עם חריף | טחינה גולמית 37% | — | — | tahini protection | WATER_EARLY |
| חציל על האש | חציל קלוי 72% | 72% | — | conc. floor | NOT_PREDOMINANT |
| חציל על האש בטחינה | חציל קלוי 44% | 44% | — | high-water veg | WATER_EARLY |
| מעדן חצילים | חציל מטוגן (40%) | 40% | — | high-water veg | WATER_EARLY |

---

*BSIP2-061 Pilot Re-Run Specification — TASK-051A*  
*Pending implementation. No production deployment.*  
*Implementation target: bsip2_061_water_predominance.py — version bump to pilot_v2*
