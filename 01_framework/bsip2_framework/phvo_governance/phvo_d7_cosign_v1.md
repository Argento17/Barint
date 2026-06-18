# PHVO Governance D7 Co-Sign
**Document:** phvo_d7_cosign_v1.md  
**Agent:** Product Agent  
**Date:** 2026-06-14  
**Task:** TASK-280 Phase-2  
**Depends on:** P103 D6 ruling (Nutrition Agent, 2026-06-14, ACCEPTED by orchestrator)  
**Evidence registry:** EV-086 — `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` line 2064  

---

## D7 Authority

Per decision_rights_matrix.md D7: Scoring Rule Approval requires BOTH Product Agent AND Nutrition Agent sign-off. Nutrition Agent issued the D6 ruling (P103, 2026-06-14). This document is the Product Agent D7 co-sign.

Hard rule: D7 approval requires BOTH agents. No unilateral approval where a Nutrition ruling exists. That condition is met here — D6 precedes this D7.

---

## Ratification of D6 Rulings (Q1–Q4)

### Q1 — מחמאה REMOVED from `_PHVO_MARKERS`: RATIFIED

The removal is correct. מחמאה (clarified butter/ghee) is animal fat, not an industrial trans fat source. Fix-B's code comment identifying it as "margarine/shortening" was a factual error. The PHVO detection mechanism was designed for industrial partial hydrogenation of vegetable oils; applying it to animal fat is a category error that creates both a double-penalty (sat_fat already covers animal fat correctly) and a false-positive on kosher/traditional products.

The sat_fat dimension handles מחמאה correctly. No compensating rule is needed after removal.

**Decisive reason for ratification:** The chemical distinction between industrial trans fat (PHVO-derived elaidic acid) and animal fat (CLA/vaccenic acid) is settled food chemistry. The engine already encodes this distinction in EV-050. Extending the PHVO ceiling to animal fat directly contradicts the architecture EV-050 established.

### Q2 — Ceiling = 40 RETAINED + position gate N ≤ 8: RATIFIED

Ceiling value 40 is correct. It penalizes without executing. It is calibrated consistently with the existing trans-fat penalty scale. The alternatives (30 = disproportionate for ingredient-list-presence detection; 50 = de facto no penalty) are less defensible.

The position gate (fire only if PHVO marker appears in `ingredient_order` positions 1–8, 1-indexed) is ratified with one precision note: the BSIP2 `ingredient_order` uses 1-indexed positions (`item["position"]` starts at 1). The implementation spec must use `item["position"] <= 8`, not `<= 7`. The D6 ruling used "0-indexed positions 0–7" but the codebase convention is 1-indexed. The gate covers the same 8 ingredients either way; the implementation must follow the 1-indexed convention already in use.

The fallback (full-text search when `ingredient_order` is empty/None) is the safe default. Ratified.

**Condition on Q2:** Data Agent must verify the position gate against the snacks corpus before the first snacks re-score. If any product has a PHVO marker at position 1–8 that the gate incorrectly fires on (beyond the known snk-019 edge case), Data Agent surfaces it to orchestrator before the re-score proceeds.

### Q3 — All-categories scope: RATIFIED

The Q1 removal eliminates the primary false-positive path. Maintaining all-categories scope avoids a category exclusion list that adds maintenance burden for no current benefit. The EV-050 exemption gate remains structurally sound and unchanged.

No category exclusion list is authorized. If corpus analysis post-implementation reveals systematic false positives in any category, a separate D6/D7 ruling reopens this question.

### Q4 — Grade-change patch principle: RATIFIED

Patch if and only if the corrected engine produces a grade change (any grade boundary crossing). Within-grade score movement ships on the next scheduled re-score. This is consistent with Bari's standard: "unknown is acceptable; wrong is not" applies to grade labels, not to exact scores within a grade.

**Implementation note:** The orchestrator determines grade impact after Data Agent runs the corrected engine. Patch authorization is an orchestrator decision, not Data Agent's to make unilaterally.

---

## snk-019 Edge Case Ruling: Option A

snk-019's מרגרינה is declared as a coconut oil composite (שמן קוקוס + E471), not a partially-hydrogenated vegetable oil. The PHVO ceiling firing on the label "מרגרינה" is technically a borderline case — coconut oil does not require hydrogenation.

**Ruling: Option A — fire as-is.**

The "מרגרינה" label is an industrial-processing signal. A product formulated and labeled as מרגרינה is an ultra-processed functional fat regardless of whether the underlying base fat is coconut, palm, or hydrogenated vegetable oil. The fat_quality ceiling at 40 is appropriate for this class of ingredient. Adding a sub-exclusion for coconut/palm-declared margarines (Option B) creates audit complexity — the Data Agent must then maintain logic distinguishing margarine sub-types, with ambiguous ingredient text as the sole input. That complexity is not justified by the marginal benefit.

The simpler rule ships correctly for the population of real-world cases: products using מרגרינה as a functional fat are in the industrial-processing class the PHVO ceiling targets, regardless of the specific fat source.

**Reversal condition:** If a significant share of the snacks corpus (>10% of products) turns out to be coconut/palm-oil declared margarines where the PHVO ceiling materially distorts scores relative to actual fat quality, reopen with Data Agent corpus analysis.

---

## Implementation Authorization

Authorized to Data Agent for Phase-3 implementation dispatch (P105):

### signal_extractor.py — Required Changes

1. **Remove `"מחמאה"` from `_PHVO_MARKERS`** (the entry currently at line 1167).

2. **Fix code comment at line 1167** (the removed entry): Replace with:
   ```python
   # "מחמאה" REMOVED — clarified butter (ghee), animal fat, not PHVO.
   # D6 ruling Q1 (TASK-280 / EV-086). Use sat_fat dimension for animal fat scoring.
   ```

3. **Fix code comment at line 1158**: The current comment says "Fix-B: added שומנים מוקשים, שומן מוקשה (generic hardened fat, covers מחמאה-style ingredient declarations), מחמאה (margarine), מרגרינה (margarine)." Remove the מחמאה references and the "margarine" misidentification. Corrected comment:
   ```python
   # Fix-B (TASK-275): added שומנים מוקשים, שומן מוקשה (generic hardened fat plural/singular),
   # מרגרינה (margarine). מחמאה was also added by Fix-B but removed by D6 Q1 ruling (TASK-280/EV-086).
   ```

4. **Replace full-text `has_phvo` assignment (line 1170) with position-aware detection:**
   ```python
   # Position-aware PHVO detection (EV-086, D6 Q2 ruling, TASK-280).
   # Fire only if a PHVO marker appears in the first 8 ingredient positions (1-indexed).
   # Fallback to full-text search when ingredient_order is empty or None.
   _PHVO_MARKER_MAX_POSITION = 8
   if ingredient_order:
       has_phvo = any(
           m in item["text"]
           for item in ingredient_order
           if item.get("position", 99) <= _PHVO_MARKER_MAX_POSITION
           for m in _PHVO_MARKERS
       )
   else:
       # Fallback: ingredient_order unavailable — retain full-text search
       has_phvo = any(m in full_text for m in _PHVO_MARKERS)
   ```

### score_engine.py — No Changes Required

The ceiling logic (`min(fat_quality, 40) when has_phvo=True`) is correct. The `_PHVO_FAT_QUALITY_CEIL = 40` value is ratified. The position gate enforcement lives in signal_extractor.py — when `has_phvo` is set correctly there, score_engine.py behavior is automatically correct.

### No-Regression Gates (all three must PASS before merge)

1. `engine_invariants.py` — must PASS 342 cases.
2. Brined cheeses through current engine (flag-off) — must be byte-identical to `run_brined_004`.
3. Milk through current engine — must be byte-identical to `run_005_headpin` (frozen invariant).

---

## Scope Boundary

This D7 authorizes:
- The signal_extractor.py changes described above
- No score_engine.py edits
- No comparison JSON edits

This D7 does NOT authorize:
- Snacks re-score (separate orchestrator decision after implementation + no-regression proof)
- Patching any deployed JSON (separate decision, only if corrected engine shows grade change)
- Any modification to the EV-050 natural-dairy-trans-fat exemption gate
- Any modification to frozen categories (milk run_005_headpin, brined run_brined_004)

---

## Decision Log

| Item | Options | Chosen | Decisive Reason | Reversal Condition |
|------|---------|--------|-----------------|-------------------|
| Q1 מחמאה | RETAIN / REMOVE | REMOVE | Animal fat vs. industrial trans fat is a category error in the engine; double-penalty with sat_fat; conflicts with EV-050 architecture | Revisit if evidence emerges that commercial מחמאה products contain PHVO from processing additives |
| Q2 ceiling value | 30 / 40 / 50 | 40 | Calibrated to existing trans-fat penalty scale; penalizes without executing; 30 is disproportionate; 50 removes the penalty | Revisit if corpus pilot shows ceiling=40 produces systematic grade distortions relative to actual fat quality |
| Q2 position gate | None / N≤8 / other N | N≤8 | Israeli ingredient ordering convention makes position ≤8 the meaningful contribution zone; binary full-text match conflates dominant fat with trace functional use | Revisit if corpus analysis shows PHVO markers in position 9+ at meaningful product mass (validated by Data Agent) |
| Q3 category scope | All-categories / exclusion list | All-categories | Q1 removal eliminates primary false positive; exclusion list adds maintenance burden | Revisit if corpus reveals systematic false positives in a specific category post-implementation |
| Q4 patch principle | Always patch / grade-change only / never patch | Grade-change only | Consumer-facing grade label is the quality signal Bari stakes trust on; within-grade score precision is a re-score cadence question | Fixed principle; not revisable without owner-level ruling |
| snk-019 | Option A (fire) / Option B (sub-exclusion) | Option A | "מרגרינה" label is an industrial-processing signal regardless of fat source; Option B creates audit complexity without proportional benefit | Revisit if >10% of snacks corpus has coconut/palm-declared margarines causing material score distortion |

---

## Spec-Conflict Notice

The brief (P104) specifies writing EV-086 to `C:\Bari\01_framework\operations\evidence_registry_v1.md`. That path does not exist. The PHVO scoring engine references EV-050, which lives in the BSIP2 evidence registry at `C:\Bari\03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md` (EV-NNN prefix). The framework governance registry at `C:\Bari\01_framework\governance\evidence_registry_v1.md` uses BEV-NNN prefix and BEV-086 is already occupied. EV-086 was therefore written to the correct path: the BSIP2 evidence registry at line 2064. This is the compliant alternative to silent faithful execution of a flawed spec path.
